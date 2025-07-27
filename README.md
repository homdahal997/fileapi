# File Conversion API Service

A comprehensive, scalable file conversion API service built with Django and Django REST Framework. This service supports conversion between 200+ file formats across various categories including documents, images, audio, video, archives, spreadsheets, presentations, and ebooks.

## 🚀 Features

### Core Conversion Capabilities
- **200+ File Formats**: Support for documents, images, audio, video, archives, spreadsheets, presentations, ebooks
- **Batch Processing**: Convert multiple files simultaneously with progress tracking
- **Asynchronous Processing**: Background job processing with Celery and Redis
- **Real-time Progress**: WebSocket-based progress updates for long-running conversions

### Cloud Storage Integration
- **AWS S3**: Import from and export to Amazon S3 buckets
- **Google Cloud Storage**: Seamless integration with GCS
- **Dropbox**: Direct file import/export from Dropbox accounts
- **Azure Blob Storage**: Support for Microsoft Azure storage
- **OneDrive**: Microsoft OneDrive integration

### Authentication & Security
- **JWT Authentication**: Secure token-based authentication
- **API Key Management**: Generate and manage multiple API keys per user
- **Rate Limiting**: Configurable rate limits based on user tiers
- **Data Encryption**: Encryption in transit and at rest
- **GDPR Compliance**: Privacy-first design with data retention policies

### Developer Experience
- **Interactive Documentation**: Swagger/OpenAPI documentation with live testing
- **SDKs and Code Samples**: Ready-to-use code examples in multiple languages
- **Webhook Notifications**: Real-time notifications for job completion
- **Comprehensive Error Handling**: Detailed error messages and retry mechanisms

### Scalability & Monitoring
- **Horizontal Scaling**: Microservices architecture for easy scaling
- **Health Checks**: Built-in monitoring endpoints
- **Performance Analytics**: Detailed usage and performance metrics
- **Load Balancing**: Ready for deployment behind load balancers

## 🏗️ Architecture

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │    │   API Gateway   │    │   Web Frontend  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
┌─────────────────────────────────────────────────────────────────┐
│                        Django Application                       │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   Authentication│   Conversions   │   Storage Integrations      │
│   - JWT Auth    │   - File Upload │   - AWS S3                  │
│   - API Keys    │   - Format Det. │   - Google Cloud            │
│   - Rate Limit  │   - Queue Jobs  │   - Dropbox                 │
└─────────────────┴─────────────────┴─────────────────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   Redis/Cache   │    │   File Storage  │
│   - User Data   │    │   - Sessions    │    │   - Input Files │
│   - Job Metadata│    │   - Queue Jobs  │    │   - Output Files│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Celery Workers│    │   Celery Beat   │    │   Monitoring    │
│   - File Conv.  │    │   - Cleanup     │    │   - Health      │
│   - Cloud Ops   │    │   - Quotas      │    │   - Metrics     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack
- **Backend**: Django 5.2, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache/Queue**: Redis
- **Task Queue**: Celery with Redis broker
- **Authentication**: JWT, API Keys
- **Documentation**: Swagger/OpenAPI (drf-yasg)
- **File Processing**: Pillow, python-magic, various format-specific libraries
- **Cloud SDKs**: boto3 (AWS), google-cloud-storage, dropbox
- **Deployment**: Docker, Gunicorn, Nginx

## 📋 Prerequisites

- Python 3.12+
- Redis Server
- PostgreSQL (for production)
- FFmpeg (for audio/video conversions)
- ImageMagick (for advanced image processing)
- LibreOffice (for document conversions)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/file-conversion-api.git
cd file-conversion-api
```

### 2. Set Up Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Load Initial Data
```bash
python manage.py loaddata initial_file_formats.json
python manage.py loaddata cloud_storage_providers.json
```

### 7. Start Services

#### Start Redis (required for Celery)
```bash
redis-server
```

#### Start Celery Worker
```bash
celery -A fileconvert_api worker --loglevel=info
```

#### Start Celery Beat (for scheduled tasks)
```bash
celery -A fileconvert_api beat --loglevel=info
```

#### Start Django Development Server
```bash
python manage.py runserver
```

## 📖 API Documentation

### Access Documentation
- **Swagger UI**: http://localhost:8000/
- **ReDoc**: http://localhost:8000/redoc/
- **JSON Schema**: http://localhost:8000/swagger.json

### Authentication Methods

#### 1. JWT Authentication
```bash
# Login to get JWT token
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Use token in subsequent requests
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/v1/conversions/jobs/
```

#### 2. API Key Authentication
```bash
# Generate API key via web interface or API
curl -X POST http://localhost:8000/api/v1/auth/api-keys/generate/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My API Key"}'

