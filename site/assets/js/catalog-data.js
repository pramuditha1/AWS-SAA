window.SAA_CATALOG = [
  {
    "name": "IAM",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/iam.html",
    "blurb": "Users, groups, roles, policies, least privilege.",
    "aliases": "identity access"
  },
  {
    "name": "AWS STS",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/iam.html",
    "blurb": "Temporary credentials and AssumeRole.",
    "aliases": "security token service"
  },
  {
    "name": "AWS Organizations",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/governance.html",
    "blurb": "Multi-account structure and SCPs.",
    "aliases": "scp ou"
  },
  {
    "name": "AWS Control Tower",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/governance.html",
    "blurb": "Landing zone and account factory.",
    "aliases": "guardrails"
  },
  {
    "name": "AWS KMS",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/security.html",
    "blurb": "Customer managed keys and envelope encryption.",
    "aliases": "cmk encryption"
  },
  {
    "name": "ACM",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/security.html",
    "blurb": "TLS certificates for HTTPS in transit.",
    "aliases": "certificate manager"
  },
  {
    "name": "Amazon S3",
    "category": "Storage",
    "priority": "must",
    "href": "learn/s3.html",
    "blurb": "Object storage, classes, lifecycle, encryption, replication.",
    "aliases": "bucket glacier"
  },
  {
    "name": "Amazon S3 Glacier",
    "category": "Storage",
    "priority": "must",
    "href": "learn/s3.html",
    "blurb": "Archive storage classes and restore times.",
    "aliases": "flexible retrieval deep archive"
  },
  {
    "name": "Amazon EC2",
    "category": "Compute",
    "priority": "must",
    "href": "learn/ec2.html",
    "blurb": "Instances, families, AMIs, placement, purchasing.",
    "aliases": "graviton hibernate"
  },
  {
    "name": "Amazon EBS",
    "category": "Storage",
    "priority": "must",
    "href": "learn/storage.html",
    "blurb": "Block volumes for EC2, snapshots, gp3 vs io2.",
    "aliases": "volume"
  },
  {
    "name": "Amazon EFS",
    "category": "Storage",
    "priority": "must",
    "href": "learn/storage.html",
    "blurb": "Shared Linux NFS file system across AZs.",
    "aliases": "nfs"
  },
  {
    "name": "Amazon FSx",
    "category": "Storage",
    "priority": "must",
    "href": "learn/storage.html",
    "blurb": "Windows, Lustre, NetApp, OpenZFS file systems.",
    "aliases": "lustre"
  },
  {
    "name": "Amazon VPC",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/vpc.html",
    "blurb": "Subnets, IGW, NAT, SG vs NACL, peering, endpoints.",
    "aliases": "nacl security group"
  },
  {
    "name": "AWS PrivateLink",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/vpc.html",
    "blurb": "Private connectivity with interface endpoints.",
    "aliases": "vpc endpoint"
  },
  {
    "name": "Elastic Load Balancing",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/elb-asg.html",
    "blurb": "ALB, NLB, and Gateway Load Balancer.",
    "aliases": "alb nlb gwlb"
  },
  {
    "name": "Amazon EC2 Auto Scaling",
    "category": "Compute",
    "priority": "must",
    "href": "learn/elb-asg.html",
    "blurb": "Horizontal scaling with launch templates.",
    "aliases": "asg"
  },
  {
    "name": "Amazon RDS",
    "category": "Database",
    "priority": "must",
    "href": "learn/databases.html",
    "blurb": "Managed relational databases, Multi-AZ, replicas.",
    "aliases": "mysql postgres"
  },
  {
    "name": "Amazon Aurora",
    "category": "Database",
    "priority": "must",
    "href": "learn/databases.html",
    "blurb": "MySQL/PostgreSQL compatible, 6 copies, serverless.",
    "aliases": "aurora serverles"
  },
  {
    "name": "Amazon DynamoDB",
    "category": "Database",
    "priority": "must",
    "href": "learn/dynamodb.html",
    "blurb": "Key-value NoSQL, on-demand, DAX, global tables.",
    "aliases": "dax streams"
  },
  {
    "name": "Amazon ElastiCache",
    "category": "Database",
    "priority": "must",
    "href": "learn/databases.html",
    "blurb": "Redis/Memcached caching in front of databases.",
    "aliases": "redis"
  },
  {
    "name": "Amazon Route 53",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/route53.html",
    "blurb": "DNS, routing policies, health checks, failover.",
    "aliases": "alias latency geo"
  },
  {
    "name": "Amazon CloudFront",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/cloudfront.html",
    "blurb": "CDN, OAC, signed URLs, edge functions.",
    "aliases": "cdn oai"
  },
  {
    "name": "AWS Global Accelerator",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/cloudfront.html",
    "blurb": "Anycast static IPs over the AWS backbone.",
    "aliases": "ga anycast"
  },
  {
    "name": "Amazon SQS",
    "category": "Application Integration",
    "priority": "must",
    "href": "learn/messaging.html",
    "blurb": "Queues for loose coupling, standard vs FIFO.",
    "aliases": "queue dlq"
  },
  {
    "name": "Amazon SNS",
    "category": "Application Integration",
    "priority": "must",
    "href": "learn/messaging.html",
    "blurb": "Pub/sub fan-out to many subscribers.",
    "aliases": "topic"
  },
  {
    "name": "Amazon Kinesis",
    "category": "Analytics",
    "priority": "must",
    "href": "learn/messaging.html",
    "blurb": "Real-time streaming with multiple consumers.",
    "aliases": "data streams"
  },
  {
    "name": "Amazon Data Firehose",
    "category": "Analytics",
    "priority": "must",
    "href": "learn/messaging.html",
    "blurb": "Load streams into S3, Redshift, OpenSearch.",
    "aliases": "kinesis firehose"
  },
  {
    "name": "AWS Lambda",
    "category": "Serverless",
    "priority": "must",
    "href": "learn/lambda.html",
    "blurb": "Event-driven compute, 15 minute max.",
    "aliases": "function"
  },
  {
    "name": "Amazon API Gateway",
    "category": "Front-End Web and Mobile",
    "priority": "must",
    "href": "learn/dynamodb.html",
    "blurb": "REST/HTTP/WebSocket APIs in front of Lambda.",
    "aliases": "rest http"
  },
  {
    "name": "AWS Step Functions",
    "category": "Application Integration",
    "priority": "must",
    "href": "learn/lambda.html",
    "blurb": "Orchestrate serverless workflows.",
    "aliases": "state machine"
  },
  {
    "name": "Amazon EventBridge",
    "category": "Application Integration",
    "priority": "must",
    "href": "learn/monitoring.html",
    "blurb": "Event bus, SaaS events, scheduled rules.",
    "aliases": "event bus"
  },
  {
    "name": "Amazon CloudWatch",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/monitoring.html",
    "blurb": "Metrics, logs, alarms, dashboards.",
    "aliases": "alarm"
  },
  {
    "name": "AWS CloudTrail",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/monitoring.html",
    "blurb": "API audit trail for governance.",
    "aliases": "audit"
  },
  {
    "name": "AWS Config",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/governance.html",
    "blurb": "Record configuration and evaluate rules.",
    "aliases": "compliance"
  },
  {
    "name": "AWS CloudFormation",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/governance.html",
    "blurb": "Infrastructure as code templates and stacks.",
    "aliases": "iac"
  },
  {
    "name": "AWS Systems Manager",
    "category": "Management and Governance",
    "priority": "must",
    "href": "learn/governance.html",
    "blurb": "Session Manager, Parameter Store, Patch Manager.",
    "aliases": "ssm"
  },
  {
    "name": "Amazon ECS",
    "category": "Containers",
    "priority": "must",
    "href": "learn/containers.html",
    "blurb": "AWS-native container orchestration.",
    "aliases": "fargate tasks"
  },
  {
    "name": "Amazon EKS",
    "category": "Containers",
    "priority": "must",
    "href": "learn/containers.html",
    "blurb": "Managed Kubernetes control plane.",
    "aliases": "kubernetes"
  },
  {
    "name": "AWS Fargate",
    "category": "Serverless",
    "priority": "must",
    "href": "learn/containers.html",
    "blurb": "Serverless compute for ECS/EKS tasks.",
    "aliases": "no servers"
  },
  {
    "name": "AWS Direct Connect",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/networking-advanced.html",
    "blurb": "Dedicated private link from on-premises.",
    "aliases": "dx vif"
  },
  {
    "name": "AWS Site-to-Site VPN",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/networking-advanced.html",
    "blurb": "IPsec VPN, fast to set up, internet path.",
    "aliases": "vpn"
  },
  {
    "name": "AWS Transit Gateway",
    "category": "Networking and Content Delivery",
    "priority": "must",
    "href": "learn/networking-advanced.html",
    "blurb": "Hub-and-spoke for many VPCs and on-prem.",
    "aliases": "tgw"
  },
  {
    "name": "AWS WAF",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/security.html",
    "blurb": "Layer 7 firewall for ALB, CloudFront, API Gateway.",
    "aliases": "sql injection xss"
  },
  {
    "name": "AWS Shield",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/security.html",
    "blurb": "DDoS protection. Standard is free.",
    "aliases": "ddos"
  },
  {
    "name": "AWS Secrets Manager",
    "category": "Security, Identity, and Compliance",
    "priority": "must",
    "href": "learn/security.html",
    "blurb": "Rotate database secrets automatically.",
    "aliases": "password rotation"
  },
  {
    "name": "AWS Backup",
    "category": "Storage",
    "priority": "must",
    "href": "learn/migration.html",
    "blurb": "Central backup policies across services.",
    "aliases": "restore"
  },
  {
    "name": "AWS DMS",
    "category": "Migration and Transfer",
    "priority": "must",
    "href": "learn/migration.html",
    "blurb": "Homogeneous and heterogeneous database migration.",
    "aliases": "cdc sct"
  },
  {
    "name": "AWS DataSync",
    "category": "Migration and Transfer",
    "priority": "must",
    "href": "learn/storage.html",
    "blurb": "Online data movement to S3/EFS/FSx.",
    "aliases": "migration"
  },
  {
    "name": "AWS Storage Gateway",
    "category": "Storage",
    "priority": "must",
    "href": "learn/storage.html",
    "blurb": "Hybrid file, volume, and tape gateways.",
    "aliases": "file gateway"
  },
  {
    "name": "AWS Snow Family",
    "category": "Migration and Transfer",
    "priority": "must",
    "href": "learn/storage.html",
    "blurb": "Offline petabyte-scale transfer appliances.",
    "aliases": "snowball edge"
  },
  {
    "name": "AWS Cost Explorer",
    "category": "AWS Cost Management",
    "priority": "must",
    "href": "learn/cost.html",
    "blurb": "Visualize and forecast spend.",
    "aliases": "billing"
  },
  {
    "name": "AWS Budgets",
    "category": "AWS Cost Management",
    "priority": "must",
    "href": "learn/cost.html",
    "blurb": "Alerts when cost or usage exceeds a threshold.",
    "aliases": "alert"
  },
  {
    "name": "Savings Plans",
    "category": "AWS Cost Management",
    "priority": "must",
    "href": "learn/cost.html",
    "blurb": "1 or 3 year compute discount commitment.",
    "aliases": "compute sp"
  },
  {
    "name": "Amazon GuardDuty",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/security.html",
    "blurb": "Threat detection from CloudTrail, VPC Flow, DNS.",
    "aliases": "ids"
  },
  {
    "name": "Amazon Inspector",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/security.html",
    "blurb": "Vulnerability scanning for EC2, ECR, Lambda.",
    "aliases": "cve"
  },
  {
    "name": "Amazon Macie",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/security.html",
    "blurb": "Discover sensitive data in S3.",
    "aliases": "pii"
  },
  {
    "name": "AWS Security Hub",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/security.html",
    "blurb": "Central findings from GuardDuty, Inspector, Macie.",
    "aliases": "cspm"
  },
  {
    "name": "Amazon Cognito",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/identity-federation.html",
    "blurb": "User pools and identity pools for apps.",
    "aliases": "user pool"
  },
  {
    "name": "IAM Identity Center",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/identity-federation.html",
    "blurb": "SSO across accounts and applications.",
    "aliases": "sso"
  },
  {
    "name": "AWS Directory Service",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/identity-federation.html",
    "blurb": "Managed Microsoft AD and AD Connector.",
    "aliases": "microsoft ad"
  },
  {
    "name": "AWS Network Firewall",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/networking-advanced.html",
    "blurb": "Managed IPS/IDS at VPC perimeter.",
    "aliases": "dpi"
  },
  {
    "name": "AWS Firewall Manager",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/security.html",
    "blurb": "Org-wide WAF, Shield, and SG policies.",
    "aliases": "central"
  },
  {
    "name": "AWS RAM",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/specialty-security.html",
    "blurb": "Share subnets, TGW, and other resources.",
    "aliases": "resource access manager"
  },
  {
    "name": "AWS CloudHSM",
    "category": "Security, Identity, and Compliance",
    "priority": "should",
    "href": "learn/specialty-security.html",
    "blurb": "Dedicated HSM when you need FIPS single-tenant keys.",
    "aliases": "hsm"
  },
  {
    "name": "AWS Elastic Beanstalk",
    "category": "Compute",
    "priority": "should",
    "href": "learn/containers.html",
    "blurb": "PaaS: upload code, AWS runs the platform.",
    "aliases": "paas"
  },
  {
    "name": "AWS Batch",
    "category": "Compute",
    "priority": "should",
    "href": "learn/containers.html",
    "blurb": "Managed batch jobs on EC2 or Fargate.",
    "aliases": "queue jobs"
  },
  {
    "name": "AWS Outposts",
    "category": "Compute",
    "priority": "should",
    "href": "learn/hybrid-edge.html",
    "blurb": "AWS racks running in your datacenter.",
    "aliases": "hybrid"
  },
  {
    "name": "AWS Transfer Family",
    "category": "Migration and Transfer",
    "priority": "should",
    "href": "learn/migration.html",
    "blurb": "SFTP/FTPS/FTP into S3 or EFS.",
    "aliases": "sftp"
  },
  {
    "name": "AWS AppSync",
    "category": "Application Integration",
    "priority": "should",
    "href": "learn/integration-extras.html",
    "blurb": "Managed GraphQL APIs.",
    "aliases": "graphql"
  },
  {
    "name": "Amazon MSK",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/integration-extras.html",
    "blurb": "Managed Apache Kafka.",
    "aliases": "kafka"
  },
  {
    "name": "AWS Glue",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "Serverless ETL and Data Catalog.",
    "aliases": "crawler"
  },
  {
    "name": "Amazon Athena",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "SQL over S3, pay per TB scanned.",
    "aliases": "presto"
  },
  {
    "name": "Amazon Redshift",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "Petabyte data warehouse.",
    "aliases": "spectrum"
  },
  {
    "name": "Amazon EMR",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "Managed Hadoop/Spark clusters.",
    "aliases": "spark"
  },
  {
    "name": "Amazon OpenSearch Service",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "Search and log analytics.",
    "aliases": "elasticsearch"
  },
  {
    "name": "AWS Lake Formation",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "Governed data lake permissions.",
    "aliases": "lake"
  },
  {
    "name": "Amazon QuickSight",
    "category": "Analytics",
    "priority": "should",
    "href": "learn/analytics.html",
    "blurb": "BI dashboards (Quick Suite on the exam).",
    "aliases": "quicksight"
  },
  {
    "name": "Amazon Rekognition",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Images and video: faces, objects, moderation.",
    "aliases": "vision"
  },
  {
    "name": "Amazon Transcribe",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Speech to text.",
    "aliases": "stt"
  },
  {
    "name": "Amazon Polly",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Text to speech.",
    "aliases": "tts"
  },
  {
    "name": "Amazon Translate",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Language translation.",
    "aliases": "i18n"
  },
  {
    "name": "Amazon Comprehend",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "NLP: sentiment, entities, PII.",
    "aliases": "nlp"
  },
  {
    "name": "Amazon Textract",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Extract text and forms from documents.",
    "aliases": "ocr"
  },
  {
    "name": "Amazon Lex",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Chatbots (same tech as Alexa).",
    "aliases": "bot"
  },
  {
    "name": "Amazon SageMaker AI",
    "category": "Machine Learning",
    "priority": "should",
    "href": "learn/ml.html",
    "blurb": "Build, train, and deploy ML models.",
    "aliases": "notebook"
  },
  {
    "name": "AWS X-Ray",
    "category": "Developer Tools",
    "priority": "should",
    "href": "learn/monitoring.html",
    "blurb": "Trace distributed applications.",
    "aliases": "trace"
  },
  {
    "name": "AWS Trusted Advisor",
    "category": "Management and Governance",
    "priority": "should",
    "href": "learn/governance.html",
    "blurb": "Checks for cost, security, limits, performance.",
    "aliases": "support"
  },
  {
    "name": "AWS Compute Optimizer",
    "category": "Management and Governance",
    "priority": "should",
    "href": "learn/cost.html",
    "blurb": "Right-size EC2, EBS, Lambda, Auto Scaling.",
    "aliases": "rightsizing"
  },
  {
    "name": "Amazon MQ",
    "category": "Application Integration",
    "priority": "should",
    "href": "learn/messaging.html",
    "blurb": "Managed ActiveMQ/RabbitMQ for legacy brokers.",
    "aliases": "activemq"
  },
  {
    "name": "Amazon ECR",
    "category": "Containers",
    "priority": "should",
    "href": "learn/containers.html",
    "blurb": "Container image registry.",
    "aliases": "docker"
  },
  {
    "name": "AWS Application Migration Service",
    "category": "Migration and Transfer",
    "priority": "should",
    "href": "learn/migration.html",
    "blurb": "Lift and shift servers (MGN).",
    "aliases": "mgn"
  },
  {
    "name": "AWS Client VPN",
    "category": "Networking and Content Delivery",
    "priority": "should",
    "href": "learn/networking-advanced.html",
    "blurb": "Managed VPN for users into a VPC.",
    "aliases": "client vpn"
  },
  {
    "name": "AWS Cost and Usage Report",
    "category": "AWS Cost Management",
    "priority": "must",
    "href": "learn/cost.html",
    "blurb": "Most detailed billing export to S3.",
    "aliases": "cur"
  },
  {
    "name": "Amazon AppFlow",
    "category": "Application Integration",
    "priority": "name",
    "href": "learn/integration-extras.html",
    "blurb": "SaaS to AWS data transfer (Salesforce, etc.).",
    "aliases": "saas"
  },
  {
    "name": "AWS Data Exchange",
    "category": "Analytics",
    "priority": "name",
    "href": "learn/analytics.html",
    "blurb": "Third-party datasets in AWS.",
    "aliases": "dataset"
  },
  {
    "name": "AWS Amplify",
    "category": "Front-End Web and Mobile",
    "priority": "name",
    "href": "learn/identity-federation.html",
    "blurb": "Frontend hosting and app backend helpers.",
    "aliases": "hosting"
  },
  {
    "name": "AWS Device Farm",
    "category": "Front-End Web and Mobile",
    "priority": "name",
    "href": "learn/identity-federation.html",
    "blurb": "Real device testing farm.",
    "aliases": "mobile test"
  },
  {
    "name": "Amazon DocumentDB",
    "category": "Database",
    "priority": "name",
    "href": "learn/specialty-databases.html",
    "blurb": "MongoDB-compatible document database.",
    "aliases": "mongodb"
  },
  {
    "name": "Amazon Neptune",
    "category": "Database",
    "priority": "name",
    "href": "learn/specialty-databases.html",
    "blurb": "Graph database for relationships.",
    "aliases": "gremlin sparql"
  },
  {
    "name": "Amazon Keyspaces",
    "category": "Database",
    "priority": "name",
    "href": "learn/specialty-databases.html",
    "blurb": "Managed Apache Cassandra.",
    "aliases": "cassandra"
  },
  {
    "name": "Amazon Kendra",
    "category": "Machine Learning",
    "priority": "name",
    "href": "learn/ml.html",
    "blurb": "Enterprise search over documents.",
    "aliases": "search"
  },
  {
    "name": "AWS Audit Manager",
    "category": "Security, Identity, and Compliance",
    "priority": "name",
    "href": "learn/specialty-security.html",
    "blurb": "Collect evidence for audits.",
    "aliases": "compliance"
  },
  {
    "name": "AWS Artifact",
    "category": "Security, Identity, and Compliance",
    "priority": "name",
    "href": "learn/specialty-security.html",
    "blurb": "Download AWS compliance reports.",
    "aliases": "soc iso"
  },
  {
    "name": "Amazon Detective",
    "category": "Security, Identity, and Compliance",
    "priority": "name",
    "href": "learn/specialty-security.html",
    "blurb": "Investigate findings with a graph of activity.",
    "aliases": "investigation"
  },
  {
    "name": "AWS License Manager",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/governance.html",
    "blurb": "Track software licenses.",
    "aliases": "oracle sql server"
  },
  {
    "name": "Amazon Managed Grafana",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/monitoring.html",
    "blurb": "Managed Grafana dashboards.",
    "aliases": "grafana"
  },
  {
    "name": "Amazon Managed Service for Prometheus",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/monitoring.html",
    "blurb": "Managed Prometheus metrics.",
    "aliases": "amp"
  },
  {
    "name": "Amazon Elastic Transcoder",
    "category": "Media Services",
    "priority": "name",
    "href": "learn/ml.html",
    "blurb": "Legacy video transcoding (know the name).",
    "aliases": "video"
  },
  {
    "name": "Amazon Kinesis Video Streams",
    "category": "Media Services",
    "priority": "name",
    "href": "learn/messaging.html",
    "blurb": "Ingest video from devices.",
    "aliases": "camera"
  },
  {
    "name": "AWS Wavelength",
    "category": "Compute",
    "priority": "name",
    "href": "learn/hybrid-edge.html",
    "blurb": "AWS compute inside 5G carrier networks.",
    "aliases": "edge 5g"
  },
  {
    "name": "VMware Cloud on AWS",
    "category": "Compute",
    "priority": "name",
    "href": "learn/hybrid-edge.html",
    "blurb": "VMware SDDC running on AWS.",
    "aliases": "vmware"
  },
  {
    "name": "AWS Serverless Application Repository",
    "category": "Compute",
    "priority": "name",
    "href": "learn/lambda.html",
    "blurb": "Publish and deploy serverless apps.",
    "aliases": "sar"
  },
  {
    "name": "Amazon ECS Anywhere",
    "category": "Containers",
    "priority": "name",
    "href": "learn/containers.html",
    "blurb": "Run ECS on your own hardware.",
    "aliases": "hybrid containers"
  },
  {
    "name": "Amazon EKS Anywhere",
    "category": "Containers",
    "priority": "name",
    "href": "learn/containers.html",
    "blurb": "Run EKS on your own hardware.",
    "aliases": "hybrid k8s"
  },
  {
    "name": "Amazon EKS Distro",
    "category": "Containers",
    "priority": "name",
    "href": "learn/containers.html",
    "blurb": "Open-source Kubernetes distribution from AWS.",
    "aliases": "eks-d"
  },
  {
    "name": "AWS Auto Scaling",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/elb-asg.html",
    "blurb": "Unified scaling plans across multiple resources.",
    "aliases": "application auto scaling"
  },
  {
    "name": "AWS Health Dashboard",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/governance.html",
    "blurb": "Service health and account events.",
    "aliases": "phs"
  },
  {
    "name": "AWS CLI",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/foundations.html",
    "blurb": "Command line access to AWS APIs.",
    "aliases": "command line"
  },
  {
    "name": "AWS Management Console",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/foundations.html",
    "blurb": "Web console for AWS.",
    "aliases": "browser"
  },
  {
    "name": "AWS Service Catalog",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/governance.html",
    "blurb": "Approved product portfolios for teams.",
    "aliases": "portfolio"
  },
  {
    "name": "AWS Well-Architected Tool",
    "category": "Management and Governance",
    "priority": "name",
    "href": "learn/well-architected.html",
    "blurb": "Review workloads against the six pillars.",
    "aliases": "lens"
  },
  {
    "name": "Amazon Aurora Serverless",
    "category": "Database",
    "priority": "must",
    "href": "learn/databases.html",
    "blurb": "Aurora that scales to zero and charges per ACU.",
    "aliases": "aurora v2"
  }
];
