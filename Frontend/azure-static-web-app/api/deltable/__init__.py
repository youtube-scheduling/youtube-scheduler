import logging
from azure.data.tables import TableServiceClient
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    pk=req.route_params.get('pk')
    rk=req.route_params.get('rk')
    message=f"pk:{pk},rk:{rk}"
    #return func.HttpResponse(message)
    conn_str="DefaultEndpointsProtocol=https;AccountName=storageforys;AccountKey=sTNZfBUGl7EbNxi7duoUuzXnBuWPdfVIcgn4HzDu2y8q6BVz9oJNxr0XkJD2lFmZBsNHVpSbz8rbEzLFLZHfbQ==;EndpointSuffix=core.windows.net"
    table_service_client = TableServiceClient.from_connection_string(conn_str=conn_str)
    table_name = "myTable"  
    table_client = table_service_client.get_table_client(table_name=table_name)
    table_client.delete_entity(row_key=rk,partition_key=pk)
    return func.HttpResponse(message)