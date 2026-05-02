# CS15: Route 53 - DNS & Routing
### AWS SAA-C03 Cheat Sheet

---

## DNS Fundamentals

### Key Concepts
- **DNS**: Translates domain names (example.com) → IP addresses (93.184.216.34)
- **Route 53**: AWS managed DNS service (name = port 53 for DNS)
- **100% SLA** — the only AWS service with this guarantee
- Also a **Domain Registrar** (buy domain names)

### DNS Record Types
| Record | Maps | Example |
|--------|------|---------|
| **A** | Domain → IPv4 | example.com → 1.2.3.4 |
| **AAAA** | Domain → IPv6 | example.com → 2001:db8::1 |
| **CNAME** | Domain → another domain | app.example.com → elb-123.amazonaws.com |
| **Alias** | Domain → AWS resource | example.com → d1234.cloudfront.net |
| **NS** | Nameservers for zone | example.com → ns-1.awsdns.com |
| **MX** | Mail servers | example.com → mail.example.com |
| **TXT** | Text data (verification) | example.com → "v=spf1..." |
| **SOA** | Zone authority info | Start of Authority record |

### CNAME vs Alias

| Feature | CNAME | Alias |
|---------|-------|-------|
| Zone apex (naked domain) | ❌ Cannot use | ✅ Can use |
| Cost | Charged per query | **Free** for AWS resources |
| Target | Any hostname | AWS resources only (ELB, CloudFront, S3, etc.) |
| Example | www.example.com → elb.aws | example.com → elb.aws |
| Health checks | ❌ | ✅ (free) |

> **Key Rule**: Use **Alias** for AWS resources (it's free and works at zone apex). Use CNAME only for non-AWS targets.

### Alias Targets (What Alias Can Point To)
- ELB, CloudFront, API Gateway, S3 Website, VPC Interface Endpoint
- Global Accelerator, Route 53 record in same hosted zone
- **Cannot** alias to EC2 DNS name

---

## Hosted Zones

| Type | Description | Cost |
|------|-------------|------|
| **Public Hosted Zone** | Routes internet traffic to resources | $0.50/month per zone |
| **Private Hosted Zone** | Routes traffic within VPC(s) | $0.50/month per zone |

---

## Routing Policies

### Simple Routing
- Map domain to one or more IP addresses
- If multiple values: Client receives ALL, chooses randomly (client-side LB)
- **No health checks** on individual records
- Use Case: Single resource, no special routing needs

### Weighted Routing
- Route X% of traffic to each resource
- Weights don't need to add to 100 (it's proportional)
- **Health checks**: Yes — unhealthy targets removed
- Weight = 0 → no traffic; All weights = 0 → equal distribution
- Use Case: A/B testing, gradual deployments, load distribution

```
Record A (Weight 70) → Production server (70% traffic)
Record B (Weight 20) → New version (20% traffic)
Record C (Weight 10) → Canary (10% traffic)
```

### Latency-Based Routing
- Route to the region with **lowest latency** for the user
- Latency measured from user to AWS region
- **Health checks**: Yes
- Use Case: Global applications where speed matters

### Failover Routing
- **Active-Passive** setup
- Primary: Must have health check
- Secondary: Used when primary is unhealthy
- Use Case: Active-passive disaster recovery

```
DNS Query → Health Check on Primary
              ├── Healthy → Return Primary IP
              └── Unhealthy → Return Secondary IP
```

### Geolocation Routing
- Route based on **user's geographic location** (continent, country, state)
- Must set a **default** record (for non-matching locations)
- **Health checks**: Yes
- Use Case: Content localization, restrict distribution, compliance

> **Difference from Latency**: Geolocation = WHERE user is physically. Latency = which region responds fastest. A US user always gets US routing even if a EU server is faster.

### Geoproximity Routing
- Route based on geographic location of users AND resources
- Uses **bias** to expand or shrink routing region
- Positive bias (+) = attract more traffic
- Negative bias (-) = send traffic away
- Requires **Route 53 Traffic Flow** (visual editor)
- Use Case: Shift traffic between regions without moving resources

### Multi-Value Routing
- Return up to **8 healthy records** to client
- Client chooses one (client-side load balancing)
- **Health checks**: Yes (only healthy records returned)
- Use Case: Simple load balancing without ELB
- NOT a substitute for ELB (but better than Simple routing)

### IP-Based Routing
- Route based on **client's IP address** (CIDR blocks)
- Define CIDR-to-endpoint mappings
- Use Case: Route specific ISPs/offices to specific endpoints, optimize costs

---

## Health Checks

### Types
| Type | Monitors |
|------|----------|
| **Endpoint** | Monitor an IP or domain (HTTP, HTTPS, TCP) |
| **Calculated** | Combine multiple health checks (AND, OR, NOT) |
| **CloudWatch Alarm** | Monitor CloudWatch metric state |

### Endpoint Health Check
- 15 global health checkers evaluate your endpoint
- Healthy if **≥ 18%** of checkers report healthy
- Interval: 30 sec (default) or 10 sec ($$)
- Supports: HTTP, HTTPS, TCP
- HTTP/HTTPS: Can check response body (first 5120 bytes) for string match
- **Must allow Route 53 health checker IPs** in security groups/firewall

### Key Points
- Health checks are PUBLIC — they access your endpoints from the internet
- For **private resources**: Use CloudWatch Alarm + Calculated Health Check
- Unhealthy endpoint → Route 53 stops returning it
- Health check + Failover routing = Automatic DR

> **Exam Tips**:
> - "Route traffic to closest region" = Latency-based
> - "A/B testing with traffic split" = Weighted
> - "Different content per country" = Geolocation
> - "Automatic failover to DR site" = Failover + Health Check
> - "Cannot use CNAME for naked domain" → Use Alias record
> - "Free DNS queries" → Use Alias (to AWS resources)

---

## Route 53 + Architecture Patterns

### Blue-Green Deployment
```
DNS: app.example.com
  ├── Weighted 100% → Blue (current production)
  └── Weighted 0%   → Green (new version)
  
Cutover: Shift weight from Blue to Green gradually
```

### Active-Passive Failover
```
DNS: app.example.com (Failover policy)
  ├── Primary → ALB in us-east-1 (Health Check ✅)
  └── Secondary → ALB in eu-west-1 (used when primary fails)
```

### Active-Active Multi-Region
```
DNS: app.example.com (Latency policy)
  ├── us-east-1 → ALB (Health Check ✅)
  ├── eu-west-1 → ALB (Health Check ✅)
  └── ap-southeast-1 → ALB (Health Check ✅)
Users routed to lowest-latency region automatically
```

---

## Domain Registration
- Route 53 is also a domain registrar
- Can transfer domains TO Route 53
- Can use Route 53 DNS without buying domain from AWS (change NS records at registrar)
- Domain registration ≠ DNS hosting (they're separate)
