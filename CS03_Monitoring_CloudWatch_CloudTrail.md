# CS03: Monitoring - CloudWatch, CloudTrail, EventBridge
### AWS SAA-C03 Cheat Sheet

---

## CloudWatch (Monitoring & Observability)

### Key Concepts
- **Monitoring service** for AWS resources and applications
- Collects metrics, logs, events, and alarms
- Think: "How is my resource PERFORMING?"

### CloudWatch Metrics
- **Default metrics** (free, every 5 min): CPU, Network, Disk I/O, Status Checks
- **Detailed monitoring** (paid, every 1 min): Enabled per instance
- **Custom metrics**: Push your own data (e.g., memory usage, application metrics)
  - Use `PutMetricData` API
  - Resolution: Standard (60 sec) or High Resolution (1 sec)
- **Important**: RAM/Memory is NOT a default metric → must use custom metric or CloudWatch Agent

### CloudWatch Alarms
- Watch a single metric and trigger actions
- States: **OK → INSUFFICIENT_DATA → ALARM**
- Actions on ALARM:
  - **EC2**: Stop, Terminate, Reboot, Recover
  - **Auto Scaling**: Scale out/in
  - **SNS**: Send notification
- **Composite Alarms**: Combine multiple alarms with AND/OR logic
- **Period**: Length of time to evaluate (min 10 sec for high-res, 60 sec standard)

### CloudWatch Logs
- Centralized log collection and analysis
- **Log Groups**: Collection of log streams (typically one per application)
- **Log Streams**: Sequence of events from same source
- **Key Integrations**:
  - EC2 (via CloudWatch Agent)
  - Lambda (automatic)
  - ECS, EKS, Fargate
  - Route 53 DNS queries
  - API Gateway
  - CloudTrail
- **Log Insights**: Query logs with purpose-built query language
- **Metric Filters**: Create metrics from log patterns (e.g., count ERROR occurrences)
- **Subscription Filters**: Real-time feed to:
  - Lambda, Kinesis Data Streams, Kinesis Data Firehose
  - Cross-account log sharing

### CloudWatch Logs Export
- **S3 Export**: Batch export (up to 12 hours delay) - use `CreateExportTask`
- **Real-time**: Use Subscription Filter → Kinesis Data Firehose → S3
- **Cross-account**: Subscription Filter → Kinesis in other account

### CloudWatch Agent
- Must install on EC2/on-premises to collect:
  - **Memory utilization** (not available by default!)
  - **Disk space** (detailed)
  - **Custom application logs**
  - **System-level metrics**
- **Unified Agent**: Newer, collects both metrics + logs (prefer this)

### CloudWatch Dashboards
- Global (can include graphs from multiple regions)
- Custom visualization of metrics
- Cross-account dashboards possible

### CloudWatch Synthetics (Canaries)
- Configurable scripts that run on schedule
- Monitor APIs, URLs, website flows
- Check availability and latency
- Can take screenshots, detect visual issues

> **Exam Tips**:
> - "Monitor memory/disk" = CloudWatch Agent (custom metric)
> - "Trigger auto-scaling based on metric" = CloudWatch Alarm
> - "Analyze log patterns" = CloudWatch Logs Insights
> - "Real-time log processing" = Subscription Filter
> - "Monitor API endpoint availability" = CloudWatch Synthetics

---

## CloudTrail (Auditing & Governance)

### Key Concepts
- **Audit trail** for ALL API calls in your AWS account
- Think: "WHO did WHAT and WHEN?"
- Enabled by **default** (90 days of management events)
- Records: Console actions, CLI calls, SDK calls, API calls

### Event Types

| Type | What It Records | Default | Example |
|------|----------------|---------|---------|
| **Management Events** | Control plane operations | ✅ Free (90 days) | CreateBucket, TerminateInstance |
| **Data Events** | Data plane operations | ❌ Extra cost | GetObject, PutObject, Lambda Invoke |
| **Insights Events** | Unusual activity patterns | ❌ Extra cost | Unusual API call rate |

