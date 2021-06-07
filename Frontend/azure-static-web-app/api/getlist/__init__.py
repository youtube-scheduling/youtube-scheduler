import logging
from azure.data.tables import TableServiceClient, TableClient
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str="DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net"
    table_service_client = TableServiceClient.from_connection_string(conn_str=conn_str)
    table_client = table_service_client.get_table_client(table_name="myTable")
    table_list={}
    cnt=1
    for entity in table_client.list_entities():
        tmp_list={}
        tmp_list["PartitionKey"]=entity["PartitionKey"]
        tmp_list["title"]=entity["title"]
        table_list[entity["RowKey"]]=tmp_list
        #tmp=entity["title"]
        #title[entity["RowKey"]]=tmp
        #cnt+=1 
        #print(title)
    str_list=str(table_list)
    print(str_list)
    return func.HttpResponse(str_list)
   
