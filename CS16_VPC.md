# CS16: VPC - Virtual Private Cloud
### AWS SAA-C03 Cheat Sheet

---

## VPC Fundamentals

### Key Concepts
- **Your private network** in AWS (logically isolated)
- **Regional resource** — spans all AZs in a region
- Max 5 VPCs per region (soft limit)
- CIDR range: /16 (65,536 IPs) to /28 (16 IPs)
- Default VPC: Created automatically, has internet access

### VPC Architecture
```
┌─────────────── VPC (10.0.0.0/16) ──────────────────────┐
│                                                         │
│  ┌──── AZ-a ─────┐         ┌──── AZ-b ─────┐         │
│  │                │         │                │         │
│  │ Public Subnet  │         │ Public Subnet  │         │
│  │ 10.0.1.0/24   │         │ 10.0.3.0/24   │         │
│  │ [NAT GW] [Web]│         │ [Web Server]   │         │
│  │                │         │                │         │
│  │ Private Subnet │         │ Private Subnet │         │
│  │ 10.0.2.0/24   │         │ 10.0.4.0/24   │         │
│  │ [App] [DB]    │         │ [App] [DB]     │         │
│  └────────────────┘         └────────────────┘         │
│                                                         │
│  Internet Gateway (IGW)                                 │
└─────────────────────────────────────────────────────────┘
```

### Key Components
| Component | Purpose |
|-----------|---------|
| **Subnet** | Partition of VPC within ONE AZ |
| **Route Table** | Controls traffic routing |
| **Internet Gateway (IGW)** | Connect VPC to internet |
| **NAT Gateway** | Internet access for private subnets (outbound only) |
| **Security Group** | Instance-level firewall (stateful) |
| **NACL** | Subnet-level firewall (stateless) |
| **VPC Peering** | Connect two VPCs |
| **VPC Endpoints** | Private access to AWS services |

---

## Subnets

### Public vs Private Subnet
| Feature | Public Subnet | Private Subnet |
|---------|---------------|----------------|
| Route to IGW | ✅ Yes (0.0.0.0/0 → IGW) | ❌ No |
| Public IP | Auto-assign option | No public IP |
| Internet access | Direct (in + out) | Via NAT Gateway (out only) |
| Use Case | Web servers, bastion hosts | App servers, databases |

### Reserved IPs (5 per subnet)
- `.0` — Network address
- `.1` — VPC router
- `.2` — DNS server
- `.3` — Reserved for future
- `.255` — Broadcast (not supported but reserved)

> Example: 10.0.0.0/24 = 256 - 5 = **251 usable IPs**

---

## Internet Gateway (IGW)
- Allows VPC instances to access the internet
- **One IGW per VPC** (1:1 relationship)
- Horizontally scaled, redundant, highly available
- Must also: Assign public IP + route table entry to IGW

## NAT Gateway
- Enables **private subnet** instances to reach the internet (outbound)
- Internet cannot initiate connections to private instances
- **Managed by AWS** (auto-scaling, HA within AZ)
- **Deploy in PUBLIC subnet** with Elastic IP
- Charged: Per hour + per GB processed
- **Not free** — significant cost for high traffic

### NAT Gateway HA Pattern
```
Deploy one NAT Gateway per AZ:
AZ-a: NAT-GW-a in public subnet → route table for private-a
AZ-b: NAT-GW-b in public subnet → route table for private-b
(Each AZ is independent — no cross-AZ dependency)
```

### NAT Gateway vs NAT Instance
| Feature | NAT Gateway | NAT Instance |
|---------|-------------|--------------|
| Managed | ✅ AWS managed | ❌ Self-managed EC2 |
| Bandwidth | Up to 100 Gbps | Depends on instance type |
| Availability | HA within AZ | DIY (scripting, ASG) |
| Security Groups | ❌ No | ✅ Yes |
| Bastion host | ❌ No | ✅ Can double as |
| Cost | Higher | Lower (t2.micro free tier) |
| **Recommendation** | ✅ Use this | ❌ Legacy |

---

## Security Groups vs NACLs

