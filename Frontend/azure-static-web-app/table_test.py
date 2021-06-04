from azure.data.tables import TableServiceClient, TableClient, UpdateMode
import string
import random

number_of_strings = 5
length_of_string = 8

entity = {
        'PartitionKey': 'data',
        'RowKey': 'UWUJnu3T',
        'title': 'azure key vault란?',
        'description': 'azure key vault에 대한 설명',
        'tag': '#azure,#ms',
        'category':'17',
        'time':'2021-06-03'
    }
conn_str="DefaultEndpointsProtocol=https;AccountName=sh0909storage;AccountKey=Sg/73AcJ6ah/DP38yZ087H4YBSXc0irmBKZd2C5o3I6eFhDWhQeH1zAJ45U3f9d86CdYJVaeY5wRWarKoF1QoA==;EndpointSuffix=core.windows.net"
'''
table_service_client = TableServiceClient.from_connection_string(conn_str=conn_str)
table_name = "myTable"
#table_client = table_service_client.create_table(table_name=table_name)
table_client = table_service_client.get_table_client(table_name=table_name)
entity = table_client.create_entity(entity=entity)

table_client.delete_entity(row_key="brand2",partition_key="color")
print("s")
'''
brand="brand2"
#my_filter="RowKey eq '"+brand+"'"
#print(my_filter)
#my_filter = "RowKey eq 'brand2' and PartitionKey eq 'color'"
table_client = TableClient.from_connection_string(conn_str=conn_str, table_name="mytable")
table_client.update_entity(mode=UpdateMode.REPLACE,entity=entity)
replaced = table_client.get_entity(partition_key=entity["PartitionKey"], row_key=entity["RowKey"])
print("Replaced entity: {}".format(replaced))
'''
entities = table_client.query_entities(my_filter)
for entity in entities:
    for key in entity.keys():
        print("Key: {}, Value: {}".format(key, entity[key]))'''


