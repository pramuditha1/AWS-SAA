# CS08: Management & Governance - Organizations, Config, CloudFormation, Systems Manager
### AWS SAA-C03 Cheat Sheet

---

## AWS Organizations

### Key Concepts
- **Centrally manage multiple AWS accounts**
- Consolidate billing (one payment method)
- Hierarchical structure: Root → OUs → Accounts

### Structure
```
Management Account (Payer)
└── Root
    ├── OU: Production
    │   ├── Account: Prod-App1
    │   └── Account: Prod-App2
    ├── OU: Development
    │   ├── Account: Dev-Team1
    │   └── Account: Dev-Team2
    └── OU: Security
        └── Account: Security-Audit
```

### Key Features
| Feature | Description |
|---------|-------------|
| **Consolidated Billing** | Single bill, volume discounts across all accounts |
| **SCPs (Service Control Policies)** | Restrict services/actions for OUs/accounts |
| **RAM (Resource Access Manager)** | Share resources across accounts |
| **AWS Control Tower** | Automated multi-account setup with best practices |
| **Tag Policies** | Enforce tagging standards |
| **Backup Policies** | Centralized backup management |

### Service Control Policies (SCPs)
- Define **maximum permissions** for accounts/OUs
- **Do NOT grant permissions** — only restrict
- Applied hierarchically (Root → OU → Account)
- **Does NOT affect Management Account**
- Use cases: Block regions, prevent deletion of CloudTrail, restrict services

### SCP Strategies
```
Deny List (default):
- FullAWSAccess SCP attached by default
- Add explicit Deny SCPs for what you want to block

Allow List:
- Remove FullAWSAccess
- Only allow specific services
```

> **Exam Tips**:
> - "Centrally manage multiple AWS accounts" = Organizations
> - "Restrict services in member accounts" = SCPs
> - "Volume discount across accounts" = Consolidated Billing
> - "SCPs don't affect management account" = Always remember this!
> - "Share resources across accounts" = RAM

---

## AWS Control Tower

### Key Concepts
- **Automated setup** of secure, multi-account AWS environment
- Implements best practices (landing zone)
- Built on top of Organizations, SCPs, IAM Identity Center, Config

### Key Features
- **Landing Zone**: Pre-configured multi-account environment
- **Guardrails**: Pre-packaged governance rules
  - **Preventive**: SCPs that prevent actions (e.g., block root user)
  - **Detective**: AWS Config rules that detect violations
  - **Proactive**: CloudFormation hooks to block non-compliant resources
- **Account Factory**: Standardized account provisioning
- **Dashboard**: Compliance overview

> **Exam Tip**: "Set up secure multi-account environment quickly with best practices" = Control Tower.

---

## AWS CloudFormation (Infrastructure as Code)

### Key Concepts
- **Infrastructure as Code (IaC)** — define AWS resources in templates
- Declarative: Define WHAT you want, CloudFormation figures out HOW
- Templates in YAML or JSON
- Free service (pay only for resources created)

### Key Components
| Component | Description |
|-----------|-------------|
| **Template** | YAML/JSON file defining resources |
| **Stack** | Collection of resources from one template |
| **StackSet** | Deploy stacks across multiple accounts/regions |
| **Change Set** | Preview changes before applying |
| **Drift Detection** | Detect manual changes to stack resources |