# Use API key in requests
curl -H "Authorization: Api-Key YOUR_API_KEY" \
  http://localhost:8000/api/v1/conversions/jobs/
```

### Core API Endpoints

#### File Conversion
```bash
# Upload and convert a file
curl -X POST http://localhost:8000/api/v1/conversions/convert/ \
  -H "Authorization: Api-Key YOUR_API_KEY" \
  -F "file=@document.pdf" \
  -F "output_format=docx" \
  -F "webhook_url=https://your-app.com/webhook"

# Check conversion status
curl -H "Authorization: Api-Key YOUR_API_KEY" \
  http://localhost:8000/api/v1/conversions/jobs/{job_id}/

# Download converted file
curl -H "Authorization: Api-Key YOUR_API_KEY" \
  http://localhost:8000/api/v1/conversions/jobs/{job_id}/download/
```

#### Batch Conversion
```bash
# Start batch conversion
curl -X POST http://localhost:8000/api/v1/conversions/batch-convert/ \
  -H "Authorization: Api-Key YOUR_API_KEY" \
  -F "files=@file1.pdf" \
  -F "files=@file2.doc" \
  -F "files=@file3.txt" \
  -F "output_format=docx" \
  -F "name=Document Batch"
```

#### Cloud Storage Integration
```bash
# List storage providers
curl -H "Authorization: Api-Key YOUR_API_KEY" \
  http://localhost:8000/api/v1/storage/providers/

# Connect cloud storage
curl -X POST http://localhost:8000/api/v1/storage/connections/ \
  -H "Authorization: Api-Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws_s3",
    "name": "My S3 Bucket",
    "credentials": {
      "access_key_id": "YOUR_ACCESS_KEY",
      "secret_access_key": "YOUR_SECRET_KEY"
    },
    "default_bucket": "my-conversion-bucket"
  }'

# Import file from cloud storage
curl -X POST http://localhost:8000/api/v1/storage/import/ \
  -H "Authorization: Api-Key YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "storage_connection_id": 1,
    "source_path": "/documents/report.pdf",
    "convert_to": "docx"
  }'
```

## 🔄 Supported File Formats

### Documents
- **Input**: PDF, DOC, DOCX, ODT, RTF, TXT, MD, HTML, EPUB
- **Output**: PDF, DOCX, ODT, RTF, TXT, HTML, EPUB

### Images
- **Input**: JPG, JPEG, PNG, GIF, BMP, TIFF, WEBP, SVG, ICO
- **Output**: JPG, PNG, GIF, BMP, TIFF, WEBP, SVG, ICO

### Audio
- **Input**: MP3, WAV, FLAC, AAC, OGG, M4A, WMA
- **Output**: MP3, WAV, FLAC, AAC, OGG

### Video
- **Input**: MP4, AVI, MKV, MOV, WMV, FLV, WEBM
- **Output**: MP4, AVI, MKV, MOV, WEBM

### Archives
- **Input/Output**: ZIP, RAR, 7Z, TAR, GZ, BZ2

### Spreadsheets
- **Input/Output**: XLS, XLSX, ODS, CSV

### Presentations
- **Input/Output**: PPT, PPTX, ODP

### E-books
- **Input/Output**: EPUB, MOBI, AZW, AZW3, FB2

## 🎯 Usage Examples

### Python SDK Example
```python
import requests

