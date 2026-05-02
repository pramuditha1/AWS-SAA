# CS14: Databases - RDS, Aurora, ElastiCache
### AWS SAA-C03 Cheat Sheet

---

## RDS (Relational Database Service)

### Key Concepts
- **Managed relational database** — AWS handles patches, backups, HA
- Supported engines: PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, IBM Db2
- Runs on EC2 instances (you choose instance type)
- **Cannot SSH** into RDS instances

### RDS Key Features

| Feature | Description |
|---------|-------------|
| **Multi-AZ** | Synchronous standby in another AZ for HA (failover) |
| **Read Replicas** | Async copies for read scaling (up to 15) |
| **Automated Backups** | Daily full backup + transaction logs (PITR) |
| **Manual Snapshots** | User-initiated, persist until deleted |
| **Encryption** | At rest (KMS), in transit (SSL/TLS) |
| **IAM Authentication** | Token-based auth for MySQL/PostgreSQL |
| **RDS Proxy** | Connection pooling for Lambda/many connections |

---

### Multi-AZ Deployments

```
         Writes/Reads
Client ──────────────→ Primary (AZ-a)
                          │ Synchronous Replication
                          ↓
                       Standby (AZ-b) ← NOT readable
                       
On failure: Automatic failover (DNS points to standby)
Failover time: ~60-120 seconds
```

**Key Points:**
- **Synchronous** replication (zero data loss)
- Standby is **NOT readable** (just for failover)
- Same region, different AZ
- Automatic failover (DNS CNAME flips)
- Failover triggers: AZ failure, instance failure, storage failure, manual failover
- **No performance benefit** — purely for availability

### Multi-AZ Cluster (New)
- 1 writer + 2 readers across 3 AZs
- Readers ARE readable (unlike standby)
- Faster failover (~35 seconds)
- Available for MySQL and PostgreSQL

---

### Read Replicas

```
         Writes              Reads
Client ──────→ Primary ←──── Client (writes)
                  │ Async Replication
                  ├──→ Read Replica 1 ←── Client (reads)
                  ├──→ Read Replica 2 ←── Client (reads)
                  └──→ Read Replica 3 (Cross-Region) ←── Global reads
```

**Key Points:**
- **Asynchronous** replication (eventual consistency)
- Up to **15 read replicas** (Aurora) or **5** (other RDS engines)
- Can be in same AZ, cross-AZ, or **cross-region**
- Can be **promoted** to standalone DB (breaks replication)
- Cross-region replicas: Good for DR + global reads
- Application must update connection string to use replicas

**Cost:**
- Same region replica: No data transfer fee
- Cross-region replica: Data transfer fee applies

### Multi-AZ vs Read Replicas

| Feature | Multi-AZ | Read Replicas |
|---------|----------|---------------|
| Purpose | High Availability | Read Scalability |
| Replication | Synchronous | Asynchronous |
| Readable | ❌ No (standby only) | ✅ Yes |
| Cross-region | ❌ No | ✅ Yes |
| Failover | Automatic | Manual promotion |
| Use case | Production HA | Reporting, analytics, global reads |

> **Exam Tip**: "HA for database" = Multi-AZ. "Scale reads" = Read Replicas. "DR in another region" = Cross-region Read Replica.

---

### RDS Backups & Restore

**Automated Backups:**
- Retention: 1–35 days (default 7, 0 = disabled)
- Daily full snapshot + transaction logs (every 5 min)
- Point-in-time recovery (PITR): Restore to any second within retention
- Backup window: Configurable (avoid peak hours)
- Stored in S3 (managed by AWS)

**Manual Snapshots:**
- User-triggered, kept forever until you delete
- Can copy cross-region (for DR)
- Can share with other accounts
- Restored to a **new RDS instance** (not in-place)

**Restore:**
- Always creates a **NEW database instance**
- Can restore from automated backup (PITR) or manual snapshot
- Can restore with different instance class, storage, Multi-AZ

---

### RDS Proxy

**Key Concepts:**
- **Managed connection pooler** for RDS
- Pools and shares database connections
- Reduces failover time by ~66%
- Enforces IAM authentication

**Use Cases:**
- **Lambda functions**: Many short-lived connections → exhausts DB connections
- Reduce failover impact (proxy handles reconnection)
- IAM-based DB authentication

**Key Points:**
- Only accessible from VPC (never publicly)
- Supports MySQL, PostgreSQL, MariaDB, SQL Server
- Auto-scales (serverless)

> **Exam Tip**: "Lambda timing out connecting to RDS" or "too many DB connections" = RDS Proxy.

---

## Amazon Aurora

### Key Concepts
- AWS **cloud-optimized** relational database
- Compatible with MySQL and PostgreSQL
- **5x faster than MySQL**, **3x faster than PostgreSQL**
- Up to **128 TB** auto-scaling storage
- Up to **15 read replicas** (sub-10ms replica lag)

### Aurora Architecture
```
┌─────────────────────────────────────────────┐
│        Aurora Cluster (Single Region)        │
│                                             │
│  Writer Endpoint → [Writer Instance]        │
│                        ↓                    │
│  ┌─────────── Shared Storage Volume ───────┐│
│  │  6 copies across 3 AZs (auto-healing)  ││
│  └─────────────────────────────────────────┘│
│                        ↑                    │
│  Reader Endpoint → [Reader 1] [Reader 2]... │
│                    (up to 15 replicas)       │
└─────────────────────────────────────────────┘
```

