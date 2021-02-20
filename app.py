from flask import Flask, render_template, request, redirect, url_for, session,flash,make_response,session
import cv2
import base64


app = Flask(__name__)

app.secret_key = 'secret'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'GET':
        flag = 0
        return render_template('encode.html',flag=flag)
    else:
        image = request.files['file']  
        image_string = base64.b64encode(image.read())
        # print(image_string)
        image_string = image_string.decode("utf-8")
        flag = 1
        return render_template('encode.html',flag=flag,string=image_string)

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'GET':
        return render_template('decode.html',)




if __name__ == '__main__':
    app.run(debug = True)
