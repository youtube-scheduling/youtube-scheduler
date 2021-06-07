import logging
from azure.data.tables import TableClient, UpdateMode
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str="DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net"
    body=req.get_json()
    #print(type(body))
    table_client = TableClient.from_connection_string(conn_str=conn_str, table_name="mytable")
    table_client.update_entity(mode=UpdateMode.REPLACE,entity=body)
    return func.HttpResponse("Success")