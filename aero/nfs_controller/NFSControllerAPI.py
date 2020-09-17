# Author: Ragy Haddad
import sys,os
import json
from flask import Flask,request,jsonify
from aero.nfs_controller.NFSClientController import ls_cmd,mkdir_cmd,exec_cmd
from werkzeug.utils import secure_filename


app = Flask(__name__)
upload_path = "/exports/api_file_transfers"
if os.path.isdir(upload_path) == False:
    os.system("mkdir -p %s" % upload_path)

app.config["UPLOAD_FOLDER"] = upload_path 

@app.route("/",methods=["GET"])
def home():
    return "NFS CLIENT API\n"

# GET/ 
# List directory 
@app.route("/fs/ls/",methods=["GET"],strict_slashes=False)
def list_command():
    if request.args.get('path'):
        path = request.args.get("path")
    else:
        path = "."
    output = ls_cmd(path)
    return output

# POST/ 
# Push local file to diretory 
@app.route("/fs/cp/",methods=["POST"])
def cp_cmd():
    if request.method == "POST":
        if "file" not in request.files:
            return "File Key not in request: file=<FILE> required in upload\n"
        file = request.files["file"]
        if file.filename == "":
            return ("No filename specified")
        try:
            nfs_path = request.form.get("path")
        except:
            return "Path key required"
        file.save(os.path.join(nfs_path,file.filename))
        return "File Uploaded\n"

# POST/ 
# Mkdir on the file server
@app.route("/fs/mkdir/",methods=["POST"])
def mkdir_cmd():
    if request.method == "POST":
        try:
            path = request.form.get("path")
        except:
            return "Path key required"
        output = mkdir_cmd(path)
        return output

# POST/
# Execute Command on NFS CLIENT Server
@app.route("/fs/exec/",methods=["POST"])
def exec_command():
    if request.method == "POST":
        try:
            command = request.form.get("command")
        except:
            return "Command key required"
        output = exec_cmd(command)
        return output
# GET/ 

    # Get directory from cloud to NFS client directory 

# POST/ 

    # curl a file onto NFS client directory

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)