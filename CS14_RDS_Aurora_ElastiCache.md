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
| **IAM Authentication** | Token-based auth for MySQL/MariaDB/PostgreSQL |
| **RDS Proxy** | Connection pooling for Lambda/many connections |
| **Storage Auto Scaling** | Grows storage automatically up to a max you set |
| **Blue/Green Deployments** | Safe upgrades: staging copy, switch over in ~1 min |
| **RDS Custom** | OS + DB admin access (Oracle, SQL Server only) |

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
- Up to **15 read replicas** per primary (RDS and Aurora). Oracle: AWS recommends ≤ 5 to limit lag.
- Can be in same AZ, cross-AZ, or **cross-region**
- Can be **promoted** to standalone DB (breaks replication)
- Cross-region replicas: Good for DR + global reads
- Application must update connection string to use replicas
- A read replica can itself be **Multi-AZ** (HA for the replica)
- **RDS does NOT auto-scale read replicas**. You add/remove them yourself. (Aurora Auto Scaling does this for Aurora.)

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
- Reduces failover time by up to 66%
- Can **enforce IAM authentication**; DB credentials stay in **Secrets Manager**

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

### RDS Security

**Encryption at rest (KMS):**
- Must be chosen **at creation**. You can't turn it on for a running unencrypted DB.
- Encrypt an existing DB: **snapshot → copy snapshot with encryption → restore → switch the app**
- Read replicas of an encrypted DB are encrypted. Cross-Region copies need a KMS key in the target Region.

**Encryption in transit:** SSL/TLS. Force it with a parameter (`rds.force_ssl` for PostgreSQL/SQL Server, `require_secure_transport` for MySQL/MariaDB).

**Authentication:**
- **IAM DB authentication** (MySQL, MariaDB, PostgreSQL, Aurora): short-lived token instead of a password
- **Secrets Manager**: stores the DB password and **rotates it automatically**. RDS can manage the master password in Secrets Manager for you.
- Kerberos / Active Directory for SQL Server, Oracle, PostgreSQL, MySQL

> **Exam Tip**: "Rotate DB credentials automatically" = Secrets Manager (not SSM Parameter Store). "Encrypt existing unencrypted RDS" = snapshot → encrypted copy → restore.

---

### RDS Operations

| Need | Feature |
|------|---------|
| Storage fills up unpredictably | **Storage Auto Scaling** (set a maximum storage threshold) |
| Engine upgrade with minimal downtime and easy rollback | **Blue/Green Deployment**: green copy stays in sync, switchover usually < 1 min, endpoints unchanged (MySQL, MariaDB, PostgreSQL, Aurora) |
| Single-AZ → Multi-AZ | Modify the instance. **No downtime.** |
| Dev/test DB not used every day | **Stop** it (max **7 days**, then RDS starts it again). Longer: snapshot + delete. |
| OS-level metrics (per-process CPU/memory) | **Enhanced Monitoring** (agent on the host, 1-sec granularity) |
| Which SQL queries load the DB | **Performance Insights** / CloudWatch Database Insights |
| Long-term / cross-account / central backup policy | **AWS Backup** (+ cross-Region automated backup replication) |
| Audit DB activity in near real time | **Database Activity Streams** → Kinesis |

- Deleting a DB deletes its **automated backups** (unless you choose to retain them). Take a **final snapshot**.
- **Parameter group** = engine settings. **Option group** = engine add-ons (e.g., Oracle TDE, SQL Server native backup to S3).

---

### RDS Custom
- Managed RDS **plus admin access to the OS and database**. **Oracle and SQL Server only.**
- For legacy/packaged apps that need custom patches, OS agents, or file system changes
- Shared responsibility: AWS still does backups and HA; you own your customizations

| Need | Choose |
|------|--------|
| Fully managed, no OS access | RDS |
| Managed, but need OS/DB admin access (Oracle/SQL Server) | **RDS Custom** |
| Full control, manage everything | Database on EC2 |

> **Exam Tip**: "Needs access to the underlying OS of the database" or "install custom software on the DB host" = RDS Custom (or EC2). Plain RDS never gives OS/SSH access.

---

## Amazon Aurora

