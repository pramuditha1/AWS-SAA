# CS21: Machine Learning on AWS
### AWS SAA-C03 Cheat Sheet

---

## ML Services Overview (SAA-C03 Level)

> **Note**: SAA exam tests ML services at a **high level** — know WHAT each service does and WHEN to use it. No deep ML knowledge needed.

---

## Amazon Rekognition

### What It Does
- **Image and video analysis** using deep learning
- No ML expertise needed

### Capabilities
| Feature | Description |
|---------|-------------|
| Object/Scene detection | Identify objects, scenes in images |
| Facial analysis | Detect faces, emotions, age range, gender |
| Face comparison | Compare faces (identity verification) |
| Celebrity recognition | Identify famous people |
| Text in images | Extract text (OCR) from images/video |
| Content moderation | Detect inappropriate/unsafe content |
| Custom labels | Train on your own images |
| PPE Detection | Detect personal protective equipment |
| Video analysis | People pathing, activity detection |

### Use Cases
- User identity verification (face comparison)
- Content moderation (social media)
- Surveillance and security (face detection)
- Media asset management (auto-tagging)

> **Exam Tip**: "Detect faces/objects in images" or "content moderation" = Rekognition.

---

## Amazon Transcribe

### What It Does
- **Speech-to-text** (automatic speech recognition - ASR)
- Convert audio to text

### Key Features
- Real-time or batch transcription
- Multi-language support
- Custom vocabulary (industry terms)
- **PII redaction** (automatically remove sensitive info)
- Automatic language identification
- Speaker diarization (identify different speakers)

### Use Cases
- Meeting transcription, call center analytics
- Subtitles/closed captioning
- Medical transcription (Transcribe Medical)

> **Exam Tip**: "Convert speech/audio to text" = Transcribe. "Transcribe medical conversations" = Transcribe Medical.

---

## Amazon Polly

### What It Does
- **Text-to-speech** (opposite of Transcribe)
- Turns text into lifelike speech

### Key Features
- Multiple voices and languages
- **SSML** support (control pronunciation, speed, emphasis)
- **Lexicons**: Customize pronunciation of specific words
- **Neural TTS**: More natural-sounding speech
- **Speech Marks**: Lip-sync metadata

### Use Cases
- Accessibility (read content aloud)
- Voice response systems (IVR)
- E-learning content narration
- IoT devices (Alexa-style responses)

> **Exam Tip**: "Convert text to speech" or "read articles aloud" = Polly.

---

## Amazon Translate

### What It Does
- **Neural machine translation** (language translation)
- Translate text between languages

### Key Features
- 75+ languages
- Real-time and batch translation
- Custom terminology (preserve brand names, technical terms)
- Active Custom Translation (adapt to your domain)
- Integrates with other services (Transcribe → Translate → Polly pipeline)

> **Exam Tip**: "Translate content to multiple languages" = Translate.

---

## Amazon Lex

### What It Does
- Build **conversational chatbots** (same tech as Alexa)
- Natural Language Understanding (NLU) + Automatic Speech Recognition (ASR)

### Key Concepts
- **Intents**: What the user wants to do (BookFlight, OrderPizza)
- **Utterances**: Ways users express intent ("I want to book a flight")
- **Slots**: Parameters to fulfill intent (destination, date, time)
- **Fulfillment**: Action to take (call Lambda function)

### Use Cases
- Customer service chatbots
- Voice-enabled applications
- Call center automation (with Amazon Connect)

> **Exam Tip**: "Build a chatbot" or "conversational interface" = Lex.

---

## Amazon Connect

### What It Does
- **Cloud-based contact center** (phone system)
- Virtual call center, no hardware needed
- Pay per minute of use

### Key Integration
```
Phone Call → Amazon Connect → Lex (chatbot) → Lambda (logic) → DynamoDB (data)
```

> **Exam Tip**: "Cloud call center" or "phone-based customer service" = Connect.

---

## Amazon Comprehend

### What It Does
- **Natural Language Processing (NLP)** — understand text
- Extract insights from text using ML

### Capabilities
| Feature | Description |
|---------|-------------|
| Sentiment analysis | Positive, negative, neutral, mixed |
| Entity recognition | People, places, dates, organizations |
| Key phrase extraction | Important phrases in text |
| Language detection | Identify language of text |
| Topic modeling | Group documents by topic |
| PII detection | Find personally identifiable information |
| Custom classification | Train on your own categories |

