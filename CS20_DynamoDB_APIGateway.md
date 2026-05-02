# CS20: DynamoDB & API Gateway
### AWS SAA-C03 Cheat Sheet

---

## DynamoDB

### Key Concepts
- **Fully managed NoSQL** database (key-value + document)
- **Serverless** — no servers to manage, auto-scales
- Single-digit **millisecond latency** at any scale
- Multi-AZ by default (3 AZs, highly available)
- Maximum item size: **400 KB**
- Supports **transactions** (ACID)

### Data Model
```
Table
  └── Items (like rows)
       └── Attributes (like columns, schema-free)

Primary Key (must define at creation):
  Option 1: Partition Key only (must be unique)
  Option 2: Partition Key + Sort Key (combination must be unique)
```

### Key Concepts
| Concept | Description |
|---------|-------------|
| **Partition Key** | Hash key - determines which partition stores the item |
| **Sort Key** | Range key - allows multiple items per partition key (sorted) |
| **Item** | Single data record (like a row) |
| **Attribute** | Data field (schema-free, each item can differ) |
| **Indexes** | Additional access patterns beyond primary key |

---

### Capacity Modes

| Mode | How It Works | Use Case |
|------|-------------|----------|
| **Provisioned** | Set RCU/WCU manually (or Auto Scaling) | Predictable traffic, cost control |
| **On-Demand** | Pay per request, auto-scales instantly | Unpredictable, spiky, new tables |

**Read/Write Capacity Units:**
- **1 WCU** = 1 write/sec for item up to 1 KB
- **1 RCU** = 1 strongly consistent read/sec for item up to 4 KB
- **1 RCU** = 2 eventually consistent reads/sec for item up to 4 KB
- **Transactional**: 2x the cost (2 WCU per transactional write, 2 RCU per transactional read)

**Calculation Example:**
```
10 items/sec × 6 KB each (strongly consistent reads):
  Each item needs: ceiling(6/4) = 2 RCUs
  Total: 10 × 2 = 20 RCUs

10 items/sec × 6 KB each (eventually consistent):
  Total: 20 / 2 = 10 RCUs
```

> **Exam Tip**: If you see RCU/WCU calculations, remember: RCU is per 4 KB, WCU is per 1 KB. Eventually consistent = half the RCUs.

---

### Secondary Indexes

| Type | Description | Key Points |
|------|-------------|------------|
| **GSI (Global Secondary Index)** | Alternate partition + sort key | New partition key, can add anytime, has own RCU/WCU |
| **LSI (Local Secondary Index)** | Same partition key, different sort key | Must create at table creation, shares table's RCU/WCU |

**GSI:**
- Can have different partition AND sort key from base table
- Has its own provisioned capacity (separate RCU/WCU)
- **Supports eventual consistency only**
- Can add/remove after table creation
- Up to 20 per table

