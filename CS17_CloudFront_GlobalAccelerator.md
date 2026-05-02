# CS17: CloudFront & Global Accelerator
### AWS SAA-C03 Cheat Sheet

---

## CloudFront (CDN)

### Key Concepts
- **Content Delivery Network** — caches content at **edge locations** (400+)
- Reduces latency by serving content from nearest edge
- **Global service** (not regional)
- Integrates with: S3, ALB, EC2, API Gateway, custom origins
- DDoS protection included (Shield Standard)

### How CloudFront Works
```
User (Sydney) → Edge Location (Sydney)
                    ├── Cache HIT → Return immediately (fast!)
                    └── Cache MISS → Fetch from Origin → Cache → Return

Origins:
- S3 Bucket (static content)
- ALB / EC2 (dynamic content)
- Custom HTTP server (on-premises)
- API Gateway
```

### CloudFront Origins

| Origin | Access Method | Use Case |
|--------|--------------|----------|
| **S3 Bucket** | OAC (Origin Access Control) | Static files, website hosting |
| **ALB** | Must be public (SG allows CF IPs) | Dynamic content |
| **EC2** | Must be public (SG allows CF IPs) | Custom applications |
| **Custom Origin** | Any HTTP endpoint | On-premises servers |
| **MediaStore / MediaPackage** | Direct integration | Video streaming |