### Aurora Key Features
| Feature | Description |
|---------|-------------|
| **6 copies of data** | Across 3 AZs (4/6 needed for writes, 3/6 for reads) |
| **Self-healing storage** | Automatically detects and repairs corruption |
| **Auto-scaling storage** | 10 GB → 128 TB automatically |
| **Writer Endpoint** | Always points to current writer |
| **Reader Endpoint** | Load-balanced connection to all read replicas |
| **Custom Endpoints** | Route to specific subset of instances |
| **Backtrack** | Rewind DB to point in time WITHOUT restore (MySQL only) |
| **Failover** | < 30 seconds (promotes replica automatically) |
| **Cloning** | Fast, copy-on-write clone for testing |

### Aurora Serverless

**Key Concepts:**
- **Auto-scales compute** capacity based on demand
- Scales to **zero** when no connections (v2 scales to 0.5 ACU minimum)
- Pay per ACU-second (Aurora Capacity Unit)
- No capacity planning needed

**Versions:**
| Feature | Serverless v1 | Serverless v2 |
|---------|---------------|---------------|
| Scaling | Pause to 0, step-based | 0.5 ACU min, instant scaling |
| Speed | 15-30 sec scale | Sub-second scaling |
| Read replicas | ❌ | ✅ |
| Multi-AZ | ❌ | ✅ |
| Global Database | ❌ | ✅ |
| **Use Case** | Infrequent/unpredictable | Production variable workloads |

> **Exam Tip**: "Variable/unpredictable database workload" or "scale to zero" = Aurora Serverless.

### Aurora Global Database
- **1 primary region** (read/write) + up to **5 secondary regions** (read-only)
- Replication lag: **< 1 second** cross-region
- Promotes secondary region in **< 1 minute** (for DR)
- Up to 16 read replicas per secondary region
- Use Case: Global applications with low-latency reads, disaster recovery

### Aurora Multi-Master (Write Scaling)
- All instances can do reads AND writes
- Instant failover (no need to promote replica)
- Use Case: Continuous write availability (zero write downtime)

> **Exam Tip**: "Cross-region DR with < 1 second RPO" = Aurora Global Database. "Zero downtime for writes" = Aurora Multi-Master.

---

## ElastiCache

### Key Concepts
- **Managed in-memory cache** (Redis or Memcached)
- Sub-millisecond latency
- Reduces database load by caching frequent queries
- Session store for stateless applications

### Redis vs Memcached

| Feature | Redis | Memcached |
|---------|-------|-----------|
| Data structures | Rich (strings, lists, sets, sorted sets, hashes) | Simple key-value only |
| Persistence | ✅ (RDB/AOF) | ❌ (pure cache) |
| Replication | ✅ Multi-AZ with auto-failover | ❌ |
| Clustering | ✅ (sharding) | ✅ (sharding) |
| Backup/Restore | ✅ | ❌ |
| Pub/Sub | ✅ | ❌ |
| Lua scripting | ✅ | ❌ |
| Multi-threaded | ❌ (single-threaded) | ✅ |
| Use Case | HA, persistence, complex data, sessions | Simple caching, multi-threaded |

> **Memory Aid**: Redis = **R**ich features, **R**eplication, **R**esilience. Memcached = **M**ulti-threaded, **M**inimal features.

### Caching Strategies

| Strategy | How It Works | Pros | Cons |
|----------|--------------|------|------|
| **Lazy Loading (Cache-Aside)** | Read: Check cache → if miss, read DB → write to cache | Only requested data cached; node failure not fatal | Cache miss penalty; stale data possible |
| **Write-Through** | Write: Write to cache AND DB simultaneously | Cache always current; no stale data | Write penalty; cache may have unused data |
| **Session Store** | Store user session in cache (TTL-based) | Stateless app tier; fast session access | Data lost if cache clears (use Redis for persistence) |

### ElastiCache Use Cases
1. **Database caching**: Cache frequent DB queries (reduce RDS load)
2. **Session management**: Store sessions for stateless web apps
3. **Leaderboards**: Redis sorted sets (gaming)
4. **Real-time analytics**: Counters, rate limiting
5. **Pub/Sub messaging**: Redis pub/sub for real-time updates

### ElastiCache Security
- **In-transit encryption** (TLS)
- **At-rest encryption** (KMS)
- **Redis AUTH**: Password-based authentication
- **IAM Authentication**: For Redis (newer feature)
- VPC-based (no public access)
- Security groups

### ElastiCache Serverless (Redis)
- Auto-scales capacity
- No node management
- Pay per usage (GB-hours + ECPUs)
- Simplified operations

> **Exam Tips**:
> - "Reduce DB read load" = ElastiCache (Lazy Loading pattern)
> - "Store user sessions for stateless app" = ElastiCache (Redis preferred for persistence)
> - "Need replication and persistence" = Redis (not Memcached)
> - "Simple multi-threaded cache" = Memcached
> - "Real-time leaderboard" = Redis Sorted Sets
> - "Cache vs DynamoDB DAX" = DAX is DynamoDB-only; ElastiCache is general purpose
