# CS10: Well-Architected Framework & Exam Strategy
### AWS SAA-C03 Cheat Sheet

---

## AWS Well-Architected Framework - 6 Pillars

### Overview
| Pillar | Key Question |
|--------|-------------|
| **Operational Excellence** | How do you run and monitor systems? |
| **Security** | How do you protect information and systems? |
| **Reliability** | How do you recover from failures? |
| **Performance Efficiency** | How do you use resources efficiently? |
| **Cost Optimization** | How do you avoid unnecessary costs? |
| **Sustainability** (NEW) | How do you minimize environmental impact? |

---

### Pillar 1: Operational Excellence
**Key Principles:**
- Perform operations as code (CloudFormation, CDK)
- Make frequent, small, reversible changes
- Refine operations procedures frequently
- Anticipate failure (chaos engineering)
- Learn from operational failures

**Key Services:**
| Service | Role |
|---------|------|
| CloudFormation | IaC |
| AWS Config | Track configuration changes |
| CloudWatch | Monitor and alert |
| CloudTrail | Audit API calls |
| X-Ray | Trace distributed systems |
| Systems Manager | Operational management |
| EventBridge | Automate responses |

---

### Pillar 2: Security
**Key Principles:**
- Implement strong identity foundation (least privilege)
- Enable traceability (logging everything)
- Apply security at all layers
- Automate security best practices
- Protect data in transit and at rest
- Keep people away from data
- Prepare for security events

**Key Services:**
| Service | Role |
|---------|------|
| IAM | Identity and access control |
| Organizations + SCPs | Account-level guardrails |
| KMS | Encryption keys |
| CloudTrail | API auditing |
| GuardDuty | Threat detection |
| Security Hub | Central security findings |
| WAF + Shield | Network/app protection |
| VPC | Network isolation |
| Config | Compliance checking |

---

### Pillar 3: Reliability
**Key Principles:**
- Automatically recover from failure
- Test recovery procedures
- Scale horizontally to increase availability
- Stop guessing capacity
- Manage change in automation

