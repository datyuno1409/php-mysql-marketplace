#!/bin/bash

set -e

echo "🚀 Starting deployment of PHP MySQL Marketplace..."

SERVER_HOST="103.9.205.28"
SERVER_PORT="2012"
SERVER_USER="root"
REPO_URL="https://github.com/datyuno1409/php-mysql-marketplace.git"
APP_NAME="marketplace"

echo "📦 Cloning repository on server..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "rm -rf /tmp/$APP_NAME && git clone $REPO_URL /tmp/$APP_NAME"

echo "🐳 Building Docker image..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "cd /tmp/$APP_NAME && docker build -t $APP_NAME-php:latest ."

echo "📋 Applying Kubernetes manifests..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "cd /tmp/$APP_NAME && kubectl apply -f k8s/"

echo "⏳ Waiting for deployments to be ready..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "kubectl wait --for=condition=available --timeout=300s deployment/mysql-deployment -n marketplace"
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "kubectl wait --for=condition=available --timeout=300s deployment/php-deployment -n marketplace"
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "kubectl wait --for=condition=available --timeout=300s deployment/nginx-deployment -n marketplace"

echo "🌐 Getting service information..."
ssh -p $SERVER_PORT $SERVER_USER@$SERVER_HOST "kubectl get services -n marketplace"

echo "✅ Deployment completed successfully!"
echo "🔗 Access your application at: http://$SERVER_HOST"
