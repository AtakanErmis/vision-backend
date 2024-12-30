# Vision-Backend

Back-end Layer for NKU Project I - Vision

## Features
- Translation using Google Cloud Translation API
- Florence-2-Large VLM for Image-to-Text retrieval

## Installation

### Prerequisites
- Python 3.10 or higher
- A virtual environment (optional but recommended)
- CUDA-supported hardware

### Steps

1. Clone the repository
2. Initialize a virtual environment using `python -m venv venv`
3. Run `pip install -r requirements.txt` to install the dependencies
4. You have to get credentials and create api project for Google Cloud Translation API. You can provide yout GCloud service account using this command: `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/pk-nku-proje-i-vision-63955b549645.json`
5. Run `fastapi dev api/main.py` to start the development server
6. The server will be running on `http://localhost:8000`

If you want to run for production deployment, use this command: `fastapi run api/main.py`

## API Documentation

You can access Swagger API Documentation from `http://localhost:8000/docs`.