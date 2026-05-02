# CS04: Advanced Networking - Direct Connect, Transit Gateway, VPC Endpoints
### AWS SAA-C03 Cheat Sheet

---

## Hybrid Connectivity Options

### AWS Direct Connect (DX)

**Key Concepts:**
- **Dedicated private connection** from on-premises to AWS
- Physical fiber connection at AWS Direct Connect location
- Does NOT go over the public internet
- **Takes weeks/months** to establish (not quick!)

**Connection Types:**
| Type | Speed | Port |
|------|-------|------|
| Dedicated | 1 Gbps, 10 Gbps, 100 Gbps | Physical port at DX location |
| Hosted | 50 Mbps to 10 Gbps | Via AWS Partner |

**Virtual Interfaces (VIFs):**
| VIF Type | Purpose | Access |
|----------|---------|--------|
| **Public VIF** | Access AWS public services (S3, DynamoDB) | Public endpoints |
| **Private VIF** | Access VPC resources | Private IPs in VPC |
| **Transit VIF** | Access VPCs via Transit Gateway | Multiple VPCs |

**Key Features:**
- **Consistent network performance** (no internet variability)
- Data in transit is **NOT encrypted** by default
  - Add VPN on top of DX for encryption (IPsec)
- **High availability**: Use 2 DX connections at different locations
- **Link Aggregation Groups (LAG)**: Bundle multiple connections
- **DX Gateway**: Connect DX to multiple VPCs across regions
- **Failover**: DX (primary) + VPN (backup) is common HA pattern

**DX Resiliency Patterns:**
```
Maximum Resiliency:    2 locations × 2 connections each
High Resiliency:       2 locations × 1 connection each  
Development/Test:      1 location  × 1 connection
```

> **Exam Tips**:
> - "Consistent, dedicated bandwidth from on-prem to AWS" = Direct Connect
> - "Encrypted connection over internet" = Site-to-Site VPN
> - "Private + Encrypted" = VPN over Direct Connect
> - "Need connectivity NOW" = VPN (DX takes weeks)
> - DX + VPN as backup = High availability

---

### Site-to-Site VPN

**Key Concepts:**
- Encrypted connection over the **public internet**
- Quick to set up (minutes/hours vs weeks for DX)
- Components:
  - **Virtual Private Gateway (VGW)**: AWS side
  - **Customer Gateway (CGW)**: On-premises side (hardware/software)
  - **VPN Connection**: Two IPsec tunnels for HA

**Key Features:**
- **IPsec encrypted** (AES-256)
- Supports **static routing** or **dynamic routing (BGP)**
- **Accelerated VPN**: Uses Global Accelerator for better performance
- Cost: Per hour + per GB transferred
- Bandwidth: Up to 1.25 Gbps per tunnel

**VPN CloudHub:**
- Connect multiple branch offices through hub-and-spoke model
- Multiple VPN connections to same VGW
- Branches can communicate with each other via AWS

> **Exam Tip**: VPN = quick, encrypted, over internet, variable performance. DX = slow setup, dedicated, consistent performance, not encrypted by default.

---

## Transit Gateway

### Key Concepts
- **Regional network hub** that connects VPCs and on-premises networks
- Star/hub-and-spoke topology (simplifies complex networking)
- Supports: VPCs, VPN, Direct Connect, Transit Gateway Peering

### Before vs After Transit Gateway
```
BEFORE (Mesh):              AFTER (Hub-and-spoke):
VPC-A ←→ VPC-B             VPC-A ──┐
VPC-A ←→ VPC-C                     ├── Transit Gateway
VPC-B ←→ VPC-C             VPC-B ──┤
VPC-A ←→ On-prem           VPC-C ──┤
VPC-B ←→ On-prem           On-prem─┘
(N×(N-1)/2 connections)    (N connections)
```

### Key Features
- **Cross-region peering**: Connect Transit Gateways across regions
- **Cross-account**: Share via RAM (Resource Access Manager)
- **Route Tables**: Control which VPCs can communicate
- **Multicast support**: Only AWS service supporting IP multicast
- **ECMP (Equal Cost Multi-Path)**: Aggregate bandwidth of multiple VPN tunnels
- Supports **thousands of VPC connections**

### Transit Gateway vs VPC Peering

| Feature | Transit Gateway | VPC Peering |
|---------|----------------|-------------|
| Topology | Hub-and-spoke | Point-to-point |
| Transitive routing | ✅ Yes | ❌ No |
| Scale | Thousands of VPCs | Limited |
| Cross-region | ✅ (via peering) | ✅ |
| Bandwidth | Up to 50 Gbps | No limit (within region) |
| Cost | Higher | Lower |
| Use Case | Large-scale, many VPCs | Few VPCs, simple connectivity |

> **Exam Tips**:
> - "Connect many VPCs together" = Transit Gateway
> - "Transitive routing needed" = Transit Gateway (VPC peering is NOT transitive)
> - "IP multicast" = Transit Gateway
> - "Simple 2 VPC connection" = VPC Peering (cheaper)
> - "Increase VPN bandwidth" = Transit Gateway + ECMP

