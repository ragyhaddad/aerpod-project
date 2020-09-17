# Author: Ragy Haddad
import sys,os 
import json 
import requests
import logging
import subprocess,shlex
from subprocess import PIPE,Popen
# Interface With The NFSClientAPI Through the NFSAdapter
class NFSAdapter:
    def __init__(self,port=3000,address="localhost"):
        pass
        self.port = port 
        self.address = address
        self.base_url = "http://%s:%s" % (self.address,self.port)
        self.deploymeny_connection = False
    
    # Check if Attachment to APIs it working
    def check_deployment_connection(self):
        pass

    # /GET
    # LS Command 
    def ls_cmd(self,path):
        sub_url = "/fs/ls/?path=%s" % path.strip()
        url = self.base_url + sub_url
        r = requests.get(url)
        r = r.text
        sys.stdout.write(r)

    # /POST
    # Move local files to NFS
    def cp_cmd_file(self,local_path,target_path):
        sub_url = "/fs/cp/"
        url = self.base_url + sub_url 
        file = { "file" : open(local_path,"rb")}
        data = {"path":target_path}
        r = requests.post(url,files=file,data=data)
        r = r.text 
        sys.stdout.write(r)

    # /Set up portforwarding
    # Forward Service Ports to local ports
    def attach_nfs(self):
        FNULL = open(os.devnull, 'w')
        logging.info("Attaching to NFS FileSystem")
        cmd_nfs = "kubectl port-forward deployment/nfs-controller-deployment 3000:3000"
        cmd_nfs_arr = shlex.split(cmd_nfs)
        try:
            # p = subprocess.call(cmd_nfs_arr,stdout=FNULL,stderr=PIPE,shell=False)
            os.system(cmd_nfs) 
            print("Connected to NFS Client on PORT 3000")
        except:
            logging.error("NFS Client Deploment is not up, please check that the NFSController Deployment is running on the cluster")