### Origin Access Control (OAC)
- **Restricts S3 access to CloudFront only** (users can't bypass CF)
- Replaces legacy OAI (Origin Access Identity)
- S3 bucket policy grants access only to CloudFront distribution
- Supports: S3, Lambda Function URLs, MediaStore
- **Supports SSE-KMS** encryption (OAI didn't)

```
S3 Bucket Policy:
  Allow: cloudfront:GetObject
  Condition: aws:SourceArn = CloudFront distribution ARN
```

---

### CloudFront Key Features

| Feature | Description |
|---------|-------------|
| **Edge Locations** | 400+ globally, cache content |
| **Regional Edge Caches** | Larger cache between edge and origin |
| **TTL (Time to Live)** | How long content stays in cache |
| **Invalidation** | Force remove objects from cache ($) |
| **Price Classes** | Limit edge locations to reduce cost |
| **Geo Restriction** | Allow/block countries (whitelist/blacklist) |
| **Signed URLs/Cookies** | Restrict access to paid/private content |
| **Field-Level Encryption** | Encrypt specific fields at edge |
| **Lambda@Edge** | Run code at edge locations |
| **CloudFront Functions** | Lightweight functions at edge (faster than Lambda@Edge) |

---

### Cache Behaviors

- Route requests to different origins based on **path pattern**
- Example:
  - `/images/*` → S3 bucket (static)
  - `/api/*` → ALB (dynamic, no cache)
  - `Default (*)` → S3 website (static)
- Each behavior has its own: TTL, viewer protocol, allowed methods, etc.

### Cache Invalidation
- Remove objects from cache before TTL expires
- Path-based: `/images/logo.png` or `/images/*`
- **Costs money** (per invalidation path)
- Alternative: Use **versioned file names** (app-v2.js) — instant, free

---

### Signed URLs vs Signed Cookies

| Feature | Signed URL | Signed Cookie |
|---------|-----------|---------------|
| Access | One file per URL | Multiple files |
| URL change | ✅ URL modified | ❌ URL unchanged |
| Use Case | Individual file download | Streaming, entire site access |

**vs S3 Pre-signed URLs:**
| Feature | CloudFront Signed URL | S3 Pre-signed URL |
|---------|----------------------|-------------------|
| Access via | Edge locations (cached, fast) | Direct to S3 |
| IP restriction | ✅ | ❌ |
| Caching | ✅ | ❌ |
| Use Case | Distributed content | Direct S3 access |

---

### Lambda@Edge vs CloudFront Functions

| Feature | CloudFront Functions | Lambda@Edge |
|---------|---------------------|-------------|
| Runtime | JavaScript only | Node.js, Python |
| Execution time | < 1 ms | Up to 5-30 sec |
| Triggers | Viewer Request/Response only | All 4 (Viewer + Origin) |
| Scale | Millions of requests/sec | Thousands/sec |
| Network access | ❌ | ✅ |
| Use Case | Simple transforms (headers, URL rewrite, redirects) | Complex logic (auth, API calls, body manipulation) |

### Common Edge Function Use Cases
- URL rewrites and redirects
- Header manipulation (add security headers)
- A/B testing (route to different origins)
- Authentication/authorization at edge
- Bot detection
- Image transformation

---

### CloudFront + S3 Static Website

```
Pattern 1: CloudFront + S3 (HTTPS + custom domain)
User → CloudFront (HTTPS, custom cert) → S3 Bucket (OAC, private)

Pattern 2: S3 Website Hosting (HTTP only, no custom domain)  
User → S3 Website Endpoint (HTTP only)

Exam Choice: Pattern 1 (HTTPS support, better performance, geo-restriction)
```

> **Exam Tip**: "S3 website with HTTPS" = CloudFront in front of S3. S3 website hosting alone doesn't support HTTPS.

---

## Global Accelerator

### Key Concepts
- **Network layer (L3/L4)** optimization using AWS global network
- Routes traffic through AWS backbone instead of public internet
- Provides **2 static Anycast IPs** (global entry points)
- Reduces latency, jitter, packet loss

### How It Works
```
User → Nearest Edge Location → AWS Private Network → Your Application (any region)
       (via Anycast IP)         (optimized path)

vs Normal:
User → Public Internet (variable hops) → Your Application
```

### Key Features
| Feature | Description |
|---------|-------------|
| **2 Static IPs** | Anycast IPs that don't change |
| **Health Checks** | Automatic failover to healthy endpoints |
| **Endpoint Groups** | Group by region with traffic dial (%) |
| **Endpoints** | ALB, NLB, EC2, Elastic IP |
| **Client Affinity** | Route same client to same endpoint |
| **DDoS protection** | Shield Standard included |

### Traffic Dial
- Percentage of traffic to send to each region endpoint group
- Use for: Blue/green deployments, gradual region migration
- Example: US endpoints 80%, EU endpoints 20%

### Endpoint Weights
- Within an endpoint group, control traffic distribution
- Example: ALB-1 weight 128, ALB-2 weight 128 (50/50)

---

## CloudFront vs Global Accelerator

| Feature | CloudFront | Global Accelerator |
|---------|-----------|-------------------|
| Layer | L7 (HTTP/HTTPS) | L3/L4 (TCP/UDP) |
| Content | Caches content at edge | Does NOT cache (proxies) |
| Static IP | ❌ (uses DNS) | ✅ 2 Anycast IPs |
| Protocol | HTTP/HTTPS/WebSocket | TCP/UDP |
| Best for | Static content, cacheable APIs | Non-HTTP (gaming, IoT, VoIP), non-cacheable |
| IP whitelisting | ❌ (IPs change) | ✅ (static IPs) |
| Failover | DNS-based (slower) | Instant (< 1 min) |
| DDoS | Shield Standard | Shield Standard |

### When to Choose Which

| Scenario | Choose |
|----------|--------|
| Cache static content globally | CloudFront |
| HTTPS website acceleration | CloudFront |
| API caching | CloudFront |
| Gaming (UDP, low latency) | Global Accelerator |
| IoT (MQTT, TCP) | Global Accelerator |
| Need static IP for allowlisting | Global Accelerator |
| Instant failover between regions | Global Accelerator |
| VoIP / video conferencing | Global Accelerator |
| Non-cacheable dynamic content | Global Accelerator |
| HTTP with caching | CloudFront |
| HTTP without caching, need speed | Either (GA for consistency) |

> **Exam Tips**:
> - "Static IPs for global application" = Global Accelerator
> - "Cache content at edge" = CloudFront
> - "Reduce latency for TCP/UDP application" = Global Accelerator
> - "Instant failover between regions" = Global Accelerator
> - "HTTPS website with custom domain" = CloudFront
> - "IP whitelisting requirement" = Global Accelerator
