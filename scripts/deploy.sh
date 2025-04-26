#!/bin/bash

# Exit immediately if any command fails
set -e

# Load environment variables from .env file (if you have one)
export $(grep -v '^#' .env | xargs)

# Check if required variables are set
if [ -z "$PROJECT_ID" ] || [ -z "$REGION" ] || [ -z "$REPOSITORY" ] || [ -z "$SERVICE_NAME" ]; then
  echo "Missing environment variables. Check your .env file!"
  exit 1
fi

echo "hey"

# Enable Artifact Registry API (one-time, but safe to keep)
gcloud services enable artifactregistry.googleapis.com

# Create the Artifact Registry repository if not exists already
gcloud artifacts repositories create $REPOSITORY \
  --repository-format=docker \
  --location=$REGION \
  --description="Docker repository for Support Agent app" || echo "Repository may already exist, skipping."


# Compose image name
IMAGE_NAME="$REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY/$SERVICE_NAME:latest"

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
