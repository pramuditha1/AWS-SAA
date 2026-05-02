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
- **Pull-based**: Consumers poll for messages
- Decouple producers from consumers
- Unlimited throughput, unlimited messages in queue

### SQS Standard vs FIFO

| Feature | Standard | FIFO |
|---------|----------|------|
| Throughput | Unlimited | 300 msg/s (batch: 3000) |
| Ordering | Best-effort (no guarantee) | **Strict order guaranteed** |
| Delivery | At-least-once (possible duplicates) | **Exactly-once** |
| Deduplication | ❌ | ✅ (5 min window) |
| Name | Any name | Must end in `.fifo` |
| Use Case | High throughput, order doesn't matter | Order matters (financial, inventory) |

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
| **Visibility Timeout** | 30 sec | 0 - 12 hours | Time message is hidden after being read |
| **Message Retention** | 4 days | 1 min - 14 days | How long message stays in queue |
| **Max Message Size** | - | Up to 256 KB | Use Extended Client Library for larger |
| **Delivery Delay** | 0 | 0 - 15 min | Delay before message becomes visible |
| **Long Polling Wait** | 0 | 1 - 20 sec | Wait time for ReceiveMessage call |
| **Receive Message Wait** | 0 (short poll) | Up to 20 sec (long poll) | Reduces empty responses |

### Long Polling vs Short Polling
- **Short Polling** (default): Returns immediately (even if empty) — costs more
- **Long Polling**: Waits up to 20 sec for messages — **preferred** (reduces API calls, saves cost)

### Dead Letter Queue (DLQ)
- Messages that fail processing X times → sent to DLQ
- **MaxReceiveCount**: How many retries before DLQ
- Useful for debugging failed messages
- DLQ must be same type (Standard DLQ for Standard queue, FIFO DLQ for FIFO)
- **DLQ Redrive**: Move messages back from DLQ to source queue for reprocessing

### SQS + Auto Scaling Pattern
```
SQS Queue (messages pile up)
    ↓
CloudWatch Alarm: ApproximateNumberOfMessages > threshold
    ↓
Auto Scaling Group: Scale out (add more consumer instances)
```

> **Exam Tips**:
> - "Decouple microservices" = SQS
> - "Handle traffic spikes without losing data" = SQS (buffer)
> - "Process messages in order" = SQS FIFO
> - "Messages processed multiple times" = Increase Visibility Timeout
> - "Scale consumers based on load" = SQS queue depth + Auto Scaling
> - "Message too large" = SQS Extended Client Library (store in S3)

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
| **Message Archiving** | Store messages via Kinesis Data Firehose |
| **Encryption** | KMS encryption at rest |
| **Access Policies** | Resource-based policy for cross-account |

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
| Persistence | No (delivered or lost) | Yes (messages stored) |
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
| Throughput | MB/s per shard | 300 msg/s (3000 batch) |
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
| Migrate from ActiveMQ/RabbitMQ | Amazon MQ |
| Notifications (email, SMS) | SNS |
| Event-driven architecture | EventBridge |
| Buffer during traffic spikes | SQS |
