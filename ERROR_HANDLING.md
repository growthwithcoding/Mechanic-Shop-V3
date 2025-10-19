# Enhanced Error Handling Documentation

## Overview

The Mechanic Shop API V3 now features a comprehensive error handling system that provides detailed logging, unique error tracking, and environment-aware responses.

## Key Features

### 1. **Unique Error IDs**
Every error response includes a unique UUID error_id that can be used to track and debug specific errors.

**Example Response:**
```json
{
    "error": "Database Error",
    "message": "A database error occurred. Please contact support with error ID: 7f9c8d4e-3b2a-4c1d-9e8f-6a5b4c3d2e1f",
    "error_id": "7f9c8d4e-3b2a-4c1d-9e8f-6a5b4c3d2e1f",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

### 2. **Request Context Logging**
All errors are logged with comprehensive context including:
- Timestamp
- HTTP method and endpoint
- User ID (from JWT token)
- IP address and User-Agent
- Query parameters
- Request body (with sensitive fields redacted)

### 3. **Environment-Aware Responses**

#### Development Mode (DEBUG=True)
Returns detailed error information including:
- Exception type
- Full error message
- Stack trace
- Database constraint details

**Example:**
```json
{
    "error": "Database Error",
    "message": "A database error occurred...",
    "error_id": "7f9c8d4e-3b2a-4c1d-9e8f-6a5b4c3d2e1f",
    "timestamp": "2025-01-19T18:30:45.123456",
    "details": {
        "type": "IntegrityError",
        "message": "Duplicate entry 'test@example.com' for key 'email'",
        "traceback": "Traceback (most recent call last):\n..."
    }
}
```

#### Production Mode (DEBUG=False)
Returns safe, user-friendly messages without exposing internal details:

```json
{
    "error": "Database Error",
    "message": "A database error occurred. Please contact support with error ID: 7f9c8d4e-3b2a-4c1d-9e8f-6a5b4c3d2e1f",
    "error_id": "7f9c8d4e-3b2a-4c1d-9e8f-6a5b4c3d2e1f",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

### 4. **Categorized Error Types**

#### HTTP Error Handlers
- **400 Bad Request** - Invalid request format or parameters
- **401 Unauthorized** - Authentication required or invalid token
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource does not exist
- **405 Method Not Allowed** - HTTP method not supported for endpoint
- **500 Internal Server Error** - Unexpected server errors

#### Database Error Handlers

##### IntegrityError (400)
Handles constraint violations with user-friendly messages:
- **Duplicate Entry**: "A record with this information already exists"
- **Foreign Key Violation**: "Referenced record does not exist"

**Example:**
```json
{
    "error": "Database Integrity Error",
    "message": "A record with this information already exists",
    "error_id": "abc123...",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

##### OperationalError (503)
Handles connection and operational issues:
- **Connection Lost**: "Database connection lost. Please try again"
- **Timeout/Deadlock**: "Database is busy. Please try again"

##### DataError (400)
Handles data type mismatches and invalid values:
- "Invalid data format or type"

##### General SQLAlchemyError (500)
Catches all other database errors with full logging

#### Validation Error Handler (400)
Marshmallow validation errors return structured validation messages:

```json
{
    "error": "Validation Error",
    "message": "Request validation failed",
    "validation_errors": {
        "email": ["Not a valid email address."],
        "age": ["Must be greater than or equal to 18."]
    },
    "error_id": "xyz789...",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

### 5. **Sensitive Data Redaction**
The following fields are automatically redacted from logs:
- password
- token
- secret
- api_key

**Before logging:**
```json
{
    "email": "user@example.com",
    "password": "secret123"
}
```

**After redaction:**
```json
{
    "email": "user@example.com",
    "password": "***REDACTED***"
}
```

## Error Response Structure

All error responses follow this consistent structure:

```json
{
    "error": "Error Type",
    "message": "Human-readable error description",
    "error_id": "unique-uuid-string",
    "timestamp": "ISO-8601 timestamp",
    "details": {
        // Only included in development mode
    }
}
```

## Logging

### Log Format
Errors are logged with the following information:

```python
{
    "error_id": "unique-uuid",
    "error_type": "Error classification",
    "status_code": 500,
    "error_message": "Error description",
    "context": {
        "timestamp": "ISO-8601 timestamp",
        "method": "GET/POST/PUT/DELETE",
        "path": "/api/endpoint",
        "endpoint": "blueprint.function_name",
        "remote_addr": "client IP",
        "user_agent": "client user agent",
        "user_id": "authenticated user ID or null",
        "query_params": {},
        "request_data": {}
    },
    "additional_info": {
        // Error-specific information
    },
    "traceback": "Full stack trace for 500 errors"
}
```

### Accessing Logs
Logs are written using Python's standard logging module with the logger name `__name__` (application module).

## Best Practices

### For Developers

1. **Reference Error IDs in Bug Reports**
   - Always include the error_id when reporting issues
   - Use error_id to search logs for specific errors

2. **Use Development Mode for Debugging**
   - Set `DEBUG=True` in development to see detailed error information
   - Never use DEBUG mode in production

3. **Handle Expected Errors in Route Handlers**
   - Use try-except blocks for known error conditions
   - Return appropriate HTTP status codes
   - Let the error handlers catch unexpected errors

4. **Add Sensitive Fields to Redaction List**
   - Update the `sensitive_fields` list in `get_request_context()` if you add new sensitive data fields

### For API Consumers

1. **Always Check error_id**
   - Save error_id for troubleshooting
   - Include error_id when contacting support

2. **Parse validation_errors**
   - For 400 Validation Error responses, check the `validation_errors` field for specific field-level issues

3. **Retry on 503**
   - Operational errors (503) indicate temporary issues
   - Implement exponential backoff retry logic

4. **Don't Parse error Messages**
   - Error messages may change; use `error` field to determine error type programmatically

## Example Error Scenarios

### Scenario 1: Duplicate Email Registration
**Request:**
```bash
POST /auth/register
{
    "email": "existing@example.com",
    "password": "password123",
    "name": "John Doe"
}
```

**Response:**
```json
{
    "error": "Database Integrity Error",
    "message": "A record with this information already exists",
    "error_id": "7f9c8d4e-3b2a-4c1d-9e8f-6a5b4c3d2e1f",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

### Scenario 2: Invalid Foreign Key
**Request:**
```bash
POST /service_tickets
{
    "vehicle_id": 9999,  // Non-existent vehicle
    "description": "Oil change"
}
```

**Response:**
```json
{
    "error": "Database Integrity Error",
    "message": "Referenced record does not exist",
    "error_id": "abc123...",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

### Scenario 3: Database Connection Lost
**Response:**
```json
{
    "error": "Database Operational Error",
    "message": "Database connection lost. Please try again",
    "error_id": "xyz789...",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```
**Status Code:** 503 (Service Unavailable)

### Scenario 4: Validation Error
**Request:**
```bash
POST /customers
{
    "email": "not-an-email",
    "phone": "12345"  // Too short
}
```

**Response:**
```json
{
    "error": "Validation Error",
    "message": "Request validation failed",
    "validation_errors": {
        "email": ["Not a valid email address."],
        "phone": ["String does not match expected pattern."]
    },
    "error_id": "def456...",
    "timestamp": "2025-01-19T18:30:45.123456"
}
```

## Future Enhancements

Potential improvements to consider:

1. **Error Tracking Service Integration**
   - Sentry, Rollbar, or similar services
   - Automatic error aggregation and alerting

2. **Rate Limiting on Error Responses**
   - Prevent abuse from repeated error-triggering requests

3. **Error Metrics Dashboard**
   - Track error rates by endpoint
   - Monitor error trends over time

4. **Custom Error Classes**
   - Business logic specific exceptions
   - More granular error categorization

5. **Structured Logging**
   - JSON formatted logs for easier parsing
   - Integration with log aggregation services (ELK, Splunk)

## Configuration

### Logging Configuration
Add to `config.py` for production:

```python
import logging

class ProductionConfig(Config):
    # ... existing config ...
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configure logging
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            file_handler = RotatingFileHandler(
                'logs/mechanic_shop.log',
                maxBytes=10240000,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Mechanic Shop API startup')
```

## Testing Error Handling

### Unit Tests
Test error handlers by triggering specific exceptions:

```python
def test_database_integrity_error(client):
    """Test duplicate entry error handling"""
    # Create initial customer
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    
    # Attempt duplicate
    response = client.post('/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'name': 'Test User'
    })
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error_id' in data
    assert data['error'] == 'Database Integrity Error'
```

### Integration Tests
Test real error scenarios through API endpoints:

```python
def test_404_error(client):
    """Test 404 not found error"""
    response = client.get('/customers/99999')
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error_id' in data
    assert data['error'] == 'Not Found'
```

## Support

For questions or issues with error handling:
1. Check application logs using the error_id
2. Verify your environment configuration (DEBUG setting)
3. Review this documentation for error type explanations
4. Contact the development team with error_id and context

---

**Last Updated:** January 19, 2025  
**Version:** 3.0.0