### Key Concepts
- AWS **cloud-optimized** relational database
- Compatible with MySQL and PostgreSQL
- **5x faster than MySQL**, **3x faster than PostgreSQL**
- Up to **128 TiB** auto-scaling storage (256 TiB on newer engine versions)
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
| **Auto-scaling storage** | 10 GB → 128 TiB automatically |
| **Writer Endpoint** | Always points to current writer |
| **Reader Endpoint** | Load-balanced connection to all read replicas |
| **Custom Endpoints** | Route to specific subset of instances |
| **Backtrack** | Rewind DB to point in time WITHOUT restore (MySQL only) |
| **Failover** | < 30 seconds (promotes replica automatically) |
| **Cloning** | Fast, copy-on-write clone for testing |
| **Aurora Auto Scaling** | Adds/removes Aurora Replicas on CPU or connections |
| **Babelfish** | Aurora PostgreSQL that understands SQL Server's T-SQL (see below) |

### Aurora Endpoints

| Endpoint | Points to | Use for |
|----------|-----------|---------|
| **Cluster (writer)** | Current writer | All writes, DDL |
| **Reader** | All Aurora Replicas, load-balanced | Read-only queries |
| **Custom** | A subset of instances you choose (max 5 per cluster by default) | e.g., send analytics to 2 large replicas, app reads to the small ones |
| **Instance** | One specific instance | Troubleshooting only (no failover handling) |
| **Global writer** (Global Database) | Writer in the current primary Region | Writes that follow a cross-Region failover |

- A custom endpoint only **groups instances**. It doesn't change what SQL the database understands.
- Failover order: replicas have **priority tiers 0–15**. Lowest tier is promoted first (same tier → largest instance).

### Aurora Storage Pricing: Standard vs I/O-Optimized
| | Aurora Standard | Aurora I/O-Optimized |
|--|-----------------|----------------------|
| I/O charges | Pay per million I/O requests | **No I/O charges** (higher instance + storage price) |
| Choose when | I/O < 25% of Aurora bill | I/O **≥ 25%** of Aurora bill (I/O-heavy apps) |

> **Exam Tip**: "Aurora bill dominated by unpredictable I/O charges" = switch to Aurora I/O-Optimized.

### Aurora Serverless

**Key Concepts:**
- **Auto-scales compute** capacity based on demand, in steps as small as 0.5 ACU
- 1 ACU ≈ 2 GiB memory + matching CPU/network
- Range: **0 – 256 ACU** (Aurora MySQL), up to 384 ACU (Aurora PostgreSQL) on current versions
- **Min 0 ACU = auto-pause**: scales to zero when idle, resumes on the next connection
- Pay per ACU-hour actually used
- Works with readers, Multi-AZ, Global Database, RDS Proxy
- **Mixed cluster**: provisioned writer + Serverless v2 readers (or the reverse)

**Versions:**
- **Serverless v1**: old, retired. If an older question mentions "pause to zero", it means v1.
- **Serverless v2**: the current product. Exam questions just say "Aurora Serverless".

> **Exam Tip**: "Variable/unpredictable database workload", "dev/test DB idle most of the day" or "scale to zero" = Aurora Serverless v2. Steady 24/7 load is usually cheaper on provisioned instances (+ Reserved Instances).

### Aurora Global Database
- **1 primary region** (read/write) + up to **10 secondary regions** (read-only)
- Replication at the **storage layer**, lag typically **< 1 second**
- Up to **16** read replicas per secondary region
- **Switchover** (planned, no data loss) vs **failover** (Region outage, may lose the last second of writes)
- **Global writer endpoint** follows the primary after a switchover/failover → no connection-string change
- **Write forwarding**: apps in a secondary Region can send writes, Aurora forwards them to the primary
- Use Case: Global applications with low-latency reads, disaster recovery

### Write Scaling (Multi-Master is gone)
- **Aurora Multi-Master** only existed on Aurora MySQL 5.6 (v1), which reached end of life in Feb 2023. Older practice questions may still mention it.
- Today: one writer per cluster. For more write capacity: a bigger writer instance, **Aurora Limitless Database** (PostgreSQL, sharded writes), or DynamoDB if the data model allows.

