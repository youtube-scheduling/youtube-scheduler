import datetime
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRET_FILE = ${{secrets.oauth}}
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)

upload_date_time = datetime.datetime(2021, 4, 17, 0, 0, 0).isoformat() + '.000Z'

request_body = {
    'snippet': {
        'categoryI': 19,
        'title': ' upload test',
        'description': 'anyvideo',
        'tags': ['fortest', 'Youtube API']
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
