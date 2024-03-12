# myapp/views.py
import csv
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

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
def update_csv(request):
    if request.method == 'POST':
        data = json.loads(request.POST['data'])  # Get data from POST request and convert it from JSON
        csv_data = '\n'.join([','.join(row) for row in data])  # Convert data to CSV format
        blob_client = blob_service_client.get_blob_client("project3data", "daycare_database.csv")
        blob_client.upload_blob(csv_data, overwrite=True)  # Upload CSV data to Azure Blob Storage
        return JsonResponse({'status': 'success'})  # Return success status
