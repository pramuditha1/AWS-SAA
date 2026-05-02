# CS01: Storage - EBS, EFS, FSx, Storage Gateway, Snow Family
### AWS SAA-C03 Cheat Sheet

---

## EBS (Elastic Block Store)

### Key Concepts
- **Block storage** attached to EC2 instances (like a virtual hard drive)
- **AZ-locked**: EBS volumes exist in ONE AZ only
- **Persistent**: Data persists after instance stop/termination (if configured)
- **One-to-one** by default (one volume → one instance), EXCEPT Multi-Attach

### EBS Volume Types

| Type | Category | Max IOPS | Max Throughput | Use Case |
|------|----------|----------|----------------|----------|
| **gp3** | General SSD | 16,000 | 1,000 MB/s | Most workloads, boot volumes |
| **gp2** | General SSD | 16,000 | 250 MB/s | Legacy general purpose |
| **io2/io2 Block Express** | Provisioned IOPS SSD | 256,000 | 4,000 MB/s | Databases, critical apps needing sustained IOPS |
| **io1** | Provisioned IOPS SSD | 64,000 | 1,000 MB/s | High-performance databases |
| **st1** | Throughput HDD | 500 | 500 MB/s | Big data, data warehouses, log processing |
| **sc1** | Cold HDD | 250 | 250 MB/s | Infrequent access, lowest cost |

> **Exam Tip**: SSD (gp/io) = IOPS-intensive. HDD (st1/sc1) = Throughput-intensive. Only SSD can be boot volumes.

### EBS Key Features
- **Snapshots**: Point-in-time backup → stored in S3 (regional)
  - Can copy snapshots cross-region for DR
  - Can create AMI from snapshot
  - **Fast Snapshot Restore (FSR)**: eliminates latency on first read (costs extra)
- **Encryption**:
  - Uses AWS KMS keys (AES-256)
  - Encrypted at rest + in transit between EC2 and EBS
  - To encrypt unencrypted volume: snapshot → copy with encryption → create new volume
- **Multi-Attach (io1/io2 only)**: Attach one volume to up to 16 Nitro instances in same AZ
- **EBS-optimized instances**: Dedicated throughput between EC2 and EBS

### Instance Store vs EBS

| Feature | Instance Store | EBS |
|---------|---------------|-----|
| Persistence | ❌ Ephemeral (lost on stop/terminate) | ✅ Persistent |
| Performance | Highest IOPS (millions) | Up to 256K IOPS |
| Use Case | Cache, temp data, buffers | Databases, boot volumes |
| Cost | Included with instance | Separate charge |
| Backup | Manual (no snapshots) | Snapshots to S3 |

> **Exam Tip**: If question mentions "highest possible IOPS" or "temporary high-performance storage" → Instance Store. If "data must persist" → EBS.

---

## EFS (Elastic File System)

### Key Concepts
- **Managed NFS** (Network File System) - shared file storage
- **Multi-AZ**: Accessible from multiple AZs simultaneously
- **Linux only** (NFS v4.1 protocol) - NOT compatible with Windows
- **Serverless**: No capacity planning, auto-scales
- **Pay-per-use**: Only pay for storage consumed

### EFS Storage Classes
| Class | Use Case | Cost |
|-------|----------|------|
| **Standard** | Frequently accessed | Higher storage, lower access |
| **Standard-IA** | Infrequent access | Lower storage, higher access cost |
| **One Zone** | Single AZ, frequent access | 47% cheaper than Standard |
| **One Zone-IA** | Single AZ, infrequent | Cheapest option |

### EFS Key Features
- **Performance Modes**: General Purpose (default, low latency) vs Max I/O (high throughput, higher latency)
- **Throughput Modes**: Bursting (scales with size) vs Provisioned (fixed) vs Elastic (auto-scales)
- **Lifecycle Management**: Auto-move files to IA after X days
- **Cross-region replication**: For DR
- **Encryption**: At rest (KMS) and in transit (TLS)

### EFS vs EBS vs S3

| Feature | EFS | EBS | S3 |
|---------|-----|-----|-----|
| Type | File storage (NFS) | Block storage | Object storage |
| Access | Multi-instance, Multi-AZ | Single instance (mostly) | Anywhere (HTTP) |
| OS | Linux only | Linux + Windows | N/A |
| Performance | Good | Highest (io2) | High throughput |
| Cost | Pay per use | Pay per provisioned | Pay per use |
| Use Case | Shared files, CMS, web serving | Databases, boot volumes | Static assets, backups, data lake |

> **Exam Tip**: "Shared storage across multiple EC2 Linux instances" = EFS. "Shared Windows file system" = FSx for Windows.

---

## FSx (File Systems)

