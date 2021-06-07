import logging
import os, uuid, requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    img = req.files['imgFile']
    video=req.files['videoFile']
    row_key = req.params.rowKey
    print(img.filename)
    print(video.filename)
    img_extension = img.filename[img.filename.index('.'):]
    vid_extension = video.filename[video.filename.index('.'):]

    table_service = TableService(connection_string='DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net')
    entity = table_service.get_entity('myTable', 'data', row_key)
    entity['vid_extension'] = vid_extension
    entity['img_extension'] = img_extension
    table_service.update_entity('myTable', entity)

    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net") # this is my table key
    blob_client = blob_service_client.get_blob_client(container="imgforyoutube", blob= row_key + img_extension)
    blob_client.upload_blob(img.stream.read())
    blob_client = blob_service_client.get_blob_client(container = "fileforyoutube", blob = row_key + vid_extension)
    blob_client.upload_blob(video.stream.read())

    return func.HttpResponse("success")

