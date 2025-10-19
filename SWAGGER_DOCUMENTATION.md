# Swagger API Documentation - Mechanic Shop API V3

## Overview

This document provides information about the Swagger/OpenAPI documentation integrated into the Mechanic Shop API V3 using Flasgger.

## Accessing the Documentation

Once the application is running, you can access the interactive Swagger UI at:

```
http://localhost:5000/api/docs
```

This provides an interactive interface where you can:
- View all API endpoints
- See request/response schemas
- Test endpoints directly from the browser
- View authentication requirements

## Configuration

The Swagger configuration is located in `application/__init__.py`:

```python
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Mechanic Shop API V3",
        "description": "A comprehensive RESTful API for managing a mechanic shop",
        "version": "3.0.0",
        "contact": {
            "name": "API Support",
            "email": "support@mechanicshop.com"
        }
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    }
}
```

## Documentation Structure

Each route is documented using YAML format within the docstring:

```python
@app.route("/example", methods=['POST'])
def example_route():
    """
    Short description
    ---
    tags:
      - Category Name
    summary: Brief summary
    description: Detailed description
    security:
      - Bearer: []  # For protected routes
    parameters:
      - in: body
        name: body
        description: Request body description
        required: true
        schema:
          type: object
          required:
            - field1
            - field2
          properties:
            field1:
              type: string
              example: value1
            field2:
              type: integer
              example: 123
    responses:
      200:
        description: Success response
        schema:
          type: object
          properties:
            result:
              type: string
              example: Success
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    # Route implementation
```

## API Categories (Tags)

The API is organized into the following categories:

### 1. Authentication
- User registration
- Login
- Current user information

### 2. Customers
- Customer CRUD operations
- Customer pagination
- Vehicle management (nested routes)

### 3. Mechanics
- Mechanic CRUD operations
- Activity-based queries
- Performance metrics

### 4. Inventory
- Part CRUD operations
- Quantity adjustments
- Category filtering
- Low stock queries

### 5. Service Tickets
- Ticket CRUD operations
- Mechanic assignments
- Part additions
- Ticket status management

## Authentication Documentation

All protected routes include security definitions:

```yaml
security:
  - Bearer: []
```

This indicates that the route requires a JWT token in the Authorization header.

### How to Authenticate in Swagger UI:

1. First, call the `/auth/register` or `/auth/login` endpoint
2. Copy the `access_token` from the response
3. Click the "Authorize" button at the top of the Swagger UI
4. Enter: `Bearer YOUR_TOKEN_HERE`
5. Click "Authorize"
6. All subsequent requests will include the token

## Request/Response Examples

### Example: POST /auth/register

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "phone": "555-123-4567"
}
```

**Response (201):**
```json
{
  "message": "Customer registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "customer": {
    "customer_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "555-123-4567"
  }
}
```

## Error Responses

All endpoints document standard error responses:

- **400 Bad Request**: Invalid input data or validation errors
- **401 Unauthorized**: Missing or invalid authentication token
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server-side error

## Validation

The API uses Marshmallow schemas for validation. The Swagger documentation reflects these validation rules:

- Required fields are marked with `required: true`
- Field types are specified (string, integer, number, boolean, etc.)
- Examples are provided for each field
- Format specifications are included (email, password, etc.)

## Best Practices for Documentation

1. **Be Descriptive**: Use clear, concise descriptions
2. **Provide Examples**: Include realistic example data
3. **Document All Responses**: Include both success and error responses
4. **Specify Required Fields**: Clearly mark required vs optional fields
5. **Use Proper Types**: Specify correct data types and formats
6. **Tag Consistently**: Group related endpoints with consistent tags
7. **Include Security**: Document authentication requirements

## Extending the Documentation

To add documentation to a new route:

1. Add the docstring with YAML format
2. Include all required sections (tags, summary, description, parameters, responses)
3. Specify security requirements if needed
4. Provide comprehensive examples
5. Document all possible response codes

## JSON Schema Export

The API spec can be accessed in JSON format at:

```
http://localhost:5000/apispec.json
```

This can be used with various tools:
- Postman (import collection)
- API testing tools
- Code generators
- Documentation generators

## Testing with Swagger UI

The Swagger UI allows you to test endpoints directly:

1. Select an endpoint
2. Click "Try it out"
3. Fill in the required parameters
4. Click "Execute"
5. View the response

## Common Use Cases

### 1. Creating a New Customer
```
POST /auth/register
→ Returns access_token
→ Use token for subsequent requests
```

### 2. Managing Inventory
```
POST /inventory (create part)
GET /inventory (list parts)
PATCH /inventory/{id}/adjust-quantity (adjust stock)
```

### 3. Service Ticket Workflow
```
POST /service_tickets (create ticket)
PUT /service_tickets/{id}/assign-mechanic/{mechanic_id}
POST /service_tickets/{id}/parts/{part_id}
PUT /service_tickets/{id} (update status)
```

## Additional Resources

- **Flasgger Documentation**: https://github.com/flasgger/flasgger
- **OpenAPI Specification**: https://swagger.io/specification/
- **Swagger UI**: https://swagger.io/tools/swagger-ui/

## Troubleshooting

### Swagger UI Not Loading

1. Verify flasgger is installed: `pip install flasgger`
2. Check that Swagger is initialized in `application/__init__.py`
3. Ensure the app is running on the correct port
4. Clear browser cache

### Documentation Not Showing

1. Verify docstrings are properly formatted
2. Check YAML syntax (indentation matters)
3. Ensure route is registered with the blueprint
4. Restart the application

### Authentication Issues in Swagger UI

1. Ensure token is prefixed with "Bearer "
2. Check token hasn't expired
3. Verify token was copied completely
4. Re-authenticate if needed

## Maintenance

Keep documentation up to date when:
- Adding new routes
- Modifying request/response schemas
- Changing authentication requirements
- Updating validation rules
- Adding new query parameters

Regular documentation reviews ensure accuracy and completeness.
