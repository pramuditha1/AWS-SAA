# CS09: Cost Optimization - Pricing, Savings Plans, Billing
### AWS SAA-C03 Cheat Sheet

---

## EC2 Pricing Models

### Pricing Comparison

| Model | Discount | Commitment | Use Case |
|-------|----------|------------|----------|
| **On-Demand** | 0% (baseline) | None | Short-term, unpredictable, testing |
| **Reserved (1yr)** | ~40% | 1 year | Steady-state, predictable workloads |
| **Reserved (3yr)** | ~60% | 3 years | Long-term, committed workloads |
| **Savings Plans** | Up to 72% | $/hour commitment | Flexible across instance families |
| **Spot Instances** | Up to 90% | None (can be interrupted) | Fault-tolerant, flexible workloads |
| **Dedicated Hosts** | Most expensive | Optional reservation | Compliance, licensing (per-socket/core) |
| **Dedicated Instances** | Premium over On-Demand | None | Isolation requirement |
| **Capacity Reservations** | 0% (On-Demand price) | None | Guarantee capacity in an AZ |

---

## Savings Plans

### Types of Savings Plans

| Type | Flexibility | Discount |
|------|------------|----------|
| **Compute Savings Plans** | Any instance family, size, OS, tenancy, region. Also covers Fargate + Lambda | Highest flexibility, moderate discount |
| **EC2 Instance Savings Plans** | Specific instance family in specific region. Any size, OS, tenancy | Less flexible, higher discount |
| **SageMaker Savings Plans** | SageMaker instances | ML workloads |

### Key Points
- Commit to a consistent amount of compute usage ($/hour)
- 1 or 3 year terms
- Payment options: No Upfront, Partial Upfront, All Upfront (more upfront = more discount)
- Usage beyond commitment charged at On-Demand rates
- **Preferred over Reserved Instances** for most cases (more flexible)

> **Exam Tip**: "Commit to spending but need flexibility across instance types/regions" = Compute Savings Plans. "Commit to specific instance family" = EC2 Instance Savings Plans.

---

## Reserved Instances

### Types
| Type | Description |
|------|-------------|
| **Standard RI** | Highest discount, can't change instance family |
| **Convertible RI** | Lower discount, CAN change instance family/OS/tenancy |
| **Scheduled RI** | Capacity reservation for specific time window (deprecated, use On-Demand Capacity Reservations) |

### Key Points
- Regional RIs: Discount applies to any AZ in region, no capacity reservation
- Zonal RIs: Discount + capacity reservation in specific AZ
- Can sell unused RIs on the Reserved Instance Marketplace
- Convertible RIs can be exchanged but NOT sold on marketplace

### Reserved Instances vs Savings Plans
| Feature | Reserved Instances | Savings Plans |
|---------|-------------------|---------------|
| Flexibility | Limited (Standard) or Moderate (Convertible) | High |
| Applies to | EC2, RDS, ElastiCache, Redshift, OpenSearch | EC2, Fargate, Lambda (Compute SP) |
| Capacity reservation | ✅ (Zonal RI) | ❌ |
| Resale | ✅ (Standard RI) | ❌ |

---

## Spot Instances

### Key Concepts
- **Up to 90% off On-Demand** price
- AWS can reclaim with **2-minute notice**
- You set a **max price** — instance runs while spot price ≤ your max
- NOT suitable for: Databases, critical workloads, stateful applications

### Spot Strategies
| Strategy | Description |
|----------|-------------|
| **Spot Fleet** | Collection of Spot + On-Demand instances to meet target capacity |
| **Spot Block** | Reserved Spot for 1-6 hours (being deprecated) |
| **Diversify** | Use multiple instance types/AZs to reduce interruption risk |

### Spot Fleet Allocation Strategies
| Strategy | Description |
|----------|-------------|
| **lowestPrice** | Launch from pool with lowest price (cost-optimized) |
| **diversified** | Distribute across pools (availability-optimized) |
| **capacityOptimized** | Pool with highest available capacity (fewer interruptions) |
| **priceCapacityOptimized** | Balance of price and capacity (recommended) |

### Handling Spot Interruption
- **2-minute warning** via instance metadata + CloudWatch Events
- Best practices:
  - Checkpointing (save state frequently)
  - Use SQS for job queues (retry interrupted work)
  - Mix with On-Demand in Auto Scaling Group
  - Use multiple instance types and AZs

> **Exam Tips**:
> - "Cheapest compute option" = Spot Instances
> - "Big data, batch processing, CI/CD, image processing" = Good Spot use cases
> - "Database workload" = NOT Spot (use RI or On-Demand)
> - "Reduce interruption risk" = diversified or priceCapacityOptimized strategy

