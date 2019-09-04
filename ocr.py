import cv2
import numpy as np
import pytesseract
from PIL import Image
from pytesseract import image_to_string
import os

# Path of working folder on Disk
# src_path = "/home/jeffin/Desktop/"
src_path = os.getcwd()

def get_string(img_path):
    # Read image with opencv
    print(img_path)
    img = cv2.imread(img_path)
    print(img)
    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    # Write image after removed noise
    cv2.imwrite(src_path + "/removed_noise.png", img)

    #  Apply threshold to get image with only black and white
    #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(src_path + "/thres.png", img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open(src_path + "/thres.png"))

    # Remove template file
    #os.remove(temp)

    return result


# print('--- Start recognize text from image ---')
def generate_data():
	
	content = (get_string(src_path + "/test") )
	f = open("content.txt", "w")
	f.write(content)
	f.close()
	f = open("content.txt", "r")
	lines = f.readlines()
	data = {}
	for i in range(len(lines)):
		# print(lines[i])
		if lines[i].split(" ")[0] == "Billed":
			billed =i
		if lines[i].split(" ")[0] == "Description":
			des=i
		if lines[i].split(" ")[0] == "Subtotal":
			subtotal=i
			# print(lines[i+2].split(""))
	print("------ Done -------")
	print(billed,des,subtotal)
	billed_data = lines[billed+2].split(" ")
	data["billed_to"]=billed_data[0]+billed_data[1]
	data["invoice_number"]=billed_data[2]
	items_dir={}
	item_no=0
	item_info=[]
	for i in range(des+1,subtotal):
		if lines[i] != "\n":
			item_info.append(lines[i])
	item_info = item_info[::2]
	for j in item_info:
		item_no+=1
		temp_item={}
		item_data = j.split(" ")
		temp_item["amount"]=item_data[-1].split("\n")[0]
		temp_item["qty"]=item_data[-2]
		temp_item["unit_cost"]=item_data[-3]
		temp_item["Description"]="_".join(item_data[:-3])
		items_dir[str(item_no)]=temp_item
	price_info = []
	for k in range(subtotal,subtotal+3):
		if lines[k]!= "\n":
			price_info.append(lines[k])
	# print(price_info)

	data["subtotal"] = price_info[0].split(" ")[-1].split("\n")[0]
	data["tax"] = price_info[1].split(" ")[-1].split("\n")[0]
	data["total"] = price_info[2].split(" ")[-1].split("\n")[0]


	data["items"] = items_dir
	return(data)
# print(generate_data())