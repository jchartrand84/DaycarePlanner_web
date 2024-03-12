# myapp/views.py
import csv
import json
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from azure.storage.blob import BlobServiceClient


# Create a blob service client
connection_string = "DefaultEndpointsProtocol=https;AccountName=chartrandstorage;AccountKey=Krv2HxrUMXOXCCJ+Q9Qyt83PABUhMTOZTR/gAgbmy12+EbnRl/c+0TrzP5iY9MR7U0G0/OclWi1y+AStljapfw==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)


def menu_view(request):
    return render(request, 'menu.html')


def daycare_database_view(request):
    blob_client = blob_service_client.get_blob_client("project3data", "daycare_database.csv")
    download_stream = blob_client.download_blob().readall()
    reader = csv.reader(download_stream.decode('utf-8').splitlines())
    data = list(reader)
    return render(request, 'daycare_database.html', {'data': data})


@csrf_exempt
def update_csv_full(request):
    if request.method == 'POST':
        data_from_post = json.loads(request.POST['data'])  # Get data from POST request and convert it from JSON
        blob_client = blob_service_client.get_blob_client("project3data", "daycare_database.csv")
        csv_data = '\n'.join([','.join(row) for row in data_from_post])  # Convert all data to CSV format
        blob_client.upload_blob(csv_data, overwrite=True)  # Upload CSV data to Azure Blob Storage
        return JsonResponse({'status': 'success'})  # Return success status


@csrf_exempt
def update_csv_single(request):
    if request.method == 'POST':
        updated_row = json.loads(request.POST['data'])[0]  # Get data from POST request and convert it from JSON
        blob_client = blob_service_client.get_blob_client("project3data", "daycare_database.csv")
        download_stream = blob_client.download_blob().readall()
        reader = csv.reader(download_stream.decode('utf-8').splitlines())
        data = list(reader)
        row_index = next((index for index, row in enumerate(data) if row[0] == updated_row[0]), None)
        if row_index is not None:
            data[row_index] = updated_row  # Update the row
        csv_data = '\n'.join([','.join(row) for row in data])  # Convert data to CSV format
        blob_client.upload_blob(csv_data, overwrite=True)  # Upload CSV data to Azure Blob Storage
        return JsonResponse({'status': 'success'})  # Return success status


def payment_menu_view(request):
    blob_client = blob_service_client.get_blob_client("project3data", "daycare_database.csv")
    download_stream = blob_client.download_blob().readall()
    reader = csv.reader(download_stream.decode('utf-8').splitlines())
    data = list(reader)
    # Filter out children with a balance of 0
    data = [row for row in data if len(row) > 2 and float(row[2]) > 0]
    return render(request, 'payment_menu.html', {'data': data})


def daycare_scheduler_view(request):
    return render(request, 'daycare_scheduler.html')


def get_children(request):
    blob_client = blob_service_client.get_blob_client("project3data", "daycare_database.csv")
    download_stream = blob_client.download_blob().readall()
    reader = csv.reader(download_stream.decode('utf-8').splitlines())
    data = list(reader)
    children = [row[0] for row in data]  # Assume the child's name is in the first column
    return JsonResponse(children, safe=False)


@csrf_exempt
def get_attendance_records(request):
    blob_client = blob_service_client.get_blob_client("project3data", "attendance.csv")
    download_stream = blob_client.download_blob().readall()
    reader = csv.reader(download_stream.decode('utf-8').splitlines())
    data = list(reader)
    records = [{'title': row[0], 'start': row[1]} for row in data if len(row) >= 2]  # Check that each row has at least two elements
    return JsonResponse(records, safe=False)


@csrf_exempt
def add_attendance_record(request):
    if request.method == 'POST':
        child = request.POST['child']
        date = request.POST['date']  # Keep date format as YYYY-MM-DD
        blob_client = blob_service_client.get_blob_client("project3data", "attendance.csv")
        download_stream = blob_client.download_blob().readall()
        reader = csv.reader(download_stream.decode('utf-8').splitlines())
        data = list(reader)
        # Check for duplicate entries
        if any(row[0].strip().lower() == child.lower() and row[1].strip() == date for row in data if len(row) > 1):
            return JsonResponse({'status': 'error', 'message': 'Duplicate entry'})
        # Check for past date
        if datetime.strptime(date, '%Y-%m-%d').date() < datetime.now().date():
            return JsonResponse({'status': 'error', 'message': 'Cannot add records for past dates'})
        # Check for more than 6 children
        if sum(1 for row in data if len(row) > 1 and row[1].strip() == date) >= 6:
            return JsonResponse({'status': 'error', 'message': 'Cannot add more than 6 children in a day'})
        # Add the new record
        data.append([child, date])
        csv_data = '\n'.join([','.join(row) for row in data])  # Convert data to CSV format
        blob_client.upload_blob(csv_data, overwrite=True)  # Upload CSV data to Azure Blob Storage
        return JsonResponse({'status': 'success'})  # Return success status


@csrf_exempt
def remove_attendance_record(request):
    if request.method == 'POST':
        child = request.POST['child']
        date = request.POST['date']  # Keep date format as YYYY-MM-DD
        # Check for past date
        if datetime.strptime(date, '%Y-%m-%d').date() < datetime.now().date():
            return JsonResponse({'status': 'error', 'message': 'Cannot remove records for past dates'})
        blob_client = blob_service_client.get_blob_client("project3data", "attendance.csv")
        download_stream = blob_client.download_blob().readall()
        reader = csv.reader(download_stream.decode('utf-8').splitlines())
        data = list(reader)
        data = [row for row in data if len(row) > 1 and not (row[0].strip().lower() == child.lower() and row[1].strip() == date)]  # Remove the attendance record
        csv_data = '\n'.join([','.join(row) for row in data])  # Convert data to CSV format
        blob_client.upload_blob(csv_data, overwrite=True)  # Upload CSV data to Azure Blob Storage
        return JsonResponse({'status': 'success'})  # Return success status


@csrf_exempt
def check_attendance_record(request):
    if request.method == 'POST':
        child = request.POST['child']
        date = request.POST['date']  # Keep date format as YYYY-MM-DD
        blob_client = blob_service_client.get_blob_client("project3data", "attendance.csv")
        download_stream = blob_client.download_blob().readall()
        reader = csv.reader(download_stream.decode('utf-8').splitlines())
        data = list(reader)
        exists = any(row[0].strip().lower() == child.lower() and row[1].strip() == date for row in data if len(row) > 1 and row[0].strip() != '')
        return JsonResponse({'exists': exists})