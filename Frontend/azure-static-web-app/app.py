from flask import Flask, render_template, request
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import requests
import os,uuid,sys
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import json


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def get_infomation():
    
    if request.method == 'POST':
        data = request.form
        table_service = TableService(account_name='jsondataforyoutube',account_key ='RAmtG8i+T8bpsY9aZZBedsODThcvCh1VwHyU/EHfOEyB11UDImCpia+gHyou8bLyRqsIbjDdwx3SXCpfZWgyRA==')
        table_service.create_table('tasktable')

        path = os.getcwd()
        path = path + '/data'
        img_path = path + '/image.jpg'
        video_path = path + '/video.avi'

        #f = open(text_path, "w")

        cutted_tags = data['tag'].split(',')

        dic_data = dict()
        
        #f.write(data['title'])
        #f.write('\n')

        dic_data['title'] = data['title']
        dic_data['tags'] = cutted_tags
        dic_data['content'] = data['content']
        dic_data['date'] = data['date']
        dic_data['time'] = data['time']
        json_data = json.dumps(dic_data)

        task = {'PartitionKey': 'text_data', 'RowKey': "21",'description': json_data, 'priority': 250}

        table_service.insert_entity('tasktable', task)

        print('storage success')

        blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=jsondataforyoutube;AccountKey=RAmtG8i+T8bpsY9aZZBedsODThcvCh1VwHyU/EHfOEyB11UDImCpia+gHyou8bLyRqsIbjDdwx3SXCpfZWgyRA==;EndpointSuffix=core.windows.net")
        container_name = "fileforyoutube"
        container_name_img = "imgforyoutube"

        #initial code for create blob container
        #container_client = blob_service_client.create_container(container_name)
        #container_client = blob_service_client.create_container(container_name_img)

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
        

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug = True)