### Use Cases
- Analyze customer reviews (sentiment)
- Document organization and classification
- Compliance (find PII in documents)

> **Exam Tip**: "Sentiment analysis" or "extract meaning from text" = Comprehend. "Find PII in text" = Comprehend (in S3 = Macie).

---

## Amazon Textract

### What It Does
- **Extract text and data from documents** (scanned docs, forms, tables)
- Beyond simple OCR — understands document structure

### Capabilities
- Text extraction from any document (printed + handwritten)
- **Forms**: Extract key-value pairs (Name: John, DOB: 1/1/90)
- **Tables**: Extract tabular data with row/column structure
- **Queries**: Ask specific questions about document content

### Use Cases
- Invoice processing, tax documents
- Medical records digitization
- ID verification (extract from passports, licenses)
- Form processing automation

> **Exam Tip**: "Extract data from forms/invoices/documents" = Textract. "Simple OCR on images" = Rekognition Text.

---

## Amazon SageMaker

### What It Does
- **Build, train, and deploy ML models** at scale
- Full ML workflow platform for data scientists

### Key Features
- Jupyter notebooks (development)
- Built-in algorithms
- Managed training infrastructure
- Model hosting (real-time or batch inference)
- Auto-scaling endpoints
- SageMaker Studio (IDE for ML)

> **Exam Tip**: "Custom ML model development" or "train your own model" = SageMaker. For pre-built AI = use specific service (Rekognition, Comprehend, etc.)

---

## Amazon Forecast

### What It Does
- **Time-series forecasting** using ML
- Predict future values (demand, revenue, inventory)

### Use Cases
- Demand planning (retail inventory)
- Financial forecasting
- Resource planning (capacity)
- Weather impact on sales

> **Exam Tip**: "Predict future demand/sales" = Forecast.

---

## Amazon Kendra

### What It Does
- **Intelligent search** service powered by ML
- Natural language document search (enterprise search)

### Key Features
- Understands natural language questions
- Searches across multiple data sources (S3, RDS, SharePoint, etc.)
- Returns specific answers (not just documents)
- Relevance tuning and feedback

> **Exam Tip**: "Enterprise search across documents" or "find answers in documents" = Kendra.

---

## Amazon Personalize

### What It Does
- **Real-time personalized recommendations**
- Same technology as Amazon.com recommendations

### Use Cases
- Product recommendations (e-commerce)
- Content recommendations (streaming, news)
- Personalized search results
- Targeted marketing

> **Exam Tip**: "Product recommendations" or "personalized user experience" = Personalize.

---

## Amazon Fraud Detector

### What It Does
- **Detect potentially fraudulent activity** using ML
- Online fraud detection

### Use Cases
- Payment fraud
- Account takeover
- Fake account creation
- Identity theft prevention

> **Exam Tip**: "Detect fraud" = Fraud Detector.

---

## Quick Reference - Which Service?

| Need | Service |
|------|---------|
| Detect objects/faces in images | **Rekognition** |
| Speech → Text | **Transcribe** |
| Text → Speech | **Polly** |
| Translate languages | **Translate** |
| Build chatbot | **Lex** |
| Cloud call center | **Connect** |
| Understand text meaning/sentiment | **Comprehend** |
| Extract data from documents | **Textract** |
| Build custom ML models | **SageMaker** |
| Time-series forecasting | **Forecast** |
| Enterprise search | **Kendra** |
| Personalized recommendations | **Personalize** |
| Detect fraud | **Fraud Detector** |
| Detect PII in S3 | **Macie** |
| Simple OCR in images | **Rekognition** (text detection) |
| Complex document OCR with forms/tables | **Textract** |

---

## Common ML Architecture Patterns

### Pattern 1: Content Moderation
```
User uploads image → S3 → Lambda → Rekognition (moderation)
  → If unsafe: reject + notify admin (SNS)
  → If safe: proceed with upload
```

### Pattern 2: Multi-language Customer Service
```
Customer audio → Transcribe (speech→text) → Translate (→ English)
  → Comprehend (sentiment + intent) → Lex (chatbot response)
  → Translate (→ customer language) → Polly (text→speech)
```

### Pattern 3: Document Processing
```
Scanned documents → S3 → Textract (extract data)
  → Comprehend (classify, find PII) → DynamoDB (store structured data)
  → Kendra (make searchable)
```
