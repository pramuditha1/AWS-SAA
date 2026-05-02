# CS07: Analytics - Redshift, Glue, Athena, OpenSearch, EMR
### AWS SAA-C03 Cheat Sheet

---

## Amazon Redshift (Data Warehouse)

### Key Concepts
- **Columnar data warehouse** for analytics (OLAP, not OLTP)
- Petabyte-scale, SQL-based analytics
- Based on PostgreSQL (but NOT used as OLTP database)
- **10x better performance** than traditional data warehouses

### Architecture
- **Leader Node**: Query planning, result aggregation
- **Compute Nodes**: Execute queries, store data
- **Node Types**: RA3 (managed storage), DC2 (dense compute), DS2 (dense storage)

### Key Features
| Feature | Description |
|---------|-------------|
| **Columnar Storage** | Data stored by columns, great for analytics queries |
| **Massive Parallel Processing (MPP)** | Distributes queries across nodes |
| **Redshift Spectrum** | Query data in S3 without loading into Redshift |
| **Redshift Serverless** | Auto-scales, pay per use (no cluster management) |
| **Concurrency Scaling** | Auto-adds capacity for burst read queries |
| **Materialized Views** | Pre-computed results for faster queries |
| **Cross-region snapshots** | DR and data sharing |

### Redshift Data Loading
- **COPY command**: Fastest way to load (from S3, DynamoDB, EMR)
- **Kinesis Data Firehose**: Stream data into Redshift
- **AWS Glue**: ETL jobs load into Redshift
- S3 → COPY is the preferred pattern

### Redshift vs RDS
| Feature | Redshift | RDS |
|---------|----------|-----|
| Workload | OLAP (analytics) | OLTP (transactions) |
| Query type | Complex aggregations on large data | Simple reads/writes |
| Data size | Petabytes | Terabytes |
| Joins | Column-based, optimized for analytics | Row-based |
| Use Case | Business intelligence, reporting | Web apps, CRUD |

> **Exam Tips**:
> - "Analytics/BI queries on petabytes of data" = Redshift
> - "Query S3 data from Redshift without loading" = Redshift Spectrum
> - "Serverless data warehouse" = Redshift Serverless
> - "OLTP database for web app" = RDS/Aurora (NOT Redshift)

---

## Amazon Athena (Serverless S3 Query)

### Key Concepts
- **Serverless** interactive query service
- Query data **directly in S3** using standard SQL
- No infrastructure to manage, no data loading needed
- Pay per query ($5 per TB scanned)
- Uses **Presto** engine under the hood

### Key Features
- Supports: CSV, JSON, Parquet, ORC, Avro, etc.
- **Partitioning**: Organize data by key (e.g., year/month/day) to reduce scan cost
- **Compression**: Use columnar formats (Parquet/ORC) to reduce data scanned
- **Federated Query**: Query data in other sources (RDS, DynamoDB, on-premises) via Lambda connectors
- **CTAS**: Create Table As Select - transform and store results
- Integrates with **QuickSight** for visualization

### Cost Optimization
- Use **columnar formats** (Parquet, ORC): 30-90% less data scanned
- **Partition data** in S3: Only scan relevant partitions
- **Compress** data: Less data = less cost
- Use larger files (avoid many small files)

### Common Use Cases
- Ad-hoc querying of S3 data lakes
- Analyze CloudTrail logs, ELB logs, VPC Flow Logs
- Business intelligence with QuickSight
- One-time data exploration

> **Exam Tips**:
> - "Query data in S3 without loading anywhere" = Athena
> - "Serverless SQL queries on S3" = Athena
> - "Analyze CloudTrail/VPC Flow Logs" = Athena
> - "Reduce Athena costs" = Partition + columnar format + compression
> - "Interactive queries, pay per query" = Athena

---

## AWS Glue (ETL Service)

### Key Concepts
- **Serverless ETL** (Extract, Transform, Load) service
- Discover, prepare, and combine data for analytics
- Apache Spark under the hood

### Key Components
| Component | Description |
|-----------|-------------|
| **Glue Data Catalog** | Central metadata repository (databases, tables, schemas) |
| **Glue Crawlers** | Scan data sources, infer schema, populate Data Catalog |
| **Glue Jobs** | ETL scripts (PySpark or Scala) that transform data |
| **Glue Studio** | Visual ETL authoring |
| **Glue DataBrew** | Visual data preparation (no code) |

### Glue Data Catalog
- **Central metadata store** for your data lake
- Used by: Athena, Redshift Spectrum, EMR
- One catalog per region per account
- Stores: Table definitions, partition info, schema
- Think of it as "Apache Hive Metastore compatible"

### Common Pattern
```
S3 (raw data) → Glue Crawler (discover schema) → Glue Data Catalog
                                                         ↓
S3 (raw) → Glue ETL Job (transform) → S3 (processed/Parquet)
                                                         ↓
                                              Athena / Redshift Spectrum (query)
```

### Glue Job Bookmarks
- Track previously processed data
- Prevent reprocessing of old data
- Useful for incremental ETL

