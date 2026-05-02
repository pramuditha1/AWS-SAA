# CS06: Migration & Disaster Recovery
### AWS SAA-C03 Cheat Sheet

---

## Disaster Recovery Strategies

### Key Metrics
- **RPO (Recovery Point Objective)**: How much data loss is acceptable (time between last backup and disaster)
- **RTO (Recovery Time Objective)**: How much downtime is acceptable (time to recover)

```
Cost/Complexity: Low ──────────────────────────────────────── High
RPO/RTO:         Hours ────────────────────────────────────── Near-zero

┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐
│  Backup  │  │  Pilot   │  │  Warm    │  │  Multi-Site /    │
│ & Restore│  │  Light   │  │ Standby  │  │  Active-Active   │
└──────────┘  └──────────┘  └──────────┘  └──────────────────┘
  Cheapest      Low cost      Medium cost    Most expensive
  Hours RTO     10s min RTO   Minutes RTO    Real-time (near 0)
```

### Strategy Details

| Strategy | Description | RPO | RTO | Cost |
|----------|-------------|-----|-----|------|
| **Backup & Restore** | Regular backups to S3/Glacier, restore when needed | Hours | Hours | $ |
| **Pilot Light** | Minimal version always running (core DB replicated) | Minutes | 10s of minutes | $$ |
| **Warm Standby** | Scaled-down but fully functional system always running | Seconds | Minutes | $$$ |
| **Multi-Site Active/Active** | Full production in multiple regions | Near-zero | Near-zero | $$$$ |

### DR Strategy Details

**Backup & Restore:**
- S3 for data, AMIs for server configs
- RDS automated backups + snapshots
- EBS snapshots copied cross-region
- Cheapest but longest recovery time

**Pilot Light:**
- Core infrastructure always running (e.g., RDS replica in DR region)
- App servers as AMIs, ready to launch
- Route 53 health checks for failover
- Scale up on disaster

**Warm Standby:**
- Fully functional scaled-down copy in DR region
- Can serve traffic at reduced capacity
- Scale to production size on disaster
- Auto Scaling ready to scale out

**Multi-Site Active/Active:**
- Full production in 2+ regions
- Route 53 latency/weighted routing
- DynamoDB Global Tables, Aurora Global Database
- Zero/near-zero downtime

> **Exam Tips**:
> - "Cheapest DR option" = Backup & Restore
> - "RPO of seconds, RTO of minutes" = Warm Standby
> - "Near-zero RPO and RTO" = Multi-Site Active/Active
> - "Core DB always running in DR, minimal cost" = Pilot Light

---

## AWS Database Migration Service (DMS)

### Key Concepts
- Migrate databases to AWS **with minimal downtime**
- Source database remains operational during migration
- Supports: Homogeneous (Oracle→Oracle) and Heterogeneous (Oracle→Aurora) migrations

### Components
- **Replication Instance**: EC2 instance running DMS
- **Source Endpoint**: Connection to source database
- **Target Endpoint**: Connection to target database
- **Replication Task**: Defines migration settings

### Migration Types
| Type | Description |
|------|-------------|
| **Full Load** | Migrate all existing data |
| **CDC (Change Data Capture)** | Ongoing replication of changes |
| **Full Load + CDC** | Migrate existing + keep syncing changes |

### AWS Schema Conversion Tool (SCT)
- Convert database schema from one engine to another
- Required for **heterogeneous migrations** (e.g., Oracle → PostgreSQL)
- NOT needed for homogeneous migrations (e.g., MySQL → MySQL)

### Supported Sources & Targets
- **Sources**: Oracle, SQL Server, MySQL, PostgreSQL, MongoDB, S3, and more
- **Targets**: RDS, Aurora, Redshift, DynamoDB, S3, and more

> **Exam Tips**:
> - "Migrate database with minimal downtime" = DMS
> - "Convert Oracle to Aurora" = SCT + DMS
> - "Continuous replication" = DMS CDC
> - "Same engine migration" = DMS (no SCT needed)

---

## Data Migration Services Summary

| Scenario | Service |
|----------|---------|
| Database migration (online, minimal downtime) | DMS |
| Large data transfer offline (TB/PB) | Snow Family |
| File transfer on-premises ↔ AWS (online) | DataSync |
| Ongoing hybrid file access | Storage Gateway |
| Transfer files via SFTP/FTPS | Transfer Family |
| Replicate block storage | EBS Snapshots cross-region |
| Replicate S3 data | S3 Cross-Region Replication |