---

## Cost Optimization Strategies

### Compute Optimization
| Strategy | Savings |
|----------|---------|
| Right-size instances (use Compute Optimizer) | 10-30% |
| Savings Plans (Compute) | Up to 72% |
| Spot for fault-tolerant workloads | Up to 90% |
| Use Graviton (ARM) instances | ~20% better price/performance |
| Lambda for sporadic workloads | Pay per invocation only |
| Auto Scaling (scale in when low traffic) | Variable |

### Storage Optimization
| Strategy | Details |
|----------|---------|
| S3 Lifecycle Policies | Auto-transition to cheaper storage classes |
| S3 Intelligent-Tiering | Auto-moves based on access patterns |
| EBS: Delete unattached volumes | Common waste |
| EBS: Use gp3 over gp2 | Same performance, 20% cheaper |
| Compress data before storing | Less storage = less cost |
| Use S3 analytics to find optimization opportunities | Identify IA candidates |

### Database Optimization
| Strategy | Details |
|----------|---------|
| Reserved Instances for RDS | Up to 60% off |
| Aurora Serverless for variable workloads | Auto-scales to zero |
| DynamoDB On-Demand for unpredictable | Pay per request |
| DynamoDB Reserved Capacity for predictable | Up to 77% off |
| Read Replicas to offload reads | Reduce primary instance size |
| ElastiCache to reduce DB load | Fewer DB queries = smaller DB needed |

### Network Optimization
| Strategy | Details |
|----------|---------|
| Use VPC Endpoints for S3/DynamoDB | Avoid NAT Gateway data charges |
| Same-AZ communication when possible | No cross-AZ data transfer fee |
| CloudFront for content delivery | Reduce origin data transfer |
| Compress responses | Less data transfer |
| S3 Transfer Acceleration | Only when speed needed (costs more) |

---

## AWS Cost Management Tools

### AWS Cost Explorer
- Visualize spending over time (up to 12 months forecast)
- Filter by service, region, account, tag
- **Rightsizing recommendations** for EC2
- Monthly/daily/hourly granularity
- Savings Plans recommendations

### AWS Budgets
- Set custom budgets (cost, usage, RI/SP utilization)
- **Alerts** via email or SNS when threshold exceeded
- Can trigger **actions** (e.g., apply SCP, stop EC2)
- Types: Cost budget, Usage budget, Reservation budget, Savings Plans budget

### Cost Anomaly Detection
- ML-powered unusual spend detection
- Automatic (no thresholds to set manually)
- Alerts via SNS or email
- Root cause analysis

### AWS Compute Optimizer
- ML-based recommendations for:
  - EC2 instance types (right-sizing)
  - EBS volume types
  - Lambda memory configuration
- Uses CloudWatch metrics (14 days minimum)

### Cost Allocation Tags
- Organize costs by project, team, environment
- **AWS-generated tags** (e.g., aws:createdBy)
- **User-defined tags** (e.g., Project: WebApp, Environment: Production)
- Must be **activated** in Billing Console to appear in reports

---

## Data Transfer Costs

### Key Rules
| Transfer Type | Cost |
|---------------|------|
| Internet → AWS (ingress) | **FREE** |
| AWS → Internet (egress) | **Charged** (varies by region) |
| Same AZ (private IP) | **FREE** |
| Cross AZ (same region) | ~$0.01/GB each way |
| Cross Region | ~$0.02/GB |
| VPC Peering cross-AZ | Same as cross-AZ |
| S3 → CloudFront | **FREE** |
| NAT Gateway processing | $0.045/GB |
| VPC Gateway Endpoint (S3/DynamoDB) | **FREE** |
| VPC Interface Endpoint | $0.01/GB |

> **Exam Tips**:
> - "Reduce data transfer costs" = Same AZ, VPC Endpoints, CloudFront
> - "S3 data transfer to EC2 in same region" = Free via VPC Gateway Endpoint
> - "NAT Gateway is expensive for data transfer" = Use VPC Endpoints instead for AWS services
> - Data IN to AWS is almost always free

---

## Well-Architected Cost Optimization Principles

1. **Implement cloud financial management** - Dedicate team/tooling to cost management
2. **Adopt a consumption model** - Pay only for what you use (serverless, auto-scaling)
3. **Measure overall efficiency** - Track cost per business outcome
4. **Stop spending on undifferentiated heavy lifting** - Use managed services
5. **Analyze and attribute expenditure** - Tags, cost allocation
