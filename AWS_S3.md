# AWS S3 (Simple Storage Service) Cheat Sheet
### For AWS Certified Solutions Architect – Associate Exam (SAA-C03)

---

## Key Concepts
- **Amazon S3**: Scalable, serverless object storage designed for industry-leading durability and availability.
  - **Durability**: 11 9's (99.999999999%) — replicates data across a minimum of 3 Availability Zones.
  - **Availability**: 99.99% for S3 Standard.
  - **Max Object Size**: 5 TB. Objects > 5 GB **must** use Multipart Upload.
  - **Namespace**: Bucket names are **globally unique** but buckets are **region-scoped**.
- **Consistency Model**: S3 provides **strong read-after-write consistency** for all operations (PUTs, DELETEs) — no eventual consistency lag (updated Dec 2020).

> **Exam Tip!** Questions still test whether you know S3 now has strong consistency. No need for workarounds like delays or re-reads.

---

## S3 Features

### **1. S3 Versioning**
- Protects data from accidental **deletions/overwrites**.
  - **Key Points**:
    - Enabled at the **bucket level** (once enabled, can only be *suspended*, never deleted).
    - Each version gets a unique **Version ID**.
    - A **Delete Marker** is added on deletion (object not physically removed).
    - **MFA Delete**: Requires MFA to permanently delete versions or change versioning state. Must be enabled by the **root account**.

---

### **2. S3 Replication**
Replication requires **versioning enabled** on both source and destination buckets.

| Type | Description |
|---|---|
| **CRR** (Cross-Region Replication) | Replicates objects to a bucket in a **different region**. Use case: compliance, lower-latency access, DR. |
| **SRR** (Same-Region Replication) | Replicates objects within the **same region**. Use case: log aggregation, live replication between production and test. |

- **Key Rules**:
  - Replication is **not retroactive** — only new objects after enabling are replicated.
  - Delete markers can optionally be replicated (not by default).
  - Permanent version deletions are **not** replicated (to prevent malicious deletes propagating).
  - Replication requires an **IAM role** with permissions to read source and write to destination.

> **Exam Tip!** CRR is the go-to answer for cross-region disaster recovery or global performance. SRR for same-region log aggregation.

---

### **3. Retention and Data Lifecycle**
Lifecycle Policies automate storage class transitions and expiration.

- **Transition Actions**: Move objects to a cheaper class after N days.
  - Example: S3 Standard → S3 Standard-IA after 30 days → S3 Glacier Flexible Retrieval after 90 days.
- **Expiration Actions**: Permanently delete objects (or versions) after N days.
  - Use case: Automatically clean up old log files.
- **Minimum days before transition**:
  - Standard → Standard-IA or One Zone-IA: minimum **30 days**.
  - Standard-IA → Glacier: minimum **30 days** in IA class.

---

### **4. S3 Object Lock (WORM Protection)**
- Prevents objects from being deleted or overwritten — **Write Once, Read Many (WORM)**.
- **Retention Modes**:
  - **Governance Mode**: Users with special IAM permissions (`s3:BypassGovernanceRetention`) can alter/delete. Good for internal compliance.
  - **Compliance Mode**: **No one** — including root — can delete or alter until retention expires. Strictest level.
- **Legal Hold**: Independent of retention period. Can be applied/removed by users with `s3:PutObjectLegalHold` permission.
- Must enable Object Lock at **bucket creation time**.

> **Exam Tip!** Compliance Mode = regulatory requirement, no exceptions. Governance Mode = internal policy with overrides.

---

### **5. S3 Event Notifications**
Trigger actions automatically when objects are created, deleted, or restored.

- **Destinations**: AWS Lambda, Amazon SQS, Amazon SNS, or **Amazon EventBridge** (for advanced filtering).
- **Triggering Events**: `s3:ObjectCreated`, `s3:ObjectRemoved`, `s3:ObjectRestore`, `s3:Replication` events, etc.
- **EventBridge Integration**: Enables routing to 18+ AWS services with advanced filtering rules.

> **Exam Tip!** If the question asks for an event-driven pipeline triggered by file upload → S3 Event Notification → Lambda is the classic answer.

---

### **6. Multipart Upload**
- Recommended for objects **> 100 MB**, required for objects **> 5 GB**.
- Allows uploading parts in **parallel** → faster uploads.
- Failed parts can be **retried independently**.
- Use **Lifecycle Policy** to automatically abort incomplete multipart uploads (cost management).

---

### **7. S3 Transfer Acceleration**
- Uses **CloudFront edge locations** to accelerate uploads to S3 from distant clients.
- Data routes through the AWS backbone network for faster transfer.
- Compatible with Multipart Upload.
- Separate endpoint: `bucket.s3-accelerate.amazonaws.com`.

