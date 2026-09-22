#!/usr/bin/env python3
"""Generate the SAA-C03 static study site. Run from the AWS-SAA repo root."""
from __future__ import annotations

import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


def esc(text: str) -> str:
    return htmlmod.escape(text, quote=True)


def inline(text: str) -> str:
    # Protect code spans first
    parts: list[str] = []
    buf = []
    i = 0
    while i < len(text):
        if text[i] == "`":
            j = text.find("`", i + 1)
            if j != -1:
                parts.append(("text", "".join(buf)))
                buf = []
                parts.append(("code", text[i + 1 : j]))
                i = j + 1
                continue
        buf.append(text[i])
        i += 1
    parts.append(("text", "".join(buf)))

    out = []
    for kind, chunk in parts:
        if kind == "code":
            out.append(f"<code>{esc(chunk)}</code>")
            continue
        chunk = esc(chunk)
        chunk = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", chunk)
        chunk = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", chunk)
        chunk = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', chunk)
        out.append(chunk)
    return "".join(out)


def md_to_html(src: str) -> str:
    lines = src.replace("\r\n", "\n").split("\n")
    html: list[str] = []
    i = 0
    in_list = None  # "ul" | "ol"

    def close_list():
        nonlocal in_list
        if in_list:
            html.append(f"</{in_list}>")
            in_list = None

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            close_list()
            lang = stripped[3:].strip()
            i += 1
            body = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            cls = "ascii-diagram" if lang in ("", "text", "diagram") else ""
            html.append(f'<pre class="{cls}"><code>{esc(chr(10).join(body))}</code></pre>')
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*[-: ]+\|", lines[i + 1]):
            close_list()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            header = [c.strip() for c in rows[0].strip("|").split("|")]
            body_rows = rows[2:]
            html.append('<div class="table-wrap"><table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
            for row in body_rows:
                cells = [c.strip() for c in row.strip("|").split("|")]
                html.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
            html.append("</tbody></table></div>")
            continue

        if stripped.startswith("#"):
            close_list()
            m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
            if m:
                level = len(m.group(1))
                text = m.group(2).strip()
                slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
                html.append(f'<h{level} id="{slug}">{inline(text)}</h{level}>')
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            close_list()
            html.append("<hr>")
            i += 1
            continue

        if stripped.startswith(">"):
            close_list()
            quotes = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quotes.append(re.sub(r"^>\s?", "", lines[i].strip()))
                i += 1
            joined = " ".join(quotes)
            cls = "exam-tip"
            if re.search(r"skip|out of scope|do not study", joined, re.I):
                cls = "exam-skip"
            html.append(f'<div class="{cls}">{inline(joined)}</div>')
            continue

        ul = re.match(r"^([ \t]*)[-*]\s+(.*)$", line.rstrip())
        ol = re.match(r"^([ \t]*)\d+\.\s+(.*)$", line.rstrip())
        if ul or ol:
            kind = "ul" if ul else "ol"
            text = (ul or ol).group(2)
            indent = len((ul or ol).group(1).replace("\t", "    "))
            nested = indent >= 2
            if in_list != kind:
                close_list()
                html.append(f"<{kind}>")
                in_list = kind
            if nested:
                html.append(f'<li class="nested">{inline(text)}</li>')
            else:
                html.append(f"<li>{inline(text)}</li>")
            i += 1
            continue

        if not stripped:
            close_list()
            i += 1
            continue

        close_list()
        para = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if (
                not nxt
                or nxt.startswith("#")
                or nxt.startswith("|")
                or nxt.startswith(">")
                or nxt.startswith("```")
                or nxt.startswith("- ")
                or nxt.startswith("* ")
                or re.match(r"^\d+\.\s+", nxt)
                or nxt in ("---", "***")
            ):
                break
            para.append(nxt)
            i += 1
        html.append(f"<p>{inline(' '.join(para))}</p>")

    close_list()
    return "\n".join(html)


NAV = [
    ("Exam", [
        ("index.html", "Service catalog"),
        ("exam/overview.html", "Exam overview"),
        ("exam/domain-1-secure.html", "Domain 1 · Secure 30%"),
        ("exam/domain-2-resilient.html", "Domain 2 · Resilient 26%"),
        ("exam/domain-3-performance.html", "Domain 3 · Performance 24%"),
        ("exam/domain-4-cost.html", "Domain 4 · Cost 20%"),
        ("exam/out-of-scope.html", "Out of scope"),
    ]),
    ("Learn", [
        ("learn/foundations.html", "Foundations"),
        ("learn/well-architected.html", "Well-Architected"),
        ("learn/iam.html", "IAM"),
        ("learn/identity-federation.html", "Cognito & federation"),
        ("learn/security.html", "KMS, WAF, Shield"),
        ("learn/specialty-security.html", "Security extras"),
        ("learn/s3.html", "S3"),
        ("learn/storage.html", "EBS, EFS, FSx"),
        ("learn/ec2.html", "EC2"),
        ("learn/elb-asg.html", "Auto Scaling & ELB"),
        ("learn/vpc.html", "VPC"),
        ("learn/networking-advanced.html", "Hybrid networking"),
        ("learn/route53.html", "Route 53"),
        ("learn/cloudfront.html", "CloudFront & GA"),
        ("learn/databases.html", "RDS, Aurora, ElastiCache"),
        ("learn/dynamodb.html", "DynamoDB & API Gateway"),
        ("learn/specialty-databases.html", "DocumentDB, Neptune"),
        ("learn/messaging.html", "SQS, SNS, Kinesis"),
        ("learn/lambda.html", "Lambda & Step Functions"),
        ("learn/integration-extras.html", "AppSync, MSK, AppFlow"),
        ("learn/monitoring.html", "CloudWatch & CloudTrail"),
        ("learn/containers.html", "ECS, EKS, Fargate"),
        ("learn/migration.html", "Migration & DR"),
        ("learn/analytics.html", "Analytics"),
        ("learn/governance.html", "Organizations & Config"),
        ("learn/cost.html", "Cost optimization"),
        ("learn/hybrid-edge.html", "Outposts & Wavelength"),
        ("learn/ml.html", "Machine learning"),
    ]),
    ("Compare", [
        ("compare/storage.html", "Storage picker"),
        ("compare/databases.html", "Database picker"),
        ("compare/messaging.html", "Messaging picker"),
        ("compare/compute.html", "Compute picker"),
        ("compare/networking.html", "Networking picker"),
        ("compare/dr.html", "DR picker"),
    ]),
    ("Sinhala", [
        ("sinhala/index.html", "Sinhala notes"),
    ]),
]


def rel_prefix(path: str) -> str:
    depth = path.count("/")
    return "" if depth == 0 else "../" * depth


def nav_html(path: str) -> str:
    prefix = rel_prefix(path)
    chunks = []
    for group, items in NAV:
        links = []
        for href, label in items:
            cls = ' class="active"' if href == path else ""
            links.append(f'<a{cls} href="{prefix}{href}">{esc(label)}</a>')
        chunks.append(f'<div class="nav-group"><h2>{esc(group)}</h2>{"".join(links)}</div>')
    return "\n".join(chunks)


def wrap(path: str, title: str, crumb: str, content: str) -> str:
    prefix = rel_prefix(path)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} · SAA-C03 Study</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Sinhala:wght@400;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/docs.css">
