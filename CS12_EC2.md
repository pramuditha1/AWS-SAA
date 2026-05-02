# CS12: EC2 - Elastic Compute Cloud
### AWS SAA-C03 Cheat Sheet

---

## EC2 Overview

### Key Concepts
- **Virtual servers** (instances) in the AWS cloud
- Full control over OS, networking, storage
- Pay per second (Linux/Windows) or per hour
- **Regional service** — choose region, then AZ

---

## Instance Types

### Naming Convention: `m5.xlarge`
- **m** = Instance family (General Purpose)
- **5** = Generation
- **xlarge** = Size (vCPUs + Memory)

### Instance Families

| Family | Optimized For | Use Case | Mnemonic |
|--------|--------------|----------|----------|
| **M** (m5, m6i, m7g) | General Purpose | Web servers, app servers, small DBs | **M**edium / balanced |
| **C** (c5, c6i, c7g) | Compute | Batch processing, ML, gaming, HPC | **C**ompute |
| **R** (r5, r6i, r7g) | Memory | In-memory DBs, real-time processing | **R**AM |
| **X** (x1, x2idn) | Memory (extreme) | SAP HANA, large in-memory DBs | e**X**treme memory |
| **I** (i3, i4i) | Storage (IOPS) | NoSQL DBs, data warehousing | **I**/O |
| **D** (d2, d3) | Storage (Dense) | MapReduce, HDFS, distributed FS | **D**ense storage |
| **T** (t3, t4g) | Burstable | Dev/test, low-traffic web | **T**urbo burst |
| **G** (g4, g5) | GPU | ML training, video encoding, 3D | **G**raphics |
| **P** (p4, p5) | GPU (HPC) | Deep learning training | **P**erformance GPU |
| **HPC** (hpc6a) | High Performance | Tightly coupled HPC workloads | |

### Graviton (ARM-based)
- Instances ending in **g** (m7g, c7g, r7g, t4g)
- **40% better price/performance** vs x86
- Supports Linux only
- Great for: Web servers, containerized apps, microservices

### Burstable Instances (T-series)
- Baseline CPU + burst credits
- **Unlimited mode**: Can burst beyond credits (charges apply)
- Good for variable workloads (not sustained high CPU)

---

## EC2 Placement Groups

| Strategy | Description | Use Case |
|----------|-------------|----------|
| **Cluster** | Instances in SAME rack, same AZ | Low latency, high throughput (HPC, big data) |
| **Spread** | Instances on DIFFERENT hardware (max 7/AZ) | High availability, critical instances |
| **Partition** | Groups on different racks (up to 7 partitions/AZ) | Hadoop, Cassandra, Kafka (large distributed) |

```
Cluster:    [Rack] ← All instances here (low latency, risk of failure)
Spread:     [Rack1] [Rack2] [Rack3] ← 1 instance per rack (max HA)
Partition:  [Rack1-Group] [Rack2-Group] [Rack3-Group] ← Groups isolated
```

> **Exam Tips**:
> - "Low latency between instances" = Cluster
> - "Maximize availability, each instance isolated" = Spread
> - "Large distributed workload, rack-level isolation" = Partition

---

## EC2 Networking

### ENI (Elastic Network Interface)
- Virtual network card attached to EC2
- Attributes: Primary private IP, secondary IPs, Elastic IP, MAC address, Security Groups
- Can be detached and reattached to another instance (same AZ)
- Use Case: Management network, dual-homed instances, failover

### Elastic IP
- Static public IPv4 address
- You own it until you release it
- **Charged when NOT associated** with a running instance
- Max 5 per region (can request increase)
- Anti-pattern: Usually indicates poor architecture (use DNS or load balancers instead)

### Enhanced Networking
- **ENA (Elastic Network Adapter)**: Up to 100 Gbps
- **EFA (Elastic Fabric Adapter)**: For HPC, OS-bypass for ultra-low latency
- No extra charge, just use supported instance types

---

## EC2 Purchasing Options

