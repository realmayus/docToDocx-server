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
    app.run(port=5001, debug=False)