</head>
<body data-root="{prefix}">
  <a class="skip" href="#main">Skip to content</a>
  <header class="topbar">
    <button class="menu-btn" aria-label="Open menu">☰</button>
    <a class="brand" href="{prefix}index.html">
      <span class="brand-mark">S</span>
      SAA-C03 <span class="sub">study site</span>
    </a>
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input id="site-search" type="search" placeholder="Search services…" autocomplete="off">
      <div id="search-results" hidden></div>
    </div>
  </header>
  <div class="layout">
    <aside class="sidebar">{nav_html(path)}</aside>
    <main id="main">
      <div class="crumb">{crumb}</div>
      {content}
    </main>
  </div>
  <script src="{prefix}assets/js/catalog-data.js"></script>
  <script src="{prefix}assets/js/nav.js?v=2"></script>
  <script src="{prefix}assets/js/search.js"></script>
  <script src="{prefix}assets/js/catalog.js"></script>
  <script type="module">
    import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
    mermaid.initialize({{
      startOnLoad: true,
      theme: "dark",
      securityLevel: "loose",
      themeVariables: {{
        darkMode: true,
        background: "#0a101c",
        primaryColor: "#243656",
        primaryTextColor: "#e8eef8",
        primaryBorderColor: "#ff9900",
        lineColor: "#9aabc4",
        secondaryColor: "#1a2438",
        tertiaryColor: "#121a2b",
        nodeTextColor: "#e8eef8"
      }}
    }});
  </script>
