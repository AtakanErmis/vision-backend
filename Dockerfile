FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Move project files to the container
COPY . /app
COPY nku-proje-1-vision-pk.json /app/nku-proje-1-vision-pk.json
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Set the environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/nku-proje-1-vision-pk.json

# Run the application
CMD ["fastapi", "run", "api/main.py"]

