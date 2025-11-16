# 🏗️ First Contact EIS - GCP Architecture

## System Overview

First Contact EIS is deployed as a **fully serverless, cloud-native application** on Google Cloud Platform, leveraging managed services for maximum reliability, scalability, and minimal operational overhead.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Cloud Load Balancer                         │
│                       (Global HTTPS LB - Optional)                  │
└────────────┬────────────────────────────────────────────────────────┘
             │
             ├──────────────────────────────────────────────────┐
             │                                                  │
┌────────────▼──────────┐                        ┌──────────────▼──────────┐
│   Cloud Run Services  │                        │    Cloud Run Services   │
│  ┌─────────────────┐  │                        │   ┌──────────────────┐  │
│  │ Backend API     │  │                        │   │ Client Portal    │  │
│  │ (FastAPI)       │  │                        │   │ (Next.js)        │  │
│  │ - AI Modules    │  │                        │   ├──────────────────┤  │
│  │ - Auth          │  │                        │   │ Caseworker       │  │
│  │ - CRUD APIs     │  │                        │   │ (Next.js)        │  │
│  └────────┬────────┘  │                        │   ├──────────────────┤  │
│           │           │                        │   │ City Analytics   │  │
│           │           │                        │   │ (Next.js)        │  │
└───────────┼───────────┘                        │   ├──────────────────┤  │
            │                                    │   │ Kiosk UI         │  │
            │                                    │   │ (Next.js)        │  │
            │                                    │   ├──────────────────┤  │
            │                                    │   │ Admin Dashboard  │  │
            │                                    │   │ (Next.js)        │  │
            │                                    │   └──────────────────┘  │
            │                                    └─────────────────────────┘
            │
            ├─────────VPC Connector──────────┐
            │                                │
┌───────────▼───────────┐     ┌──────────────▼─────────────┐
│   Cloud SQL (PG 15)   │     │  Cloud Memorystore (Redis) │
│  ┌─────────────────┐  │     │  ┌──────────────────────┐  │
│  │ Primary         │  │     │  │  Cache & Sessions    │  │
│  │ (Private IP)    │  │     │  │  (Private Network)   │  │
│  ├─────────────────┤  │     │  └──────────────────────┘  │
│  │ Read Replica    │  │     └────────────────────────────┘
│  │ (Optional)      │  │
│  ├─────────────────┤  │
│  │ Auto Backups    │  │
│  │ PITR Enabled    │  │
│  └─────────────────┘  │
└───────────────────────┘
            │
            │
┌───────────▼───────────────────────────────────────────────┐
│                    Supporting Services                    │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │Secret Manager│  │Cloud Storage │  │Cloud Tasks     │  │
│  │- DB Password │  │- Static Files│  │- Background    │  │
│  │- JWT Secret  │  │- Uploads     │  │  Jobs          │  │
│  │- API Keys    │  │- Backups     │  │- Scheduled     │  │
│  └──────────────┘  └──────────────┘  └────────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │Cloud         │  │Artifact      │  │Cloud Scheduler │  │
│  │Monitoring    │  │Registry      │  │- Daily Tasks   │  │
│  │& Logging     │  │- Containers  │  │- Maintenance   │  │
│  └──────────────┘  └──────────────┘  └────────────────┘  │
└───────────────────────────────────────────────────────────┘
            │
            │
┌───────────▼───────────────────────────────────────────────┐
│                   CI/CD Pipeline                          │
│  ┌────────────────────────────────────────────────────┐   │
│  │              Cloud Build                           │   │
│  │  1. Pull code from GitHub                          │   │
│  │  2. Build 6 container images (parallel)            │   │
│  │  3. Push to Artifact Registry                      │   │
│  │  4. Deploy to Cloud Run                            │   │
│  │  5. Run database migrations                        │   │
│  └────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

## Component Details

### Cloud Run Services

#### Backend API
- **Image**: Python 3.11 slim with FastAPI
- **Resources**: 2 vCPU, 2GB RAM
- **Scaling**: 0-10 instances (configurable)
- **Timeout**: 300s
- **Concurrency**: 80 requests per instance
- **Features**:
  - 6 AI modules for intelligent case management
  - JWT authentication
  - PostgreSQL via SQLAlchemy
  - Redis caching
  - Background task processing

#### Frontend Services (5x Next.js)
- **Images**: Node 18 Alpine with Next.js 14
- **Resources**: 1 vCPU, 512MB RAM each
- **Scaling**: 0-10 instances (configurable)
- **Features**:
  - Server-side rendering
  - Static optimization
  - API proxy to backend
  - TypeScript
  - Tailwind CSS

### Cloud SQL (PostgreSQL 15)

#### Configuration
- **Tier**: db-f1-micro (dev) to db-custom-4-16384 (prod)
- **Storage**: SSD with auto-resize
- **Backups**:
  - Automated daily backups
  - 7-day retention
  - Point-in-time recovery enabled
  - Transaction log retention: 7 days

#### High Availability (Production)
- Regional deployment
- Automatic failover
- Read replicas for scaling
- Connection pooling via Cloud SQL Proxy

#### Security
- Private IP only (no public access)
- SSL/TLS required
- Encrypted at rest
- IAM database authentication

### Cloud Memorystore (Redis)

#### Configuration
- **Version**: Redis 7.0
- **Tier**: Basic (dev/staging) or Standard HA (production)
- **Memory**: 1GB (dev) to 5GB+ (production)
- **Network**: Private VPC access only

#### Use Cases
- Session storage
- API response caching
- Rate limiting
- Real-time features
- Background job queue

### Networking

