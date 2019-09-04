from flask import Flask,request,jsonify
from ocr import generate_data
import matplotlib.pyplot as plt
app = Flask(__name__)

response = {"data" : 0, "message":"message"}

@app.route("/convert", methods=["POST"])
def call_convert():
	if request.files.get("image") == None:
		response["message"] = "No image"
		return jsonify(response)
	else:
		img = plt.imread(request.files.get("image"))
		plt.imsave("test.png",img)
		response["message"] = generate_data()
		return jsonify(response)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=4000, debug=False)