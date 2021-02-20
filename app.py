from flask import Flask, render_template, request, redirect, url_for, session,flash,make_response,session
import cv2
import base64
import stegno
import numpy as np

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
		message = request.form['message']
		image = request.files['file']
		print(image)
		image_str = request.files['file'].read()

		npimg = np.fromstring(image_str, np.uint8)
		image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
		
		encoded = stegno.encode(image, message)

		base64_encoded = stegno.base64writer(encoded, "jpg")

		flag = 1
		return render_template('encode.html',flag=flag, string = base64_encoded.decode("utf-8"))

@app.route('/decode', methods=['GET', 'POST'])
def decode():
	if request.method == 'GET':
		return render_template('decode.html',)
	if request.method == 'POST':
		image_str = request.files['file']
		print(image_str)

		npimg = np.fromstring(image_str, np.uint8)
		image = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

		print(image[:10])
		message = stegno.decode(image)

		# print(message)
		return render_template('decode.html',)




if __name__ == '__main__':
	app.run(debug = True)
