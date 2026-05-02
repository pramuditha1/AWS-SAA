# CS11: IAM - Identity & Access Management
### AWS SAA-C03 Cheat Sheet

---

## Core Concepts

### What is IAM?
- **Global service** (not regional)
- Controls WHO can access WHAT in your AWS account
- **Free** — no charge for IAM usage
- **Root Account**: Created by default, has FULL access. Never use for daily tasks!

### IAM Entities

| Entity | Description | Key Point |
|--------|-------------|-----------|
| **Users** | People or applications | Long-term credentials |
| **Groups** | Collection of users | Easier permission management |
| **Roles** | Temporary identity assumed by services/users | Short-term credentials via STS |
| **Policies** | JSON documents defining permissions | Attach to users, groups, or roles |

---

## IAM Policies

### Policy Structure (JSON)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowS3Read",
      "Effect": "Allow",          // Allow or Deny
      "Action": "s3:GetObject",   // What action
      "Resource": "arn:aws:s3:::my-bucket/*",  // On what resource
      "Condition": {}             // Optional conditions
    }
  ]
}
```

### Policy Types
| Type | Attached To | Use Case |
|------|------------|----------|
| **Identity-based** | Users, Groups, Roles | Most common - who can do what |
| **Resource-based** | S3, SQS, Lambda, etc. | Cross-account access, no role needed |
| **Permission Boundary** | Users, Roles | Set MAX permissions (guardrail) |
| **SCP** | AWS Organization OU/Account | Account-level restrictions |
| **Session Policy** | STS session | Limit assumed role permissions |

### Policy Evaluation Logic
```
1. Explicit DENY? → DENIED (always wins)
2. SCP allows? → Check next (if Organizations)
3. Permission Boundary allows? → Check next (if set)
4. Identity-based policy ALLOW? → ALLOWED
5. Resource-based policy ALLOW? → ALLOWED
6. Otherwise → DENIED (implicit deny)
```

> **Key Rule**: Explicit Deny ALWAYS overrides any Allow.

---

## IAM Roles

### When to Use Roles
| Scenario | Role Type |
|----------|-----------|
| EC2 needs to access S3 | EC2 Instance Role (Instance Profile) |
| Lambda needs DynamoDB access | Lambda Execution Role |
| Cross-account access | Cross-account role (AssumeRole) |
| Federated users (SAML/OIDC) | Federation role |
| AWS service needs another service | Service-linked role |

### Instance Profile
- Container for an IAM Role attached to EC2
- One role per instance at a time
- Applications on EC2 get temporary credentials automatically
- **Never embed access keys in EC2** — always use roles!

### Cross-Account Access
```
Account A (Trusting):
  - Create Role with Trust Policy allowing Account B
  
Account B (Trusted):
  - User/Role calls sts:AssumeRole on Account A's role
  - Gets temporary credentials for Account A
```

---

## IAM Security Best Practices

### MFA (Multi-Factor Authentication)
- Enable for **root account** (mandatory best practice)
- Enable for all IAM users with console access
- Types: Virtual MFA (Google Auth), U2F key, Hardware TOTP

### Password Policy
- Minimum length
- Character requirements (upper, lower, numbers, symbols)
- Password expiration
- Prevent password reuse

### Access Keys
- For programmatic access (CLI/SDK)
- **Two keys per user** maximum
- Rotate regularly
- Never share or commit to code
- Use IAM Roles instead when possible

### Security Tools
| Tool | Purpose |
|------|---------|
| **IAM Credentials Report** | Account-level: Lists all users and credential status |
| **IAM Access Advisor** | User-level: Shows services accessed and last accessed time |
| **Access Analyzer** | Find resources shared with external entities |

---

## IAM Key Exam Points

### Remember These Rules
1. **New users have NO permissions** by default
2. **Root account** should have MFA, not used for daily tasks
3. **Roles > Access Keys** for AWS service access
4. **Least privilege** — give minimum permissions needed
5. **Groups** cannot be nested (no groups within groups)
6. **A user can belong to multiple groups** (max 10)
7. **Policies can be inline** (embedded) or **managed** (reusable)
8. **AWS Managed Policies** — pre-built by AWS (can't edit)
9. **Customer Managed Policies** — you create and manage (recommended)

### Common Exam Scenarios

| Scenario | Solution |
|----------|----------|
| "EC2 needs to call S3 API" | Attach IAM Role to EC2 (never access keys) |
| "Temporary access for contractor" | IAM Role with time-limited session |
| "Restrict what a developer can do" | Permission Boundary |
| "Block all users from certain region" | SCP (Organization level) |
| "Application on-premises needs AWS access" | IAM User with access keys (or federate) |
| "Mobile app users need AWS resource access" | Cognito + IAM Role (web identity federation) |

> **Exam Tip**: If a question mentions "least privilege" or "security best practice," look for the answer that limits permissions the most while still being functional.
