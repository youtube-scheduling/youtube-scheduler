import json
import requests
import logging
import azure.functions as func


def main(req: func.HttpRequest, tabledatas) -> func.HttpResponse:

    rowkey = req.params.get('RowKey')
    datas = json.loads(tabledatas)
    
    refdata = None
    for data in datas:
        if data['RowKey'] == rowkey:
            refdata = data
            break
    
    try:
        video_name = refdata['video']
        thumbnail_name = refdata['thumbnail']
    except Exception:
        print("No Entity(RowKey:{}) in Table Storage".format(rowkey))

    request_body = {
        'snippet': {
            'title': refdata['title'],
            'description': refdata['description'],
            'tags': refdata['tags'].split(', ')
        }
    }
    datas = {
        'request_body' : request_body,
        'video' : video_name
    }

    URL = "https://yvsfunction.azurewebsites.net/api/YoutubeUpload"
    res = requests.post(URL, data=json.dumps(datas))


    return func.HttpResponse("{}\n{}".format(request_body, res))
