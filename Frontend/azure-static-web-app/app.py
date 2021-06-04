from flask import Flask, render_template, request
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import requests
import os,uuid,sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import json
import time
#import asyncio

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def get_infomation():
    
    if request.method == 'POST':
        start = time.time()
        #loop = asyncio.get_event_loop()
        data = request.form
        cutted_tags = data['tag'].split(',')

        dic_data = dict()
        
        dic_data['title'] = data['title']
        dic_data['tags'] = cutted_tags
        dic_data['content'] = data['content']
        dic_data['date'] = data['date']
        dic_data['time'] = data['time']

        upload_table(dic_data)

        video = request.files['video']
        img = request.files['img']

        #loop.run_until_complete(asyncio.gather(upload_table(json_data), upload_blob(video,img)))

        upload_blob(video,img)

        end = time.time()

        print(end-start)
        

    return render_template('add.html')

def upload_table(dic_data):
    table_service = TableService(account_name='jsondataforyoutube',account_key ='RAmtG8i+T8bpsY9aZZBedsODThcvCh1VwHyU/EHfOEyB11UDImCpia+gHyou8bLyRqsIbjDdwx3SXCpfZWgyRA==')
    table_service.create_table('tasktable')

    task = {'PartitionKey': 'text_data', 'RowKey': "14", 'title' : dic_data['title'],'description': dic_data['content'],'time': '2021-06-11'}
    #Rowkey need to change every upload

    table_service.insert_entity('tasktable', task)

    print('storage success')

    #await asyncio.sleep(1)


def upload_blob(video, img):
    path = os.getcwd()
    path = path + '/data'


    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=jsondataforyoutube;AccountKey=RAmtG8i+T8bpsY9aZZBedsODThcvCh1VwHyU/EHfOEyB11UDImCpia+gHyou8bLyRqsIbjDdwx3SXCpfZWgyRA==;EndpointSuffix=core.windows.net") # this is my table key
    container_name = "fileforyoutube"
    container_name_img = "imgforyoutube"

    #initial code for create blob container
    #container_client = blob_service_client.create_container(container_name)
    #container_client = blob_service_client.create_container(container_name_img)

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

if __name__ == '__main__':

    app.run(debug = True)
