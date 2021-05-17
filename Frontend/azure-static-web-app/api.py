from flask import Flask,request
from flask import render_template, Flask, request
 
app = Flask (__name__)
 
@app.route('/')
def hello_world():
    return 'Hello, World!'
 
@app.route('/video',methods=['POST'])
def hello_user():
    if request.method == 'POST':
        f=request.files['video']
        f.save("./img/"+f.filename)
        return 'success'
    
if __name__ == "__main__":
    app.run()