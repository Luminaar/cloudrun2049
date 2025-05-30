FROM ubuntu:latest

# Install google cloud sdk
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates gnupg

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list


RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add -

# Install necessary packages
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get update && apt-get install -y google-cloud-sdk

# Install google-cloud-pubsub
RUN pip3 install google-cloud-pubsub

# Create a mount point
RUN mkdir /mnt/bucket

# Copy the application code
COPY main.py /app/main.py

# Copy the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entry point
ENTRYPOINT ["/entrypoint.sh"]
