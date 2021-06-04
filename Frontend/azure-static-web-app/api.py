from flask import Flask,request
from flask import render_template, Flask, request
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

app = Flask (__name__)

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)

@app.route('/video',methods=['POST'])
def blob_upload():
    if request.method == 'POST':
        f_video=request.files['video']
        f_img=request.files['img']
        #f_img.save("./img/"+f_img.filename)

    try:
        print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")
        connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        # Create the BlobServiceClient object which will be used to create a container client
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)

        # Create a unique name for the container
        #container_name = str(uuid.uuid4())
        container_name = 'example'

        # Create the container
        #container_client = blob_service_client.create_container(container_name)
        # Create a local directory to hold blob data
        local_path = "./storage"
        #os.mkdir(local_path)

        # Create a file in the local data directory to upload and download
        #local_file_name = str(uuid.uuid4()) + ".txt"
        #local_file_name = 'example.txt'
        #upload_file_path = os.path.join(local_path, local_file_name)
        video_name=f_video.filename
        img_name=f_img.filename

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=img_name)

        print("\nUploading to Azure Storage as blob:\n\t" + img_name)

        # Upload the created file
        with open(f_img, "rb") as data:
            blob_client.upload_blob(data)
        return 'success'
        #print("\nListing blobs...")

        # List the blobs in the container
        #blob_list = container_client.list_blobs()
        #for blob in blob_list:
        #    print("\t" + blob.name)

    except Exception as ex:
        print('Exception:')
        print(ex)

@app.route('/')
def blob_list(request):
    print("\nListing blobs...")
    container_client=blob_service_client.get_container_client('example')
    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print(type(blob))




if __name__ == "__main__":
    app.run()