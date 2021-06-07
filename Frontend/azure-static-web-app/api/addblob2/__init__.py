import logging
import os, uuid, requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    img = req.files['imgFile']
    video=req.files['videoFile']
    print(img.filename)
    print(video.filename)
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sh0909storage;AccountKey=Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==;EndpointSuffix=core.windows.net") # this is my table key
    blob_client = blob_service_client.get_blob_client(container="imgforyoutube", blob= img.filename)
    blob_client.upload_blob(img.stream.read())
    blob_client = blob_service_client.get_blob_client(container = "fileforyoutube", blob = video.filename)
    blob_client.upload_blob(video.stream.read())

    return func.HttpResponse("success")

