# Use slim-buster (debian based) Container to build this container 
# for Network Automation
FROM python:3.9.0rc1-slim-buster

# Install "yum database update", python38, and NORNIR module
#RUN yum -y update && yum install -y python38 && python3 -m pip install nornir
RUN python3 -m pip install nornir

# Copy scripts and necessary files to /src folder
COPY . /src/Nornir/

# Run bash
CMD ["/bin/bash"]