### Key Features
- **Trail**: Configure delivery to S3 bucket (for long-term storage beyond 90 days)
- **Multi-region trail**: Single trail captures events from ALL regions
- **Organization trail**: Capture all events across all accounts in Organization
- **Log file integrity validation**: Detect if logs were tampered with (SHA-256 hash)
- **Integration**: CloudTrail → S3 → Athena (for SQL analysis of logs)
- **CloudTrail Lake**: Managed data lake for CloudTrail events (SQL queries without Athena setup)

### CloudTrail vs CloudWatch

| Aspect | CloudTrail | CloudWatch |
|--------|-----------|------------|
| Purpose | WHO did what (audit) | HOW resources perform (monitoring) |
| Data | API call records | Metrics, logs, alarms |
| Question answered | "Who deleted the bucket?" | "Is CPU > 80%?" |
| Default retention | 90 days (Management Events) | Depends on metric type |
| Storage | S3 (long-term) | CloudWatch (built-in) |

> **Exam Tips**:
> - "Who terminated the instance?" = CloudTrail
> - "Track all API calls for compliance" = CloudTrail
> - "Detect unusual API activity" = CloudTrail Insights
> - "Long-term audit log storage" = CloudTrail → S3
> - "Query audit logs with SQL" = CloudTrail → S3 → Athena (or CloudTrail Lake)

---

## Amazon EventBridge (Events)

### Key Concepts
- **Serverless event bus** for building event-driven architectures
- Formerly "CloudWatch Events" (superset with more features)
- Routes events from sources to targets based on rules

### Event Sources
- **AWS Services**: EC2 state change, CodePipeline, S3, GuardDuty findings, etc.
- **Custom Applications**: Your apps send events via API
- **SaaS Partners**: Zendesk, Datadog, Auth0, etc.
- **Scheduled**: Cron/rate expressions

### Targets (30+ supported)
- Lambda, Step Functions, SQS, SNS, Kinesis
- ECS tasks, CodePipeline, CodeBuild
- API Gateway, Redshift, S3
- Cross-account, cross-region event buses

### Key Features
- **Schema Registry**: Discover event structure, generate code bindings
- **Archive & Replay**: Store events and replay them later
- **Content-based filtering**: Filter on event content (not just source)
- **Multiple targets per rule** (up to 5)
- **Dead Letter Queue (DLQ)**: Handle failed deliveries

### Common Patterns
```
GuardDuty Finding → EventBridge Rule → SNS → Email Alert
EC2 Instance State Change → EventBridge → Lambda → Auto-remediate
Scheduled (cron) → EventBridge → Lambda → Batch Job
CloudTrail API Call → EventBridge → Step Function → Workflow
```

> **Exam Tips**:
> - "React to AWS events automatically" = EventBridge
> - "Schedule a Lambda function" = EventBridge (cron)
> - "Fan-out events to multiple targets" = EventBridge (or SNS)
> - "Trigger on GuardDuty finding" = EventBridge rule

---

## AWS X-Ray

### Key Concepts
- **Distributed tracing** for applications
- Visualize request flow through microservices
- Identify performance bottlenecks and errors
- Works with: EC2, ECS, Lambda, Elastic Beanstalk, API Gateway

### Key Features
- Service map visualization
- Trace request path across services
- Identify which service is causing latency
- Supports annotations and metadata for filtering

> **Exam Tip**: "Debug distributed microservices performance" = X-Ray. "Monitor resource metrics" = CloudWatch.

---

## Monitoring Decision Tree

```
Need to know WHO did something?          → CloudTrail
Need to know HOW resource is performing? → CloudWatch
Need to REACT to events automatically?   → EventBridge
Need to DEBUG microservices requests?    → X-Ray
Need to find COMPLIANCE violations?      → AWS Config
Need to detect THREATS?                  → GuardDuty
```
