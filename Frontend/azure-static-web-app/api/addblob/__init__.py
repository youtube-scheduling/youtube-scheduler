from flask import Flask,request
from flask import render_template, Flask, request
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import os, uuid
import azure.functions as func
import logging

@app.route('/video',methods=['POST'])
def blob_upload():
    if request.method == 'POST':
        f_video=request.files['video']
        f_img=request.files['img']

        upload_blob(f_video, f_img)

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

    #await asyncio.sleep(1)_

if __name__ == "__main__":
    app.run()