### Template Anatomy
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: My stack
Parameters:         # Input values
Mappings:          # Key-value lookups
Conditions:        # Conditional resource creation
Resources:         # AWS resources (REQUIRED - only mandatory section)
Outputs:           # Return values (can be exported for cross-stack reference)
```

### Key Features
- **Cross-stack references**: Export outputs, import in other stacks
- **Nested Stacks**: Reuse templates as components
- **Rollback**: Automatic on failure (or manual)
- **Deletion Policy**: 
  - `Delete` (default): Delete resource when stack deleted
  - `Retain`: Keep resource after stack deletion
  - `Snapshot`: Create snapshot before deletion (EBS, RDS)
- **DependsOn**: Explicit resource creation order
- **cfn-init / cfn-signal**: Bootstrap EC2 instances
- **Stack Policies**: Protect resources from unintended updates

### CloudFormation vs Terraform vs CDK
| Feature | CloudFormation | Terraform | CDK |
|---------|---------------|-----------|-----|
| Provider | AWS only | Multi-cloud | Generates CloudFormation |
| Language | YAML/JSON | HCL | Python, TypeScript, etc. |
| State | Managed by AWS | You manage state file | AWS (via CFn) |

> **Exam Tips**:
> - "Deploy infrastructure across multiple regions/accounts" = StackSets
> - "Detect if someone manually changed resources" = Drift Detection
> - "Keep RDS database even if stack deleted" = DeletionPolicy: Retain
> - "Preview changes before updating stack" = Change Set
> - "Reuse common template patterns" = Nested Stacks

---

## AWS Config

### Key Concepts
- **Track configuration changes** and compliance of AWS resources
- Think: "Are my resources configured correctly?"
- Records configuration history over time
- Evaluates against **rules** for compliance

### Key Features
| Feature | Description |
|---------|-------------|
| **Config Rules** | Define desired configuration (managed or custom) |
| **Conformance Packs** | Collection of rules + remediation (compliance frameworks) |
| **Remediation** | Automatic fix via SSM Automation |
| **Aggregator** | Multi-account, multi-region view |
| **Timeline** | View resource configuration history |
| **Relationships** | See resource dependencies |

### Config Rules Examples
- `restricted-ssh`: No security group allows 0.0.0.0/0 to port 22
- `s3-bucket-public-read-prohibited`: S3 buckets aren't public
- `encrypted-volumes`: All EBS volumes are encrypted
- `rds-multi-az-support`: RDS instances are Multi-AZ
- Custom rules via Lambda functions

### Config vs CloudTrail vs CloudWatch
| Service | Question Answered |
|---------|-------------------|
| **Config** | "Is this resource configured correctly?" / "What changed?" |
| **CloudTrail** | "Who made this API call?" |
| **CloudWatch** | "How is this resource performing?" |

> **Exam Tips**:
> - "Ensure all EBS volumes are encrypted" = Config Rule
> - "Track configuration change history" = AWS Config
> - "Auto-remediate non-compliant resources" = Config + SSM Automation
> - "Multi-account compliance dashboard" = Config Aggregator
> - "Compliance framework enforcement" = Config Conformance Packs

---

## AWS Systems Manager (SSM)

### Key Concepts
- **Manage EC2 and on-premises** infrastructure at scale
- Free for EC2 instances (SSM Agent pre-installed on Amazon Linux/Windows AMIs)
- No SSH/RDP needed — connect via Session Manager

### Key Features

| Feature | Description |
|---------|-------------|
| **Session Manager** | Secure shell access without SSH (no port 22 needed!) |
| **Run Command** | Execute commands on multiple instances (no SSH) |
| **Patch Manager** | Automate OS patching |
| **Parameter Store** | Centralized config/secret storage (free tier) |
| **Automation** | Runbooks for common tasks |
| **Inventory** | Collect software/OS info from instances |
| **State Manager** | Maintain instance in defined state |
| **Maintenance Windows** | Schedule patching and tasks |

### Parameter Store vs Secrets Manager
| Feature | Parameter Store | Secrets Manager |
|---------|----------------|-----------------|
| Cost | Free (standard), paid (advanced) | $0.40/secret/month |
| Rotation | ❌ No built-in | ✅ Auto-rotation |
| Size limit | 8 KB (standard), 8 KB (advanced) | 64 KB |
| Hierarchy | ✅ Path-based (/app/db/password) | ❌ Flat |
| Cross-account | ❌ | ✅ Resource policies |
| KMS encryption | ✅ Optional | ✅ Always |

### Session Manager Benefits
- No SSH keys to manage
- No port 22 open in security groups
- Full audit trail in CloudTrail
- Can restrict access via IAM
- Logs to S3 or CloudWatch

> **Exam Tips**:
> - "Manage instances without SSH/bastion" = SSM Session Manager
> - "Patch instances automatically" = SSM Patch Manager
> - "Run command on 100 instances" = SSM Run Command
> - "Store database password (no rotation needed)" = Parameter Store
> - "Store database password (auto-rotation needed)" = Secrets Manager

---

## AWS Trusted Advisor

### Key Concepts
- **Best practice recommendations** across 5 categories:
  1. **Cost Optimization** (underutilized resources)
  2. **Performance** (service limits, overutilized)
  3. **Security** (open security groups, MFA, IAM)
  4. **Fault Tolerance** (backups, Multi-AZ, HA)
  5. **Service Limits** (approaching limits)

### Free vs Business/Enterprise Support
| Tier | Available Checks |
|------|-----------------|
| **Basic/Developer** | 7 core checks (S3 public, SG ports, IAM, MFA, EBS snapshots, RDS snapshots, service limits) |
| **Business/Enterprise** | All checks + API access + CloudWatch integration |

> **Exam Tip**: "Recommendations for cost, security, performance" = Trusted Advisor. Full access requires Business/Enterprise Support plan.

---

## AWS Well-Architected Tool

### Key Concepts
- Review workloads against AWS Well-Architected Framework
- Identify risks and get improvement plans
- Free self-service tool in AWS Console
- Based on the 6 pillars (see CS10)

---

## Cost Management Tools

| Tool | Purpose |
|------|---------|
| **AWS Cost Explorer** | Visualize and analyze spending patterns |
| **AWS Budgets** | Set custom budgets with alerts |
| **Cost Anomaly Detection** | ML-based unusual spend detection |
| **Compute Optimizer** | Right-sizing recommendations for EC2, EBS, Lambda |
| **Savings Plans** | Flexible discount model (commit $/hour) |
| **Reserved Instances** | Capacity reservation with discount |

---

## Service Catalog

### Key Concepts
- Create and manage **approved IT service catalogs**
- End users launch pre-approved CloudFormation templates
- Governance: Control what users can deploy
- Self-service: Users deploy without needing CloudFormation knowledge

> **Exam Tip**: "Allow developers to deploy approved resources only" = Service Catalog.
