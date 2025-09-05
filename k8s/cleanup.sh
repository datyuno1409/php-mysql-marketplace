#!/bin/bash

echo "🧹 Cleaning up marketplace deployment..."

kubectl delete namespace marketplace --ignore-not-found=true

echo "✅ Cleanup completed!"