#### VPC
- **CIDR**: 10.0.0.0/24 (main subnet)
- **VPC Connector**: 10.8.0.0/28 (Cloud Run access)
- **Private Google Access**: Enabled
- **Service Networking**: For Cloud SQL and Redis

#### Security
- No public IPs for databases
- VPC connector for secure Cloud Run → Database communication
- Cloud Armor (optional) for DDoS protection
- SSL certificates managed by Cloud Run

### Storage

#### Cloud Storage
- **Buckets**:
  - Assets bucket (static files, uploads)
  - Terraform state bucket
  - Backup bucket
- **Features**:
  - Versioning enabled
  - Lifecycle policies (90-day retention)
  - CORS configured
  - Uniform bucket-level access

### Secrets Management

#### Secret Manager
- **Secrets**:
  - Database password (auto-generated)
  - JWT secret key (auto-generated)
  - API keys (optional)
- **Features**:
  - Automatic replication
  - Version management
  - IAM-based access control
  - Audit logging

### Background Jobs

#### Cloud Tasks
- **Queue**: firstcontact-eis-tasks
- **Rate Limits**:
  - Max concurrent: 100
  - Max per second: 500
- **Retry Config**:
  - Max attempts: 5
  - Max retry duration: 4s
  - Exponential backoff

#### Cloud Scheduler
- **Jobs**:
  - Daily cleanup (2 AM)
  - Database maintenance
  - Analytics aggregation
  - Report generation

### Monitoring & Observability

#### Cloud Monitoring
- **Metrics**:
  - Request count
  - Latency (p50, p95, p99)
  - Error rate
  - CPU/Memory usage
  - Database connections

#### Cloud Logging
- **Log Types**:
  - Application logs
  - Audit logs
  - System logs
- **Retention**: 30 days (configurable)
- **Export**: BigQuery (optional)

#### Alerts
- High error rate (>5%)
- High latency (>2s p95)
- Service down
- Database high connections
- Budget exceeded

### CI/CD

#### Cloud Build
- **Trigger**: GitHub push to main
- **Steps**:
  1. Build backend image (Python)
  2. Build 5 frontend images (Next.js) - parallel
  3. Push all images to Artifact Registry
  4. Deploy backend to Cloud Run
  5. Deploy frontends to Cloud Run
  6. Run database migrations
  7. Health checks

#### Build Optimization
- Multi-stage Dockerfiles
- Layer caching
- Parallel builds
- Minimal base images (Alpine)
- Build time: ~8-10 minutes

### Security Architecture

#### Defense in Depth
1. **Network Layer**
   - Private VPC
   - No public IPs for data stores
   - VPC Service Controls (optional)

2. **Application Layer**
   - JWT authentication
   - RBAC with IAM
   - Input validation
   - CSRF protection

3. **Data Layer**
   - Encryption at rest
   - Encryption in transit (SSL/TLS)
   - Secret Manager for credentials
   - Database IAM authentication

4. **Monitoring Layer**
   - Audit logging
   - Security Command Center (optional)
   - Anomaly detection
   - SIEM integration (optional)

## Scalability

### Horizontal Scaling
- **Cloud Run**: Auto-scales 0-100+ instances
- **Cloud SQL**: Read replicas for read scaling
- **Redis**: Sharding (manual setup)

### Vertical Scaling
- **Cloud Run**: Up to 8 vCPU, 32GB RAM per instance
- **Cloud SQL**: Up to 96 vCPU, 624GB RAM
- **Redis**: Up to 300GB memory

### Geographic Distribution
- **Multi-region**: Deploy Cloud Run in multiple regions
- **Global Load Balancer**: Route to nearest region
- **Cloud SQL Cross-region replicas**: For disaster recovery

## Disaster Recovery

### RTO/RPO
- **RTO (Recovery Time Objective)**: < 1 hour
- **RPO (Recovery Point Objective)**: < 5 minutes

### Backup Strategy
1. **Database**:
   - Daily automated backups
   - Point-in-time recovery
   - Cross-region backup (production)

2. **Application**:
   - Container images in Artifact Registry
   - Infrastructure as Code (Terraform)
   - Git repository

3. **Recovery Procedure**:
   - Restore database from backup
   - Redeploy services via Cloud Build
   - Update DNS if needed

## Cost Optimization

### Development
- Scale-to-zero for all services
- Smallest database tier (db-f1-micro)
- Basic Redis (1GB)
- Minimal logging retention

### Production
- Min 1 instance for critical services
- Sustained use discounts
- Committed use discounts (1-3 year)
- Preemptible VMs for background jobs (if applicable)

### Cost Breakdown (Monthly, Production)
- Cloud Run: $20-50
- Cloud SQL: $100-150
- Cloud Memorystore: $80-100
- Cloud Storage: $5-10
- Networking: $5-10
- Monitoring: $5-10
- **Total: ~$215-330/month**

## Performance Characteristics

### Latency
- **API Response**: < 200ms (p95)
- **AI Processing**: < 3s
- **Page Load**: < 2s
- **Database Query**: < 50ms (p95)

### Throughput
- **Requests/second**: 1000+ (with 10 instances)
- **Concurrent users**: 5000+
- **Database connections**: 100 (configurable)

### Availability
- **Cloud Run SLA**: 99.95%
- **Cloud SQL SLA**: 99.95%
- **Overall SLA**: 99.9%+

## Compliance

### Standards
- HIPAA-equivalent data protection
- HUD/HMIS compliance
- SOC 2 Type II (via GCP)
- GDPR ready

### Audit
- All access logged
- Immutable audit trail
- Regular compliance scans
- Data residency controls

---

**Architecture designed for scale, security, and operational excellence**
