import json
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main(req: func.HttpRequest, tabledatas) -> func.HttpResponse:
    search_key = req.params.get('search_key')
    
    datas = json.loads(tabledatas)
    blob_service_client = BlobServiceClient.from_connection_string('BLOB_STORAGE_CONNECTION_STRING')
    container_client = blob_service_client.get_container_client('ref-files')
    
    refdata = None
    for data in datas:
        if data['RowKey'] == search_key:
            refdata = data
    
    if refdata:
        video_name = refdata['video']
        thumbnail_name = refdata['thumbnail']
    else:
        return func.HttpResponse(f"Table Entity Found Error(Wrong Search Key)")

    blobs = container_client.list_blobs()
    video = None
    thumbnail = None
    for blob in blobs:
        if blob.name == 'videos/' + video_name:
            video = blob
        elif blob.name == 'thumbnails/' + thumbnail_name:
            thumbnail = blob
    
    return func.HttpResponse(f"{video.name} {thumbnail.name}")