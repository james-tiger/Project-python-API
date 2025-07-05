# Python API Project

A robust RESTful API built with Python, featuring modern development practices, comprehensive documentation, and scalable architecture.

## Overview

This project implements a full-featured RESTful API using Python and Flask/FastAPI framework. It provides a solid foundation for building scalable web services with authentication, data validation, error handling, and comprehensive testing.

## Features

- **RESTful API Design**: Clean, intuitive endpoint structure following REST principles
- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **Data Validation**: Comprehensive input validation and sanitization
- **Database Integration**: SQLAlchemy ORM with PostgreSQL/MySQL support
- **Error Handling**: Centralized error handling with meaningful HTTP status codes
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Testing Suite**: Comprehensive unit and integration tests
- **Logging**: Structured logging with configurable levels
- **Configuration Management**: Environment-based configuration
- **Rate Limiting**: API rate limiting and throttling
- **CORS Support**: Cross-Origin Resource Sharing configuration
- **Health Checks**: System health monitoring endpoints

## Tech Stack

- **Framework**: Flask/FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic/Marshmallow
- **Testing**: pytest
- **Documentation**: Swagger/OpenAPI
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Docker and Docker Compose (optional)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/james-tiger/Project-python-API.git
cd Project-python-API
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize the database:**
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

6. **Run the application:**
```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Docker Setup

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

2. **Run database migrations:**
```bash
docker-compose exec api python manage.py db upgrade
```

## API Documentation

### Base URL
```
http://localhost:5000/api/v1
```

### Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Core Endpoints

#### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - User logout

#### Users
- `GET /users` - Get all users (admin only)
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

#### Resources (Example)
- `GET /resources` - Get all resources
- `GET /resources/{id}` - Get resource by ID
- `POST /resources` - Create new resource
- `PUT /resources/{id}` - Update resource
- `DELETE /resources/{id}` - Delete resource

### Example Requests

#### Register a new user
```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "secure_password123"
  }'
```

#### Create a resource
```bash
curl -X POST http://localhost:5000/api/v1/resources \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "name": "Sample Resource",
    "description": "This is a sample resource",
    "category": "example"
  }'
```

## Project Structure

```
Project-python-API/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── resource.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── resources.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── resource_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_users.py
│   └── test_resources.py
├── migrations/
├── docs/
│   ├── api-documentation.md
│   └── deployment-guide.md
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── app.py
├── manage.py
└── README.md
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/test_dbname

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Categories

- **Unit Tests**: Test individual functions and methods
- **Integration Tests**: Test API endpoints and database interactions
- **Authentication Tests**: Test JWT authentication and authorization
- **Validation Tests**: Test input validation and error handling

## API Rate Limiting

The API implements rate limiting to prevent abuse:

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Admin users**: 5000 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Error Handling

The API uses standard HTTP status codes and returns consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The provided data is invalid",
    "details": {
      "email": ["This field is required"]
    }
  }
}
```

Common status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Unprocessable Entity
- `500` - Internal Server Error

## Logging

The application uses structured logging with different levels:

```python
import logging

logger = logging.getLogger(__name__)

# Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.info("User authenticated", extra={"user_id": user.id})
logger.error("Database connection failed", extra={"error": str(e)})
```

## Security

### Security Measures Implemented

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for password storage
- **Input Validation**: Comprehensive validation of all inputs
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CORS Configuration**: Proper Cross-Origin Resource Sharing setup
- **Rate Limiting**: Protection against DoS attacks
- **Security Headers**: HTTP security headers implementation

### Security Best Practices

1. Always use HTTPS in production
2. Regularly update dependencies
3. Implement proper logging and monitoring
4. Use environment variables for sensitive data
5. Implement proper error handling (don't expose internals)
6. Regular security audits and penetration testing

## Deployment

### Production Deployment

1. **Environment Setup:**
```bash
# Set production environment
export FLASK_ENV=production
export DEBUG=False
```

2. **Database Setup:**
```bash
# Run migrations
python manage.py db upgrade
```

3. **Using Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

4. **Using Docker:**
```bash
docker build -t python-api .
docker run -p 5000:5000 python-api
```

### Monitoring

- **Health Check Endpoint**: `GET /health`
- **Metrics Endpoint**: `GET /metrics`
- **Application Logs**: Structured JSON logging
- **Database Monitoring**: Connection pool metrics

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Add type hints where appropriate

## Performance Optimization

- **Database Indexing**: Proper indexing for frequently queried fields
- **Connection Pooling**: Database connection pooling
- **Caching**: Redis caching for frequently accessed data
- **Pagination**: Efficient pagination for large datasets
- **Query Optimization**: Optimized database queries

## Future Enhancements

- [ ] GraphQL API support
- [ ] Microservices architecture
- [ ] Advanced monitoring and alerting
- [ ] API versioning strategy
- [ ] WebSocket support for real-time features
- [ ] Advanced caching strategies
- [ ] Message queue integration
- [ ] API analytics and usage tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Email: support@example.com
- Documentation: [API Documentation](docs/api-documentation.md)

## Author

**James Tiger**
- GitHub: [@james-tiger](https://github.com/james-tiger)
- LinkedIn: [james-tiger](https://linkedin.com/in/james-tiger)

## Acknowledgments

- Thanks to the Flask/FastAPI community for excellent documentation
- Contributors and testers who helped improve this project
- Open source libraries that made this project possible

---

*Built with ❤️ using Python*
