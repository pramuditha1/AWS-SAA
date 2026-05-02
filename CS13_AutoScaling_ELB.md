# CS13: Auto Scaling & Elastic Load Balancing
### AWS SAA-C03 Cheat Sheet

---

## Auto Scaling Group (ASG)

### Key Concepts
- **Automatically scale EC2 instances** based on demand
- Ensures minimum, desired, and maximum instance count
- **Free** (pay only for EC2 instances launched)
- Spans multiple AZs for high availability

### ASG Configuration
```
┌─────────────────────────────────────────────┐
│              Auto Scaling Group              │
│                                             │
│  Minimum: 2    Desired: 4    Maximum: 8    │
│                                             │
│  AZ-a: [i1] [i2]    AZ-b: [i3] [i4]      │
│                                             │
│  Launch Template: AMI, Instance Type, SG,   │
│                   Key Pair, User Data, IAM  │
└─────────────────────────────────────────────┘
```

### Launch Template vs Launch Configuration
| Feature | Launch Template | Launch Configuration |
|---------|----------------|---------------------|
| Versioning | ✅ | ❌ |
| Mixed instance types | ✅ | ❌ |
| Spot + On-Demand mix | ✅ | ❌ |
| T2 unlimited | ✅ | ❌ |
| Status | **Recommended** | Legacy (deprecated) |

### Scaling Policies

| Policy Type | How It Works | Use Case |
|-------------|--------------|----------|
| **Target Tracking** | Keep metric at target value (e.g., CPU = 50%) | Simplest, most common |
| **Step Scaling** | Add/remove X instances based on alarm thresholds | Granular control |
| **Simple Scaling** | Add/remove X instances, then wait cooldown | Basic (least recommended) |
| **Scheduled** | Scale at specific times | Known traffic patterns (business hours) |
| **Predictive** | ML-based, forecasts future traffic | Recurring patterns (daily/weekly cycles) |

### Scaling Metrics
| Metric | Good For |
|--------|----------|
| **CPUUtilization** | Compute-bound applications |
| **RequestCountPerTarget** | Web applications (requests per instance) |
| **Average Network In/Out** | Network-bound applications |
| **Custom Metric** (via CloudWatch) | Application-specific (e.g., queue depth) |
| **SQS Queue Length** | Processing workloads (ApproximateNumberOfMessages) |

### Key ASG Features
- **Health Checks**: EC2 (default) or ELB health checks
- **Cooldown Period**: Wait X seconds after scaling before next action (default 300s)
- **Warm-up Period**: Time for new instance to stabilize before counting metrics
- **Instance Refresh**: Rolling replacement of instances (for AMI updates)
- **Lifecycle Hooks**: Run custom actions during launch/terminate
  - `Pending:Wait` → run setup script → `Pending:Proceed`
  - `Terminating:Wait` → save logs → `Terminating:Proceed`
- **Termination Policy**: Which instance to terminate first
  - Default: Oldest launch config → Closest to billing hour → Random
  - Options: OldestInstance, NewestInstance, OldestLaunchConfiguration, etc.

### ASG + Mixed Instances
- Combine On-Demand + Spot instances
- Set base On-Demand capacity
- Define Spot allocation (capacity-optimized, lowest-price, etc.)
- Automatic Spot replacement if interrupted

> **Exam Tips**:
> - "Scale based on SQS queue depth" = Custom metric with Target Tracking or Step Scaling
> - "Known traffic pattern at 9 AM" = Scheduled Scaling
> - "Keep CPU around 70%" = Target Tracking
> - "Run script before instance terminates" = Lifecycle Hook
> - "Update AMI across fleet with zero downtime" = Instance Refresh

---

## Elastic Load Balancing (ELB)

### Overview
- Distributes incoming traffic across multiple targets
- **Managed service** — AWS handles scaling, HA, maintenance
- Integrates with: Auto Scaling, CloudWatch, ACM, WAF, Route 53

### Load Balancer Types

| Type | Layer | Protocols | Key Feature |
|------|-------|-----------|-------------|
| **ALB** (Application) | Layer 7 | HTTP, HTTPS, gRPC | Content-based routing |
| **NLB** (Network) | Layer 4 | TCP, UDP, TLS | Ultra-low latency, static IP |
| **GLB** (Gateway) | Layer 3 | IP | Network appliances (firewall, IDS) |
| ~~CLB~~ (Classic) | Layer 4/7 | HTTP, TCP | **Legacy — don't use** |

---

## ALB (Application Load Balancer)

### Key Features
- **Layer 7** (HTTP/HTTPS)
- **Content-based routing**:
  - Path-based: `/api/*` → Service A, `/images/*` → Service B
  - Host-based: `api.example.com` → Service A
  - Query string/headers: `?platform=mobile` → Mobile Service
  - HTTP method: GET → read service, POST → write service
- **Target Groups**: EC2, ECS tasks, Lambda, private IP addresses
- **Health Checks**: HTTP endpoint on targets
- **Sticky Sessions** (Session Affinity): Route same client to same target
  - Application cookie (custom) or Duration-based cookie
