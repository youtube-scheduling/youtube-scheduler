import logging
import os, uuid, requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    name = req.files['imgFile']
    video=req.files['videoFile']
    print(name.filename)
    print(video.filename)
    upload_blob(video,name)
    return func.HttpResponse("success")

def upload_blob(video, img):
    #path = os.getcwd()
    path = './data'


    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=nM7gq0Ht+3Aoy5RFzaA/epWvi/w8aiMvPTIqmMDci65K9aogBIfB1o4E6bYHygk0sOzN8eA6OKr2d0CdU/mMTg==;EndpointSuffix=core.windows.net") # this is my table key
    container_name = "fileforyoutube"
    container_name_img = "imgforyoutube"

    #initial code for create blob container
    #container_client = blob_service_client.create_container(container_name)
    #container_client = blob_service_client.create_container(container_name_img)

    #str(uuid.uuid4()) is the name of file
    local_file_name = str(uuid.uuid4()) + ".avi"
    upload_file_path = os.path.join(path, local_file_name)
    upload_file_path=video.filename
    video.save(upload_file_path)

    blob_client = blob_service_client.get_blob_client(container = container_name, blob = local_file_name)
    blob_client.upload_blob(upload_file_path)

    local_file_name = str(uuid.uuid4()) + ".img"
    upload_file_path_img = os.path.join(path, local_file_name)
    img.save(upload_file_path_img)

    blob_client = blob_service_client.get_blob_client(container=container_name_img, blob= local_file_name)
    blob_client.upload_blob(upload_file_path_img)

    print('blob success')

    #await asyncio.sleep(1)
