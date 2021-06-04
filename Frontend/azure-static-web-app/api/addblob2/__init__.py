import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.files['imgFile']
    video=req.files['videoFile']
    #print(name.filename)
    return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")

