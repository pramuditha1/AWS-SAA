# CS18: Messaging - SQS, SNS, Kinesis, Amazon MQ
### AWS SAA-C03 Cheat Sheet

---

## Decoupling Overview
```
Tight Coupling (bad):         Loose Coupling (good):
App A → App B (direct)        App A → [Queue/Topic] → App B
If B fails, A fails           If B fails, messages wait in queue
```

---

## SQS (Simple Queue Service)

### Key Concepts
- **Fully managed message queue** (oldest AWS service!)
- **Pull-based**: Consumers poll for messages, process them, then **delete** them
- Decouple producers from consumers, buffer traffic spikes
- Unlimited messages in a queue. Regional, stored across multiple AZs.
- Each message goes to **one** consumer (competing consumers). Copies for many consumers → SNS fan-out.

### SQS Standard vs FIFO

| Feature | Standard | FIFO |
|---------|----------|------|
| Throughput | Nearly unlimited | **300 API calls/s per action** (Send / Receive / Delete). Batch of 10 → **3,000 msg/s** |
| Ordering | Best-effort (no guarantee) | **Strict order per message group ID** |
| Delivery | At-least-once (possible duplicates) | **Exactly-once processing** (5-min dedup window) |
| Name | Any name | Must end in `.fifo` |
| DLQ | Standard DLQ | Must be a FIFO DLQ |
| Use Case | High throughput, order doesn't matter | Order matters (banking, payments, inventory) |

- **No in-place conversion** between Standard and FIFO. Create a new queue and switch producers/consumers.

### FIFO Deep Dive

**Message group ID: what "in order" actually means**
- Required on every FIFO message
- Order is guaranteed **within a group**, not across groups
- Different groups are processed **in parallel**. Use e.g. `accountId` as the group ID.
- One group ID for everything = single-threaded bottleneck

**Deduplication: 5-minute window**
- A retried send with the same deduplication ID within 5 min is accepted but **not added twice**
- Two options: send an explicit `MessageDeduplicationId`, or enable **content-based deduplication** (SHA-256 hash of the body)

**Throughput math (exam favourite)**
```
FIFO limit is on API CALLS, not messages:
  300 calls/s per action (SendMessage, ReceiveMessage, DeleteMessage)
  messages/s = 300 × messages per call (batch, max 10)

Batch size needed = peak msg/s ÷ 300, rounded up

Example: peak 1,000 msg/s, must be in order
  no batching  → 300 × 1  =   300  ❌
  batch of 2   → 300 × 2  =   600  ❌
  batch of 4   → 300 × 4  = 1,200  ✅  smallest batch that works
  batch of 10  → 300 × 10 = 3,000  ✅  FIFO maximum (without high-throughput mode)
```
- Batch APIs: `SendMessageBatch`, `DeleteMessageBatch`, `ReceiveMessage` with up to 10 messages
- **High-throughput FIFO mode** (opt-in): partitions by message group ID. Up to 70,000 calls/s in the largest Regions (700,000 msg/s with batching). Exam questions usually still use **300 / 3,000**.

### Message Lifecycle
```
Producer → Send Message → [SQS Queue] → Consumer Polls → Process → Delete Message
                                              ↓
                            Visibility Timeout (message hidden from others)
                                              ↓
                            If not deleted: message reappears (retry)
```

### Key Settings

| Setting | Default | Range | Purpose |
|---------|---------|-------|---------|
| **Visibility Timeout** | 30 sec | 0 sec - 12 hours | Hide a received message while a consumer works on it |
| **Message Retention** | 4 days | 1 min - 14 days | How long an undeleted message stays |
| **Max Message Size** | 1 MiB | 1 byte - 1 MiB | Was **256 KB** until 2025 (most exam questions still say 256 KB) |
| **Delivery Delay** (delay queue) | 0 | 0 - 15 min | Hide **new** messages before first delivery |
| **Receive Wait Time** (long polling) | 0 (short poll) | 1 - 20 sec | How long `ReceiveMessage` waits for messages |
| **Batch** | - | Up to 10 messages per call | Fewer API calls → lower cost, higher FIFO throughput |

**Visibility timeout tuning:**
- Too short → message reappears while still being processed → **processed twice**
- Too long → slow retry after a consumer crash
- A consumer that needs more time calls `ChangeMessageVisibility`

