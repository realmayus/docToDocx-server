import os
import subprocess
import configparser
from flask import Flask, request, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

app = Flask(__name__)

config = configparser.ConfigParser()
config.read("./config.ini")
libreoffice_binary = config["config"]["libreoffice_bin"]
allow = config["config"]["allow_origins"].split(",")


#  const allowedOrigins = ['http://localhost:8081', 'http://localhost:8080'];
#  const origin = req.headers.origin;
#  if (allowedOrigins.includes(origin)) {
#    res.setHeader('Access-Control-Allow-Origin', origin);
#  }
#  //res.header('Access-Control-Allow-Origin', 'http://127.0.0.1:8020');
#  res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
#  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
#  res.header('Access-Control-Allow-Credentials', "true");

@app.after_request
def add_cors_headers(response):
    if hasattr(request, "Origin"):
        r = request.headers['Origin']
        print(r)
        if r in allow:
            response.headers.add('Access-Control-Allow-Origin', r)
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'Cache-Control')
            response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With')
            response.headers.add('Access-Control-Allow-Headers', 'Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
        return response
    return response


@app.route("/", methods=["POST"])
def hello():
    # Delete existing files in /uploads to free up space
    for root, dirs, files in os.walk("./uploads"):
        for file in files:
            os.remove(os.path.join(root, file))

    file: FileStorage = request.files["file"]
    if file.filename.endswith('.doc'):
        file.save(os.path.join("./uploads", secure_filename(file.filename)))
        subprocess.call([libreoffice_binary, '--headless', '--convert-to', 'docx', "./uploads/" + secure_filename(file.filename), "--outdir", "./uploads/"])
        return send_from_directory(directory="./uploads/", filename=secure_filename(file.filename + "x"))
    return "File must be a .doc file", 400


if __name__ == "__main__":
    print("Allowed origins:", ", ".join(allow))
    app.run(port=5001, debug=False)
