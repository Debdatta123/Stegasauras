import numpy as np
import cv2
import base64
from random import randint

filename = "./romania.png"

def base64reader(im_b64):
	im_bytes = base64.b64decode(im_b64)
	im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
	img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
	return img

def base64writer(im_cv, filetype):
	_, im_arr = cv2.imencode('.'+filetype, im_cv)  # im_arr: image in Numpy one-dim array format.
	im_bytes = im_arr.tobytes()
	im_b64 = base64.b64encode(im_bytes)
	return im_b64

def encode(image, message):
	end = "#####"
	message = message + end

	height, width, channels = image.shape

	print(height, width)

	max_len = height*width*channels // 8
	
	if len(message) > max_len:
		error_msg = "Bigger Image Required"
		return False, error_msg

	binary_message = ''.join(format(ord(i), '08b') for i in message) 

	print(message)
	print(binary_message)

	message_len = len(binary_message)
	index = 0

	orig_image = image
	for values in image:
		for pixel in values:
			# convert RGB values to binary format
			r, g, b = pixel
			# modify the least significant bit only if there is still data to store
			if index < message_len:
				# hide the data into least significant bit of red pixel
				r = format(int(r),"08b")
				pixel[0] = int(r[:-1] + binary_message[index], 2)
				index += 1
			if index < message_len:
				# hide the data into least significant bit of green pixel
				g = format(int(g),'08b')
				pixel[1] = int(g[:-1] + binary_message[index], 2)
				index += 1
			if index < message_len:
				# hide the data into least significant bit of  blue pixel
				b = format(int(b),'08b')
				pixel[2] = int(b[:-1] + binary_message[index], 2)
				index += 1
			# if data is encoded, just break out of the loop
			if index >= message_len:
				break

	return image

def decode(image):
	binary_message = ""
	for values in image:
		for pixel in values:
			r, g, b = pixel #convert the red,green and blue values into binary format
			  
			r = format(int(r),"08b")
			binary_message += r[-1] #extracting data from the least significant bit of red pixel
			
			g = format(int(g),"08b")
			binary_message += g[-1] #extracting data from the least significant bit of red pixel
			
			b = format(int(b),"08b")
			binary_message += b[-1] #extracting data from the least significant bit of 

	bytes_message = [ binary_message[i: i+8] for i in range(0, len(binary_message), 8) ]

	message = ""
	for byte in bytes_message:
		message += chr(int(byte, 2))
		if message[-5:] == "#####": #check if we have reached the delimeter which is "#####"
			break
		
	message = message[:-5]
	if message == "":
		return False
	
	return message


# image = cv2.imread("oyo.png")
# encoded = encode(image, "Hello World")

# base64_encoded = base64writer(encoded, "png")

# image2 = base64reader(base64_encoded)

# print(decode(image2))

# diff = image2 - encoded

# cv2.imshow("diff", diff)
# # print(diff)

# message = decode(image)

# print(message)