from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os, uuid, requests
import azure.functions as func
import logging

def main():
    url = "127.0.0.1:7071/addblob"
    r = requests.post(url)
    f_video=r.files['video']
    f_img=r.files['img']

    req = requests.get(url)

    upload_blob(req[0], req[1])

    return func.HttpResponse("Success")


def upload_blob(video, img):
    path = os.getcwd()
    path = path + '/data'


    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=sh0909storage;AccountKey=Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==;EndpointSuffix=core.windows.net") # this is my table key
    container_name = "fileforyoutube"
    container_name_img = "imgforyoutube"

    #initial code for create blob container
    container_client = blob_service_client.create_container(container_name)
    container_client = blob_service_client.create_container(container_name_img)

    #str(uuid.uuid4()) is the name of file
    local_file_name = str(uuid.uuid4()) + ".avi"
    upload_file_path = os.path.join(path, local_file_name)
    video = request.files['video']
    video.save(upload_file_path)

    blob_client = blob_service_client.get_blob_client(container = container_name, blob = local_file_name)
    blob_client.upload_blob(upload_file_path)

    local_file_name = str(uuid.uuid4()) + ".img"
    upload_file_path_img = os.path.join(path, local_file_name)
    img = request.files['img']
    img.save(upload_file_path_img)

    blob_client = blob_service_client.get_blob_client(container=container_name_img, blob= local_file_name)
    blob_client.upload_blob(upload_file_path_img)

    print('blob success')

    #await asyncio.sleep(1)