> **Exam Tip!** Transfer Acceleration = speed up uploads from users far from the S3 bucket region. CloudFront = speed up downloads/static content delivery.

---

### **8. Pre-signed URLs**
- Generates a **temporary, time-limited URL** to grant access to a private object.
- Used for secure, short-term access without changing bucket policy.
- Signed with the **creator's IAM credentials** — expires after a set duration.
- **Use Case**: Allow a user to download a private file or upload directly to S3 without AWS credentials.

> **Exam Tip!** Pre-signed URLs = temporary delegated access to private S3 objects without making the bucket public.

---

### **9. S3 Select & Glacier Select**
- Retrieve a **subset of data** from an object using **SQL expressions** — without downloading the whole object.
- Reduces data transfer cost and speeds up analytics.
- Supports CSV, JSON, Parquet formats (server-side filtering).
- **Glacier Select**: Same concept applied to archived objects in Glacier.

---

### **10. S3 Object Lambda**
- Attach a **Lambda function** to an S3 GET request to **transform data on-the-fly** before returning it to the caller.
- **Use Cases**: Redact PII, convert data formats, enrich data dynamically.
- No need to store multiple copies of transformed data.

---

### **11. S3 Batch Operations**
- Run operations on **billions of existing objects** in a single job.
- **Supported Actions**: Copy objects, invoke Lambda, restore from Glacier, replace ACLs/tags, apply Object Lock.
- Works with **S3 Inventory** reports to identify target objects.

---

### **12. S3 Access Points**
- Simplify access management for **shared datasets** with many users/applications.
- Each Access Point has its own **DNS name**, **IAM policy**, and optionally a **VPC restriction**.
- Replaces complex bucket policies with per-application policies.

> **Exam Tip!** Large organizations with multiple teams accessing one bucket → S3 Access Points is the scalable solution.

---

### **13. S3 Requester Pays**
- The **requester** (not the bucket owner) pays for the data transfer and request costs.
- Bucket owner still pays for storage.
- Use case: Sharing large public datasets where the owner doesn't want to pay for every download.
- Requires requester to be **authenticated** (anonymous access not allowed).

---

### **14. S3 Storage Lens**
- **Organization-wide** storage analytics dashboard.
- Provides metrics on usage, activity, cost optimization, and security posture across all accounts/regions.
- **Free tier**: 28 default metrics. **Advanced tier**: Additional paid metrics + CloudWatch integration.

---

### **15. S3 Access Analyzer**
- Identifies **unintended public or cross-account access** to S3 buckets.
- Continuously monitors bucket policies and ACLs and generates findings.

---

## S3 Storage Classes

| **Storage Class** | **Best Use Case** | **Retrieval** | **Min Storage Duration** | **Availability** |
|---|---|---|---|---|
| **S3 Standard** | Frequently accessed data | Milliseconds | None | 99.99% |
| **S3 Intelligent-Tiering** | Unknown/unpredictable access | Milliseconds | None | 99.9% |
| **S3 Standard-IA** | Infrequent access, rapid retrieval | Milliseconds | 30 days | 99.9% |
| **S3 One Zone-IA** | Infrequent access, non-critical, re-creatable | Milliseconds | 30 days | 99.5% (1 AZ) |
| **S3 Glacier Instant Retrieval** | Archive with millisecond access (quarterly) | Milliseconds | 90 days | 99.9% |
| **S3 Glacier Flexible Retrieval** | Archive, tolerates minutes-to-hours retrieval | Expedited: 1–5 min / Standard: 3–5 hr / Bulk: 5–12 hr | 90 days | 99.99% |
| **S3 Glacier Deep Archive** | Long-term cold storage, 7–10+ year retention | Standard: ~12 hr / Bulk: ~48 hr | 180 days | 99.99% |

> **Key Exam Points:**
> - **One Zone-IA**: Cheaper than Standard-IA but stored in a **single AZ** — not suitable for irreplaceable data.
> - **Intelligent-Tiering**: Monitors access patterns and automatically moves objects between tiers. No retrieval fee — only monitoring fee per object.
> - **Glacier has 3 separate classes** — know the retrieval speed difference for each.
> - Standard-IA and One Zone-IA charge a **retrieval fee** per GB retrieved.

---

## S3 Performance Optimization

- **Prefix-based Parallelism**: S3 scales to **3,500 PUT/COPY/POST/DELETE** and **5,500 GET/HEAD** requests per second **per prefix**. More prefixes = more throughput.
- **Multipart Upload**: Use for large objects to parallelize and speed up transfers.
- **Byte-Range Fetches**: Parallelize GET requests by fetching specific byte ranges — also useful for partial file retrieval.
- **Transfer Acceleration**: Use for users uploading from geographically distant locations.

---

## S3 Security

### IAM Policies vs Bucket Policies vs ACLs