**Delay queue vs message timer:**
- Delay queue: queue-level delay for every new message (max 15 min)
- Message timer: per-message `DelaySeconds` (Standard queues only)

### Long Polling vs Short Polling
- **Short Polling** (default): Returns immediately (even if empty) — more empty responses, costs more
- **Long Polling**: Waits up to 20 sec for messages — **preferred** (fewer API calls, lower cost, lower latency)
- Enable on the queue (`ReceiveMessageWaitTimeSeconds`) or per call (`WaitTimeSeconds`)

### Dead Letter Queue (DLQ)
- A message received **maxReceiveCount** times without being deleted → moved to the DLQ
- DLQ must be same type (Standard DLQ for Standard queue, FIFO DLQ for FIFO)
- Standard queues: set DLQ retention **longer** than the source (the message keeps its original enqueue time)
- **DLQ Redrive**: Move messages back from DLQ to source queue after fixing the bug
- Alarm on DLQ depth to catch poison messages

### Large Messages
- Over the size limit → **SQS Extended Client Library**: body stored in S3, pointer sent on the queue (payload up to 2 GB)

### Security
- In transit: HTTPS endpoints
- At rest: **SSE-SQS** (SQS-managed keys, on by default for new queues) or **SSE-KMS** (your KMS key, key use audited in CloudTrail)
- Access: IAM policies + **SQS queue policy** (resource-based) for cross-account access, or to let an SNS topic / S3 bucket send messages
- Private access from a VPC: **interface VPC endpoint** (PrivateLink), so no NAT or internet path is needed

### SQS + Lambda (Event Source Mapping)
- Lambda polls the queue for you and deletes messages when the batch succeeds
- Batch size: Standard up to **10,000** (needs a batch window ≥ 1 sec), FIFO up to **10**
- Set queue **visibility timeout ≥ 6 × function timeout**
- On error the **whole batch** returns to the queue, unless you enable **partial batch response** (`ReportBatchItemFailures`)
- Put the **DLQ on the SQS queue** (maxReceiveCount ≥ 5), not on the Lambda function
- **Maximum concurrency** on the event source caps parallel invocations (protects a downstream database)

### SQS + Auto Scaling Pattern
```
SQS Queue (messages pile up)
    ↓
CloudWatch metric: ApproximateNumberOfMessagesVisible
    ↓  (better: backlog per instance = visible messages ÷ running instances)
Target tracking policy on the Auto Scaling Group → add / remove consumer instances
```

> **Exam Tips**:
> - "Decouple microservices" = SQS
> - "Handle traffic spikes without losing data" = SQS (buffer)
> - "Process messages in order" = SQS FIFO (+ message group ID)
> - "Ordered, at N messages/s" = FIFO + batching. Batch size = N ÷ 300, rounded up (1,000 msg/s → batch of 4)
> - "No duplicate messages" = FIFO dedup (dedup ID or content-based). On Standard: make consumers idempotent.
> - "Messages processed multiple times" = Visibility timeout shorter than processing time → increase it
> - "Scale consumers based on load" = Backlog per instance + target tracking
> - "Message too large" = SQS Extended Client Library (store in S3)
> - "Too many empty responses / high SQS cost" = Long polling (up to 20 sec)
> - "Delay all new messages" = Delay queue. "Delay one message" = Message timer
> - "Change Standard to FIFO" = Create a new FIFO queue (no conversion)

---

## SNS (Simple Notification Service)

### Key Concepts
- **Pub/Sub** (Publish/Subscribe) messaging
- **Push-based**: SNS pushes to subscribers
- One message → many receivers (fan-out)
- Up to **12.5 million subscribers** per topic
- Up to **100,000 topics**

### Components
```
Publisher → SNS Topic → Subscribers (multiple)
                 ├── SQS Queue
                 ├── Lambda Function
                 ├── HTTP/HTTPS Endpoint
                 ├── Email / Email-JSON
                 ├── SMS
                 ├── Kinesis Data Firehose
                 └── Platform (Mobile push)
```

### SNS Features
| Feature | Description |
|---------|-------------|
| **Message Filtering** | JSON policy to filter which messages reach which subscriber |
| **Fan-out** | One message to many SQS queues via topic |
| **FIFO Topics** | Ordered delivery (pairs with SQS FIFO) |
| **Message Archiving** | Standard: archive via Kinesis Data Firehose. FIFO: native archive + replay |
| **Encryption** | KMS encryption at rest |
| **Access Policies** | Resource-based policy for cross-account |
| **Subscription DLQ** | SQS queue per subscription for messages SNS gives up on (redrive policy) |

