#!/bin/bash

cd /workspace
export GOOGLE_APPLICATION_CREDENTIALS=/workspace/vision-backend/pk-nku-proje-i-vision-63955b549645.json
pip install -r requirements.txt
fastapi run api/main.py