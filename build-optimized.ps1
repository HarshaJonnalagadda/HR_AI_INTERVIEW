# Optimized build script for HR AI Interviewer (PowerShell)

Write-Host "🚀 Starting optimized build process..." -ForegroundColor Green

# Build backend with caching
Write-Host "📦 Building backend..." -ForegroundColor Yellow
docker build `
    --cache-from hr-ai-backend:latest `
    -t hr-ai-backend:latest `
    -f Dockerfile .

# Build frontend with caching
Write-Host "🎨 Building frontend..." -ForegroundColor Yellow
docker build `
    --cache-from hr-ai-frontend:latest `
    -t hr-ai-frontend:latest `
    -f frontend/Dockerfile.secure `
    frontend/

# Build and start all services
Write-Host "🔧 Starting all services..." -ForegroundColor Yellow
docker-compose -f docker-compose.prod.yml up -d --build

Write-Host "✅ Build complete! Services starting..." -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost" -ForegroundColor Cyan
Write-Host "🔧 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📊 Health checks will be available in 30 seconds" -ForegroundColor Yellow

# Wait for services to be healthy
Write-Host "⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service health
Write-Host "📋 Service Status:" -ForegroundColor Green
docker-compose -f docker-compose.prod.yml ps
