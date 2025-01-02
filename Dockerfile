FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# Move project files to the container
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install -r requirements.txt

# Get private key from environment variable and save it to a file
ARG RUNPOD_SECRET_nku_project_vision_pk
RUN echo "$RUNPOD_SECRET_nku_project_vision_pk" > /app/nku-proje-1-vision-pk.json

# Set the environment variable
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/nku-proje-1-vision-pk.json

# Run the application
CMD ["fastapi", "run", "api/main.py"]

