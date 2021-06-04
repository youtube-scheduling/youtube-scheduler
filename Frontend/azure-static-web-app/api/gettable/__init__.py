import logging
from azure.data.tables import TableClient
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    pk=req.route_params.get('pk')
    rk=req.route_params.get('rk')
    message=f"pk:{pk},rk:{rk}"
    conn_str="DefaultEndpointsProtocol=https;AccountName=sh0909storage;AccountKey=Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==;EndpointSuffix=core.windows.net"
    my_filter = "RowKey eq '"+rk+"'"+" and PartitionKey eq '"+pk+"'"
    print(my_filter)
    table_client = TableClient.from_connection_string(conn_str=conn_str, table_name="mytable")

    entities = table_client.query_entities(my_filter)
    table_list={}
    for entity in entities:
        for key in entity.keys():
            table_list[key]=entity[key]
            #print("Key: {}, Value: {}".format(key, entity[key]))
    str_list=str(table_list)
    return func.HttpResponse(str_list)