### SNS Scaling & Delivery (where messages actually get lost)
- **Fully managed, no servers.** SNS scales by itself. "Provision more SNS servers" is always a wrong answer.
- **Publish quota**: soft, per account per Region (us-east-1: 30,000 msg/s; most others lower). If you hit it, the **publisher** gets a throttling error on `Publish`. It's not a silent loss.
- **Delivery to Lambda = asynchronous invoke.** SNS hands the event to Lambda and moves on. The **subscriber is usually the bottleneck**, not SNS.
- **Delivery retries** (delivery policy):

| Endpoint type | Examples | Retries |
|---------------|----------|---------|
| AWS-managed | Lambda, SQS, Firehose | 100,015 attempts over 23 days |
| Customer-managed | HTTP/S, email, SMS, mobile push | 50 attempts over 6 hours (only HTTP/S policy is customizable) |

- When retries run out → message **discarded** unless the subscription has a **DLQ** (SQS).

### SNS → Lambda at Scale (classic exam trap)
```
Publisher → SNS Topic → Lambda (async invoke)
                           │
                           ├── Needs concurrency = RPS × avg duration (s)
                           │     100 rps × 0.5 s =    50  ✅
                           │   5,000 rps × 0.5 s = 2,500  ❌ > 1,000 default
                           │
                           └── Over the limit → 429 throttle → Lambda async queue
                               retries up to 6 h → then DROPPED (no DLQ/destination)
                               → "notifications not delivered"
```
- **Fix:** raise the Lambda **account concurrency quota** (Service Quotas / AWS Support). Default is 1,000 per Region.
- **Don't lose events:** add a Lambda **on-failure destination** or DLQ. Or put **SQS between SNS and Lambda** (SNS → SQS → Lambda) so the queue buffers the spike. SQS doesn't add throughput; it only stops messages from being lost.
- **Protect the function from noisy neighbours:** set **reserved concurrency** on it.

> **Exam Tip**: "SNS + Lambda, works at low traffic, messages lost at peak" = **Lambda concurrency quota**, not SNS. SNS is built to scale. Lambda's 1,000/Region default is the first wall you hit.
> **Discriminator**: if SNS itself were throttling, the *publisher* would get errors. "Published fine, but users never receive it" points at the **subscriber side** (Lambda).

### SNS + SQS Fan-Out Pattern
```
Event → SNS Topic ──→ SQS Queue A → Service A (processing)
                  ├──→ SQS Queue B → Service B (analytics)
                  └──→ SQS Queue C → Service C (archiving)

Benefits: Fully decoupled, each consumer processes independently
```

### SNS vs SQS

| Feature | SNS | SQS |
|---------|-----|-----|
| Model | Pub/Sub (push) | Queue (pull) |
| Consumers | Multiple subscribers | Single consumer group |
| Persistence | No queue. Retries, then dropped unless subscription DLQ | Yes (messages stored, 1 min–14 days) |
| Use Case | Fan-out, notifications | Decouple, buffer, process |

> **Exam Tip**: "Send one event to multiple services" = SNS (fan-out). "Decouple one producer and one consumer" = SQS.

---

## Kinesis (Real-Time Streaming)

### Kinesis Services

| Service | Purpose | Key Point |
|---------|---------|-----------|
| **Data Streams** | Ingest & process real-time data | Custom consumers, you manage |
| **Data Firehose** | Deliver streaming data to destinations | Fully managed, near real-time |
| **Data Analytics** | SQL/Flink on streaming data | Real-time analytics |
| **Video Streams** | Stream video for processing | ML, analytics on video |

### Kinesis Data Streams

**Architecture:**
```
Producers → [Shard 1] [Shard 2] [Shard 3] → Consumers
             (ordered within each shard)

Shard capacity:
- Write: 1 MB/s or 1000 records/s per shard
- Read: 2 MB/s per shard (shared) or 2 MB/s per consumer (enhanced)
```