> **Exam Tips**:
> - "ETL to prepare data for analytics" = Glue
> - "Convert CSV to Parquet" = Glue ETL Job
> - "Discover schema of data in S3" = Glue Crawler + Data Catalog
> - "Central metadata catalog for data lake" = Glue Data Catalog
> - Glue is serverless (no infrastructure to manage)

---

## Amazon OpenSearch Service (Elasticsearch)

### Key Concepts
- **Search and analytics** engine
- Successor to Amazon Elasticsearch Service
- Real-time search, log analytics, full-text search
- Deployed as a **cluster** (not serverless by default, but Serverless option exists)

### Use Cases
- **Log analytics**: Aggregate and search application logs
- **Full-text search**: Product search, website search
- **Application monitoring**: Real-time dashboards (with OpenSearch Dashboards/Kibana)
- **Security analytics**: SIEM (Security Information and Event Management)

### Common Patterns
```
CloudWatch Logs → Subscription Filter → Lambda → OpenSearch → Dashboards
Kinesis Data Streams → Kinesis Data Firehose → OpenSearch
DynamoDB Streams → Lambda → OpenSearch (search over DynamoDB data)
```

### Key Features
- Multi-AZ deployment for high availability
- Encryption at rest and in transit
- Fine-grained access control
- VPC support for network isolation
- **OpenSearch Serverless**: Auto-scales, no cluster management

### OpenSearch vs Athena vs Redshift

| Feature | OpenSearch | Athena | Redshift |
|---------|-----------|--------|----------|
| Best for | Search, log analytics | Ad-hoc S3 queries | BI/Data warehouse |
| Query type | Full-text search, dashboards | SQL on S3 | Complex analytics |
| Data loaded | Yes (indexed) | No (query in place) | Yes (loaded) |
| Real-time | ✅ | ❌ (batch) | ❌ (batch) |
| Serverless | Optional | ✅ Always | Optional |

> **Exam Tips**:
> - "Full-text search over data" = OpenSearch
> - "Real-time log analytics with dashboards" = OpenSearch + Dashboards
> - "Search DynamoDB data" = DynamoDB → Stream → Lambda → OpenSearch

---

## Amazon Kinesis (Real-time Analytics)

### Kinesis Services (Quick Review since you covered this)

| Service | Purpose | Key Point |
|---------|---------|-----------|
| **Kinesis Data Streams** | Ingest real-time data | Custom consumers, 1-365 day retention |
| **Kinesis Data Firehose** | Deliver data to destinations | Near real-time (60 sec buffer), serverless, auto-scales |
| **Kinesis Data Analytics** | SQL/Flink on streaming data | Real-time analytics on streams |

### Firehose Destinations
- S3, Redshift (via S3), OpenSearch, Splunk, HTTP endpoints, 3rd party partners

### Key Difference
- **Streams**: Real-time (~200ms), custom processing, manage consumers
- **Firehose**: Near real-time (60s min), managed delivery, no custom code

---

## Amazon EMR (Elastic MapReduce)

### Key Concepts
- Managed **big data platform** (Hadoop, Spark, Hive, Presto, etc.)
- Process vast amounts of data
- Cluster of EC2 instances

### Node Types
| Node | Purpose |
|------|---------|
| **Master** | Manages cluster, coordinates tasks |
| **Core** | Run tasks + store data (HDFS) |
| **Task** | Only run tasks (no storage), can use Spot instances |

### Use Cases
- Machine learning, data transformation
- Big data analytics (Spark, Hadoop)
- Log analysis at massive scale
- Genomics, financial analysis

> **Exam Tip**: "Process large amounts of data with Hadoop/Spark" = EMR. "Simple ETL" = Glue (serverless, easier).

---

## Amazon QuickSight

### Key Concepts
- **Serverless BI visualization** service
- Create dashboards and visualizations
- Pay per session pricing
- **SPICE**: In-memory computation engine for fast performance

### Data Sources
- Athena, RDS, Aurora, Redshift, S3, OpenSearch, on-premises databases
- SaaS: Salesforce, Jira, etc.

> **Exam Tip**: "Create business dashboards from AWS data" = QuickSight. "BI tool" = QuickSight.

---

## AWS Lake Formation

### Key Concepts
- **Build secure data lakes** easily
- Central place to manage data lake security and governance
- Fine-grained access control (column/row level)
- Built on top of Glue Data Catalog

### Key Features
- Centralized permissions (instead of IAM + S3 policies + Glue policies)
- Cross-account data sharing
- Data deduplication (ML-based)
- Blue prints for common data sources

> **Exam Tip**: "Fine-grained access control for data lake" = Lake Formation. "Build data lake quickly" = Lake Formation.

---

## Analytics Decision Matrix

| Scenario | Service |
|----------|---------|
| Data warehouse for BI | Redshift |
| Ad-hoc SQL on S3 | Athena |
| ETL / data transformation | Glue |
| Full-text search | OpenSearch |
| Real-time streaming analytics | Kinesis Analytics |
| Deliver streaming data to S3/Redshift | Kinesis Firehose |
| Big data processing (Hadoop/Spark) | EMR |
| BI dashboards | QuickSight |
| Data lake governance | Lake Formation |
| Metadata catalog | Glue Data Catalog |