</body>
</html>
"""


def write(path: str, title: str, crumb: str, content: str) -> None:
    out = SITE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(wrap(path, title, crumb, content), encoding="utf-8")


def pills(items: list[tuple[str, str]]) -> str:
    return '<div class="meta-row">' + "".join(f'<span class="pill {cls}">{esc(label)}</span>' for cls, label in items) + "</div>"


def mermaid(src: str) -> str:
    return f'<div class="mermaid">{src.strip()}</div>'


def related(prefix: str, links: list[tuple[str, str]]) -> str:
    items = "".join(f'<a href="{prefix}{href}">{esc(label)}</a>' for href, label in links)
    return f'<h2>Related pages</h2><div class="related">{items}</div>'


def docs(links: list[tuple[str, str]]) -> str:
    items = "".join(f'<li><a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a></li>' for label, url in links)
    return f"<h2>Official AWS docs</h2><ul class=\"docs-list\">{items}</ul>"


SERVICES = [
    # Must
    ("IAM", "Security, Identity, and Compliance", "must", "learn/iam.html", "Users, groups, roles, policies, least privilege.", "identity access"),
    ("AWS STS", "Security, Identity, and Compliance", "must", "learn/iam.html", "Temporary credentials and AssumeRole.", "security token service"),
    ("AWS Organizations", "Management and Governance", "must", "learn/governance.html", "Multi-account structure and SCPs.", "scp ou"),
    ("AWS Control Tower", "Management and Governance", "must", "learn/governance.html", "Landing zone and account factory.", "guardrails"),
    ("AWS KMS", "Security, Identity, and Compliance", "must", "learn/security.html", "Customer managed keys and envelope encryption.", "cmk encryption"),
    ("ACM", "Security, Identity, and Compliance", "must", "learn/security.html", "TLS certificates for HTTPS in transit.", "certificate manager"),
    ("Amazon S3", "Storage", "must", "learn/s3.html", "Object storage, classes, lifecycle, encryption, replication.", "bucket glacier"),
    ("Amazon S3 Glacier", "Storage", "must", "learn/s3.html", "Archive storage classes and restore times.", "flexible retrieval deep archive"),
    ("Amazon EC2", "Compute", "must", "learn/ec2.html", "Instances, families, AMIs, placement, purchasing.", "graviton hibernate"),
    ("Amazon EBS", "Storage", "must", "learn/storage.html", "Block volumes for EC2, snapshots, gp3 vs io2.", "volume"),
    ("Amazon EFS", "Storage", "must", "learn/storage.html", "Shared Linux NFS file system across AZs.", "nfs"),
    ("Amazon FSx", "Storage", "must", "learn/storage.html", "Windows, Lustre, NetApp, OpenZFS file systems.", "lustre"),
    ("Amazon VPC", "Networking and Content Delivery", "must", "learn/vpc.html", "Subnets, IGW, NAT, SG vs NACL, peering, endpoints.", "nacl security group"),
    ("AWS PrivateLink", "Networking and Content Delivery", "must", "learn/vpc.html", "Private connectivity with interface endpoints.", "vpc endpoint"),
    ("Elastic Load Balancing", "Networking and Content Delivery", "must", "learn/elb-asg.html", "ALB, NLB, and Gateway Load Balancer.", "alb nlb gwlb"),
    ("Amazon EC2 Auto Scaling", "Compute", "must", "learn/elb-asg.html", "Horizontal scaling with launch templates.", "asg"),
    ("Amazon RDS", "Database", "must", "learn/databases.html", "Managed relational databases, Multi-AZ, replicas.", "mysql postgres"),
    ("Amazon Aurora", "Database", "must", "learn/databases.html", "MySQL/PostgreSQL compatible, 6 copies, serverless.", "aurora serverles"),
    ("Amazon DynamoDB", "Database", "must", "learn/dynamodb.html", "Key-value NoSQL, on-demand, DAX, global tables.", "dax streams"),
    ("Amazon ElastiCache", "Database", "must", "learn/databases.html", "Redis/Memcached caching in front of databases.", "redis"),
    ("Amazon Route 53", "Networking and Content Delivery", "must", "learn/route53.html", "DNS, routing policies, health checks, failover.", "alias latency geo"),
    ("Amazon CloudFront", "Networking and Content Delivery", "must", "learn/cloudfront.html", "CDN, OAC, signed URLs, edge functions.", "cdn oai"),
    ("AWS Global Accelerator", "Networking and Content Delivery", "must", "learn/cloudfront.html", "Anycast static IPs over the AWS backbone.", "ga anycast"),
    ("Amazon SQS", "Application Integration", "must", "learn/messaging.html", "Queues for loose coupling, standard vs FIFO.", "queue dlq"),
    ("Amazon SNS", "Application Integration", "must", "learn/messaging.html", "Pub/sub fan-out to many subscribers.", "topic"),
    ("Amazon Kinesis", "Analytics", "must", "learn/messaging.html", "Real-time streaming with multiple consumers.", "data streams"),
    ("Amazon Data Firehose", "Analytics", "must", "learn/messaging.html", "Load streams into S3, Redshift, OpenSearch.", "kinesis firehose"),
    ("AWS Lambda", "Serverless", "must", "learn/lambda.html", "Event-driven compute, 15 minute max.", "function"),
    ("Amazon API Gateway", "Front-End Web and Mobile", "must", "learn/dynamodb.html", "REST/HTTP/WebSocket APIs in front of Lambda.", "rest http"),
    ("AWS Step Functions", "Application Integration", "must", "learn/lambda.html", "Orchestrate serverless workflows.", "state machine"),
    ("Amazon EventBridge", "Application Integration", "must", "learn/monitoring.html", "Event bus, SaaS events, scheduled rules.", "event bus"),
    ("Amazon CloudWatch", "Management and Governance", "must", "learn/monitoring.html", "Metrics, logs, alarms, dashboards.", "alarm"),
    ("AWS CloudTrail", "Management and Governance", "must", "learn/monitoring.html", "API audit trail for governance.", "audit"),
    ("AWS Config", "Management and Governance", "must", "learn/governance.html", "Record configuration and evaluate rules.", "compliance"),
    ("AWS CloudFormation", "Management and Governance", "must", "learn/governance.html", "Infrastructure as code templates and stacks.", "iac"),
    ("AWS Systems Manager", "Management and Governance", "must", "learn/governance.html", "Session Manager, Parameter Store, Patch Manager.", "ssm"),
    ("Amazon ECS", "Containers", "must", "learn/containers.html", "AWS-native container orchestration.", "fargate tasks"),
    ("Amazon EKS", "Containers", "must", "learn/containers.html", "Managed Kubernetes control plane.", "kubernetes"),
    ("AWS Fargate", "Serverless", "must", "learn/containers.html", "Serverless compute for ECS/EKS tasks.", "no servers"),
    ("AWS Direct Connect", "Networking and Content Delivery", "must", "learn/networking-advanced.html", "Dedicated private link from on-premises.", "dx vif"),
    ("AWS Site-to-Site VPN", "Networking and Content Delivery", "must", "learn/networking-advanced.html", "IPsec VPN, fast to set up, internet path.", "vpn"),
    ("AWS Transit Gateway", "Networking and Content Delivery", "must", "learn/networking-advanced.html", "Hub-and-spoke for many VPCs and on-prem.", "tgw"),
    ("AWS WAF", "Security, Identity, and Compliance", "must", "learn/security.html", "Layer 7 firewall for ALB, CloudFront, API Gateway.", "sql injection xss"),
    ("AWS Shield", "Security, Identity, and Compliance", "must", "learn/security.html", "DDoS protection. Standard is free.", "ddos"),
    ("AWS Secrets Manager", "Security, Identity, and Compliance", "must", "learn/security.html", "Rotate database secrets automatically.", "password rotation"),
    ("AWS Backup", "Storage", "must", "learn/migration.html", "Central backup policies across services.", "restore"),
    ("AWS DMS", "Migration and Transfer", "must", "learn/migration.html", "Homogeneous and heterogeneous database migration.", "cdc sct"),
    ("AWS DataSync", "Migration and Transfer", "must", "learn/storage.html", "Online data movement to S3/EFS/FSx.", "migration"),
    ("AWS Storage Gateway", "Storage", "must", "learn/storage.html", "Hybrid file, volume, and tape gateways.", "file gateway"),
    ("AWS Snow Family", "Migration and Transfer", "must", "learn/storage.html", "Offline petabyte-scale transfer appliances.", "snowball edge"),
    ("AWS Cost Explorer", "AWS Cost Management", "must", "learn/cost.html", "Visualize and forecast spend.", "billing"),
    ("AWS Budgets", "AWS Cost Management", "must", "learn/cost.html", "Alerts when cost or usage exceeds a threshold.", "alert"),
    ("Savings Plans", "AWS Cost Management", "must", "learn/cost.html", "1 or 3 year compute discount commitment.", "compute sp"),
    # Should
    ("Amazon GuardDuty", "Security, Identity, and Compliance", "should", "learn/security.html", "Threat detection from CloudTrail, VPC Flow, DNS.", "ids"),
    ("Amazon Inspector", "Security, Identity, and Compliance", "should", "learn/security.html", "Vulnerability scanning for EC2, ECR, Lambda.", "cve"),
    ("Amazon Macie", "Security, Identity, and Compliance", "should", "learn/security.html", "Discover sensitive data in S3.", "pii"),
    ("AWS Security Hub", "Security, Identity, and Compliance", "should", "learn/security.html", "Central findings from GuardDuty, Inspector, Macie.", "cspm"),
    ("Amazon Cognito", "Security, Identity, and Compliance", "should", "learn/identity-federation.html", "User pools and identity pools for apps.", "user pool"),
    ("IAM Identity Center", "Security, Identity, and Compliance", "should", "learn/identity-federation.html", "SSO across accounts and applications.", "sso"),
    ("AWS Directory Service", "Security, Identity, and Compliance", "should", "learn/identity-federation.html", "Managed Microsoft AD and AD Connector.", "microsoft ad"),
    ("AWS Network Firewall", "Security, Identity, and Compliance", "should", "learn/networking-advanced.html", "Managed IPS/IDS at VPC perimeter.", "dpi"),
    ("AWS Firewall Manager", "Security, Identity, and Compliance", "should", "learn/security.html", "Org-wide WAF, Shield, and SG policies.", "central"),
    ("AWS RAM", "Security, Identity, and Compliance", "should", "learn/specialty-security.html", "Share subnets, TGW, and other resources.", "resource access manager"),
    ("AWS CloudHSM", "Security, Identity, and Compliance", "should", "learn/specialty-security.html", "Dedicated HSM when you need FIPS single-tenant keys.", "hsm"),
    ("AWS Elastic Beanstalk", "Compute", "should", "learn/containers.html", "PaaS: upload code, AWS runs the platform.", "paas"),
    ("AWS Batch", "Compute", "should", "learn/containers.html", "Managed batch jobs on EC2 or Fargate.", "queue jobs"),
    ("AWS Outposts", "Compute", "should", "learn/hybrid-edge.html", "AWS racks running in your datacenter.", "hybrid"),
    ("AWS Transfer Family", "Migration and Transfer", "should", "learn/migration.html", "SFTP/FTPS/FTP into S3 or EFS.", "sftp"),
    ("AWS AppSync", "Application Integration", "should", "learn/integration-extras.html", "Managed GraphQL APIs.", "graphql"),
    ("Amazon MSK", "Analytics", "should", "learn/integration-extras.html", "Managed Apache Kafka.", "kafka"),
    ("AWS Glue", "Analytics", "should", "learn/analytics.html", "Serverless ETL and Data Catalog.", "crawler"),
    ("Amazon Athena", "Analytics", "should", "learn/analytics.html", "SQL over S3, pay per TB scanned.", "presto"),
    ("Amazon Redshift", "Analytics", "should", "learn/analytics.html", "Petabyte data warehouse.", "spectrum"),
    ("Amazon EMR", "Analytics", "should", "learn/analytics.html", "Managed Hadoop/Spark clusters.", "spark"),
    ("Amazon OpenSearch Service", "Analytics", "should", "learn/analytics.html", "Search and log analytics.", "elasticsearch"),
    ("AWS Lake Formation", "Analytics", "should", "learn/analytics.html", "Governed data lake permissions.", "lake"),
    ("Amazon QuickSight", "Analytics", "should", "learn/analytics.html", "BI dashboards (Quick Suite on the exam).", "quicksight"),
    ("Amazon Rekognition", "Machine Learning", "should", "learn/ml.html", "Images and video: faces, objects, moderation.", "vision"),
    ("Amazon Transcribe", "Machine Learning", "should", "learn/ml.html", "Speech to text.", "stt"),
    ("Amazon Polly", "Machine Learning", "should", "learn/ml.html", "Text to speech.", "tts"),
    ("Amazon Translate", "Machine Learning", "should", "learn/ml.html", "Language translation.", "i18n"),
    ("Amazon Comprehend", "Machine Learning", "should", "learn/ml.html", "NLP: sentiment, entities, PII.", "nlp"),
    ("Amazon Textract", "Machine Learning", "should", "learn/ml.html", "Extract text and forms from documents.", "ocr"),
    ("Amazon Lex", "Machine Learning", "should", "learn/ml.html", "Chatbots (same tech as Alexa).", "bot"),
    ("Amazon SageMaker AI", "Machine Learning", "should", "learn/ml.html", "Build, train, and deploy ML models.", "notebook"),
    ("AWS X-Ray", "Developer Tools", "should", "learn/monitoring.html", "Trace distributed applications.", "trace"),
    ("AWS Trusted Advisor", "Management and Governance", "should", "learn/governance.html", "Checks for cost, security, limits, performance.", "support"),
    ("AWS Compute Optimizer", "Management and Governance", "should", "learn/cost.html", "Right-size EC2, EBS, Lambda, Auto Scaling.", "rightsizing"),
    ("Amazon MQ", "Application Integration", "should", "learn/messaging.html", "Managed ActiveMQ/RabbitMQ for legacy brokers.", "activemq"),
    ("Amazon ECR", "Containers", "should", "learn/containers.html", "Container image registry.", "docker"),
    ("AWS Application Migration Service", "Migration and Transfer", "should", "learn/migration.html", "Lift and shift servers (MGN).", "mgn"),
    ("AWS Client VPN", "Networking and Content Delivery", "should", "learn/networking-advanced.html", "Managed VPN for users into a VPC.", "client vpn"),
    ("AWS Cost and Usage Report", "AWS Cost Management", "must", "learn/cost.html", "Most detailed billing export to S3.", "cur"),
    # Name-only
    ("Amazon AppFlow", "Application Integration", "name", "learn/integration-extras.html", "SaaS to AWS data transfer (Salesforce, etc.).", "saas"),
    ("AWS Data Exchange", "Analytics", "name", "learn/analytics.html", "Third-party datasets in AWS.", "dataset"),
    ("AWS Amplify", "Front-End Web and Mobile", "name", "learn/identity-federation.html", "Frontend hosting and app backend helpers.", "hosting"),
    ("AWS Device Farm", "Front-End Web and Mobile", "name", "learn/identity-federation.html", "Real device testing farm.", "mobile test"),
    ("Amazon DocumentDB", "Database", "name", "learn/specialty-databases.html", "MongoDB-compatible document database.", "mongodb"),
    ("Amazon Neptune", "Database", "name", "learn/specialty-databases.html", "Graph database for relationships.", "gremlin sparql"),
    ("Amazon Keyspaces", "Database", "name", "learn/specialty-databases.html", "Managed Apache Cassandra.", "cassandra"),
    ("Amazon Kendra", "Machine Learning", "name", "learn/ml.html", "Enterprise search over documents.", "search"),
    ("AWS Audit Manager", "Security, Identity, and Compliance", "name", "learn/specialty-security.html", "Collect evidence for audits.", "compliance"),
    ("AWS Artifact", "Security, Identity, and Compliance", "name", "learn/specialty-security.html", "Download AWS compliance reports.", "soc iso"),
    ("Amazon Detective", "Security, Identity, and Compliance", "name", "learn/specialty-security.html", "Investigate findings with a graph of activity.", "investigation"),
    ("AWS License Manager", "Management and Governance", "name", "learn/governance.html", "Track software licenses.", "oracle sql server"),
    ("Amazon Managed Grafana", "Management and Governance", "name", "learn/monitoring.html", "Managed Grafana dashboards.", "grafana"),
    ("Amazon Managed Service for Prometheus", "Management and Governance", "name", "learn/monitoring.html", "Managed Prometheus metrics.", "amp"),
    ("Amazon Elastic Transcoder", "Media Services", "name", "learn/ml.html", "Legacy video transcoding (know the name).", "video"),
    ("Amazon Kinesis Video Streams", "Media Services", "name", "learn/messaging.html", "Ingest video from devices.", "camera"),
    ("AWS Wavelength", "Compute", "name", "learn/hybrid-edge.html", "AWS compute inside 5G carrier networks.", "edge 5g"),
    ("VMware Cloud on AWS", "Compute", "name", "learn/hybrid-edge.html", "VMware SDDC running on AWS.", "vmware"),
    ("AWS Serverless Application Repository", "Compute", "name", "learn/lambda.html", "Publish and deploy serverless apps.", "sar"),
    ("Amazon ECS Anywhere", "Containers", "name", "learn/containers.html", "Run ECS on your own hardware.", "hybrid containers"),
    ("Amazon EKS Anywhere", "Containers", "name", "learn/containers.html", "Run EKS on your own hardware.", "hybrid k8s"),
    ("Amazon EKS Distro", "Containers", "name", "learn/containers.html", "Open-source Kubernetes distribution from AWS.", "eks-d"),
    ("AWS Auto Scaling", "Management and Governance", "name", "learn/elb-asg.html", "Unified scaling plans across multiple resources.", "application auto scaling"),
    ("AWS Health Dashboard", "Management and Governance", "name", "learn/governance.html", "Service health and account events.", "phs"),
    ("AWS CLI", "Management and Governance", "name", "learn/foundations.html", "Command line access to AWS APIs.", "command line"),
    ("AWS Management Console", "Management and Governance", "name", "learn/foundations.html", "Web console for AWS.", "browser"),
    ("AWS Service Catalog", "Management and Governance", "name", "learn/governance.html", "Approved product portfolios for teams.", "portfolio"),
    ("AWS Well-Architected Tool", "Management and Governance", "name", "learn/well-architected.html", "Review workloads against the six pillars.", "lens"),
    ("Amazon Aurora Serverless", "Database", "must", "learn/databases.html", "Aurora that scales to zero and charges per ACU.", "aurora v2"),
]


def generate_catalog_js() -> None:
    items = []
    for name, cat, pri, href, blurb, aliases in SERVICES:
        items.append({
            "name": name,
            "category": cat,
            "priority": pri,
            "href": href,
            "blurb": blurb,
            "aliases": aliases,
        })
    (SITE / "assets/js/catalog-data.js").write_text(
        "window.SAA_CATALOG = " + json.dumps(items, indent=2) + ";\n",
        encoding="utf-8",
    )
    (SITE / "assets/data/services.json").write_text(json.dumps(items, indent=2), encoding="utf-8")


def homepage() -> None:
    cats: dict[str, list] = {}
    for item in SERVICES:
        cats.setdefault(item[1], []).append(item)
    cat_btns = ['<button class="cat-btn active" data-category="all">All categories</button>']
    for cat in cats:
        cat_btns.append(f'<button class="cat-btn" data-category="{esc(cat)}">{esc(cat)}</button>')

    pri_label = {"must": "Must-know", "should": "Should-know", "name": "Know the name"}
    cards = []
    for name, cat, pri, href, blurb, _ in SERVICES:
        cards.append(
            f'<a class="card svc svc-card" data-priority="{pri}" data-category="{esc(cat)}" href="{href}">'
            f'<span class="pill {pri}">{pri_label[pri]}</span>'
            f'<div class="name">{esc(name)}</div>'
            f'<p>{esc(blurb)}</p></a>'
        )

    content = f"""
    <section class="hero">
      <div class="pill domain">AWS Certified Solutions Architect – Associate</div>
      <h1>Learn the services SAA-C03 actually tests</h1>
      <p class="lede">Official in-scope services, ranked by how often they appear. Every Learn chapter starts with beginner fundamentals (why / what / where / which), then use cases, diagrams aligned to AWS docs, and exam case studies. Start with <strong>Must</strong>. On the exam: meet every constraint first, then pick the cheapest option that still works.</p>
      <div class="domain-bar" title="Domain weights"><span></span><span></span><span></span><span></span></div>
      <div class="stats">
        <div class="stat"><b>65</b><span>questions · 130 minutes</span></div>
        <div class="stat"><b>720</b><span>passing score / 1000</span></div>
        <div class="stat"><b>30%</b><span>Domain 1 Security</span></div>
        <div class="stat"><b>50 + 15</b><span>scored + unmarked</span></div>
      </div>
    </section>
    <p>Filter the catalog, then open a topic. Use the <a href="compare/storage.html">decision pages</a> after each cluster — that is how SAA questions are written.</p>
    <div class="filters">
      <button class="filter-btn active" data-priority="all">All</button>
      <button class="filter-btn" data-priority="must">Must-know</button>
      <button class="filter-btn" data-priority="should">Should-know</button>
      <button class="filter-btn" data-priority="name">Know the name</button>
    </div>
    <div class="filters">{''.join(cat_btns)}</div>
    <p class="lede">Showing <strong id="shown-count">{len(SERVICES)}</strong> services.</p>
    <div id="service-catalog" class="grid">{''.join(cards)}</div>
    <h2>How to use this site</h2>
    <ol>
      <li>Read <a href="exam/overview.html">exam overview</a> once so scoring and question style are clear.</li>
      <li>Study Must-know pages in this order: IAM → KMS/S3 → VPC → EC2/ELB → databases → Route 53/CloudFront → messaging/Lambda → cost.</li>
      <li>After each topic, drill the matching <a href="compare/storage.html">compare page</a>.</li>
      <li>Skip everything on <a href="exam/out-of-scope.html">out of scope</a>. Do not deep-dive Know-the-name services.</li>
    </ol>
    """
    write("index.html", "SAA-C03 service catalog", "Home", content)


def exam_overview() -> None:
    content = f"""
    <h1>SAA-C03 exam overview</h1>
    {pills([("domain", "Official guide"), ("must", "Read once")])}
    <p class="lede">This exam checks that you can design AWS solutions that are secure, resilient, fast enough, and not wasteful — then improve a design that already exists. You do not need to memorize every API. You need to understand <em>why</em> a service exists and which constraint it satisfies.</p>
    <div class="fundamentals">
      <h2>Start here — the W questions</h2>
      <div class="w-grid">
        <div class="w-card"><h3>Why</h3><p>AWS wants architects who pick the right building blocks for a business story: who can access what, what happens if an AZ dies, how to scale, and how to avoid paying for idle capacity.</p></div>
        <div class="w-card"><h3>What</h3><p>65 questions (50 scored), 130 minutes, pass at 720/1000. Multiple choice and multiple response. Compensatory scoring — overall score matters, not a pass in every domain.</p></div>
        <div class="w-card"><h3>Where</h3><p>Study path on this site: Foundations → high-weight Learn chapters (IAM, S3, VPC, EC2, ELB, databases, messaging) → Compare pickers → practice decoding question verbs.</p></div>
        <div class="w-card"><h3>Which habit scores</h3><p>Meet <strong>every</strong> constraint in the stem first. Only then choose the cheapest or simplest remaining answer. Multi-AZ is high availability; Multi-Region is disaster recovery.</p></div>
      </div>
    </div>
    {mermaid('''
flowchart TD
  req[BusinessRequirement]
  req --> security[WhoCanAccessAndHowEncrypted]
  req --> coupling[StatefulOrDecoupled]
  req --> scale[ScaleVerticallyOrHorizontally]
  req --> ha[SingleAZ_MultiAZ_Or_MultiRegion]
  req --> cost[OnDemand_RI_SP_Or_Spot]
  security --> pick[PickTheSmallestFit]
  coupling --> pick
  scale --> pick
  ha --> pick
  cost --> pick
''')}
    <h2>Format and scoring</h2>
    <table>
      <thead><tr><th>Item</th><th>Detail</th></tr></thead>
      <tbody>
        <tr><td>Questions</td><td>65 total: 50 scored + 15 unscored (unmarked)</td></tr>
        <tr><td>Time</td><td>130 minutes</td></tr>
        <tr><td>Types</td><td>Multiple choice (1 of 4) and multiple response (2+ of 5+)</td></tr>
        <tr><td>Score</td><td>Scaled 100–1000. Pass at 720</td></tr>
        <tr><td>Model</td><td>Compensatory: you need the overall pass, not every domain</td></tr>
        <tr><td>Guessing</td><td>Unanswered is wrong. There is no penalty for guessing</td></tr>
      </tbody>
    </table>
    <h2>Domain weights</h2>
    <div class="domain-bar"><span></span><span></span><span></span><span></span></div>
    <table>
      <thead><tr><th>Domain</th><th>Weight</th><th>What it really tests</th></tr></thead>
      <tbody>
        <tr><td><a href="domain-1-secure.html">1. Design Secure Architectures</a></td><td>30%</td><td>IAM, encryption, VPC isolation, threat services</td></tr>
        <tr><td><a href="domain-2-resilient.html">2. Design Resilient Architectures</a></td><td>26%</td><td>Decoupling, Multi-AZ, DR, failover</td></tr>
        <tr><td><a href="domain-3-performance.html">3. Design High-Performing Architectures</a></td><td>24%</td><td>Right storage/compute/DB/network for speed</td></tr>
        <tr><td><a href="domain-4-cost.html">4. Design Cost-Optimized Architectures</a></td><td>20%</td><td>Cheapest option that still meets the requirement</td></tr>
      </tbody>
    </table>
    <h2>Question language — decode the verb</h2>
    <div class="says-pick"><div class="if">If the question says</div><div class="then">most cost-effective</div><p>Spot, Savings Plans, S3 lifecycle, serverless, right-size. Drop over-provisioned or unused premium features.</p></div>
    <div class="says-pick"><div class="if">If the question says</div><div class="then">least operational overhead / operationally efficient</div><p>Managed and serverless: Fargate, Lambda, Aurora Serverless, RDS, S3. Drop self-managed EC2.</p></div>
    <div class="says-pick"><div class="if">If the question says</div><div class="then">highly available / fault tolerant</div><p>Multi-AZ, ELB, Auto Scaling, Aurora 6 copies, S3 11 nines. Drop single-AZ and single instance.</p></div>
    <div class="says-pick"><div class="if">If the question says</div><div class="then">secure / least privilege</div><p>Roles not access keys, private subnets, VPC endpoints, KMS CMK, SG not 0.0.0.0/0.</p></div>
    <div class="exam-trap"><strong class="label">High-score habit</strong> For every practice question, write why the other three options fail. Distractors are valid AWS services used in the wrong constraint.</div>
    {docs([
        ("SAA-C03 exam guide", "https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html"),
        ("In-scope services", "https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/saa-03-in-scope-services.html"),
        ("Out-of-scope services", "https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/saa-03-out-of-scope-services.html"),
    ])}
    """
    write("exam/overview.html", "Exam overview", "Exam / Overview", content)


def domain_pages() -> None:
    d1 = f"""
    <h1>Domain 1 — Design Secure Architectures (30%)</h1>
    {pills([("must", "Highest weight"), ("domain", "Tasks 1.1–1.3")])}
    <p class="lede">Almost a third of scored questions. If time is short, this domain plus S3/VPC still moves the score most.</p>
    <h2>Task 1.1 Secure access to AWS resources</h2>
    <ul>
      <li>IAM users, groups, roles, policies, permission boundaries, STS, MFA, root user hygiene</li>
      <li>Cross-account roles, federation, IAM Identity Center, Directory Service</li>
      <li>Organizations, OUs, SCPs, Control Tower</li>
      <li>Resource policies (S3, SQS, Lambda, KMS, Secrets Manager)</li>
      <li>Shared responsibility and global infrastructure (Regions, AZs)</li>
    </ul>
    <h2>Task 1.2 Secure workloads and applications</h2>
    <ul>
      <li>VPC: public/private subnets, SG, NACL, NAT, route tables</li>
      <li>VPC endpoints and PrivateLink instead of public AWS APIs</li>
      <li>VPN and Direct Connect for on-premises</li>
      <li>WAF, Shield, Cognito, GuardDuty, Macie, Secrets Manager, ACM</li>
      <li>DDoS, SQL injection, and other external threat vectors</li>
    </ul>
    <h2>Task 1.3 Data security controls</h2>
    <ul>
      <li>Encryption at rest with KMS; encryption in transit with TLS/ACM</li>
      <li>Key policies, rotation, CloudHSM when dedicated HSM is required</li>
      <li>Backups, replication, S3 Object Lock, lifecycle, classification (Macie)</li>
    </ul>
    {related("../", [("learn/iam.html", "IAM"), ("learn/security.html", "KMS / WAF"), ("learn/vpc.html", "VPC"), ("learn/s3.html", "S3 encryption")])}
    """
    d2 = f"""
    <h1>Domain 2 — Design Resilient Architectures (26%)</h1>
    {pills([("must", "Second highest"), ("domain", "Tasks 2.1–2.2")])}
    <h2>Task 2.1 Scalable and loosely coupled</h2>
    <ul>
      <li>Multi-tier, microservices, stateless vs stateful</li>
      <li>SQS, SNS, EventBridge, Step Functions, API Gateway</li>
      <li>ALB, Auto Scaling, Lambda, Fargate, ECS, EKS</li>
      <li>Caching, read replicas, edge (CloudFront)</li>
      <li>Object vs file vs block storage</li>
    </ul>
    <h2>Task 2.2 Highly available and fault-tolerant</h2>
    <ul>
      <li>Multi-AZ vs Multi-Region, Route 53 failover</li>
      <li>DR: backup/restore, pilot light, warm standby, active-active; RPO/RTO</li>
      <li>RDS Proxy, immutable infrastructure, quotas/throttling</li>
      <li>S3 durability, backups, X-Ray for visibility</li>
    </ul>
    {related("../", [("compare/dr.html", "DR picker"), ("learn/messaging.html", "Decoupling"), ("learn/elb-asg.html", "ELB / ASG"), ("learn/migration.html", "Migration & DR")])}
    """
    d3 = f"""
    <h1>Domain 3 — Design High-Performing Architectures (24%)</h1>
    {pills([("should", "Right tool for the job"), ("domain", "Tasks 3.1–3.5")])}
    <ul>
      <li><strong>3.1 Storage:</strong> S3 / EBS / EFS / FSx / hybrid (DataSync, Storage Gateway)</li>
      <li><strong>3.2 Compute:</strong> instance families, Lambda memory, Fargate, Batch, EMR, Auto Scaling metrics</li>
      <li><strong>3.3 Databases:</strong> Aurora vs DynamoDB vs ElastiCache, read replicas, DAX, RDS Proxy</li>
      <li><strong>3.4 Network:</strong> CloudFront vs Global Accelerator, ALB vs NLB, VPN / DX / PrivateLink</li>
      <li><strong>3.5 Ingestion:</strong> Kinesis, Firehose, Glue, Athena, Lake Formation, DataSync</li>
    </ul>
    {related("../", [("compare/storage.html", "Storage"), ("compare/compute.html", "Compute"), ("compare/databases.html", "Databases"), ("compare/networking.html", "Networking")])}
    """
    d4 = f"""
    <h1>Domain 4 — Design Cost-Optimized Architectures (20%)</h1>
    {pills([("must", "Constraint on almost every question"), ("domain", "Tasks 4.1–4.4")])}
    <p>Cost is only 20% by weight, but “most cost-effective” appears across other domains. Never pick a cheaper option that breaks HA, security, or performance requirements.</p>
    <ul>
      <li><strong>Storage:</strong> S3 classes and lifecycle, EBS gp3 vs io2, EFS IA, Glacier, Requester Pays</li>
      <li><strong>Compute:</strong> Spot, Savings Plans, RI, right-size, Graviton, Lambda, Fargate, hibernate</li>
      <li><strong>Database:</strong> Aurora Serverless, DynamoDB on-demand vs provisioned, RDS reserved, stop non-prod</li>
      <li><strong>Network:</strong> NAT count per AZ vs shared NAT, VPC endpoints vs NAT to S3, CloudFront to cut data transfer, DX vs VPN</li>
    </ul>
    <div class="exam-tip"><strong class="label">Exam tip</strong> NAT Gateway is billed hourly plus per-GB. A VPC gateway endpoint to S3/DynamoDB is free and is often the cost answer for private-subnet access to those APIs.</div>
    {related("../", [("learn/cost.html", "Cost page"), ("compare/compute.html", "Compute picker"), ("learn/s3.html", "S3 classes")])}
    """
    write("exam/domain-1-secure.html", "Domain 1 Secure", "Exam / Domain 1", d1)
    write("exam/domain-2-resilient.html", "Domain 2 Resilient", "Exam / Domain 2", d2)
    write("exam/domain-3-performance.html", "Domain 3 Performance", "Exam / Domain 3", d3)
    write("exam/domain-4-cost.html", "Domain 4 Cost", "Exam / Domain 4", d4)

    oos = f"""
    <h1>Out of scope — do not study these</h1>
    {pills([("skip", "Official out-of-scope list")])}
    <p class="lede">The official list is non-exhaustive. If a service is here, skip deep study even if a blog post mentions it. These pages mark them as skip so you spend time on in-scope architecture.</p>
    <table>
      <thead><tr><th>Category</th><th>Out of scope</th></tr></thead>
      <tbody>
        <tr><td>Compute</td><td>Amazon Lightsail</td></tr>
        <tr><td>Developer Tools</td><td>CDK, CloudShell, CodeArtifact, CodeBuild, CodeCommit, CodeDeploy, Corretto, FIS, Tools and SDKs</td></tr>
        <tr><td>Application Integration</td><td>Amazon MWAA (Managed Airflow)</td></tr>
        <tr><td>AR / VR</td><td>Amazon Sumerian</td></tr>
        <tr><td>Blockchain</td><td>Amazon Managed Blockchain</td></tr>
        <tr><td>Database</td><td>Amazon RDS on VMware</td></tr>
        <tr><td>Front-end</td><td>Amazon Location Service</td></tr>
        <tr><td>Game Tech</td><td>Amazon GameLift</td></tr>
        <tr><td>IoT</td><td>All IoT services</td></tr>
        <tr><td>Machine Learning</td><td>Personalize, SageMaker Canvas, SageMaker Ground Truth, A2I, DeepComposer, DLAMI, Deep Learning Containers, DevOps Guru, Elastic Inference, HealthLake, Inferentia, MXNet / PyTorch / TensorFlow on AWS</td></tr>
        <tr><td>Management</td><td>Console Mobile App, Distro for OpenTelemetry</td></tr>
        <tr><td>Media</td><td>Elemental appliances, MediaConnect/Convert/Live/Package/Tailor, Amazon IVS</td></tr>
        <tr><td>Migration</td><td>Migration Evaluator</td></tr>
        <tr><td>Networking</td><td>AWS Cloud Map</td></tr>
        <tr><td>Quantum</td><td>Amazon Braket</td></tr>
        <tr><td>Satellite</td><td>AWS Ground Station</td></tr>
      </tbody>
    </table>
    <div class="exam-skip"><strong class="label">Skip in CS21</strong> Amazon Personalize is officially out of scope. Forecast, Connect, and Fraud Detector are not on the in-scope list — treat as low value.</div>
    """
    write("exam/out-of-scope.html", "Out of scope", "Exam / Out of scope", oos)


CHAPTERS = [
    ("learn/foundations.html", "Foundations", "Learn / Foundations", "foundations.html"),
    ("learn/well-architected.html", "Well-Architected Framework", "Learn / Well-Architected", "well-architected.html"),
    ("learn/iam.html", "IAM", "Learn / IAM", "iam.html"),
    ("learn/identity-federation.html", "Cognito and federation", "Learn / Federation", "identity-federation.html"),
    ("learn/security.html", "KMS, WAF, Shield", "Learn / Security", "security.html"),
    ("learn/specialty-security.html", "Security extras", "Learn / Security extras", "specialty-security.html"),
    ("learn/s3.html", "Amazon S3", "Learn / S3", "s3.html"),
    ("learn/storage.html", "EBS, EFS, FSx", "Learn / Storage", "storage.html"),
    ("learn/ec2.html", "Amazon EC2", "Learn / EC2", "ec2.html"),
    ("learn/elb-asg.html", "Auto Scaling and ELB", "Learn / ELB & ASG", "elb-asg.html"),
    ("learn/vpc.html", "Amazon VPC", "Learn / VPC", "vpc.html"),
    ("learn/networking-advanced.html", "Hybrid networking", "Learn / Hybrid networking", "networking-advanced.html"),
    ("learn/route53.html", "Amazon Route 53", "Learn / Route 53", "route53.html"),
    ("learn/cloudfront.html", "CloudFront and Global Accelerator", "Learn / Edge", "cloudfront.html"),
    ("learn/databases.html", "RDS, Aurora, ElastiCache", "Learn / Databases", "databases.html"),
    ("learn/dynamodb.html", "DynamoDB and API Gateway", "Learn / DynamoDB", "dynamodb.html"),
    ("learn/specialty-databases.html", "Specialty databases", "Learn / Specialty DBs", "specialty-databases.html"),
    ("learn/messaging.html", "SQS, SNS, Kinesis", "Learn / Messaging", "messaging.html"),
    ("learn/lambda.html", "Lambda and Step Functions", "Learn / Serverless", "lambda.html"),
    ("learn/integration-extras.html", "AppSync, MSK, AppFlow", "Learn / Integration extras", "integration-extras.html"),
    ("learn/monitoring.html", "CloudWatch and CloudTrail", "Learn / Monitoring", "monitoring.html"),
    ("learn/containers.html", "ECS, EKS, Fargate", "Learn / Containers", "containers.html"),
    ("learn/migration.html", "Migration and disaster recovery", "Learn / Migration & DR", "migration.html"),
    ("learn/analytics.html", "Analytics", "Learn / Analytics", "analytics.html"),
    ("learn/governance.html", "Organizations and Config", "Learn / Governance", "governance.html"),
    ("learn/cost.html", "Cost optimization", "Learn / Cost", "cost.html"),
    ("learn/hybrid-edge.html", "Outposts and Wavelength", "Learn / Hybrid", "hybrid-edge.html"),
    ("learn/ml.html", "Machine learning services", "Learn / ML", "ml.html"),
]


def learn_chapters() -> None:
    missing = []
    for out, title, crumb, src in CHAPTERS:
        path = ROOT / "tools/chapters" / src
        if not path.exists():
            missing.append(str(path))
            continue
        write(out, title, crumb, path.read_text(encoding="utf-8"))
    if missing:
        raise SystemExit("Missing chapters:\n" + "\n".join(missing))


COMPARE = [
    ("compare/storage.html", "Storage picker", "Compare / Storage", "storage.html"),
    ("compare/databases.html", "Database picker", "Compare / Databases", "databases.html"),
    ("compare/messaging.html", "Messaging picker", "Compare / Messaging", "messaging.html"),
    ("compare/compute.html", "Compute picker", "Compare / Compute", "compute.html"),
    ("compare/networking.html", "Networking picker", "Compare / Networking", "networking.html"),
    ("compare/dr.html", "DR picker", "Compare / DR", "dr.html"),
]


def compare_pages() -> None:
    missing = []
    for out, title, crumb, src in COMPARE:
        path = ROOT / "tools/compare" / src
        if not path.exists():
            missing.append(str(path))
            continue
        write(out, title, crumb, path.read_text(encoding="utf-8"))
    if missing:
        raise SystemExit("Missing compare pages:\n" + "\n".join(missing))


def sinhala() -> None:
    content = f"""
    <h1 lang="si">සිංහල සටහන් · Sinhala study notes</h1>
    {pills([("name", "Placeholder"), ("should", "Paste later")])}
    <p class="lede">English pages are complete. Drop exported Claude artifacts here when you have them. This page already loads Noto Sans Sinhala.</p>
    <div class="dropzone" lang="si">
      <p><strong>ඔබේ Claude artifacts මෙහි එකතු කරන්න.</strong></p>
      <p>Save each artifact as HTML under <code>site/sinhala/</code> (for example <code>iam-si.html</code>) and add a card on this page.</p>
      <p>Keep the same topic titles as the English Learn pages so you can switch languages without losing your place.</p>
    </div>
    <h2>Suggested mapping when you paste</h2>
    <table>
      <thead><tr><th>English page</th><th>Create</th></tr></thead>
      <tbody>
        <tr><td>IAM</td><td><code>sinhala/iam-si.html</code></td></tr>
        <tr><td>S3</td><td><code>sinhala/s3-si.html</code></td></tr>
        <tr><td>VPC</td><td><code>sinhala/vpc-si.html</code></td></tr>
        <tr><td>EC2 / ELB</td><td><code>sinhala/compute-si.html</code></td></tr>
        <tr><td>Databases</td><td><code>sinhala/databases-si.html</code></td></tr>
      </tbody>
    </table>
    <p>Until then, study the English <a href="../learn/foundations.html">foundations</a> and <a href="../compare/storage.html">decision pages</a> — those are the high-score path.</p>
    """
    write("sinhala/index.html", "Sinhala notes", "Sinhala", content)


def main() -> None:
    SITE.mkdir(parents=True, exist_ok=True)
    generate_catalog_js()
    homepage()
    exam_overview()
    domain_pages()
    learn_chapters()
    compare_pages()
    sinhala()
    print(f"Wrote site into {SITE}")


if __name__ == "__main__":
    main()
