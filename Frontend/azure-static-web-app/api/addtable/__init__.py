from azure.data.tables import TableServiceClient
import requests
import os,uuid,sys
import json
import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    body=req.get_json()
    #print(type(body))
    #dic_data = json.loads(body)
    upload_table(body)
    return func.HttpResponse("Success")

def upload_table(dic_data):
    conn_str="DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net"
    service = TableServiceClient.from_connection_string(conn_str=conn_str)
    table_client = service.get_table_client(table_name="myTable")

    task = {'PartitionKey': 'data', 'RowKey': str(uuid.uuid4()), 'title' : dic_data['title'],'description': dic_data['content'],'tag':dic_data['tag'],'category':dic_data['category'],'date':dic_data['date'],'time': dic_data['time']}
    #Rowkey need to change every upload

    task = table_client.create_entity(entity= task)
    print('storage success')