| Mechanism | Scope | Use Case |
|---|---|---|
| **IAM Policies** | User/Role level | Control what AWS principals can do with S3 |
| **Bucket Policies** | Bucket/object level | Grant cross-account access, enforce encryption, restrict IPs |
| **ACLs** | Object/bucket level | Legacy mechanism; largely replaced by policies (disabled by default on new buckets) |
| **S3 Access Points** | Application level | Simplify large-scale multi-team access to shared datasets |

- **Block Public Access**: Can be set at **account level** or **bucket level**. Overrides bucket policies and ACLs.
- **Pre-signed URLs**: Temporary delegated access to private objects.

---

### Encryption Options

| Type | Key Management | Description |
|---|---|---|
| **SSE-S3** | AWS managed | AES-256. Default encryption. No extra cost. |
| **SSE-KMS** | AWS KMS | Audit trail via CloudTrail. Control key rotation. May incur KMS API costs. |
| **SSE-C** | Customer provided | You supply key per request; AWS does not store it. HTTPS required. |
| **Client-Side Encryption (CSE)** | Customer managed | Encrypt before upload. AWS never sees plaintext. |
| **DSSE-KMS** | AWS KMS | Dual-layer server-side encryption with KMS keys (for strict compliance). |

> **Exam Tip!** SSE-KMS allows **key audit via CloudTrail** — preferred for regulated industries. SSE-S3 is the simplest default option.

---

### VPC Endpoints for S3

- **Gateway Endpoint**: Free, routes S3 traffic through AWS private network without Internet Gateway. Added to **route tables**.
- **Interface Endpoint (AWS PrivateLink)**: Paid, provides a private IP within your VPC for S3 access. Supports on-premises access via VPN/Direct Connect.

> **Exam Tip!** Private EC2 instances accessing S3 without Internet → use **Gateway Endpoint** (free and simpler).

---

### Security Monitoring & Logging

- **Server Access Logging**: Logs all requests made to a bucket in a target logging bucket. Used for security audits and access pattern analysis.
- **AWS CloudTrail**: Logs S3 management API calls (bucket creation, policy changes) and optionally data events (object-level GET/PUT) for audit trails.
- **S3 Access Analyzer**: Detects unintended public or cross-account bucket access.

---

## S3 Gateways (AWS Storage Gateway)

| Gateway Type | Protocol | Use Case |
|---|---|---|
| **S3 File Gateway** | NFS, SMB | Store files as S3 objects from on-premises. Recently accessed files cached locally. |
| **Volume Gateway** | iSCSI | Block storage backed by S3. **Cached mode**: primary in cloud. **Stored mode**: primary on-premises. |
| **Tape Gateway** | iSCSI VTL | Virtual tape library backed by S3 and Glacier. Replace physical tape infrastructure. |

> **Exam Tip!** File Gateway = file shares to S3. Tape Gateway = replace legacy tape backups. Volume Gateway = block storage/DR.

---

## S3 Static Website Hosting

- Enable directly on the bucket to host HTML/CSS/JS without a web server.
- **Endpoint format**: `http://bucket-name.s3-website-region.amazonaws.com`
- Requires **public read access** (or use CloudFront with OAC for private).
- Does **not** support HTTPS natively — use **CloudFront** in front for HTTPS + custom domain.
- Supports **index document** and **error document** configuration.
- **Use Case with CloudFront**: Use **Origin Access Control (OAC)** to keep bucket private while serving via CloudFront.

---

## Integration: S3 and AWS Athena

- **Purpose**: Run SQL queries directly on data stored in S3 — serverless, no infrastructure to manage.
- **Supported Formats**: CSV, JSON, Parquet, ORC, Avro, Apache Hive — columnar formats (Parquet, ORC) are fastest/cheapest.
- **Billing**: Pay per query based on **data scanned** — use partitioning and columnar formats to reduce cost.
- **Common Use Cases**: Query VPC Flow Logs, CloudTrail logs, ALB access logs, ELB logs stored in S3.
- **Partition Projection**: Speeds up queries and reduces cost for structured/date-partitioned data.

> **Exam Insight**: Athena + S3 = serverless ad-hoc log analysis. Pair with **AWS Glue** Data Catalog for schema management.

---

## Exam-Relevant Use Cases

| Scenario | Recommended Solution |
|---|---|
| Private EC2 → S3, no internet | S3 Gateway VPC Endpoint |
| Temporary access to private S3 object | Pre-signed URL |
| Multiple teams accessing shared dataset | S3 Access Points |
| Prevent object deletion for 7 years | S3 Object Lock – Compliance Mode |
| Replicate to another region for DR | Cross-Region Replication (CRR) |
| Large file upload from remote users | Transfer Acceleration + Multipart Upload |
| Aggregate logs from multiple accounts | Same-Region Replication (SRR) |
| Detect unintended public bucket access | S3 Access Analyzer |
| On-premises file shares to S3 | S3 File Gateway |
| Replace tape backup infrastructure | Tape Gateway |
| Query web server logs stored in S3 | Athena |
| Transform data during retrieval | S3 Object Lambda |
| Bulk operations on existing objects | S3 Batch Operations |
| Serve static website with HTTPS + CDN | S3 + CloudFront (with OAC) |
| Archive data accessed quarterly | S3 Glacier Instant Retrieval |
| Lowest-cost 10-year archive | S3 Glacier Deep Archive |

