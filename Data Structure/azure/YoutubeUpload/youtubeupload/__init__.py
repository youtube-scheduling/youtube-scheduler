import os
import json
import datetime
import pathlib
import pickle
import tempfile
import base64
import logging
import datetime
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from google.auth.transport.requests import Request


def Create_Service(container, client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
   
    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    pickle_blob = container.get_blob_client(pickle_file)
    with open('/tmp/' + pickle_file, "wb+") as my_pickle:
        download_stream = pickle_blob.download_blob()
        my_pickle.write(download_stream.readall())

    if os.path.exists('/tmp/' + pickle_file):
        with open('/tmp/' + pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open('/tmp/' + pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


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
    
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container = blob_service_client.get_container_client('ys-function')
    client_secret_blob = container.get_blob_client('client_secret.json')
    with open('/tmp/client_secret.json', "wb+") as my_client_secret:
        download_stream = client_secret_blob.download_blob()
        my_client_secret.write(download_stream.readall())

    table = req['table']

    fileforyoutube = blob_service_client.get_container_client('fileforyoutube')
    imgforyoutube = blob_service_client.get_container_client('imgforyoutube')

    video_name = req['video']
    video_blob = fileforyoutube.get_blob_client(video_name)
    vid_ext = table['video']
    with open('/tmp/v.' + vid_ext, 'wb+') as my_video:
        download_stream = video_blob.download_blob()
        my_video.write(download_stream.readall())

    try:
        thumbnail_name = req['thumbnail']
        thumbnail_blob = imgforyoutube.get_blob_client(thumbnail_name)
        thum_ext = table['thumbnail']
        with open('/tmp/t.' + thum_ext, 'wb+') as my_thumbnail:
            download_stream = thumbnail_blob.download_blob()
            my_thumbnail.write(download_stream.readall())
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
        CLIENT_SECRET_FILE = '/tmp/client_secret.json'
        API_NAME = 'youtube'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

        service = Create_Service(container, CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

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

        try:
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
            status_code = 403

    except:
        status_code = 500


    return func.HttpResponse(status_code = status_code)
