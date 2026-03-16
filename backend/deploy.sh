#!/bin/bash
# deploy.sh — One-command deploy to Google Cloud Run
# Prerequisites: gcloud CLI installed and authenticated
# Usage: GEMINI_API_KEY=your_key bash deploy.sh

set -e

PROJECT_ID="second-pair-of-eyes"
SERVICE_NAME="second-pair-of-eyes"
REGION="us-central1"

echo "🚀 Deploying Second Pair of Eyes to Google Cloud Run..."

gcloud config set project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --platform managed \
  --allow-unauthenticated \
  --port 8000 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "GEMINI_API_KEY=${GEMINI_API_KEY}"

echo ""
echo "✅ Deployment complete!"
echo "Service URL:"
gcloud run services describe $SERVICE_NAME --region $REGION --format "value(status.url)"