| Option | Discount | Commitment | Best For |
|--------|----------|------------|----------|
| **On-Demand** | 0% | None | Short-term, unpredictable |
| **Reserved (Standard)** | ~72% | 1 or 3 years | Steady-state workloads |
| **Reserved (Convertible)** | ~54% | 1 or 3 years | Steady-state + flexibility |
| **Savings Plans** | ~72% | $/hour for 1-3 years | Flexible compute commitment |
| **Spot** | ~90% | None (interruptible) | Fault-tolerant, flexible |
| **Dedicated Host** | Varies | Optional reservation | Licensing, compliance |
| **Dedicated Instance** | Premium | None | Hardware isolation |
| **Capacity Reservation** | 0% | None | Guaranteed capacity |

---

## EC2 User Data & Metadata

### User Data
- Script that runs **once at first boot** (by default)
- Used for: Install software, download files, configure instance
- Base64 encoded
- Runs as **root** user
- Max 16 KB

### Instance Metadata (IMDS)
- URL: `http://169.254.169.254/latest/meta-data/`
- Get: Instance ID, AMI ID, instance type, security groups, IAM role credentials
- **IMDSv2** (recommended): Requires token (PUT request first) — more secure
- Credentials from instance role are fetched here (temporary, auto-rotated)

---

## AMI (Amazon Machine Image)

### Key Concepts
- **Template** for launching instances (OS + software + config)
- **Region-specific** (must copy AMI to use in another region)
- Types: Public (AWS), Marketplace (3rd party), Private (your own)

### AMI Lifecycle
```
Running Instance → Create AMI (creates EBS snapshots) → Launch new instances
                                    ↓
                      Copy to other regions (for DR/global deployment)
```

### Key Points
- AMIs are backed by EBS snapshots
- Can share AMIs cross-account
- Can encrypt AMI (copy with encryption)
- **Golden AMI**: Pre-configured AMI with all software → faster launch times

> **Exam Tip**: "Fastest way to launch pre-configured instances" = Golden AMI. "Deploy same instance in multiple regions" = Copy AMI cross-region.

---

## EC2 Hibernate

### Key Concepts
- **RAM state saved to EBS** root volume (must be encrypted)
- Instance resumes exactly where it left off
- Faster boot than stop/start (OS doesn't restart)
- Max hibernate: **60 days**
- Root EBS must be encrypted and large enough for RAM
- Supported on: On-Demand, Reserved, Spot instances

### Stop vs Terminate vs Hibernate
| Action | EBS Root | RAM | Public IP | Use Case |
|--------|----------|-----|-----------|----------|
| **Stop** | Preserved | Lost | Lost (unless Elastic IP) | Pause, change instance type |
| **Terminate** | Deleted (default) | Lost | Lost | Done with instance |
| **Hibernate** | Preserved + RAM dump | Saved | Lost (unless Elastic IP) | Fast resume, long-init apps |

---

## EC2 Security

### Security Groups
- **Virtual firewall** at the instance level
- **Stateful**: If traffic allowed in, response automatically allowed out
- **Only ALLOW rules** (no deny rules)
- Default: All inbound DENIED, all outbound ALLOWED
- Can reference other security groups (not just IPs)
- Attached to ENI (not instance directly)
- Changes take effect **immediately**

### Key Security Group Rules
| Type | Protocol | Port | Source | Purpose |
|------|----------|------|--------|---------|
| SSH | TCP | 22 | Your IP | Linux access |
| RDP | TCP | 3389 | Your IP | Windows access |
| HTTP | TCP | 80 | 0.0.0.0/0 | Web traffic |
| HTTPS | TCP | 443 | 0.0.0.0/0 | Secure web |
| Custom | TCP | App port | SG of ALB | App behind load balancer |

> **Exam Tips**:
> - "Instance can't reach internet" = Check SG outbound + route table + IGW
> - "Instance can't be reached" = Check SG inbound rules
> - "Allow communication between instances" = Reference security group ID in rule
> - Security Groups are STATEFUL, NACLs are STATELESS

---

## EC2 Status Checks

| Check | What It Monitors | Recovery |
|-------|------------------|----------|
| **System Status** | AWS hardware/infrastructure | Stop/Start (moves to new host) or CloudWatch alarm auto-recovery |
| **Instance Status** | Guest OS issues | Reboot or fix OS config |

### Auto Recovery
- CloudWatch Alarm → Recover action
- Instance keeps: Same instance ID, private IP, Elastic IP, metadata, placement group
- Requires: EBS-backed instance (not instance store)
