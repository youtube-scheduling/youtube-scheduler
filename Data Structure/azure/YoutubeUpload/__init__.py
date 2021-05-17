import logging
import datetime
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


def main(req: func.HttpRequest) -> func.HttpResponse:

    request_body = req.form['request_body']
    video_name = req.form['video']

    blob_service_client = BlobServiceClient.from_connection_string('BLOB_STORAGE_CONNECTION_STRING')
    container_client = blob_service_client.get_container_client('ref-files')

    blobs = container_client.list_blobs()
    video = None
    for blob in blobs:
        if blob.name == 'videos/' + video_name:
            video = blob
            break
    
    try:
        video = container_client.get_blob_client(video)
    except Exception:
        print("No File {} in Blob Storage".format(video_name))

    with open(video_name, "wb") as my_blob:
       download_stream = video.download_blob()
       my_blob.write(download_stream.readall())
    
    CLIENT_SECRET_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build('youtube', 'v3', credentials=credentials)   

    video = MediaFileUpload(video_name)

    response_upload = youtube.videos().insert(
        part='snippet',
        body=request_body,
        media_body=video
    ).execute()


    return func.HttpResponse("{}".format(request_body))