**Key Services:**
| Service | Role |
|---------|------|
| Auto Scaling | Handle demand changes |
| ELB | Distribute traffic |
| Route 53 | DNS failover |
| Multi-AZ | High availability |
| S3 (11 9's durability) | Durable storage |
| RDS Multi-AZ | Database HA |
| CloudWatch | Detect failures |
| AWS Backup | Data protection |

**Key Patterns:**
- Multi-AZ for HA within a region
- Multi-Region for DR
- Loose coupling (SQS, EventBridge)
- Design for failure (assume things will fail)
- Stateless applications (store state externally)

---

### Pillar 4: Performance Efficiency
**Key Principles:**
- Democratize advanced technologies (use managed services)
- Go global in minutes
- Use serverless architectures
- Experiment more often
- Consider mechanical sympathy (right tool for job)

**Key Services:**
| Service | Role |
|---------|------|
| Auto Scaling | Match capacity to demand |
| Lambda | Serverless compute |
| CloudFront | Content delivery, low latency |
| Global Accelerator | Network performance |
| ElastiCache | Caching |
| EBS io2 | High IOPS storage |
| RDS Read Replicas | Read scaling |
| DynamoDB DAX | DynamoDB caching |

---

### Pillar 5: Cost Optimization
**Key Principles:**
- Implement cloud financial management
- Adopt consumption model
- Measure overall efficiency
- Stop spending on undifferentiated heavy lifting
- Analyze and attribute expenditure

**Key Services:**
| Service | Role |
|---------|------|
| Savings Plans / RIs | Commit for discount |
| Spot Instances | Spare capacity discount |
| S3 Lifecycle | Optimize storage costs |
| Compute Optimizer | Right-sizing |
| Cost Explorer | Spending visibility |
| Lambda | Pay per use |
| Auto Scaling | Scale to zero when idle |
| Trusted Advisor | Cost recommendations |

---

### Pillar 6: Sustainability (NEW - exam relevant!)
**Key Principles:**
- Understand your impact
- Establish sustainability goals
- Maximize utilization
- Anticipate and adopt more efficient offerings
- Use managed services
- Reduce downstream impact

**Key Actions:**
- Right-size resources (don't over-provision)
- Use efficient instance types (Graviton/ARM)
- Use serverless (share infrastructure)
- Optimize data storage (compress, lifecycle, delete unused)
- Minimize data movement
- Use Regions with lower carbon intensity

> **Exam Tip**: Sustainability questions often overlap with cost optimization. "Reduce environmental impact" = right-size, serverless, efficient instance types, less data movement.

---

## SAA-C03 Exam Strategy

### Exam Format
- **65 questions** in 130 minutes (~2 min per question)
- 50 scored + 15 unscored (you don't know which)
- Pass score: **720/1000**
- Multiple choice (1 correct) + Multiple response (2+ correct)

### Question Patterns

**Pattern 1: "Most cost-effective"**
- Look for: Spot, Savings Plans, S3 lifecycle, serverless, right-sizing
- Eliminate: Over-provisioned options, premium features not needed

**Pattern 2: "Most operationally efficient"**
- Look for: Managed services, serverless, automation
- Eliminate: Manual processes, self-managed options

**Pattern 3: "Highest availability/resilient"**
- Look for: Multi-AZ, Multi-Region, Auto Scaling, redundancy
- Eliminate: Single AZ, single instance, no failover

**Pattern 4: "Most secure"**
- Look for: Least privilege, encryption, private subnets, VPC endpoints
- Eliminate: Public access, overly permissive policies

**Pattern 5: "Least operational overhead"**
- Look for: Managed services, Fargate, Lambda, Aurora Serverless
- Eliminate: Self-managed EC2, manual scaling

### Key Decision Frameworks

**Choosing a Database:**
| Need | Choose |
|------|--------|
| Relational + complex queries | RDS or Aurora |
| High availability relational | Aurora (6 copies, 3 AZs) |
| Key-value, millisecond latency | DynamoDB |
| In-memory caching | ElastiCache |
| Graph data | Neptune |
| Time series | Timestream |
| Ledger/immutable | QLDB |
| Document (MongoDB compatible) | DocumentDB |
| Data warehouse (analytics) | Redshift |
| Wide column | Keyspaces (Cassandra) |

**Choosing Compute:**
| Need | Choose |
|------|--------|
| Full OS control, long-running | EC2 |
| Short tasks, event-driven | Lambda |
| Containers (managed) | ECS + Fargate |
| Containers (Kubernetes) | EKS |
| Batch processing | AWS Batch |
| No infrastructure management at all | Lambda / Fargate |

**Choosing Storage:**
| Need | Choose |
|------|--------|
| Object storage (web, backups, data lake) | S3 |
| Block storage for EC2 | EBS |
| Shared file storage (Linux) | EFS |
| Shared file storage (Windows) | FSx for Windows |
| High-performance compute storage | FSx for Lustre |
| Hybrid/on-premises access to cloud | Storage Gateway |

---

## Common Exam Scenarios & Solutions

### Scenario 1: "High traffic web application, cost-effective"
→ CloudFront + ALB + Auto Scaling Group (mixed instances: On-Demand + Spot) + Aurora

### Scenario 2: "Migrate on-premises database to AWS with minimal downtime"
→ DMS with CDC (Change Data Capture) + Schema Conversion Tool if heterogeneous

### Scenario 3: "Process uploaded images automatically"
→ S3 Event Notification → Lambda → process image → store in S3

### Scenario 4: "Decouple microservices"
→ SQS (point-to-point) or SNS (fan-out) or EventBridge (event-driven)

### Scenario 5: "Serve global users with low latency"
→ CloudFront (static) + Global Accelerator (dynamic) + Multi-region deployment

### Scenario 6: "Compliance: track all configuration changes"
→ AWS Config (configuration) + CloudTrail (API calls) + CloudWatch (metrics)

### Scenario 7: "Big data analytics on S3 data"
→ Glue (ETL/catalog) + Athena (ad-hoc queries) or Redshift (complex BI)

### Scenario 8: "Real-time streaming data processing"
→ Kinesis Data Streams → Lambda/KDA → DynamoDB/S3/OpenSearch

### Scenario 9: "Secure access to S3 from private EC2"
→ VPC Gateway Endpoint (free, no internet needed)

### Scenario 10: "Multi-account centralized security"
→ Organizations + SCPs + Control Tower + Security Hub + GuardDuty (delegated admin)

---

## Last-Minute Memory Aids

### Port Numbers to Remember
| Service | Port |
|---------|------|
| HTTP | 80 |
| HTTPS | 443 |
| SSH | 22 |
| RDP | 3389 |
| MySQL/Aurora | 3306 |
| PostgreSQL | 5432 |
| MSSQL | 1433 |
| Oracle | 1521 |

### S3 Limits
- Object size: max 5 TB
- Single PUT: max 5 GB
- Multipart Upload: required > 5 GB, recommended > 100 MB
- Bucket names: globally unique, 3-63 chars
- 3,500 PUT/COPY/POST/DELETE per second per prefix
- 5,500 GET/HEAD per second per prefix

### Key Numbers
| Service | Limit/Number |
|---------|-------------|
| Lambda timeout | 15 minutes max |
| Lambda memory | 128 MB - 10 GB |
| Lambda deployment package | 50 MB (zip), 250 MB (unzipped) |
| SQS message size | 256 KB (use Extended Client Library for larger) |
| SQS retention | 1 min - 14 days (default 4 days) |
| SQS visibility timeout | 0 sec - 12 hours (default 30 sec) |
| SNS message size | 256 KB |
| API Gateway timeout | 29 seconds |
| CloudFormation limit | 500 resources per stack |
| Security Groups per ENI | 5 (can increase) |
| Rules per Security Group | 60 inbound + 60 outbound |

### Encryption at Rest - Default Services
- S3: SSE-S3 (default since Jan 2023)
- EBS: Can enable default encryption per region
- RDS: Can enable at creation (can't add later)
- DynamoDB: Encrypted by default (AWS owned key)
- EFS: Optional at creation
- Redshift: AES-256 (optional at creation)
