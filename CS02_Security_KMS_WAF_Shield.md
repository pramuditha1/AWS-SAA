# CS02: Security - KMS, WAF, Shield, GuardDuty, Secrets Manager
### AWS SAA-C03 Cheat Sheet

---

## KMS (Key Management Service)

### Key Concepts
- Managed service for creating and controlling **encryption keys**
- Integrated with most AWS services (S3, EBS, RDS, Redshift, etc.)
- **Regional service** - keys are region-specific
- Supports **symmetric** (AES-256) and **asymmetric** (RSA, ECC) keys

### Key Types
| Type | Description | Use Case |
|------|-------------|----------|
| **AWS Managed Keys** | Created/managed by AWS (aws/service-name) | Default encryption, no management needed |
| **Customer Managed Keys (CMK)** | You create, manage, set policies | Full control, key rotation, cross-account |
| **AWS Owned Keys** | AWS owns, shared across accounts | Free, limited visibility |

### Envelope Encryption
```
┌─────────────────────────────────────┐
│  Data Key (DEK) encrypts your DATA  │
│  Master Key (CMK) encrypts the DEK  │
│  Only DEK is sent with encrypted data│
└─────────────────────────────────────┘
```
- **Why?** KMS can only encrypt up to 4 KB directly
- For large data: Generate DEK → encrypt data with DEK → encrypt DEK with CMK → store encrypted DEK with data
- `GenerateDataKey` API = returns plaintext + encrypted DEK

### Key Rotation
- **AWS Managed**: Auto-rotated every year (mandatory)
- **Customer Managed**: Optional auto-rotation (every year) or manual
- Old key material kept for decryption of old data

### KMS Key Policies
- Control access to KMS keys (like S3 bucket policies)
- **Default policy**: Allows root account full access
- **Custom policy**: Define users/roles, allow cross-account access

### Multi-Region Keys
- Same key replicated across regions (same key ID)
- Encrypt in one region, decrypt in another
- Use Case: Global DynamoDB tables, global Aurora

### S3 Encryption Options

| Type | Key Management | Key Storage |
|------|---------------|-------------|
| **SSE-S3** | AWS manages everything | AWS |
| **SSE-KMS** | You manage in KMS, audit via CloudTrail | AWS KMS |
| **SSE-C** | You provide key with every request | Customer manages |
| **Client-Side** | You encrypt before upload | Customer |

> **Exam Tip**: "Audit who used encryption key" = SSE-KMS. "Regulatory requirement to manage own keys" = SSE-C or Client-side. Default/simplest = SSE-S3.

---

## AWS WAF (Web Application Firewall)

### Key Concepts
- Protects web applications from common web exploits
- **Layer 7** (HTTP/HTTPS) protection
- Deploys on: **CloudFront, ALB, API Gateway, AppSync, Cognito**

### WAF Rules & Features
- **Web ACLs**: Contains rules, applied to resources
- **Rule Types**:
  - IP Set rules (allow/block IP ranges)
  - Rate-based rules (block if > X requests/5 min) → DDoS mitigation
  - SQL injection protection
  - Cross-site scripting (XSS) protection
  - Geo-match (block/allow by country)
  - Size constraints
  - Regex pattern matching
- **Managed Rule Groups**: Pre-built by AWS or AWS Marketplace sellers
  - Core Rule Set, Known Bad Inputs, Bot Control, etc.

> **Exam Tip**: "Block SQL injection or XSS" = WAF. "Block specific countries" = WAF geo-match. "Rate limiting" = WAF rate-based rules. "DDoS protection" = Shield (+ WAF for Layer 7).

---

## AWS Shield

### Shield Standard (FREE)
- Automatically enabled for ALL AWS customers
- Protects against Layer 3/4 DDoS attacks
- Protects: CloudFront, Route 53, ELB

### Shield Advanced ($3,000/month)
- Enhanced DDoS protection for: EC2, ELB, CloudFront, Global Accelerator, Route 53
- **24/7 DDoS Response Team (DRT)** access
- **Cost protection**: Refund for scaling costs during DDoS
- **Near real-time visibility** into attacks
- **Automatic application layer (L7) mitigation** with WAF
- Advanced metrics in CloudWatch

> **Exam Tip**: "Protection against DDoS with cost protection" = Shield Advanced. "Automatic L3/L4 protection" = Shield Standard (free, always on).

---

## AWS GuardDuty

### Key Concepts
- **Intelligent threat detection** service
- Uses ML, anomaly detection, and integrated threat intelligence
- **One-click enable** - no software/agents to install
- Analyzes: **VPC Flow Logs, CloudTrail logs, DNS logs, EKS audit logs, S3 data events**

