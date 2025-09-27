# First Contact EIS Deployment Guide

## Overview

This guide covers deploying the First Contact EIS system using Docker, Railway, and other cloud platforms. The system is designed for one-command deployment with comprehensive monitoring and scaling capabilities.

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- Git

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/longbeach/first-contact-eis.git
cd first-contact-eis
```

### 2. Environment Setup

```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

### 3. One-Command Deployment

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access Applications

- **Client Portal**: http://localhost:3000
- **Caseworker Dashboard**: http://localhost:3001
- **City Analytics**: http://localhost:3002
- **Kiosk Interface**: http://localhost:3003
- **Admin Dashboard**: http://localhost:3004
- **API Documentation**: http://localhost:8000/docs

## Docker Deployment

### Development Environment

```bash
# Start with hot reload
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f client
```

### Production Environment

```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3 --scale celery=5
```

### Environment Variables

#### Required Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@db:5432/firstcontact_eis
POSTGRES_USER=firstcontact
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=firstcontact_eis

# Redis
REDIS_URL=redis://redis:6379

# JWT
SECRET_KEY=your-super-secret-jwt-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Services (Optional - Demo mode works without these)
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Demo Mode
DEMO_MODE=true
MOCK_AI_RESPONSES=true
```

#### Optional Variables

```bash
# Application
APP_NAME=First Contact EIS
APP_VERSION=1.0.0
DEBUG=false
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Monitoring
SENTRY_DSN=your-sentry-dsn-here
```

## Railway Deployment

### 1. Install Railway CLI

```bash
npm install -g @railway/cli
```

### 2. Login and Link Project

```bash
railway login
railway link
```

### 3. Deploy

```bash
# Deploy all services
railway up

# Deploy specific service
railway up --service backend
```

### 4. Environment Variables

Set environment variables in Railway dashboard or via CLI:

```bash
railway variables set DATABASE_URL=postgresql://...
railway variables set REDIS_URL=redis://...
railway variables set SECRET_KEY=your-secret-key
```

## Vercel Deployment

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Deploy Frontend Apps

```bash
# Deploy each frontend app
cd frontend/client
vercel --prod

cd ../caseworker
vercel --prod

cd ../city
vercel --prod

cd ../kiosk
vercel --prod

cd ../admin
vercel --prod
```

### 3. Environment Variables

Set environment variables in Vercel dashboard:

```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_WS_URL=wss://your-api-domain.com
```

## AWS Deployment

### 1. ECS with Fargate

```yaml
# ecs-task-definition.json
{
  "family": "firstcontact-eis",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "firstcontact-eis/backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "DATABASE_URL",
          "value": "postgresql://..."
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/firstcontact-eis",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "backend"
        }
      }
    }
  ]
}
```

### 2. RDS Database

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier firstcontact-eis-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username firstcontact \
  --master-user-password your-password \
  --allocated-storage 20
```

### 3. ElastiCache Redis

```bash
# Create Redis cluster
aws elasticache create-cache-cluster \
  --cache-cluster-id firstcontact-eis-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

## Google Cloud Platform

### 1. Cloud Run

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/firstcontact-eis', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/firstcontact-eis']
  - name: 'gcr.io/cloud-builders/gcloud'
    args: ['run', 'deploy', 'firstcontact-eis', '--image', 'gcr.io/$PROJECT_ID/firstcontact-eis', '--platform', 'managed', '--region', 'us-central1']
```

### 2. Cloud SQL

```bash
# Create Cloud SQL instance
gcloud sql instances create firstcontact-eis-db \
  --database-version=POSTGRES_13 \
  --tier=db-f1-micro \
  --region=us-central1
```

## Monitoring and Logging

### 1. Health Checks

```bash
# Check API health
curl http://localhost:8000/health

# Check specific service
curl http://localhost:8000/api/v1/health/ready
```

### 2. Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f client

# Follow logs with timestamps
docker-compose logs -f -t backend
```

### 3. Metrics

The system exposes Prometheus metrics at `/metrics`:

```bash
curl http://localhost:8000/metrics
```

### 4. Database Migrations

```bash
# Run migrations
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend services
docker-compose up -d --scale backend=3 --scale celery=5

# Scale with load balancer
docker-compose -f docker-compose.prod.yml up -d --scale backend=5
```

### Vertical Scaling

Update resource limits in `docker-compose.prod.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

## Security

### 1. SSL/TLS

```bash
# Generate SSL certificates
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Update nginx configuration
# Add SSL configuration to nginx.conf
```

### 2. Firewall

```bash
# Allow only necessary ports
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw enable
```

### 3. Database Security

```bash
# Enable SSL for database connections
# Set up database encryption at rest
# Configure database access controls
```

## Backup and Recovery

### 1. Database Backup

```bash
# Create backup
docker-compose exec db pg_dump -U firstcontact firstcontact_eis > backup.sql

# Restore backup
docker-compose exec -T db psql -U firstcontact firstcontact_eis < backup.sql
```

### 2. Automated Backups

```bash
# Add to crontab
0 2 * * * docker-compose exec db pg_dump -U firstcontact firstcontact_eis > /backups/backup-$(date +\%Y\%m\%d).sql
```

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   ```bash
   # Check database status
   docker-compose ps db
   
   # Check database logs
   docker-compose logs db
   
   # Restart database
   docker-compose restart db
   ```

2. **Redis Connection Failed**
   ```bash
   # Check Redis status
   docker-compose ps redis
   
   # Check Redis logs
   docker-compose logs redis
   ```

3. **AI Service Not Working**
   ```bash
   # Check if demo mode is enabled
   echo $DEMO_MODE
   
   # Check AI service logs
   docker-compose logs backend | grep ai
   ```

4. **Frontend Not Loading**
   ```bash
   # Check frontend logs
   docker-compose logs client
   
   # Check if API is accessible
   curl http://localhost:8000/health
   ```

### Performance Optimization

1. **Database Optimization**
   ```sql
   -- Add indexes
   CREATE INDEX idx_cases_client_id ON cases(client_id);
   CREATE INDEX idx_cases_status ON cases(status);
   CREATE INDEX idx_cases_created_at ON cases(created_at);
   ```

2. **Redis Optimization**
   ```bash
   # Configure Redis memory policy
   redis-cli CONFIG SET maxmemory-policy allkeys-lru
   ```

3. **Frontend Optimization**
   ```bash
   # Build with optimizations
   npm run build
   
   # Enable gzip compression
   # Configure CDN
   ```

## Support

For deployment support:
- **Email**: deployment@firstcontact-eis.org
- **Documentation**: https://docs.firstcontact-eis.org
- **Issues**: https://github.com/longbeach/first-contact-eis/issues
