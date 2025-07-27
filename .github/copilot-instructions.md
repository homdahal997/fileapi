# Copilot Instructions for File Conversion API

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a comprehensive file conversion API service built with Django and Django REST Framework. The system supports conversion between 200+ file formats across various categories (documents, images, audio, video, archives, spreadsheets, presentations, ebooks, etc.).

## Architecture Principles
- **Microservices Architecture**: Separate apps for conversions, authentication, and storage integrations
- **Asynchronous Processing**: Use Celery with Redis for background tasks and queue management
- **Cloud Storage Integration**: Support for AWS S3, Google Cloud Storage, and Dropbox
- **Security First**: JWT authentication, API key management, data encryption
- **Scalability**: Designed for horizontal scaling and high availability
- **Developer Experience**: Comprehensive API documentation with Swagger/OpenAPI

## Key Technologies
- Django 4.x with Django REST Framework
- Celery for asynchronous task processing
- Redis for caching and message broker
- PostgreSQL for primary database
- JWT for authentication
- AWS SDK, Google Cloud SDK, Dropbox SDK for storage
- Swagger/OpenAPI for API documentation

## Code Style Guidelines
- Follow PEP 8 for Python code formatting
- Use type hints for all function parameters and return values
- Implement comprehensive error handling and logging
- Write docstrings for all classes and functions
- Use Django's built-in security features
- Implement proper validation for all API endpoints
- Use async/await patterns where appropriate
- Follow RESTful API design principles

## File Conversion Strategy
- Support 200+ file formats using appropriate Python libraries
- Implement format detection and validation
- Use factory pattern for converter implementations
- Support batch processing and webhooks
- Implement retry mechanisms for failed conversions
- Provide detailed conversion status and progress tracking

## Security Considerations
- Implement rate limiting and quota management
- Validate all file uploads and sanitize inputs
- Use secure file storage with encryption
- Implement proper CORS policies
- Follow GDPR and CCPA compliance requirements
- Use environment variables for sensitive configuration

## Testing Strategy
- Write unit tests for all core functionality
- Implement integration tests for API endpoints
- Use pytest for testing framework
- Mock external services in tests
- Implement load testing for performance validation