| Feature | Security Group | NACL |
|---------|---------------|------|
| Level | Instance (ENI) | Subnet |
| State | **Stateful** (return traffic auto-allowed) | **Stateless** (must allow both directions) |
| Rules | ALLOW only | ALLOW and DENY |
| Rule evaluation | All rules evaluated | Rules evaluated in **number order** (first match) |
| Default | Deny all inbound, Allow all outbound | Allow all in/out (default NACL) |
| Association | Multiple SGs per instance | One NACL per subnet |

### NACL Rule Evaluation
```
Rule 100: ALLOW TCP 443 from 0.0.0.0/0    ← Evaluated first
Rule 200: DENY TCP 443 from 10.0.0.5/32   ← Never reached for 443!
Rule *:   DENY ALL                          ← Default deny

ORDER MATTERS! Lower number = higher priority
```

### When to Use Each
- **Security Groups**: Primary firewall for instances (most questions)
- **NACLs**: Block specific IPs, add subnet-level defense, explicit DENY needed

> **Exam Tip**: "Block a specific IP address" = NACL (only option with DENY rules). Security groups cannot deny.

---

## VPC Peering

### Key Concepts
- Connect 2 VPCs privately (as if same network)
- Works **cross-account** and **cross-region**
- Uses AWS backbone (not internet)

### Rules
- **No transitive peering**: A↔B and B↔C does NOT mean A↔C
- **No overlapping CIDR** ranges
- Must update **route tables** in both VPCs
- Must update **security groups** to allow traffic
- One peering connection per VPC pair (can't have duplicate)

```
VPC-A (10.0.0.0/16) ←Peering→ VPC-B (172.16.0.0/16)
VPC-B ←Peering→ VPC-C (192.168.0.0/16)
VPC-A CANNOT talk to VPC-C (no transitive peering!)
→ Need: Transit Gateway or direct peering A↔C
```

> **Exam Tip**: "VPC A can't reach VPC C through VPC B" = VPC peering is not transitive. Use Transit Gateway for hub-and-spoke.

---

## VPC Flow Logs

### Key Concepts
- Capture **network traffic information** in your VPC
- Levels: VPC, Subnet, or ENI
- Destinations: CloudWatch Logs or S3
- Captures: Source/dest IP, ports, protocol, action (ACCEPT/REJECT), packets, bytes

### What Flow Logs DON'T Capture
- DNS traffic to Route 53 Resolver
- DHCP traffic
- Traffic to instance metadata (169.254.169.254)
- Traffic to reserved IPs (.0, .1, .2, .3)
- NTP (123) and Windows license activation

### Use Cases
- Troubleshoot security group / NACL issues
- Monitor traffic patterns
- Detect anomalies (feed to GuardDuty)
- Compliance logging

> **Exam Tip**: "Monitor all network traffic in VPC" = VPC Flow Logs. "Analyze flow logs with SQL" = Flow Logs → S3 → Athena.

---

## Bastion Host (Jump Server)

### Key Concepts
- EC2 instance in **public subnet** to SSH into private instances
- Security: Only allow SSH (port 22) from specific IPs
- Alternative: **SSM Session Manager** (no bastion needed, no port 22)

```
Your PC → SSH (port 22) → Bastion (public subnet)
                              → SSH → Private Instance (private subnet)
```

> **Exam Tip**: "Access private EC2 without bastion" = Systems Manager Session Manager (more secure, no port 22 needed).

---

## IPv6 in VPC
- All IPv6 addresses are **public** (no NAT needed)
- IPv6 CIDR assigned by AWS
- Use **Egress-only Internet Gateway** for IPv6 outbound (equivalent of NAT for IPv6)
- Dual-stack: Instances get both IPv4 and IPv6

---

## VPC Design Patterns

### Three-Tier Architecture
```
Public Subnet:  ALB (Internet-facing)
Private Subnet: Application servers (ASG)
Private Subnet: Database (RDS Multi-AZ)

Security Groups:
- ALB SG: Allow 80/443 from 0.0.0.0/0
- App SG: Allow app port from ALB SG only
- DB SG:  Allow 3306 from App SG only
```

### Key Design Principles
1. Put **only what needs internet** in public subnets
2. Use **least privilege** security groups (reference SG IDs, not IPs)
3. Deploy across **multiple AZs** for HA
4. Use **NAT Gateway per AZ** for private subnet internet
5. Use **VPC Endpoints** for AWS service access (avoid NAT charges)
6. Enable **Flow Logs** for troubleshooting and compliance
