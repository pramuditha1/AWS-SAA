# CS19: Serverless - Lambda, Step Functions
### AWS SAA-C03 Cheat Sheet

---

## AWS Lambda

### Key Concepts
- **Serverless compute** — run code without managing servers
- **Event-driven**: Code runs in response to triggers
- Pay only when code is running (per request + per duration)
- Auto-scales automatically (up to thousands of concurrent executions)
- Supports: Python, Node.js, Java, C#, Go, Ruby, Custom Runtime

### Lambda Limits

| Limit | Value |
|-------|-------|
| **Timeout** | 15 minutes (max) |
| **Memory** | 128 MB - 10,240 MB (10 GB) |
| **vCPUs** | Scales with memory (1 vCPU at 1769 MB) |
| **Deployment package** | 50 MB (zip), 250 MB (unzipped) |
| **Container image** | Up to 10 GB |
| **Environment variables** | 4 KB total |
| **Concurrency** | 1000 per region (soft limit, can increase) |
| **Ephemeral storage (/tmp)** | 512 MB - 10,240 MB |
| **Layers** | Up to 5 per function |

### Lambda Execution Model
```
Event Source → Lambda Function → Response/Side Effects
     │              │
     │              ├── Execution Environment (container)
     │              ├── /tmp directory (ephemeral, persists across warm invocations)
     │              └── Environment Variables
     │
     └── Types: Synchronous, Asynchronous, Event Source Mapping
```

### Invocation Types

| Type | Behavior | Retry | Use Case |
|------|----------|-------|----------|
| **Synchronous** | Caller waits for response | Caller retries | API Gateway, ALB, CloudFront |
| **Asynchronous** | Event queued, caller doesn't wait | 2 retries (built-in) | S3, SNS, EventBridge, CloudWatch |
| **Event Source Mapping** | Lambda polls source | Depends on source | SQS, Kinesis, DynamoDB Streams |

### Event Source Mapping (Polling)
- Lambda polls: SQS, Kinesis, DynamoDB Streams, Amazon MQ, Kafka
- **SQS**: Batch size 1-10, lambda deletes from queue after success
- **Kinesis/DynamoDB**: Reads batches from shard, retries on failure (blocks shard)
- On failure: Configure **DLQ** (SQS) or **Destination** (success/failure)

---

### Lambda Networking

**Default:**
- Runs in AWS-managed VPC (has internet access)
- Cannot access resources in YOUR VPC

**VPC-attached Lambda:**
- Deploy Lambda in your VPC subnets
- Gets ENI in your private subnet
- ❌ No internet access by default (even if function needs it)
- Need: NAT Gateway in public subnet for internet
- Need: VPC Endpoint for AWS services (S3, DynamoDB)
- Uses: **Hyperplane ENI** (faster cold start than old model)

> **Exam Tip**: "Lambda can't access internet after VPC config" = Add NAT Gateway. "Lambda access RDS in private subnet" = Deploy Lambda in VPC.

---

### Lambda Concurrency

**Types:**
| Type | Description |
|------|-------------|
| **Unreserved** | Shared pool (default), first come first served |
| **Reserved** | Guaranteed concurrency for your function (taken from pool) |
| **Provisioned** | Pre-initialized environments (no cold start) |

**Throttling:**
- Exceeds concurrency limit → throttled (429 error)
- Async: Auto-retries. Sync: Returns 429 to caller.
- Set Reserved concurrency = 0 → effectively disables function

**Cold Start:**
- First invocation: Initialize runtime + your code
- Subsequent (warm): Reuse environment (faster)
- Fix: Provisioned Concurrency (always warm)

---

### Lambda Destinations & DLQ

| Feature | DLQ | Destinations |
|---------|-----|--------------|
| Scope | Failures only | Success AND Failure |
| Targets | SQS, SNS | SQS, SNS, Lambda, EventBridge |
| Preference | Legacy | **Recommended** |

---

### Lambda Layers
- Share libraries, custom runtimes, dependencies across functions
- Up to 5 layers per function
- Reduces deployment package size
- Version controlled

### Lambda Container Images
- Package Lambda as Docker container (up to 10 GB)
- Must implement Lambda Runtime Interface
- Use AWS base images or bring your own (with Runtime Interface Client)
- Use Case: Large dependencies, existing Docker workflows

---

### Lambda Common Triggers

| Trigger | Invocation Type | Use Case |
|---------|----------------|----------|
| API Gateway | Synchronous | REST/HTTP APIs |
| ALB | Synchronous | HTTP requests behind LB |
| S3 | Asynchronous | Process uploaded files |
| DynamoDB Streams | Event Source Mapping | React to DB changes |
| SQS | Event Source Mapping | Process queue messages |
| Kinesis | Event Source Mapping | Process stream data |
| SNS | Asynchronous | Fan-out processing |
| EventBridge | Asynchronous | Scheduled tasks, event reactions |
| CloudWatch Logs | Asynchronous | Log processing |
| CloudFront (Lambda@Edge) | Synchronous | Edge compute |
| Cognito | Synchronous | Auth triggers |
| IoT | Asynchronous | IoT event processing |