- **Cross-zone load balancing**: ✅ Enabled by default (free)
- **Security Groups**: ✅ Yes
- **SSL/TLS Termination**: ✅ Yes (ACM integration)
- **WebSocket**: ✅ Supported
- **HTTP/2**: ✅ Supported
- **Fixed Response**: Return custom HTTP response without forwarding
- **Redirects**: HTTP → HTTPS, domain redirects

### ALB + ECS
- **Dynamic Port Mapping**: Multiple tasks on same instance, different ports
- ALB routes to correct port automatically
- Enables higher container density

### ALB Access Logs
- Detailed logs of all requests → S3 bucket
- Contains: Client IP, latency, request path, server response, etc.

---

## NLB (Network Load Balancer)

### Key Features
- **Layer 4** (TCP/UDP/TLS)
- **Ultra-high performance**: Millions of requests/sec, ultra-low latency
- **Static IP per AZ** (or Elastic IP attachment)
- **Preserves source IP** address
- **Target Groups**: EC2, private IP, ALB (new!)
- **Cross-zone**: Disabled by default (charges if enabled)
- **Security Groups**: ✅ Supported (recent addition)
- **No HTTP intelligence**: Can't do path/host routing
- **TCP passthrough**: TLS can be terminated or passed through

### When to Choose NLB over ALB
| Choose NLB | Choose ALB |
|-----------|-----------|
| Need static IP | Need path/host routing |
| Ultra-low latency (gaming, IoT) | HTTP/HTTPS applications |
| TCP/UDP protocols | WebSocket, gRPC |
| Extreme performance (millions rps) | Content-based routing |
| Whitelist IP (static) | WAF integration needed |
| Non-HTTP protocols | Advanced HTTP features |

---

## GLB (Gateway Load Balancer)

### Key Features
- **Layer 3** (Network layer - IP packets)
- Routes traffic through **network appliances** (firewalls, IDS/IPS, deep packet inspection)
- Uses **GENEVE protocol** (port 6081)
- Transparent to source and destination
- Single entry/exit point for all traffic

### Architecture
```
Internet → GLB → Firewall/IDS (3rd party appliances) → GLB → Your Application
```

### Use Cases
- Deploy virtual firewalls (Palo Alto, Fortinet, etc.)
- IDS/IPS systems
- Deep packet inspection
- Network traffic analysis

> **Exam Tip**: "Inspect ALL traffic through security appliances" = Gateway Load Balancer.

---

## ELB Common Features

### Health Checks
- Ping target at configured interval
- **Healthy threshold**: X consecutive successes → healthy
- **Unhealthy threshold**: X consecutive failures → unhealthy
- Unhealthy targets removed from rotation

### SSL/TLS
- **SSL Termination**: Decrypt at LB, forward unencrypted to targets
- **End-to-End Encryption**: Re-encrypt to targets (HTTPS → HTTPS)
- **ACM** (AWS Certificate Manager): Free SSL certificates, auto-renew
- **SNI (Server Name Indication)**: Host multiple SSL certs on one LB
  - Supported on ALB and NLB (not CLB)

### Connection Draining (Deregistration Delay)
- Time to complete in-flight requests before deregistering target
- Default: 300 seconds
- Set to 0 for short-lived requests

### Cross-Zone Load Balancing
```
WITHOUT Cross-Zone:                WITH Cross-Zone:
AZ-a (2 instances): 50% traffic   AZ-a (2 instances): 25% each
AZ-b (8 instances): 50% traffic   AZ-b (8 instances): 10% each
→ Uneven per-instance load         → Even per-instance load
```

| LB Type | Cross-Zone Default | Cost |
|---------|-------------------|------|
| ALB | ✅ Always on | Free |
| NLB | ❌ Disabled | Charges if enabled |
| GLB | ❌ Disabled | Charges if enabled |

---

## ASG + ELB Integration

### Architecture
```
Internet → Route 53 → ELB (ALB/NLB)
                         ↓
              ┌──── Target Group ────┐
              ↓          ↓           ↓
         [Instance] [Instance] [Instance]
              └──── Auto Scaling Group ────┘
                    Min:2 Desired:3 Max:10
```

### Key Integration Points
- ASG automatically registers new instances with ELB target group
- ASG can use **ELB health checks** (recommended over EC2-only checks)
- ELB distributes traffic; ASG manages capacity
- Span both across **multiple AZs** for HA

### High Availability Pattern
- ALB in public subnets (internet-facing)
- ASG instances in private subnets
- Multi-AZ deployment
- Health checks: ELB (application-level)
- Scaling: Target Tracking on RequestCountPerTarget

> **Exam Tips**:
> - "Web app needs HA and auto-scaling" = ALB + ASG across Multi-AZ
> - "Instances failing but ASG not replacing" = Enable ELB health checks on ASG
> - "Session stickiness needed" = ALB Sticky Sessions (but consider ElastiCache for session store)
> - "Need static IP for load balancer" = NLB (not ALB)
> - "Multiple SSL certs on one LB" = SNI (ALB or NLB)
