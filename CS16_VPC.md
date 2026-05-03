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

#### Exam-Focused Scenario
- **Scenario:** You need to host a public-facing website in a public subnet and backend processing in a private subnet. What CIDR ranges would you assign to achieve this separation effectively?
  - Assign **10.0.1.0/24** to the public subnet for web servers.
  - Assign **10.0.2.0/24** for private subnet backend processing.

---

## Internet Gateway (IGW)
- Allows VPC instances to access the internet
- **One IGW per VPC** (1:1 relationship)
- Horizontally scaled, redundant, highly available
- Must also: Assign public IP + route table entry to IGW

#### Exam Tip:
"How do public EC2 instances access the internet?" Assign a public IP and route via the IGW.

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

### Exam Scenario: Troubleshooting
- **Scenario:** Your EC2 instances can't communicate with an RDS database, even though they are in the same VPC.
  - Check Security Groups: Ensure the app SG allows inbound traffic on port 3306 from your EC2 SG.
  - Verify NACL Rules: Ensure subnet-level NACLs do not block traffic explicitly.

---

## VPC Peering

### Key Concepts
- Connect 2 VPCs privately (as if same network)
- Works **cross-account** and **cross-region**
- Uses AWS backbone (not internet)

---

## Case Study Example: High Availability
**Use Case:** Deploying a multi-tier application with redundancy
- Public subnets: Host ALB with internet-facing configuration.
- Private subnets: App and database tiers (distributed across AZs).
- NAT Gateways: Enable internet access only for private subnets (updates, API requests).
- Security Configuration:
  - ALB Security Group: Allows HTTP(S) traffic from any source.
  - App Security Group: Allows traffic only from ALB SG.
  - DB Security Group: Allows traffic only from App SG.

