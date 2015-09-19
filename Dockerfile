FROM ubuntu:latest

RUN DEBIAN_FRONTEND=noninteractive

# Update installation and install dependencies
RUN apt-get update && apt-get upgrade -y && \
		apt-get install -y python-software-properties python-pip

# Add GlusterFs 3.7 PPA
RUN add-apt-repository ppa:gluster/glusterfs-3.7 && \
    apt-get update

# Install glusterFs
RUN apt-get install -y glusterfs-server

# Install Tutum API library
RUN pip install python-tutum

# Add volume main directory
RUN mkdir /data
VOLUME ["/data"]

ADD script/autoDiscovery.py script/autoDiscovery.py


# Entry point / CMD
CMD [ "python", "script/autoDiscovery.py"]
