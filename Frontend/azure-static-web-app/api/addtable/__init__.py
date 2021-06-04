from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
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
    table_service = TableService(account_name='sh0909storage',account_key ='Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==')
    table_service.create_table('mytablee')

    task = {'PartitionKey': dic_data['PartitionKey'], 'RowKey': dic_data['RowKey'], 'title' : dic_data['title'],'description': dic_data['content'],'time': '2021-06-11'}
    #Rowkey need to change every upload

    table_service.insert_entity('tasktable', task)

    print('storage success')