### What It Detects
- Compromised EC2 instances (crypto mining, C&C communication)
- Unauthorized access patterns
- Compromised credentials
- Malicious IP reconnaissance
- S3 bucket compromise

### Key Features
- Findings categorized by severity (Low, Medium, High)
- Can trigger **EventBridge** → Lambda → auto-remediation
- **Multi-account support** via AWS Organizations
- Can protect against **cryptocurrency mining attacks**
- **Malware Protection**: Scans EBS volumes attached to EC2/ECS

> **Exam Tip**: "Detect unusual API calls or compromised instances" = GuardDuty. "Automated threat detection without agents" = GuardDuty.

---

## Amazon Inspector

### Key Concepts
- **Automated vulnerability management**
- Continuously scans workloads for vulnerabilities
- Targets: **EC2 instances, Container images (ECR), Lambda functions**
- Uses SSM Agent on EC2 for OS-level scanning

### What It Finds
- Software vulnerabilities (CVEs)
- Network reachability issues
- Unintended network exposure

### Key Features
- Automated, continuous scanning
- Risk score for prioritization
- Integrates with Security Hub
- Findings sent to EventBridge for automation

> **Exam Tip**: "Scan EC2 for vulnerabilities/CVEs" = Inspector. "Scan container images" = Inspector. "Detect threats in logs" = GuardDuty.

---

## Amazon Macie

### Key Concepts
- Uses ML to discover, classify, and protect **sensitive data** in S3
- Finds: **PII (Personally Identifiable Information)**, financial data, credentials
- Alerts via EventBridge

### Use Cases
- Data privacy compliance (GDPR, HIPAA)
- Find exposed credentials or API keys in S3
- Identify S3 buckets with sensitive data

> **Exam Tip**: "Discover PII data in S3" = Macie. "Detect sensitive data" = Macie.

---

## AWS Secrets Manager

### Key Concepts
- Store, rotate, and manage **secrets** (passwords, API keys, DB credentials)
- **Automatic rotation** using Lambda functions
- Native integration with RDS, Redshift, DocumentDB

### Secrets Manager vs Systems Manager Parameter Store

| Feature | Secrets Manager | Parameter Store |
|---------|----------------|-----------------|
| Cost | $0.40/secret/month | Free tier available |
| Rotation | ✅ Built-in auto-rotation | ❌ No native rotation |
| Cross-account | ✅ Via resource policy | ❌ No |
| RDS Integration | ✅ Native | ❌ Manual |
| Use Case | DB credentials, API keys needing rotation | Config values, non-rotating secrets |

> **Exam Tip**: "Auto-rotate database credentials" = Secrets Manager. "Store configuration parameters cheaply" = Parameter Store.

---

## AWS IAM Advanced Topics (You're Missing)

### IAM Identity Center (SSO)
- Single sign-on for multiple AWS accounts + business apps
- Central place to manage access across AWS Organization
- Integrates with AD, SAML 2.0 IdPs

### STS (Security Token Service)
- Provides **temporary credentials** for:
  - Cross-account access (AssumeRole)
  - Federation (AssumeRoleWithSAML, AssumeRoleWithWebIdentity)
  - EC2 instance roles
- Credentials expire (15 min to 12 hours)

### Resource-Based Policies vs IAM Roles (Cross-Account)
- **Resource-based policy**: Attach to resource (S3, SQS, Lambda). Principal doesn't give up permissions.
- **IAM Role**: Principal assumes role, gives up original permissions.

### Permission Boundaries
- Set maximum permissions an IAM entity CAN have
- Used to delegate admin without full privilege escalation

### AWS Organizations SCPs
- **Service Control Policies**: Set maximum permissions for entire OU/account
- Does NOT grant permissions, only restricts
- Does NOT affect management account

---

## Amazon Verified Permissions (NEW 2025)

### Key Concepts
- Fine-grained authorization service for applications
- Uses **Cedar** policy language
- Centralize authorization logic outside application code
- Zero-trust architecture support
- Integrates with Cognito and custom identity providers

> **Exam Tip**: "Fine-grained application-level authorization" = Verified Permissions. "Account/service-level permissions" = IAM.

---

## Security Services Summary

| Service | Purpose | Layer |
|---------|---------|-------|
| **WAF** | Web exploits (SQLi, XSS, rate limiting) | L7 |
| **Shield** | DDoS protection | L3/L4 (+ L7 with WAF) |
| **GuardDuty** | Threat detection from logs | Account-wide |
| **Inspector** | Vulnerability scanning | EC2, ECR, Lambda |
| **Macie** | Sensitive data discovery | S3 |
| **KMS** | Encryption key management | Data |
| **Secrets Manager** | Secret storage + rotation | Credentials |
| **IAM** | Access control | Identity |
| **Firewall Manager** | Centrally manage WAF/Shield/SG | Organization |
