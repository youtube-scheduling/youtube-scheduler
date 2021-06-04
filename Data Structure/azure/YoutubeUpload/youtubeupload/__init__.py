import os
import json
import datetime
from auth import Create_Service
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


def toKorDateTime(dateTime):
    date, time = dateTime.split('T') # YYYY-MM-DD, HH:MM:SS
    year, month, day = date.split('-')
    hour, minute, second = time.split(':')

    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    dateTime = datetime.datetime(year, month, day, hour, minute, second)
    korDateTime = dateTime + datetime.timedelta(hours = -9)
    

    return korDateTime.strftime('%Y-%m-%dT%H:%M:%S')


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

    schedule = table['time'] # String type
    schedule = toKorDateTime(schedule) # schedule to YYYY-MM-DDTHH:MM:SS
    snippet = {
            #'categoryId' : table['categoryId'],
            'title' : table['title'],
            'description' : table['description'],
            #'tags' : table['tags'].split(', ')
    }
    
    try: 
        CLIENT_SECRET_FILE = 'client_secret.json'
        API_NAME = 'youtube'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        request_body = {   
            'snippet': snippet,
            'status': {
                'privacyStatus': 'private',
                'publishAt': schedule,
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': False
        }

        mediaFile = MediaFileUpload('/tmp/v.' + vid_ext)

        response_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()

        try:
            service.thumbnails().set(
                videoId=response_upload.get('id'),
                media_body=MediaFileUpload('/tmp/t.' + thum_ext)
            ).execute()
        except:
            pass

        status_code = 200

    except:
        status_code = 500

    
    return func.HttpResponse(status_code = status_code)
