#!/bin/bash

# Set variables
PROJECT_ID="your-project-id-here"
REGION="us-central1"
REPOSITORY="my-repo"
SERVICE_NAME="support-agent"
IMAGE_NAME="us-central1-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE_NAME:latest"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

echo "Pushing Docker image to Artifact Registry..."
docker push $IMAGE_NAME

echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image=$IMAGE_NAME \
  --platform=managed \
  --region=$REGION \
  --allow-unauthenticated

echo "Deployment complete!"
