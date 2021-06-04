import logging
from azure.data.tables import TableClient, UpdateMode
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str="DefaultEndpointsProtocol=https;AccountName=sh0909storage;AccountKey=Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==;EndpointSuffix=core.windows.net"
    body=req.get_json()
    #print(type(body))
    table_client = TableClient.from_connection_string(conn_str=conn_str, table_name="mytable")
    table_client.update_entity(mode=UpdateMode.REPLACE,entity=body)
    return func.HttpResponse("Success")