---

## VPC Endpoints

### Key Concepts
- Connect to AWS services **privately** (without internet/NAT)
- Traffic stays on **AWS network** (never leaves)
- Removes need for Internet Gateway, NAT, VPN for AWS service access

### Endpoint Types

| Type | Services | How It Works | Cost |
|------|----------|--------------|------|
| **Gateway Endpoint** | S3, DynamoDB only | Route table entry | Free |
| **Interface Endpoint (PrivateLink)** | Most AWS services (100+) | ENI in your subnet | Per hour + per GB |

### Gateway Endpoints (S3 & DynamoDB)
- Add entry to route table pointing to endpoint
- No changes to security groups needed
- **Free** to use
- Specify in VPC endpoint policy what access to allow
- Must be in same region as S3 bucket

### Interface Endpoints (PrivateLink)
- Creates an **ENI** (Elastic Network Interface) in your subnet
- Gets a private IP address
- Supports security groups
- Can enable **Private DNS** to override public service DNS
- **Costs**: ~$0.01/hour + $0.01/GB processed

### AWS PrivateLink (VPC Endpoint Services)
- Expose YOUR service to other VPCs (even cross-account)
- Consumer creates Interface Endpoint → connects to your NLB
- Most secure way to share services (no VPC peering, no internet)
- Scales to thousands of consumer VPCs

```
Your VPC:  Service → NLB → PrivateLink
Their VPC: Interface Endpoint → ENI → Access your service
```

> **Exam Tips**:
> - "Access S3 from private subnet without internet" = Gateway Endpoint (free)
> - "Access AWS service privately" = Interface Endpoint
> - "Expose your service to other VPCs securely" = PrivateLink
> - "No data goes over internet to reach AWS services" = VPC Endpoints

---

## VPC Lattice (NEW 2025)

### Key Concepts
- **Application-layer networking** for service-to-service communication
- Connects services across VPCs, accounts, and compute types
- Layer 7 (HTTP/HTTPS/gRPC)
- Replaces complex service mesh (AWS App Mesh deprecated)

### Components
- **Service Network**: Logical grouping of services and policies
- **Service**: Represents your application (can be Lambda, ECS, EC2, etc.)
- **Target Group**: Instances, IPs, Lambda, ALB
- **Auth Policy**: IAM-based access control between services

### Key Features
- Cross-VPC, cross-account service connectivity
- Built-in load balancing, service discovery
- Request-level authentication and authorization
- No need for sidecar proxies or VPC peering
- Traffic management (weighted routing, canary)

> **Exam Tip**: "Connect microservices across VPCs/accounts without peering" = VPC Lattice. "Service mesh replacement" = VPC Lattice.

---

## AWS Network Firewall (NEW 2025)

### Key Concepts
- **Managed stateful firewall** for VPC
- Deep packet inspection (DPI)
- Intrusion Prevention System (IPS)
- Deployed in a dedicated firewall subnet

### Features
- **Stateful rules**: Track connection state, protocol detection
- **Stateless rules**: Process each packet independently (like NACLs but more powerful)
- **Domain filtering**: Allow/deny traffic to specific domains
- **Custom Suricata-compatible rules**
- **AWS Managed threat intelligence** rule groups
- **Centralized management** via Firewall Manager
- Logs to S3, CloudWatch, Kinesis Data Firehose

### Network Firewall vs Security Groups vs NACLs

| Feature | Security Groups | NACLs | Network Firewall |
|---------|----------------|-------|-----------------|
| Level | Instance | Subnet | VPC |
| Stateful | ✅ | ❌ | ✅ |
| Deep Packet Inspection | ❌ | ❌ | ✅ |
| Domain filtering | ❌ | ❌ | ✅ |
| IPS/IDS | ❌ | ❌ | ✅ |
| Cost | Free | Free | Paid |

> **Exam Tip**: "Inspect traffic content, block malicious domains" = Network Firewall. "Simple port/IP rules" = Security Groups/NACLs.

---

## VPC IPAM (IP Address Manager) (NEW 2025)

### Key Concepts
- Centrally plan, track, and monitor IP addresses
- Multi-account, multi-region IP address management
- Prevents IP address conflicts
- Automates IP allocation

> **Exam Tip**: "Manage IPs across 50+ accounts" = IPAM.

---

## Networking Decision Matrix

| Scenario | Solution |
|----------|----------|
| Connect on-prem to AWS (quick, encrypted) | Site-to-Site VPN |
| Connect on-prem to AWS (consistent, dedicated) | Direct Connect |
| Connect on-prem to AWS (consistent + encrypted) | VPN over Direct Connect |
| Connect few VPCs | VPC Peering |
| Connect many VPCs + on-prem (hub) | Transit Gateway |
| Access S3 privately from VPC | Gateway Endpoint |
| Access AWS services privately | Interface Endpoint |
| Expose your service privately to others | PrivateLink |
| Service-to-service across VPCs (L7) | VPC Lattice |
| Deep packet inspection in VPC | Network Firewall |
| Global traffic optimization | Global Accelerator |
| Content delivery/caching | CloudFront |
