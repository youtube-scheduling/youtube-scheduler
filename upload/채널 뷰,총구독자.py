from googleapiclient.discovery import build

api_key = ${{secrets.API_KEY}}

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part='statistics',
    id='UC_YrqSgdU24vVVrT3lOPYkw'#채널 id 알아낸 후 변경 시 다른 채널도 확인 가능
)

response = request.execute()

print(response)