### FSx for Windows File Server
- Fully managed **Windows native** file system
- Supports **SMB protocol** and **Windows NTFS**
- Integrates with **Active Directory** (AD)
- Supports **DFS (Distributed File System)** namespaces
- Can be accessed from Linux (via SMB)
- **Multi-AZ** for high availability
- Use Case: Windows apps, SharePoint, SQL Server, home directories

### FSx for Lustre
- High-performance **parallel file system** for compute-intensive workloads
- Supports **Linux only** (POSIX-compliant)
- Sub-millisecond latencies, up to hundreds of GB/s throughput
- **Integrates with S3**: Can read from/write to S3 seamlessly
- Use Case: Machine learning, HPC, video processing, financial modeling
- Deployment types:
  - **Scratch**: Temporary, highest performance, no data replication
  - **Persistent**: Long-term storage, data replicated within AZ

### FSx for NetApp ONTAP
- Fully managed NetApp ONTAP file system
- Supports NFS, SMB, and iSCSI
- Works with Linux, Windows, and macOS
- **Point-in-time cloning** (great for testing)

### FSx for OpenZFS
- Managed OpenZFS file system
- NFS protocol, Linux compatible
- Up to 1 million IOPS
- Snapshots, cloning, compression

> **Exam Tip**: Windows + AD + SMB = FSx Windows. HPC + Linux + S3 integration = FSx Lustre. Multi-protocol = NetApp ONTAP.

---

## Storage Gateway

### Key Concept
- **Hybrid cloud storage** - bridges on-premises to AWS cloud storage
- Deployed as VM on-premises (or hardware appliance)

### Gateway Types

| Type | Protocol | Backed By | Use Case |
|------|----------|-----------|----------|
| **S3 File Gateway** | NFS/SMB | S3 (all classes) | File shares backed by S3, data lake |
| **FSx File Gateway** | SMB | FSx for Windows | Low-latency access to FSx from on-premises |
| **Volume Gateway - Cached** | iSCSI | S3 + EBS snapshots | Frequently accessed data cached locally, full dataset in S3 |
| **Volume Gateway - Stored** | iSCSI | S3 (backup) | Full dataset on-premises, async backup to S3 |
| **Tape Gateway** | iSCSI (VTL) | S3 Glacier | Backup/archive, replace physical tape |

> **Exam Tip**: 
> - "On-premises NFS access to S3" = S3 File Gateway
> - "Low latency access with AWS as primary storage" = Cached Volume
> - "Keep all data on-premises with backup to AWS" = Stored Volume
> - "Replace tape backup" = Tape Gateway

---

## Snow Family (Data Migration)

### Devices

| Device | Storage | Use Case | Compute |
|--------|---------|----------|---------|
| **Snowcone** | 8 TB HDD / 14 TB SSD | Small data transfers, edge computing | 2 vCPUs, 4 GB RAM |
| **Snowball Edge Storage Optimized** | 80 TB | Large data migration | 40 vCPUs, 80 GB RAM |
| **Snowball Edge Compute Optimized** | 42 TB | Edge computing + storage | 104 vCPUs, 416 GB RAM, optional GPU |
| **Snowmobile** | 100 PB | Exabyte-scale migration | N/A (truck!) |

### Key Points
- Solves: "Large data transfer over network takes too long"
- Rule of thumb: **If transfer over network > 1 week, use Snow Family**
- Data encrypted with KMS (256-bit)
- Can run EC2 instances and Lambda functions on Snowball Edge
- **OpsHub**: GUI for managing Snow devices
- Snowball cannot directly transfer to Glacier → must go to S3 first, then lifecycle policy to Glacier

> **Exam Tip**: "Migrate 50 TB with limited bandwidth" = Snowball. "Exabytes of data" = Snowmobile. "Remote location with no internet" = Snowcone/Snowball Edge for edge computing.

---

## AWS Transfer Family
- Managed file transfer service into/out of S3 or EFS
- Supports **SFTP, FTPS, FTP, AS2** protocols
- Use Case: Partners/clients uploading files via standard protocols
- Integrates with existing authentication (AD, LDAP, custom)

---

## AWS DataSync
- **Online data transfer** service (fast, automated)
- Agent-based: Install agent on-premises
- Transfers between: On-premises ↔ AWS (S3, EFS, FSx)
- Also: AWS ↔ AWS (e.g., EFS to S3)
- Handles scheduling, bandwidth throttling, data validation
- **Encrypts data in transit** and validates integrity
- **vs Storage Gateway**: DataSync = migrate/sync. Storage Gateway = ongoing hybrid access.

> **Exam Tip**: "One-time large data migration online" = DataSync. "Ongoing hybrid access" = Storage Gateway. "Offline migration" = Snow Family.
