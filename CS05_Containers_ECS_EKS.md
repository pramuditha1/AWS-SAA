# CS05: Containers - ECS, EKS, Fargate, ECR
### AWS SAA-C03 Cheat Sheet

---

## Container Services Overview

```
┌─────────────────────────────────────────────────┐
│           ORCHESTRATION (Control Plane)          │
│    ┌─────────────┐       ┌─────────────┐       │
│    │     ECS     │       │     EKS     │       │
│    │  (AWS-native)│       │ (Kubernetes)│       │
│    └─────────────┘       └─────────────┘       │
├─────────────────────────────────────────────────┤
│           COMPUTE (Data Plane)                   │
│    ┌─────────────┐       ┌─────────────┐       │
│    │  EC2 Launch  │       │   Fargate   │       │
│    │    Type      │       │ (Serverless)│       │
│    └─────────────┘       └─────────────┘       │
├─────────────────────────────────────────────────┤
│           REGISTRY                               │
│    ┌─────────────────────────────────────┐      │
│    │           ECR (Elastic Container    │      │
│    │              Registry)              │      │
│    └─────────────────────────────────────┘      │
└─────────────────────────────────────────────────┘
```

---

## ECS (Elastic Container Service)

### Key Concepts
- **AWS-native container orchestration** service
- Manages container lifecycle (deploy, run, scale, stop)
- Deeply integrated with AWS services (ALB, IAM, CloudWatch, etc.)
- Two launch types: EC2 and Fargate

### ECS Components
| Component | Description |
|-----------|-------------|
| **Cluster** | Logical grouping of tasks/services |
| **Task Definition** | Blueprint for your container (like a Dockerfile on steroids) |
| **Task** | Running instance of a Task Definition |
| **Service** | Maintains desired count of tasks, integrates with ELB |
| **Container Instance** | EC2 instance running ECS Agent (EC2 launch type only) |

### EC2 Launch Type vs Fargate

| Feature | EC2 Launch Type | Fargate |
|---------|----------------|---------|
| Infrastructure | You manage EC2 instances | AWS manages (serverless) |
| Scaling | Must scale EC2 + tasks | Scale tasks only |
| Pricing | Pay for EC2 instances | Pay per task (vCPU + memory) |
| Control | Full OS access, GPU support | No OS access |
| Networking | awsvpc, bridge, host modes | awsvpc only |
| Use Case | Cost optimization at scale, GPU, specific requirements | Simplicity, variable workloads |

### ECS Key Features

**IAM Roles:**
- **EC2 Instance Role** (EC2 launch type): Permissions for the ECS agent
- **Task Role** (`taskRoleArn`): Permissions for the container/application itself
- **Task Execution Role**: Permissions to pull images from ECR, write logs

**Networking (awsvpc mode):**
- Each task gets its own ENI and private IP
- Required for Fargate, optional for EC2 launch type
- Enables security groups per task

**Load Balancing:**
- ALB supports **dynamic port mapping** → multiple tasks on same instance
- NLB for high throughput / TCP / static IP needs
- ALB + path-based routing for microservices

**Auto Scaling:**
- **Service Auto Scaling**: Scale number of tasks
  - Target Tracking (e.g., keep CPU at 70%)
  - Step Scaling
  - Scheduled Scaling
- **Cluster Auto Scaling** (EC2 type): Uses Capacity Provider to scale EC2 instances

**Data Volumes:**
- EFS: Shared persistent storage across tasks (works with both EC2 and Fargate)
- EBS: Task-level persistent storage
- Bind mounts: Share data between containers in same task

### ECS Anywhere
- Run ECS tasks on **on-premises** servers
- Register external instances with ECS cluster
- Manage via same ECS APIs and console

> **Exam Tips**:
> - "Run containers with least management" = ECS + Fargate
> - "Need GPU for containers" = ECS + EC2 launch type
> - "Multiple containers on same port on same host" = ALB dynamic port mapping
> - "Container needs to access S3" = Task Role (not instance role)
> - "Shared storage between containers" = EFS mount

---

## EKS (Elastic Kubernetes Service)

### Key Concepts
- **Managed Kubernetes** on AWS
- Use when: Already using Kubernetes, need portability, or need K8s ecosystem
- Supports EC2 and Fargate compute
- Control plane managed by AWS (multi-AZ)

### EKS vs ECS

| Feature | EKS | ECS |
|---------|-----|-----|
| Orchestrator | Kubernetes | AWS-native |
| Learning curve | Steep (K8s knowledge needed) | Easier (AWS-native) |
| Portability | ✅ K8s runs anywhere | ❌ AWS only |
| Ecosystem | Huge K8s ecosystem | AWS ecosystem |
| Pricing | $0.10/hour for control plane + compute | Free control plane + compute |
| Use Case | K8s expertise, multi-cloud, complex orchestration | AWS-native, simpler container needs |