**Key Features:**
| Feature | Details |
|---------|---------|
| **Retention** | 24 hours (default) → up to 365 days |
| **Ordering** | Within a shard (use partition key) |
| **Replay** | ✅ Can re-read data |
| **Immutable** | Data can't be deleted (expires after retention) |
| **Scaling** | Add/remove shards (shard splitting/merging) |
| **Consumers** | Lambda, KCL apps, Kinesis Analytics, Firehose |

**Capacity Modes:**
- **Provisioned**: Choose number of shards, pay per shard/hour
- **On-Demand**: Auto-scales, pay per stream/hour + per GB

### Kinesis Data Firehose

**Key Features:**
- **Fully managed** (no shards to manage)
- **Near real-time**: Buffer (60 sec min or 1 MB min)
- **Destinations**: S3, Redshift (via S3), OpenSearch, Splunk, HTTP, 3rd party
- **Auto-scaling** (no capacity management)
- **Transform data**: Lambda function can transform before delivery
- **No replay** (data consumed and gone)
- **Pay per data** processed

### Kinesis Data Streams vs Firehose

| Feature | Data Streams | Firehose |
|---------|-------------|----------|
| Latency | Real-time (~200ms) | Near real-time (~60s) |
| Scaling | Manual (shards) or On-Demand | Automatic |
| Consumers | Custom (Lambda, KCL, etc.) | Fixed destinations |
| Data replay | ✅ Yes | ❌ No |
| Management | You manage consumers | Fully managed |
| Storage | Temporary (1-365 days) | No storage (delivers) |
| Use Case | Custom real-time processing | ETL/delivery to S3/Redshift |

> **Exam Tips**:
> - "Real-time data ingestion + custom processing" = Kinesis Data Streams
> - "Deliver streaming data to S3" = Kinesis Data Firehose
> - "Replay data" = Kinesis Data Streams (not Firehose)
> - "Real-time analytics with SQL" = Kinesis Data Analytics
> - "Ordering guaranteed" = Kinesis (within shard, using partition key)

---

## Kinesis vs SQS Ordering

| Feature | Kinesis | SQS FIFO |
|---------|---------|----------|
| Ordering | Per shard (partition key) | Per message group ID |
| Consumers | Multiple (fan-out) | One consumer group |
| Throughput | MB/s per shard | 300 API calls/s (×10 with batching = 3,000 msg/s) |
| Replay | ✅ | ❌ |
| Use Case | Real-time analytics, many consumers | Decoupling with order guarantee |

---

## Amazon MQ

### Key Concepts
- **Managed message broker** for Apache ActiveMQ and RabbitMQ
- For companies migrating from on-premises with existing protocols
- Supports: **AMQP, MQTT, OpenWire, STOMP, WSS**
- Has both **queue** and **topic** features (like SQS + SNS combined)

### When to Use Amazon MQ vs SQS/SNS

| Use Case | Choose |
|----------|--------|
| New cloud-native application | SQS + SNS (scalable, serverless) |
| Migrating from on-prem with ActiveMQ/RabbitMQ | Amazon MQ |
| Need MQTT, AMQP, STOMP protocols | Amazon MQ |
| Need serverless, unlimited scaling | SQS + SNS |
| Existing JMS applications | Amazon MQ |

### Amazon MQ HA
- **Active/Standby** deployment across 2 AZs
- Uses **EFS** for shared storage (durable messages)
- Automatic failover to standby

> **Exam Tip**: "Migrate on-premises ActiveMQ to AWS" = Amazon MQ. "New serverless messaging" = SQS/SNS.

---

## Messaging Decision Matrix

| Scenario | Solution |
|----------|----------|
| Decouple services (1 producer, 1 consumer) | SQS |
| Fan-out one event to many consumers | SNS → SQS (fan-out) |
| Real-time streaming (100s of consumers) | Kinesis Data Streams |
| Deliver stream to S3/Redshift | Kinesis Data Firehose |
| FIFO ordering + exactly-once | SQS FIFO |
| Ordered + more than 300 msg/s | SQS FIFO + batching (up to 10/call → 3,000 msg/s) |
| Migrate from ActiveMQ/RabbitMQ | Amazon MQ |
| Notifications (email, SMS) | SNS |
| SNS → Lambda drops messages at peak | Raise Lambda concurrency quota (+ DLQ / SNS → SQS → Lambda) |
| Event-driven architecture | EventBridge |
| Buffer during traffic spikes | SQS |
