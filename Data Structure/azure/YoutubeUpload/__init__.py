import os
import json
import base64
import logging
import datetime
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


def main(req: func.HttpRequest) -> func.HttpResponse:

    req = req.get_json()

    table = req['table']

    video = req['video']
    _video = base64.b64decode(video['$content'])    
    vid_ext = table['video']
    video = open('/tmp/v.' + vid_ext, 'wb+')
    video.write(_video) 

    try:
        thumbnail = req['thumbnail']
        _thumbnail = base64.b64decode(thumbnail['$content'])
        thum_ext = table['thumbnail']
        thumbnail = open('/tmp/t.' + thum_ext, 'wb+')
        thumbnail.write(_thumbnail)
    except:
        thumbnail = None

    schedule = table['schedule'] # ISO format
    snippet = {
            #'categoryId' : table['categoryId'],
            'title' : table['title'],
            'description' : table['description'],
            'tags' : table['tags'].split(', ')
    }

    # TODO Add Youtube Upload Process


    return func.HttpResponse(status_code = 200)