### EKS Key Features
- **Managed Node Groups**: AWS manages EC2 instances for you
- **Fargate Profile**: Run pods serverlessly (no nodes to manage)
- **EKS Anywhere**: Run K8s on your own infrastructure
- **EKS Distro**: K8s distribution to run anywhere

### When to Choose EKS
- Already invested in Kubernetes
- Need to run on multiple clouds or on-premises
- Need K8s-specific features (Helm, service mesh, etc.)
- Large engineering team with K8s expertise

> **Exam Tip**: "Migrate existing Kubernetes workloads to AWS" = EKS. "Simple container deployment on AWS" = ECS.

---

## AWS Fargate

### Key Concepts
- **Serverless compute engine** for containers
- Works with both ECS and EKS
- No EC2 instances to manage, patch, or scale
- Pay only for resources your containers use

### Fargate Pricing
- Per vCPU per second
- Per GB memory per second
- No minimum charge beyond 1 minute

### Fargate Limitations
- No GPU support
- No privileged containers
- Limited storage (20 GB ephemeral by default, up to 200 GB)
- No SSH access to underlying infrastructure
- Only awsvpc networking mode (ECS)

> **Exam Tip**: "Serverless containers" or "containers without managing servers" = Fargate.

---

## ECR (Elastic Container Registry)

### Key Concepts
- **Managed Docker container registry**
- Store, manage, and deploy container images
- Integrated with ECS, EKS, and Lambda

### Key Features
- **Private repositories** (per account, per region)
- **Public repositories** (ECR Public Gallery)
- **Image scanning**: Vulnerability scanning on push
- **Image lifecycle policies**: Auto-cleanup old images
- **Cross-region/cross-account replication**
- **Encryption**: At rest with KMS
- **Immutable tags**: Prevent image tag overwriting

### Access Control
- **Repository Policy**: Resource-based policy for cross-account access
- **IAM Policy**: Standard IAM permissions
- Task Execution Role needs `ecr:GetAuthorizationToken` + `ecr:BatchGetImage`

> **Exam Tip**: "Store Docker images securely in AWS" = ECR. "Cross-account image sharing" = ECR Repository Policy.

---

## Container Architecture Patterns

### Microservices with ECS
```
Internet → ALB (path-based routing)
              ├── /api/users   → ECS Service A (Users)
              ├── /api/orders  → ECS Service B (Orders)
              └── /api/products→ ECS Service C (Products)

Each service: Fargate tasks + Auto Scaling + own Task Definition
Shared: EFS for shared files, RDS for databases, SQS for async communication
```

### Sidecar Pattern
- Multiple containers in same Task Definition
- Share: network (localhost), storage (volumes)
- Example: App container + logging sidecar + monitoring sidecar

---

## Elastic Beanstalk (Platform as a Service)

### Key Concepts
- **PaaS** - Deploy applications without managing infrastructure
- Handles: Capacity provisioning, load balancing, auto-scaling, health monitoring
- Supports: Java, .NET, PHP, Node.js, Python, Ruby, Go, Docker
- **You retain full control** of underlying resources

### Deployment Strategies
| Strategy | Downtime | Speed | Rollback |
|----------|----------|-------|----------|
| **All at once** | ✅ Yes | Fastest | Manual redeploy |
| **Rolling** | ❌ No | Slow | Manual redeploy |
| **Rolling with additional batch** | ❌ No | Slow | Manual redeploy |
| **Immutable** | ❌ No | Slow | Terminate new ASG |
| **Blue/Green** | ❌ No | Medium | Swap URLs |
| **Traffic splitting** | ❌ No | Medium | Reroute traffic |

### Key Features
- **Web Server tier**: Handles HTTP requests (ELB + ASG + EC2)
- **Worker tier**: Processes background tasks (SQS + ASG + EC2)
- **Managed platform updates**: Auto-apply OS patches
- **.ebextensions**: YAML/JSON config files for customization
- **Saved Configurations**: Reuse environment settings

> **Exam Tips**:
> - "Deploy web app quickly without managing infra" = Elastic Beanstalk
> - "Developer wants to upload code and have it run" = Elastic Beanstalk
> - "Full control over infra + container orchestration" = ECS/EKS
> - "Zero downtime deployment" = Rolling, Immutable, or Blue/Green (NOT All at once)

---

## Container Decision Matrix

| Scenario | Solution |
|----------|----------|
| Run containers with zero server management | ECS/EKS + Fargate |
| Migrate existing Kubernetes workloads | EKS |
| Simple container deployment, AWS-native | ECS |
| Need GPU for container workloads | ECS + EC2 launch type |
| Deploy app without thinking about containers | Elastic Beanstalk |
| Store container images | ECR |
| Run containers on-premises managed by AWS | ECS Anywhere / EKS Anywhere |
| Batch processing with containers | AWS Batch (with Fargate) |