---

## Diagram: Amazon S3 Architecture at a Glance
```
                        ┌─────────────────────────────────┐
                        │         Amazon S3 Bucket         │
                        │    (Region-scoped, Globally      │
                        │      Unique Bucket Name)          │
                        └────────────┬────────────────────-┘
                                     │
          ┌──────────────────────────┼─────────────────────────────┐
          │                          │                              │
  ┌───────▼───────┐        ┌─────────▼──────────┐       ┌──────────▼──────────┐
  │  Access Layer  │        │  Data Protection    │       │  Storage Tiers      │
  │               │        │                     │       │                     │
  │ IAM Policies  │        │ Versioning          │       │ Standard            │
  │ Bucket Policy │        │ Object Lock (WORM)  │       │ Intelligent-Tiering │
  │ ACLs          │        │ Replication (CRR /  │       │ Standard-IA         │
  │ Access Points │        │   SRR)              │       │ One Zone-IA         │
  │ Pre-signed URL│        │ MFA Delete          │       │ Glacier Instant     │
  │ VPC Endpoint  │        │ Encryption (SSE-S3/ │       │ Glacier Flexible    │
  │ Block Public  │        │   KMS/C/CSE)        │       │ Glacier Deep Archive│
  └───────────────┘        └─────────────────────┘       └─────────────────────┘
                                     │
          ┌──────────────────────────┼─────────────────────────────┐
          │                          │                              │
  ┌───────▼───────┐        ┌─────────▼──────────┐       ┌──────────▼──────────┐
  │  Performance  │        │  Event & Analytics  │       │  Monitoring         │
  │               │        │                     │       │                     │
  │ Multipart     │        │ Event Notifications │       │ Server Access Logs  │
  │ Transfer Accel│        │   (Lambda/SQS/SNS)  │       │ CloudTrail          │
  │ Prefix Optim  │        │ S3 Select           │       │ Storage Lens        │
  │ Byte-Range    │        │ Athena Integration  │       │ Access Analyzer     │
  │               │        │ Object Lambda       │       │                     │
  └───────────────┘        └─────────────────────┘       └─────────────────────┘
```

---

## Exam Commandments for S3

1. **Storage Classes**: Know retrieval times, minimum storage durations, and cost trade-offs for all 7 classes.
2. **Object Lock Modes**: Governance (overridable with permissions) vs Compliance (immutable, no exceptions).
3. **Replication**: CRR for cross-region DR/latency; SRR for log aggregation. Versioning required. Not retroactive.
4. **Encryption**: SSE-KMS = auditable. SSE-S3 = simplest. SSE-C = BYOK, no AWS key storage. CSE = encrypt before upload.
5. **Access Control**: IAM for user-level, Bucket Policy for resource-level, Access Points for team-level at scale.
6. **Pre-signed URLs**: Temporary delegated access without making buckets public.
7. **VPC Endpoint**: Free Gateway Endpoint for private subnets accessing S3.
8. **Athena**: Serverless SQL on S3. Use Parquet + partitioning to minimize cost.
9. **Event Notifications**: S3 → Lambda/SQS/SNS/EventBridge for event-driven pipelines.
10. **Consistency**: S3 now has **strong read-after-write consistency** — no eventual consistency workarounds needed.

---

## Quick-Reference: Glacier Retrieval Tiers

| Glacier Class | Expedited | Standard | Bulk |
|---|---|---|---|
| **Glacier Instant Retrieval** | Milliseconds | Milliseconds | Milliseconds |
| **Glacier Flexible Retrieval** | 1–5 minutes | 3–5 hours | 5–12 hours |
| **Glacier Deep Archive** | N/A | ~12 hours | ~48 hours |

---

## Resources for Practice
1. Official Docs: [S3 User Guide](https://docs.aws.amazon.com/s3/)
2. Exam Guide: [SAA-C03 Exam Guide PDF](https://docs.aws.amazon.com/pdfs/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.pdf)
3. Free Hands-On Practice: [AWS Free Tier](https://aws.amazon.com/free/)
4. Practice Questions: [Tutorials Dojo SAA-C03](https://tutorialsdojo.com/aws-certified-solutions-architect-associate-saa-c03/)
5. AWS FAQs: [S3 FAQs](https://aws.amazon.com/s3/faqs/) — frequently sourced for exam questions