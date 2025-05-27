#!/bin/bash

# Authenticate using Application Default Credentials (ADC)
gcloud auth application-default login --no-launch

# Mount the GCS bucket using gcsfuse
gcsfuse -o allow_other,rw,implicit_dirs maxk-cloudrun2049-transmissions /mnt/bucket

# Start the application
python3 /app/main.py
