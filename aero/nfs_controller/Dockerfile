FROM python:3
MAINTAINER Ragy Haddad 
RUN apt-get -y update && apt-get -y install nfs-common
RUN apt-get -y install curl 
RUN pip install flask
RUN pip install requests
RUN pip install google-cloud-storage
RUN mkdir /exports 
VOLUME /exports
EXPOSE 2049/tcp
EXPOSE 20048/tcp
EXPOSE 3000/tcp
RUN mkdir -p /home/scripts
COPY NFSClientController.py /home/scripts/NFSClientController.py 
COPY NFSControllerAPI.py /home/scripts/NFSControllerAPI.py 
WORKDIR /home/scripts
# RUN API
ENTRYPOINT [ "python3","-u","NFSControllerAPI.py"]