---

### Lambda Best Practices
1. **Minimize deployment package** (only include needed dependencies)
2. **Reuse connections** (initialize SDK clients outside handler)
3. **Use environment variables** for configuration
4. **Use Layers** for shared dependencies
5. **Set appropriate timeout** (don't use max 15 min if 10 sec is enough)
6. **Set appropriate memory** (more memory = more CPU = faster, may cost less)
7. **Use /tmp** for temporary file processing (512 MB - 10 GB)
8. **Use Provisioned Concurrency** for latency-sensitive workloads

---

## Step Functions

### Key Concepts
- **Serverless orchestration** service
- Coordinate multiple AWS services into workflows
- Visual workflow designer (state machine)
- **JSON-based** (Amazon States Language)
- Max execution: 1 year (Standard) or 5 min (Express)

### Workflow Types

| Type | Duration | Execution | Pricing | Use Case |
|------|----------|-----------|---------|----------|
| **Standard** | Up to 1 year | Exactly-once | Per state transition | Long-running, auditable |
| **Express** | Up to 5 min | At-least-once | Per execution + duration | High-volume, short (IoT, streaming) |

### State Types
| State | Purpose |
|-------|---------|
| **Task** | Execute work (Lambda, ECS, DynamoDB, SNS, SQS, etc.) |
| **Choice** | Branching logic (if/else) |
| **Parallel** | Execute branches in parallel |
| **Wait** | Delay for X time |
| **Map** | Iterate over array (like forEach) |
| **Pass** | Pass input to output (transform data) |
| **Succeed/Fail** | End execution |

### Key Features
- **Error handling**: Retry and Catch built-in
- **Input/Output processing**: Filter and transform data between states
- **Service integrations**: Direct integration with 200+ AWS services
- **Human approval**: Wait for callback (task token pattern)
- **Nested workflows**: Call one state machine from another
- **Express Workflows**: High-volume event processing

### Common Patterns
```
Pattern 1: Sequential processing
Start → Task A → Task B → Task C → End

Pattern 2: Parallel processing  
Start → Parallel → [Branch A] → End
                 → [Branch B]

Pattern 3: Error handling
Start → Task → Catch(Error) → Fallback Task → End
              → Retry(3 times, backoff)

Pattern 4: Human approval
Start → Submit Request → Wait for Callback → Approve/Reject → End
```

> **Exam Tips**:
> - "Orchestrate multiple Lambda functions" = Step Functions
> - "Visual workflow with branching logic" = Step Functions
> - "Long-running workflow (hours/days)" = Step Functions Standard
> - "Coordinate microservices" = Step Functions
> - "Simple event processing" = Lambda alone
> - "Retry with exponential backoff" = Step Functions (built-in)

---

## Serverless Architecture Patterns

### Pattern 1: REST API
```
Client → API Gateway → Lambda → DynamoDB
                          ↓
                    CloudWatch Logs
```

### Pattern 2: Event Processing
```
S3 Upload → S3 Event → Lambda → Process → Store in DynamoDB
                                    ↓
                              SNS Notification
```

### Pattern 3: Real-time Stream Processing
```
IoT Devices → Kinesis Data Streams → Lambda → DynamoDB
                                         ↓
                                    Kinesis Firehose → S3 (archive)
```

### Pattern 4: Scheduled Tasks
```
EventBridge (cron) → Lambda → RDS (cleanup)
                         → S3 (report generation)
                         → SNS (alert)
```

### Pattern 5: Web Application
```
CloudFront → S3 (static frontend)
    ↓
API Gateway → Lambda → Aurora Serverless
                  ↓
            Cognito (auth)
```

---

## Serverless Services Summary

| Service | What It Does | When to Use |
|---------|-------------|-------------|
| Lambda | Run code | Event-driven compute |
| API Gateway | REST/HTTP/WebSocket APIs | Frontend for Lambda |
| DynamoDB | NoSQL database | Serverless DB |
| S3 | Object storage | Static hosting, data lake |
| Step Functions | Workflow orchestration | Multi-step processes |
| EventBridge | Event bus | Event routing |
| SQS/SNS | Messaging | Decoupling |
| Fargate | Containers | Long-running containers |
| Aurora Serverless | SQL database | Variable DB workloads |
| AppSync | GraphQL API | GraphQL applications |
| Cognito | Authentication | User sign-up/sign-in |