class FileConversionClient:
    def __init__(self, api_key, base_url="http://localhost:8000"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Authorization": f"Api-Key {api_key}"}
    
    def convert_file(self, file_path, output_format, webhook_url=None):
        url = f"{self.base_url}/api/v1/conversions/convert/"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'output_format': output_format,
                'webhook_url': webhook_url
            }
            
            response = requests.post(url, headers=self.headers, 
                                   files=files, data=data)
            return response.json()
    
    def get_job_status(self, job_id):
        url = f"{self.base_url}/api/v1/conversions/jobs/{job_id}/"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def download_result(self, job_id, output_path):
        url = f"{self.base_url}/api/v1/conversions/jobs/{job_id}/download/"
        response = requests.get(url, headers=self.headers)
        
        with open(output_path, 'wb') as f:
            f.write(response.content)

# Usage
client = FileConversionClient("your-api-key")
job = client.convert_file("document.pdf", "docx")
print(f"Job ID: {job['id']}")

# Check status
status = client.get_job_status(job['id'])
print(f"Status: {status['status']}")

# Download when completed
if status['status'] == 'completed':
    client.download_result(job['id'], "converted_document.docx")
```

### JavaScript/Node.js Example
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

class FileConversionClient {
    constructor(apiKey, baseUrl = 'http://localhost:8000') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.headers = { 'Authorization': `Api-Key ${apiKey}` };
    }
    
    async convertFile(filePath, outputFormat, webhookUrl = null) {
        const form = new FormData();
        form.append('file', fs.createReadStream(filePath));
        form.append('output_format', outputFormat);
        
        if (webhookUrl) {
            form.append('webhook_url', webhookUrl);
        }
        
        const response = await axios.post(
            `${this.baseUrl}/api/v1/conversions/convert/`,
            form,
            {
                headers: {
                    ...this.headers,
                    ...form.getHeaders()
                }
            }
        );
        
        return response.data;
    }
    
    async getJobStatus(jobId) {
        const response = await axios.get(
            `${this.baseUrl}/api/v1/conversions/jobs/${jobId}/`,
            { headers: this.headers }
        );
        
        return response.data;
    }
    
    async downloadResult(jobId, outputPath) {
        const response = await axios.get(
            `${this.baseUrl}/api/v1/conversions/jobs/${jobId}/download/`,
            {
                headers: this.headers,
                responseType: 'stream'
            }
        );
        
        response.data.pipe(fs.createWriteStream(outputPath));
    }
}

// Usage
const client = new FileConversionClient('your-api-key');

async function convertDocument() {
    try {
        const job = await client.convertFile('document.pdf', 'docx');
        console.log(`Job ID: ${job.id}`);
        
        // Poll for completion
        let status;
        do {
            await new Promise(resolve => setTimeout(resolve, 2000));
            status = await client.getJobStatus(job.id);
            console.log(`Status: ${status.status}`);
        } while (!['completed', 'failed'].includes(status.status));
        
        if (status.status === 'completed') {
            await client.downloadResult(job.id, 'converted_document.docx');
            console.log('File downloaded successfully!');
        }
    } catch (error) {
        console.error('Conversion failed:', error.message);
    }
}

convertDocument();
```

## 🔧 Configuration

### Environment Variables
```bash
# Django Configuration
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=fileconvert_db
DB_USER=fileconvert_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/1

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Google Cloud Storage
GOOGLE_CLOUD_PROJECT=your-gcp-project
GOOGLE_CLOUD_STORAGE_BUCKET=your-gcs-bucket

# Dropbox
DROPBOX_ACCESS_TOKEN=your-dropbox-token

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

## 🚀 Deployment

### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    ffmpeg \
    imagemagick \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "fileconvert_api.wsgi:application"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DB_HOST=db
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - media_files:/app/media
      - static_files:/app/staticfiles

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=fileconvert_db
      - POSTGRES_USER=fileconvert_user
      - POSTGRES_PASSWORD=your-db-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    command: celery -A fileconvert_api worker --loglevel=info
    environment:
      - DEBUG=False
      - DB_HOST=db
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - media_files:/app/media

  celery-beat:
    build: .
    command: celery -A fileconvert_api beat --loglevel=info
    environment:
      - DEBUG=False
      - DB_HOST=db
      - CELERY_BROKER_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  media_files:
  static_files:
```

