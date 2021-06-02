import datetime
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json

with open("data.json", "r") as dt_json:

    videodata=json.load(dt_json)

CLIENT_SECRET_FILE: ${{secrets.jsonfile}}
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)

upload_date_time = videodata['uploaddate']

request_body = {
    'snippet': {
        'title': videodata['title'],
        'description': videodata['description'],
    },
    'status': {
        'privacyStatus': 'private',
        'publishAt': upload_date_time,
        'selfDeclaredMadeForKids': False, 
    }
}

mediaFile = MediaFileUpload('1.avi')

response_upload = youtube.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=mediaFile
).execute()

youtube.thumbnails().set(
    videoId=response_upload.get('id'),
    media_body=MediaFileUpload('1.png')
).execute()