> **Exam Tip**: "Cross-region DR with < 1 second RPO" = Aurora Global Database. "Low-latency reads in many Regions" = Aurora Global Database. "Read-only users in another Region need to write occasionally" = write forwarding.

---

## Babelfish for Aurora PostgreSQL

**The problem:** an app built for **Microsoft SQL Server** uses **T-SQL** (SQL Server's SQL dialect) and SQL Server drivers. Moving to PostgreSQL normally means rewriting all that SQL.

**What Babelfish does:** Aurora PostgreSQL gets a second "front door" that speaks SQL Server.
```
SQL Server app (T-SQL, SQL Server drivers, unchanged)
        │  TDS protocol, port 1433
        ▼
┌───────────────────────────────────┐
│ Aurora PostgreSQL + Babelfish     │
│  • T-SQL endpoint     :1433       │
│  • PostgreSQL endpoint :5432      │ ← new apps can use PostgreSQL SQL
└───────────────────────────────────┘
          same data, one database
```
- Understands the SQL Server **wire protocol (TDS)** and **T-SQL**
- The app keeps its **SQL Server drivers**. Usually only the connection string changes.
- Turned on when you **create** the Aurora PostgreSQL cluster (cluster parameter `rds.babelfish_status`)
- **Babelfish Compass** (free tool): reports which T-SQL features are supported before you migrate
- Not 100% of T-SQL. Expect a few changes, but far fewer than a full rewrite.
- Doesn't work with: RDS Proxy, IAM DB authentication, Database Activity Streams, zero-ETL integrations
- Only for **Aurora PostgreSQL**. Not Aurora MySQL, not RDS for PostgreSQL.

---

## Migrating Databases into RDS / Aurora

| Tool | What it moves | When |
|------|---------------|------|
| **AWS DMS** | **Data** (full load + CDC, source stays online) | Every migration with minimal downtime |
| **AWS SCT** (desktop) / **DMS Schema Conversion** (managed, in the DMS console) | **Schema + code** (tables, views, stored procedures) from one engine's dialect to another | Engines differ (heterogeneous), e.g. Oracle → PostgreSQL |
| **Babelfish** | Nothing. It lets Aurora PostgreSQL **run T-SQL**. | SQL Server app must keep working with minimal code changes |
| **Native tools** (mysqldump, pg_dump, SQL Server .bak via S3) | Data + schema, same engine | Same engine, downtime acceptable |

```
Same engine (homogeneous):   MySQL → RDS MySQL               = DMS (or native tools)
Different engine:            Oracle → Aurora PostgreSQL      = SCT/DMS Schema Conversion + DMS
SQL Server, keep app as-is:  SQL Server → Aurora PostgreSQL  = DMS (data) + Babelfish (T-SQL support)
```

**Exam question: SQL Server → Aurora PostgreSQL, avoid changing T-SQL app logic (pick two)**
- ✅ **AWS SCT + AWS DMS** → move the schema and data
- ✅ **Babelfish for Aurora PostgreSQL** → the app keeps sending T-SQL
- ❌ **Aurora Global Database**: cross-Region replication. It's about DR, not SQL dialects.
- ❌ **Custom endpoint**: only groups instances. It can't make PostgreSQL behave like SQL Server.
- ❌ **AWS Glue**: ETL for analytics data. It doesn't rewrite application queries.

> **Real-world note:** AWS's Babelfish migration guide creates the schema by running SQL Server's own DDL scripts on the Babelfish endpoint, then uses **DMS for the data**. SCT would convert T-SQL into PostgreSQL code, which is the path you take when you *don't* use Babelfish. In exam questions, "SCT + DMS" is the standard answer for "migrate schema and data".

> **Exam Tips**:
> - "SQL Server app → Aurora PostgreSQL, minimal code change / keep T-SQL" = **Babelfish**
> - "Convert schema between different engines" = **SCT** (or DMS Schema Conversion)
> - "Migrate data with minimal downtime" = **DMS** (full load + CDC)
> - "Lift SQL Server as-is, no engine change" = **RDS for SQL Server** (or RDS Custom / EC2 if OS access needed)

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