### Kubernetes Deployment
```yaml
# kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fileconvert-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fileconvert-api
  template:
    metadata:
      labels:
        app: fileconvert-api
    spec:
      containers:
      - name: web
        image: your-registry/fileconvert-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DEBUG
          value: "False"
        - name: DB_HOST
          value: postgres-service
        - name: CELERY_BROKER_URL
          value: redis://redis-service:6379/0
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: fileconvert-api-service
spec:
  selector:
    app: fileconvert-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

## 📊 Monitoring & Analytics

### Health Checks
- **Basic Health**: `/health/`
- **Detailed Health**: `/health/detailed/`
- **Database Health**: `/health/database/`
- **Redis Health**: `/health/redis/`
- **Celery Health**: `/health/celery/`

### Metrics Endpoints
- **Conversion Analytics**: `/api/v1/conversions/analytics/`
- **User Quotas**: `/api/v1/conversions/quota/`
- **Storage Usage**: `/api/v1/storage/usage/`
- **API Key Usage**: `/api/v1/auth/api-keys/{id}/usage/`

### Logging
The application provides comprehensive logging for:
- API requests and responses
- Conversion job status changes
- Authentication attempts
- Storage operations
- System errors and exceptions

## 💰 Business Model

### Pricing Tiers

#### Free Tier
- 100 conversions/month
- 1GB storage
- 1000 API requests/hour
- Email support
- Standard file formats

#### Basic Tier ($9.99/month)
- 1,000 conversions/month
- 10GB storage
- 5,000 API requests/hour
- Priority email support
- All file formats
- Cloud storage integration

#### Professional Tier ($29.99/month)
- 10,000 conversions/month
- 100GB storage
- 20,000 API requests/hour
- Priority support + phone
- Advanced conversion options
- Batch processing
- Webhooks
- Custom branding

#### Enterprise Tier (Custom pricing)
- Unlimited conversions
- Unlimited storage
- Custom rate limits
- Dedicated support
- SLA guarantees
- On-premise deployment
- Custom integrations
- Advanced analytics

## 🗺️ Roadmap

### Phase 1 (MVP) - Completed ✅
- Core file conversion API
- Basic authentication (JWT + API keys)
- Essential file formats (50+)
- Basic cloud storage (S3, GCS)
- API documentation
- Rate limiting

### Phase 2 (Q2 2025)
- [ ] Advanced file formats (200+ total)
- [ ] Batch processing optimization
- [ ] WebSocket real-time updates
- [ ] Advanced webhook system
- [ ] Mobile SDKs (iOS, Android)
- [ ] Advanced analytics dashboard

### Phase 3 (Q3 2025)
- [ ] AI-powered format detection
- [ ] OCR integration for scanned documents
- [ ] Advanced image processing filters
- [ ] Video compression optimization
- [ ] Multi-region deployment
- [ ] GraphQL API

### Phase 4 (Q4 2025)
- [ ] Blockchain-based file verification
- [ ] Advanced security (end-to-end encryption)
- [ ] Machine learning conversion optimization
- [ ] Enterprise SSO integration
- [ ] Advanced compliance features (HIPAA, SOX)
- [ ] Edge computing for faster processing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone the repository
git clone https://github.com/your-org/file-conversion-api.git
cd file-conversion-api

# Set up development environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run tests
pytest

# Run code quality checks
black .
isort .
flake8
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [https://docs.fileconvert.com](https://docs.fileconvert.com)
- **API Reference**: [https://api.fileconvert.com/docs](https://api.fileconvert.com/docs)
- **Community Forum**: [https://community.fileconvert.com](https://community.fileconvert.com)
- **Email Support**: support@fileconvert.com
- **Enterprise Support**: enterprise@fileconvert.com

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- All the open-source libraries that make this project possible
- Our beta testers and early adopters
- Contributors who help improve the service

---

**Made with ❤️ by the FileConvert Team**
