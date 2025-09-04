#!/bin/bash
# Optimized build script for HR AI Interviewer

set -e

echo "🚀 Starting optimized build process..."

# Build backend with caching
echo "📦 Building backend..."
docker build \
    --target production \
    --cache-from hr-ai-backend:latest \
    -t hr-ai-backend:latest \
    -f Dockerfile .

# Build frontend with caching
echo "🎨 Building frontend..."
docker build \
    --cache-from hr-ai-frontend:latest \
    -t hr-ai-frontend:latest \
    -f frontend/Dockerfile.secure \
    frontend/

# Build and start all services
echo "🔧 Starting all services..."
docker-compose -f docker-compose.prod.yml up -d --build

echo "✅ Build complete! Services starting..."
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000"
echo "📊 Health checks will be available in 30 seconds"

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 30

# Check service health
docker-compose -f docker-compose.prod.yml ps
