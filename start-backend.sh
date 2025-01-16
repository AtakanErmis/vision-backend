#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS=/workspace/vision-backend/nku-proje-1-vision-pk.json
pip install -r requirements.txt
fastapi run api/main.py