**LSI:**
- Same partition key, different sort key
- **Supports strong consistency**
- Must define at table creation (can't add later)
- Up to 5 per table
- Shares base table's RCU/WCU

> **Exam Tip**: "Query by different attribute" = GSI. "Different sort on same partition" = LSI. Usually GSI is the answer.

---

### DynamoDB Features

| Feature | Description |
|---------|-------------|
| **DynamoDB Streams** | Ordered stream of item-level changes (CDC) |
| **TTL (Time to Live)** | Auto-delete expired items (free, no WCU consumed) |
| **DAX (DynamoDB Accelerator)** | In-memory cache for DynamoDB (microsecond reads) |
| **Global Tables** | Multi-region, multi-active replication |
| **Point-in-Time Recovery** | Continuous backups, restore to any second (35 days) |
| **On-Demand Backup** | Full backup anytime (no performance impact) |
| **Encryption** | Always encrypted at rest (AWS owned, KMS, or CMK) |
| **PartiQL** | SQL-compatible query language for DynamoDB |

---

### DynamoDB Streams
- **Ordered** sequence of item modifications (INSERT, MODIFY, DELETE)
- Retention: **24 hours**
- Use with: Lambda triggers, Kinesis adapter
- Use Cases: Replicate changes, trigger workflows, build views, audit

```
DynamoDB Table → DynamoDB Stream → Lambda → [Process change]
                                         → OpenSearch (search)
                                         → SNS (notification)
                                         → Another table (aggregation)
```

### DynamoDB Accelerator (DAX)
- **In-memory cache** specifically for DynamoDB
- **Microsecond** read latency (vs millisecond)
- **Write-through** cache (writes go through DAX to DynamoDB)
- API-compatible (drop-in replacement, no code changes)
- Multi-AZ (3+ nodes recommended for production)
- 5-minute default TTL

**DAX vs ElastiCache:**
| Feature | DAX | ElastiCache |
|---------|-----|-------------|
| Purpose | DynamoDB caching only | General-purpose caching |
| API | DynamoDB-compatible | Redis/Memcached API |
| Integration | Transparent (no code changes) | Application-level changes |
| Use Case | DynamoDB read-heavy workloads | Any caching need |

### Global Tables
- **Multi-region, multi-active** (read AND write in any region)
- **Active-Active** replication (not active-passive)
- Sub-second replication between regions
- Requires: DynamoDB Streams enabled
- Conflict resolution: Last-writer-wins
- Use Case: Global apps with low-latency access in any region

### TTL (Time to Live)
- Automatically deletes expired items
- **No cost** (no WCU consumed)
- Define TTL attribute (epoch timestamp)
- Items deleted within 48 hours of expiration
- Expired items appear in Streams (if enabled) as DELETE
- Use Case: Session data, temporary records, log cleanup

> **Exam Tips**:
> - "Microsecond reads from DynamoDB" = DAX
> - "React to DynamoDB table changes" = DynamoDB Streams + Lambda
> - "Multi-region active-active database" = DynamoDB Global Tables
> - "Auto-expire old data" = TTL
> - "Most cost-effective for unpredictable traffic" = On-Demand mode
> - "Search DynamoDB data" = Stream to OpenSearch

---

## API Gateway

### Key Concepts
- Fully managed service to create, publish, and manage **APIs**
- Acts as "front door" for backend services
- Supports: **REST**, **HTTP**, and **WebSocket** APIs
- Serverless (pairs with Lambda, but can proxy to any HTTP backend)

### API Types

| Type | Protocol | Features | Use Case |
|------|----------|----------|----------|
| **REST API** | HTTP | Full-featured (caching, API keys, usage plans, WAF) | Full REST API with all features |
| **HTTP API** | HTTP | Cheaper, faster, simpler (no caching, limited features) | Simple proxy, OIDC/OAuth2 |
| **WebSocket API** | WebSocket | Two-way communication, persistent connection | Chat, real-time dashboards, gaming |

### REST API vs HTTP API

| Feature | REST API | HTTP API |
|---------|----------|----------|
| Cost | Higher | **70% cheaper** |
| Latency | Higher | **Lower** |
| Caching | ✅ | ❌ |
| API Keys / Usage Plans | ✅ | ❌ |
| WAF Integration | ✅ | ❌ |
| Resource Policies | ✅ | ❌ |
| Request Validation | ✅ | ❌ |
| Private integrations | ✅ | ✅ |
| OAuth 2.0 / OIDC | ✅ | ✅ (simpler) |
| Lambda Proxy | ✅ | ✅ |

---

### API Gateway Features

| Feature | Description |
|---------|-------------|
| **Stages** | Deploy to: dev, staging, prod (each has own URL) |
| **Throttling** | Default: 10,000 req/s, burst 5000 (account-level) |
| **Caching** | Cache responses (TTL 0-3600 sec), reduces backend calls |
| **CORS** | Enable cross-origin requests from browsers |
| **Usage Plans + API Keys** | Rate limiting per customer |
| **Request/Response Transformation** | Modify payloads using mapping templates |
| **Request Validation** | Validate request body/parameters |
| **Custom Domain** | Map your domain to API (via Route 53 + ACM) |
| **Canary Deployments** | Route % of traffic to new version |

### API Gateway Timeout
- **29 seconds maximum** integration timeout
- If Lambda takes > 29 sec → API Gateway returns 504 Gateway Timeout
- For longer: Use async pattern (API GW → Lambda → S3/SQS, poll for result)

---

### API Gateway Security

**Authentication & Authorization:**

| Method | Description |
|--------|-------------|
| **IAM** | Sig V4 signature (for AWS users/services) |
| **Cognito Authorizer** | User pool tokens (for app users) |
| **Lambda Authorizer** (Custom) | Custom auth logic (token/request-based) |
| **API Key** | Simple key (not for auth, use for throttling) |

**Other Security:**
- **Resource Policy**: Control who can invoke API (IP, VPC, account)
- **WAF**: Attach to REST API for SQLi, XSS protection, rate limiting
- **Mutual TLS**: Client certificate validation
- **Private API**: Accessible only from VPC (via VPC Endpoint)

### Lambda Authorizer
```
Client → API Gateway → Lambda Authorizer → Validates token
                                              → Returns IAM policy
                                              → Policy cached (up to 1 hour)
                            ↓ (if authorized)
                       Backend Lambda
```

---

### API Gateway Integration Types

| Type | Description |
|------|-------------|
| **Lambda Proxy** | Passes full request to Lambda (most common) |
| **Lambda Custom** | Transform request before Lambda, transform response |
| **HTTP Proxy** | Forward to HTTP endpoint (ALB, on-prem) |
| **HTTP Custom** | Transform request/response for HTTP backend |
| **AWS Service** | Direct integration (SQS, Step Functions, etc.) |
| **Mock** | Return response without backend |

---

### API Gateway + Lambda Architecture
```
┌─────────────────────────────────────────────┐
│  Client                                     │
│    ↓                                        │
│  API Gateway (REST/HTTP)                    │
│    ├── /users GET  → Lambda (getUsers)      │
│    ├── /users POST → Lambda (createUser)    │
│    ├── /orders/*   → Lambda (orders)        │
│    └── /health     → Mock (200 OK)          │
│                                             │
│  Backend: Lambda → DynamoDB / RDS Proxy     │
│  Auth: Cognito or Lambda Authorizer         │
│  Caching: API Gateway Cache (REST only)     │
│  Custom Domain: Route 53 + ACM cert         │
└─────────────────────────────────────────────┘
```

> **Exam Tips**:
> - "Serverless REST API" = API Gateway + Lambda + DynamoDB
> - "API timeout after 29 seconds" = API Gateway limit, use async pattern
> - "Cheapest API proxy" = HTTP API (70% cheaper than REST)
> - "Need caching and WAF" = REST API
> - "Authenticate API with user tokens" = Cognito Authorizer
> - "Custom auth logic (3rd party tokens)" = Lambda Authorizer
> - "Real-time two-way communication" = WebSocket API
> - "Rate limit per customer" = Usage Plans + API Keys
