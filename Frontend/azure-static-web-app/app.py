from flask import Flask, render_template, request
import requests
import os


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def get_infomation():
    
    if request.method == 'POST':
        data = request.form

        path = os.getcwd()
        path = path + '/storage'
        text_path = path + "/library.txt"
        img_path = path + '/image.jpg'
        video_path = path + '/video.avi'

        f = open(text_path, "w")

        cutted_tags = data['tag'].split(',')
        
        f.write(data['title'])
        f.write('\n')

        for i in cutted_tags:
            f.write(i)
            f.write(' ')
        f.write('\n');
        
        f.write(data['content'])
        f.write('\n')
        f.write(data['date'])
        f.write(' ')
        f.write(data['time'])

        f.close()

        video = request.files['video']
        video.save(video_path)

        img = request.files['img']
        img.save(img_path)

        print(data['title'])

    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug = True)
