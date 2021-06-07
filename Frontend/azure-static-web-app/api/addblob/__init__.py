from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os, uuid, requests
import azure.functions as func
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    url = "127.0.0.1:7071/api/addblob"
    r = requests.post(url)
    f_video=r.files['video']
    f_img=r.files['img']

    #req = requests.get(url)

    upload_blob(f_video,f_img)

    return func.HttpResponse("Success")


def upload_blob(video, img):
    path = os.getcwd()
    path = path + '/data'


    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net") # this is my table key
    container_name = "fileforyoutube"
    container_name_img = "imgforyoutube"

    #initial code for create blob container
    #container_client = blob_service_client.create_container(container_name)
    #container_client = blob_service_client.create_container(container_name_img)

    #str(uuid.uuid4()) is the name of file
    local_file_name = str(uuid.uuid4()) + ".avi"
    upload_file_path = os.path.join(path, local_file_name)
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
