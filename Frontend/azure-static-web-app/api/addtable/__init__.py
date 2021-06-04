from azure.data.tables import TableServiceClient
import requests
import os,uuid,sys
import json
import logging
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    body=req.get_json()
    #print(type(body))
    dic_data = json.loads(body)
    upload_table(body)
    return func.HttpResponse("Success")

def upload_table(dic_data):
    conn_str="DefaultEndpointsProtocol=https;AccountName=sh0909storage;AccountKey=Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==;EndpointSuffix=core.windows.net"
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = table_service_client.get_table_client(table_name="mytable")

    task = {'PartitionKey': dic_data['PartitionKey'], 'RowKey': dic_data['RowKey'], 'title' : dic_data['title'],'description': dic_data['content'],'time': '2021-06-11'}
    #Rowkey need to change every upload

    task = table_client.create_entity(entity= task)
    print('storage success')