---

## AWS Application Migration Service (MGN)

### Key Concepts
- Formerly: CloudEndure Migration
- **Lift-and-shift (rehost)** migration of servers to AWS
- Continuously replicates source servers
- Automated cutover with minimal downtime
- Supports: Physical, virtual, cloud servers → AWS EC2

### Migration Process
1. Install replication agent on source server
2. Continuous block-level replication to AWS
3. Launch test instances (non-disruptive)
4. Perform cutover when ready
5. Decommission source

> **Exam Tip**: "Lift-and-shift migration to EC2" = Application Migration Service (MGN)

---

## AWS Migration Strategies (7 R's)

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Rehost** (Lift & Shift) | Move as-is to cloud | Quick migration, minimal changes |
| **Replatform** (Lift & Reshape) | Minor optimizations (e.g., move to RDS) | Some cloud benefits without rewrite |
| **Repurchase** | Move to SaaS (e.g., CRM to Salesforce) | Replace with commercial product |
| **Refactor/Re-architect** | Redesign for cloud-native | Maximum cloud benefits |
| **Retire** | Decommission | No longer needed |
| **Retain** | Keep on-premises | Not ready to migrate |
| **Relocate** | Move to VMware Cloud on AWS | VMware workloads |

---

## AWS Backup

### Key Concepts
- **Centralized backup management** across AWS services
- Supports: EC2, EBS, EFS, RDS, Aurora, DynamoDB, FSx, Storage Gateway, S3
- **Cross-region** and **cross-account** backup
- Backup policies via **AWS Organizations**

### Key Features
- **Backup Plans**: Schedule, retention, lifecycle rules
- **Backup Vault**: Encrypted storage for backups
- **Vault Lock**: WORM (Write Once Read Many) - immutable backups
- **Point-in-time recovery** for supported services
- **Compliance**: Audit backup activity via CloudTrail

> **Exam Tip**: "Centralized backup across multiple AWS services" = AWS Backup. "Immutable/compliance backups" = Backup Vault Lock.

---

## Multi-Region Architecture Patterns

### Active-Passive (Failover)
```
Primary Region (Active)     DR Region (Passive)
┌───────────────────┐       ┌───────────────────┐
│  ALB + EC2/ECS    │       │  AMIs ready       │
│  RDS Multi-AZ     │──────→│  RDS Read Replica │
│  S3 (primary)     │──────→│  S3 (CRR)        │
└───────────────────┘       └───────────────────┘
         ↑                           ↑
         └────── Route 53 Failover ──┘
```

### Active-Active
```
Region 1                    Region 2
┌───────────────────┐       ┌───────────────────┐
│  ALB + EC2/ECS    │       │  ALB + EC2/ECS    │
│  Aurora Global DB │←─────→│  Aurora Global DB │
│  DynamoDB Global  │←─────→│  DynamoDB Global  │
└───────────────────┘       └───────────────────┘
         ↑                           ↑
         └── Route 53 Latency/Weighted──┘
```

### Key Services for Multi-Region
| Service | Multi-Region Feature |
|---------|---------------------|
| Route 53 | Failover/Latency routing |
| S3 | Cross-Region Replication (CRR) |
| Aurora | Global Database (< 1 sec replication) |
| DynamoDB | Global Tables |
| CloudFront | Global CDN |
| Global Accelerator | Static IPs, network optimization |
| RDS | Cross-region Read Replicas |

---

## Elastic Disaster Recovery (DRS)

### Key Concepts
- Formerly: CloudEndure Disaster Recovery
- Continuous block-level replication to AWS
- Quick recovery (minutes) for on-premises or cloud servers
- RPO: Seconds | RTO: Minutes
- Cost-effective (staging area uses minimal resources)

### DRS vs Other DR Options
| Solution | RPO | RTO | Cost | Complexity |
|----------|-----|-----|------|------------|
| Elastic DRS | Seconds | Minutes | $$ | Low |
| Pilot Light (manual) | Minutes | 10s min | $$ | Medium |
| Warm Standby | Seconds | Minutes | $$$ | Medium |
| Multi-Site | ~0 | ~0 | $$$$ | High |

> **Exam Tip**: "Automated DR with minutes RTO for on-premises servers" = Elastic Disaster Recovery (DRS)
