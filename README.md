# Mechanic Shop Management API - V3

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

An advanced RESTful API for managing automotive repair shop operations with comprehensive Swagger documentation, automated testing, JWT authentication, rate limiting, caching, and full inventory management. Built with Flask and SQLAlchemy using the Application Factory Pattern.

## 🎯 Project Overview

This is **Version 3** of the Mechanic Shop API, implementing:
- **Flask-Swagger Documentation** - Interactive API documentation with Swagger UI
- **Comprehensive Testing** - unittest framework with positive/negative test cases
- **JWT Token Authentication** - Secure customer and mechanic access
- **Rate Limiting** - API protection against abuse
- **Caching** - Performance optimization for frequently accessed data
- **Advanced Query Operations** - Pagination, filtering, and custom sorting
- **Inventory Management** - Complete parts tracking with stock management
- **Many-to-Many Relationships** - Complex data modeling with junction tables

## 👨‍💻 Author

**Austin Carlson**  
*#growthwithcoding*

- 🔗 GitHub: [https://github.com/growthwithcoding](https://github.com/growthwithcoding)
- 💼 LinkedIn: [https://www.linkedin.com/in/austin-carlson-720b65375/](https://www.linkedin.com/in/austin-carlson-720b65375/)

---

## 📋 Table of Contents

- [V3 Assignment Requirements](#-v3-assignment-requirements)
- [Advanced Features](#-advanced-features-highlights)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Database Setup](#-database-setup)
- [Swagger Documentation](#-swagger-documentation)
- [Testing](#-testing)
- [API Endpoints](#-api-endpoints)
- [Rate Limiting & Caching](#-rate-limiting--caching)
- [Authentication](#-authentication)
- [Advanced Queries](#-advanced-queries)
- [Inventory Management](#-inventory-management)
- [Testing with Postman](#-testing-with-postman)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)

---

## 📝 V3 Assignment Requirements

### Assignment: Documentation and Testing

**Instructor:** Dylan Katina

#### Documentation Requirements (Flask-Swagger)

Utilizing Flask-Swagger and Flask-Swagger-UI to document each route:

✅ **Each Route Documented With:**
- [x] **Path**: Endpoint URL
- [x] **Type**: Request method (POST, GET, PUT, DELETE)
- [x] **Tag**: Category for route organization
- [x] **Summary**: Brief description
- [x] **Description**: Detailed explanation
- [x] **Security**: Points to security definition (for token-authenticated routes)
- [x] **Parameters**: Information about required data (POST/PUT requests)
- [x] **Responses**: Response data format with examples

✅ **Definitions:**
- [x] **PayloadDefinition**: Defines incoming data shape (POST/PUT)
- [x] **ResponseDefinitions**: Defines outgoing data shape with examples

#### Testing Requirements (unittest)

✅ **Test Implementation:**
- [x] Created `tests/` folder inside project
- [x] Test file for each blueprint:
  - [x] `test_customer.py` - Customer & vehicle routes
  - [x] `test_mechanic.py` - Mechanic routes
  - [x] `test_service_ticket.py` - Service ticket routes
  - [x] `test_inventory.py` - Inventory routes
- [x] One test for every route in API
- [x] Negative tests incorporated
- [x] Tests executable with: `python -m unittest discover tests`

**Status:** ✅ All requirements completed

---

## ✨ Advanced Features Highlights

### 1. Swagger Documentation ✅ **V3 NEW**

Complete interactive API documentation:

```python
# Swagger configuration in __init__.py
swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs"
}
```

**Features:**
- Interactive UI at `/apidocs`
- Try-it-out functionality for all endpoints
- Complete request/response schemas
- Authentication integration
- Example payloads for all routes

### 2. Comprehensive Testing ✅ **V3 NEW**

Full test suite with 30+ tests:

```python
class TestMechanicRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test client and database"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            # Register test user and get token
    
    def test_create_mechanic(self):
        """Test creating a mechanic"""
        response = self.client.post('/mechanics', 
            json={...},
            headers={'Authorization': f'Bearer {self.token}'}
        )
        self.assertEqual(response.status_code, 201)
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
```

**Test Coverage:**
- Positive tests for all routes
- Negative tests for error handling
- Authentication tests
- Validation tests
- Edge case tests

### 3. Rate Limiting

Protects the API from abuse by limiting request frequency:

```python
# Example: Login endpoint limited to 5 requests per minute
@auth_bp.route("/login", methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

**Applied to:**
- **Registration**: 3 requests per hour
- **Login**: 5 requests per minute  
- **Create Customer**: 5 requests per hour
- **Create Mechanic**: 10 requests per hour
- **Create Service Ticket**: 10 requests per hour
- **Create Inventory Part**: 20 requests per hour

### 4. Caching

Improves performance by caching frequently accessed data:

```python
# Mechanics list cached for 5 minutes (300 seconds)
@mechanic_bp.route("", methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_mechanics():
    # Returns cached result if available
```

**Caching Strategy:**
- Mechanics list cached for 5 minutes
- Reduces database load on repeated requests
- Automatically invalidated on updates

### 5. JWT Token Authentication

**Token Generation:**
```python
def encode_token(customer_id):
    """Creates JWT token for authenticated access"""
    access_token = create_access_token(identity=str(customer_id))
    return access_token
```

**Protected Routes:**
```python
@jwt_required()  # Requires valid Bearer token
def protected_route():
    customer_id = get_jwt_identity()  # Extract customer ID from token
```

**Token Features:**
- 1-hour expiration
- Customer-specific tokens
- Bearer token format
- Secure password hashing with Werkzeug

### 6. Advanced Queries

#### **Pagination**
Efficient data retrieval with page-based results:

```bash
GET /customers?page=2&per_page=20
```

Response includes metadata:
```json
{
  "customers": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total_customers": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  }
}
```

#### **Mechanic Sorting by Activity**
Sort mechanics by number of tickets worked on:

```bash
GET /mechanics/by-activity?order=desc&active_only=true
```

```json
[
  {
    "mechanic_id": 5,
    "full_name": "John Smith",
    "ticket_count": 47,
    "is_active": true
  }
]
```

#### **Bulk Mechanic Assignment Editing**
Add or remove multiple mechanics from a ticket in one request:

```bash
PUT /service-tickets/1/edit
{
  "add_ids": [1, 2, 3],
  "remove_ids": [4, 5],
  "role": "Lead Technician",
  "minutes_worked": 0
}
```

### 7. Inventory Management

**Complete Parts Tracking:**
- Part catalog with SKU management
- Quantity tracking with low-stock alerts
- Cost tracking with markup calculations
- Many-to-many relationship with service tickets

**Adding Parts to Tickets:**
```bash
POST /service-tickets/1/parts/5
{
  "quantity_used": 2,
  "markup_percentage": 30.0,
  "warranty_months": 12,
  "installed_by_mechanic_id": 3
}
```

**Automatic Stock Management:**
- Decrements inventory when parts are used
- Tracks installation history
- Warranty management
- Low-stock alerts

---

## 📦 Installation

### Prerequisites

- **Python 3.11+**
- **MySQL 8.0+**
- **pip** (Python package manager)
- **Git**

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/growthwithcoding/Mechanic-Shop-V3.git
   cd Mechanic-Shop-V3
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create MySQL database**
   ```sql
   CREATE DATABASE mechanic_shop_v3;
   ```

5. **Configure environment variables**
   
   Create a `.env` file or set environment variables:
   ```bash
   # Database connection
   DEV_DATABASE_URL=mysql+mysqlconnector://root:your_password@127.0.0.1/mechanic_shop_v3
   
   # Secret keys
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   ```

6. **Run database migrations**
   ```bash
   # Windows
   set FLASK_APP=app.py
   flask db upgrade
   
   # Mac/Linux
   export FLASK_APP=app.py
   flask db upgrade
   ```

7. **Run the application**
   ```bash
   python app.py
   ```
   
   Server starts at `http://127.0.0.1:5000`

8. **Access Swagger Documentation**
   
   Navigate to: `http://127.0.0.1:5000/apidocs`

---

## ⚙️ Configuration

The application supports multiple environments through `config.py`:

### Development
```python
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@127.0.0.1/mechanic_shop_v3'
    SQLALCHEMY_ECHO = True
```

### Testing
```python
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
```

### Production
```python
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
```

### JWT Configuration
```python
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Token expires in 1 hour
```

### Rate Limiting Configuration
```python
RATELIMIT_STORAGE_URL = "memory://"  # In-memory rate limit storage
```

### Caching Configuration
```python
CACHE_TYPE = "SimpleCache"  # In-memory caching
CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes default
```

---

## 🗄 Database Setup

### Database Migrations

The project uses **Flask-Migrate** (Alembic) for database version control:

**Create a new migration:**
```bash
flask db migrate -m "Description of changes"
```

**Apply migrations:**
```bash
flask db upgrade
```

**Rollback migrations:**
```bash
flask db downgrade
```

**View migration history:**
```bash
flask db history
```

### Migration Workflow

1. Modify models in `application/models.py`
2. Generate migration: `flask db migrate -m "Add new field"`
3. Review generated migration in `migrations/versions/`
4. Apply migration: `flask db upgrade`
5. Commit to version control

---

## 📚 Swagger Documentation

### Accessing Swagger UI

Navigate to: **http://127.0.0.1:5000/apidocs**

### Features

- **Interactive API Testing** - Try out endpoints directly in browser
- **Request/Response Schemas** - Complete data format documentation
- **Authentication Integration** - Test protected routes with JWT tokens
- **Example Payloads** - Sample data for all requests
- **Response Examples** - Expected responses for all status codes

### Documentation Structure

Each route is documented with:

1. **Tags** - Organize routes by category (Authentication, Customers, Mechanics, etc.)
2. **Summary** - Brief one-line description
3. **Description** - Detailed explanation of functionality
4. **Parameters** - Request parameters (path, query, body)
5. **Request Body** - Expected payload format with schema
6. **Responses** - All possible response codes with examples
7. **Security** - Authentication requirements

### Example Documentation

```yaml
/mechanics/{mechanic_id}:
  get:
    tags:
      - Mechanics
    summary: Get mechanic by ID
    description: Retrieves detailed information about a specific mechanic including their active status and assigned service tickets
    security:
      - Bearer: []
    parameters:
      - in: path
        name: mechanic_id
        required: true
        schema:
          type: integer
        description: The unique identifier of the mechanic
    responses:
      200:
        description: Mechanic details retrieved successfully
        content:
          application/json:
            schema:
              $ref: '#/definitions/MechanicResponse'
            examples:
              success:
                value:
                  mechanic_id: 1
                  full_name: "John Smith"
                  email: "john@shop.com"
                  phone: "555-1234"
                  salary: 65000
                  is_active: true
      404:
        description: Mechanic not found
        content:
          application/json:
            example:
              error: "Mechanic not found"
```

### Schema Definitions

All payload and response schemas are defined:

```yaml
definitions:
  MechanicPayload:
    type: object
    required:
      - full_name
      - email
      - salary
    properties:
      full_name:
        type: string
        example: "John Smith"
      email:
        type: string
        format: email
        example: "john@shop.com"
      phone:
        type: string
        example: "555-1234"
      salary:
        type: integer
        example: 65000
      is_active:
        type: boolean
        default: true
        example: true
```

See `SWAGGER_DOCUMENTATION.md` for complete documentation details.

---

## 🧪 Testing

### Test Structure

```
tests/
├── __init__.py
├── test_customer.py          # Customer & authentication tests
├── test_mechanic.py          # Mechanic route tests
├── test_service_ticket.py    # Service ticket tests
└── test_inventory.py         # Inventory management tests
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run with verbose output
python -m unittest discover tests -v

# Run specific test file
python -m unittest tests.test_mechanic

# Run specific test class
python -m unittest tests.test_mechanic.TestMechanicRoutes

# Run specific test method
python -m unittest tests.test_mechanic.TestMechanicRoutes.test_create_mechanic
```

### Test Coverage by Blueprint

#### Customer Tests (`test_customer.py`)
- ✅ `test_register_customer` - Register new customer
- ✅ `test_register_duplicate_email` - Prevent duplicate emails (negative)
- ✅ `test_login_customer` - Login with valid credentials
- ✅ `test_login_invalid_credentials` - Invalid login (negative)
- ✅ `test_get_all_customers` - List customers with pagination
- ✅ `test_get_customer_by_id` - Get single customer
- ✅ `test_update_customer` - Update customer information
- ✅ `test_add_vehicle` - Add vehicle to customer
- ✅ `test_add_vehicle_invalid_customer` - Invalid customer ID (negative)

#### Mechanic Tests (`test_mechanic.py`)
- ✅ `test_create_mechanic` - Create new mechanic
- ✅ `test_create_mechanic_missing_fields` - Missing required fields (negative)
- ✅ `test_get_all_mechanics` - List all mechanics (cached)
- ✅ `test_get_mechanic_by_id` - Get single mechanic
- ✅ `test_get_mechanics_by_activity` - Sort by ticket count
- ✅ `test_update_mechanic` - Update mechanic information
- ✅ `test_delete_mechanic` - Delete mechanic
- ✅ `test_delete_nonexistent_mechanic` - Invalid mechanic ID (negative)

#### Service Ticket Tests (`test_service_ticket.py`)
- ✅ `test_create_service_ticket` - Create new ticket
- ✅ `test_create_ticket_invalid_vehicle` - Invalid vehicle ID (negative)
- ✅ `test_get_all_service_tickets` - List all tickets
- ✅ `test_get_service_ticket_by_id` - Get single ticket
- ✅ `test_update_service_ticket` - Update ticket status
- ✅ `test_assign_mechanic_to_ticket` - Assign mechanic
- ✅ `test_remove_mechanic_from_ticket` - Remove mechanic
- ✅ `test_bulk_edit_mechanics` - Add/remove multiple mechanics
- ✅ `test_assign_invalid_mechanic` - Invalid mechanic assignment (negative)

#### Inventory Tests (`test_inventory.py`)
- ✅ `test_create_part` - Create inventory part
- ✅ `test_create_part_duplicate_number` - Duplicate part number (negative)
- ✅ `test_get_all_parts` - List all parts
- ✅ `test_get_low_stock_parts` - Filter low stock parts
- ✅ `test_get_part_by_id` - Get single part
- ✅ `test_update_part` - Update part information
- ✅ `test_adjust_part_quantity` - Adjust stock quantity
- ✅ `test_adjust_insufficient_quantity` - Insufficient stock (negative)
- ✅ `test_add_part_to_ticket` - Add part to service ticket
- ✅ `test_delete_part` - Delete part

### Test Example

```python
def test_create_mechanic(self):
    """Test creating a new mechanic"""
    response = self.client.post('/mechanics',
        json={
            'full_name': 'Test Mechanic',
            'email': 'test@shop.com',
            'phone': '555-5555',
            'salary': 60000,
            'is_active': True
        },
        headers={'Authorization': f'Bearer {self.token}'}
    )
    
    self.assertEqual(response.status_code, 201)
    data = response.get_json()
    self.assertIn('mechanic_id', data)
    self.assertEqual(data['full_name'], 'Test Mechanic')
```

### Negative Test Example

```python
def test_create_mechanic_missing_fields(self):
    """Test creating mechanic with missing required fields"""
    response = self.client.post('/mechanics',
        json={
            'full_name': 'Test Mechanic'
            # Missing email and salary
        },
        headers={'Authorization': f'Bearer {self.token}'}
    )
    
    self.assertEqual(response.status_code, 400)
    data = response.get_json()
    self.assertIn('error', data)
```

See `TESTING.md` for complete testing documentation.

---

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Rate Limit | Auth Required |
|--------|----------|-------------|------------|---------------|
| POST | `/auth/register` | Register new customer | 3/hour | No |
| POST | `/auth/login` | Login and get JWT token | 5/min | No |
| GET | `/auth/me` | Get current user info | - | Yes |

### Customer Endpoints

| Method | Endpoint | Description | Pagination | Auth Required |
|--------|----------|-------------|------------|---------------|
| GET | `/customers` | List all customers | Yes | Yes |
| GET | `/customers/<id>` | Get customer details | - | Yes |
| PUT | `/customers/<id>` | Update customer | - | Yes |
| DELETE | `/customers/<id>` | Delete customer | - | Yes |
| POST | `/customers/<id>/vehicles` | Add vehicle | - | Yes |
| GET | `/customers/<id>/vehicles` | Get customer vehicles | - | Yes |

### Mechanic Endpoints

| Method | Endpoint | Description | Cached | Auth Required |
|--------|----------|-------------|--------|---------------|
| POST | `/mechanics` | Create mechanic | No | Yes |
| GET | `/mechanics` | List all mechanics | Yes (5min) | Yes |
| GET | `/mechanics/<id>` | Get mechanic details | No | Yes |
| GET | `/mechanics/by-activity` | Sort by ticket count | No | Yes |
| PUT | `/mechanics/<id>` | Update mechanic | No | Yes |
| DELETE | `/mechanics/<id>` | Delete mechanic | No | Yes |

### Service Ticket Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/service-tickets` | Create ticket | Yes |
| GET | `/service-tickets` | List all tickets | Yes |
| GET | `/service-tickets/<id>` | Get ticket details | Yes |
| PUT | `/service-tickets/<id>` | Update ticket | Yes |
| PUT | `/service-tickets/<id>/edit` | Bulk edit mechanics | Yes |
| PUT | `/service-tickets/<id>/assign-mechanic/<mechanic_id>` | Assign mechanic | Yes |
| PUT | `/service-tickets/<id>/remove-mechanic/<mechanic_id>` | Remove mechanic | Yes |
| POST | `/service-tickets/<id>/parts/<part_id>` | Add part to ticket | Yes |
| DELETE | `/service-tickets/<id>` | Delete ticket | Yes |

### Inventory Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/inventory` | Create part | Yes |
| GET | `/inventory` | List all parts | Yes |
| GET | `/inventory?low_stock=true` | Get low-stock parts | Yes |
| GET | `/inventory/<id>` | Get part details | Yes |
| PUT | `/inventory/<id>` | Update part | Yes |
| PATCH | `/inventory/<id>/adjust-quantity` | Adjust quantity | Yes |
| DELETE | `/inventory/<id>` | Delete part | Yes |

---

## 🛡 Rate Limiting & Caching

### Rate Limiting Implementation

Rate limiting prevents API abuse by limiting request frequency per IP address:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
```

**Rate Limit Patterns:**

| Endpoint | Rate Limit | Purpose |
|----------|------------|---------|
| `/auth/register` | 3 per hour | Prevent spam accounts |
| `/auth/login` | 5 per minute | Prevent brute force attacks |
| `/customers` (POST) | 5 per hour | Prevent abuse |
| `/mechanics` (POST) | 10 per hour | Moderate resource creation |
| `/service-tickets` (POST) | 10 per hour | Moderate ticket creation |
| `/inventory` (POST) | 20 per hour | Allow frequent inventory updates |

**Rate Limit Response:**
```json
{
  "error": "429 Too Many Requests",
  "message": "Rate limit exceeded"
}
```

### Caching Implementation

Caching reduces database load for frequently accessed data:

```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

@cache.cached(timeout=300)  # Cache for 5 minutes
def get_mechanics():
    # Expensive database query
    return mechanics
```

**Caching Strategy:**
- **Cached Endpoints**: GET `/mechanics` (5 minutes)
- **Cache Type**: In-memory (SimpleCache)
- **Invalidation**: Automatic after timeout
- **Benefits**: Reduced database queries, faster response times

---

## 🔐 Authentication

### JWT Token Authentication Flow

1. **User registers or logs in**
   ```bash
   POST /auth/login
   {
     "email": "user@example.com",
     "password": "password123"
   }
   ```

2. **Receive JWT token**
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "customer": { "customer_id": 1, "email": "user@example.com" }
   }
   ```

3. **Include token in subsequent requests**
   ```bash
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Token Features

- **Expiration**: 1 hour (configurable)
- **Format**: Bearer token
- **Payload**: Contains customer_id for identification
- **Security**: HMAC-SHA256 signing algorithm

### Password Security

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing password on registration
customer.password_hash = generate_password_hash(password)

# Verifying password on login
if check_password_hash(customer.password_hash, password):
    # Login successful
```

### Protected Routes

All routes marked with `@jwt_required()` need authentication:

```python
@jwt_required()
def protected_route():
    customer_id = get_jwt_identity()  # Extract user ID from token
    # Route logic
```

---

## 🔍 Advanced Queries

### 1. Pagination

**Implementation:**
```python
@customer_bp.route("", methods=['GET'])
@jwt_required()
def get_customers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    offset = (page - 1) * per_page
    query = select(Customer).limit(per_page).offset(offset)
    customers = db.session.execute(query).scalars().all()
    
    # Return with pagination metadata
```

**Usage:**
```bash
GET /customers?page=2&per_page=20
```

**Response:**
```json
{
  "customers": [...],
  "pagination": {
    "page": 2,
    "per_page": 20,
    "total_customers": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  }
}
```

### 2. Mechanic Sorting by Activity

**Implementation:**
```python
@mechanic_bp.route("/by-activity", methods=['GET'])
@jwt_required()
def get_mechanics_by_activity():
    mechanics = db.session.execute(select(Mechanic)).scalars().all()
    
    # Sort by number of tickets using relationship
    mechanics_list = list(mechanics)
    mechanics_list.sort(
        key=lambda mechanic: len(mechanic.ticket_mechanics),
        reverse=True  # Descending order
    )
    
    return jsonify([{
        'mechanic_id': m.mechanic_id,
        'full_name': m.full_name,
        'ticket_count': len(m.ticket_mechanics)
    } for m in mechanics_list])
```

**Usage:**
```bash
GET /mechanics/by-activity?order=desc&active_only=true
```

### 3. Bulk Mechanic Assignment

**Implementation:**
```python
@service_ticket_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
@jwt_required()
def edit_ticket_mechanics(ticket_id):
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])
    
    # Remove mechanics
    for mechanic_id in remove_ids:
        ticket_mechanic = db.session.execute(
            select(TicketMechanic).where(
                TicketMechanic.ticket_id == ticket_id,
                TicketMechanic.mechanic_id == mechanic_id
            )
        ).scalar_one_or_none()
        if ticket_mechanic:
            db.session.delete(ticket_mechanic)
    
    # Add mechanics
    for mechanic_id in add_ids:
        new_assignment = TicketMechanic(
            ticket_id=ticket_id,
            mechanic_id=mechanic_id,
            role=role,
            minutes_worked=0
        )
        db.session.add(new_assignment)
    
    db.session.commit()
```

---

## 📦 Inventory Management

### Part Model

```python
class Part(db.Model):
    part_id: int
    part_number: str  # Unique SKU
    name: str
    description: str
    category: str
    manufacturer: str
    current_cost_cents: int
    quantity_in_stock: int
    reorder_level: int
    supplier: str
    
    def needs_reorder(self):
        return self.quantity_in_stock <= self.reorder_level
```

### Many-to-Many with Service Tickets

**Junction Table: TicketPart**
```python
class TicketPart(db.Model):
    ticket_id: int
    part_id: int
    quantity_used: int
    unit_cost_cents: int
    markup_percentage: float
    installed_date: datetime
    warranty_months: int
    installed_by_mechanic_id: int
    
    def get_total_cost(self):
        base_cost = (self.quantity_used * self.unit_cost_cents) / 100
        markup = base_cost * (self.markup_percentage / 100)
        return round(base_cost + markup, 2)
```

### Inventory Operations

**1. Create Part**
```bash
POST /inventory
{
  "part_number": "BRK-001",
  "name": "Brake Pad Set",
  "category": "Brakes",
  "current_cost_cents": 4500,
  "quantity_in_stock": 25,
  "reorder_level": 5,
  "manufacturer": "AutoParts Inc",
  "supplier": "Parts Warehouse"
}
```

**2. Get Low-Stock Parts**
```bash
GET /inventory?low_stock=true
```

**3. Adjust Quantity**
```bash
PATCH /inventory/5/adjust-quantity
{
  "adjustment": 10  # Positive to add, negative to subtract
}
```

**4. Add Part to Ticket**
```bash
POST /service-tickets/1/parts/5
{
  "quantity_used": 2,
  "markup_percentage": 30.0,
  "warranty_months": 12,
  "installed_by_mechanic_id": 3
}
```

**Automatic Features:**
- ✅ Stock automatically decremented when part is used
- ✅ Cost captured at time of installation
- ✅ Warranty tracking
- ✅ Low-stock alerts
- ✅ Installation history

---

## 🧪 Testing with Postman

### Postman Collections

Two comprehensive Postman collections are included in `/Postman`:

#### **V1 Collection** (Initial Presentation)
- **File**: `Mechanic_Shop_API.postman_collection.json`
- **Environment**: `Mechanic_Shop_API.postman_environment.json`
- **Purpose**: Organized for initial V1 presentation with DELETE operations at the end

#### **V3 Collection** (Continuous Testing)
- **File**: `Mechanic_Shop_API_V3.postman_collection.json`
- **Environment**: `Mechanic_Shop_API_V3.postman_environment.json`
- **Purpose**: Streamlined for continuous testing after V1 presentation with all V3 features

### Complete Test Sequence

For detailed Postman testing workflow and instructions, see the full README or Postman collections.

---

## 🗃 Database Schema

### Core Models

**Customer** (Users/Accounts)
- customer_id (PK)
- first_name, last_name, email, phone
- address, city, state, postal_code
- password_hash, created_at

**Vehicle** (Customer Vehicles)
- vehicle_id (PK)
- customer_id (FK → Customer)
- vin, make, model, year, color

**Mechanic** (Staff Members)
- mechanic_id (PK)
- full_name, email, phone
- salary, is_active

**ServiceTicket** (Work Orders)
- ticket_id (PK)
- vehicle_id (FK → Vehicle)
- customer_id (FK → Customer)
- status, opened_at, closed_at
- problem_description, odometer_miles, priority

**Part** (Inventory)
- part_id (PK)
- part_number (unique), name, description
- category, manufacturer
- current_cost_cents, quantity_in_stock
- reorder_level, supplier

### Junction Tables (Many-to-Many)

**TicketMechanic**
- ticket_id (PK, FK → ServiceTicket)
- mechanic_id (PK, FK → Mechanic)
- role, minutes_worked

**TicketPart**
- ticket_id (PK, FK → ServiceTicket)
- part_id (PK, FK → Part)
- quantity_used, unit_cost_cents
- markup_percentage, warranty_months
- installed_date, installed_by_mechanic_id

### Relationships

```
Customer 1 ──────< M Vehicle
    │
    └─────< M ServiceTicket M >─────┐
                  │                  │
            (M) < │ > (M)      (M) < │ > (M)
                  │                  │
            TicketPart          TicketMechanic
                  │                  │
            (M) > │            (M) > │
                  │                  │
                Part              Mechanic
```

---

## 📁 Project Structure

```
Mechanic-Shop-V3/
├── application/                    # Main application package
│   ├── __init__.py                # Application factory with Swagger config
│   ├── extensions.py              # Flask extensions (db, jwt, limiter, cache)
│   ├── models.py                  # SQLAlchemy models (8 models)
│   └── blueprints/                # Feature modules
│       ├── auth/                  # Authentication (register, login)
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   ├── authSchemas.py
│       │   └── swagger_docs.txt   # ✅ V3 NEW
│       ├── customer/              # Customer & vehicle management
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   ├── customerSchemas.py
│       │   └── swagger_docs.txt   # ✅ V3 NEW
│       ├── mechanic/              # Mechanic management
│       │   ├── __init__.py
│       │   ├── routes.py          # Includes caching on GET
│       │   ├── mechanicSchemas.py
│       │   └── swagger_docs.txt   # ✅ V3 NEW
│       ├── service_ticket/        # Service ticket system
│       │   ├── __init__.py
│       │   ├── routes.py          # Includes part assignment
│       │   ├── serviceTicketSchemas.py
│       │   └── swagger_docs.txt   # ✅ V3 NEW
│       └── inventory/             # Parts inventory management
│           ├── __init__.py
│           ├── routes.py          # CRUD + quantity adjustment
│           ├── inventorySchemas.py
│           └── swagger_docs.txt   # ✅ V3 NEW
├── tests/                         # ✅ V3 NEW - unittest test suite
│   ├── __init__.py
│   ├── test_customer.py           # Customer route tests
│   ├── test_mechanic.py           # Mechanic route tests
│   ├── test_service_ticket.py     # Service ticket tests
│   └── test_inventory.py          # Inventory tests
├── migrations/                    # Database migrations
│   ├── versions/                  # Migration scripts
│   └── alembic.ini               # Alembic configuration
├── Postman/                       # API testing collections
│   ├── Mechanic_Shop_API.postman_collection.json
│   ├── Mechanic_Shop_API.postman_environment.json
│   ├── Mechanic_Shop_API_V3.postman_collection.json
│   └── Mechanic_Shop_API_V3.postman_environment.json
├── app.py                         # Application entry point
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
├── README.md                      # This file (comprehensive)
├── PRESENTATION.md                # Presentation guide for students
├── SWAGGER_DOCUMENTATION.md       # Complete Swagger docs
└── TESTING.md                     # Testing documentation
```

### Application Factory Pattern

The project uses the **Application Factory Pattern** for:
- **Modularity**: Blueprints organize code by feature
- **Testability**: Easy to create app instances with different configurations
- **Scalability**: Clean separation of concerns
- **Flexibility**: Support for multiple environments

---

## 🔧 Key Technologies

- **Flask 3.0+** - Web framework
- **SQLAlchemy 2.0+** - ORM for database operations
- **Flask-Migrate** - Database migrations (Alembic)
- **Flask-JWT-Extended** - JWT token authentication
- **Flask-Limiter** - Rate limiting
- **Flask-Caching** - Response caching
- **Flask-Swagger** - Swagger documentation generation ✅ **V3**
- **Flask-Swagger-UI** - Interactive API documentation ✅ **V3**
- **unittest** - Python testing framework ✅ **V3**
- **Flask-Marshmallow** - Object serialization/deserialization
- **MySQL 8.0+** - Relational database
- **Werkzeug** - Password hashing

---

## 📝 Additional Documentation

- **PRESENTATION.md** - Complete student presentation guide (separate file)
- **SWAGGER_DOCUMENTATION.md** - Detailed Swagger implementation guide
- **TESTING.md** - Comprehensive testing documentation
- **Postman/** - API testing collections with examples

---

## 🚀 Quick Start Guide

```bash
# 1. Clone and navigate to project
git clone https://github.com/growthwithcoding/Mechanic-Shop-V3.git
cd Mechanic-Shop-V3

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
mysql -u root -p
CREATE DATABASE mechanic_shop_v3;
EXIT;

# 5. Set environment variables
set FLASK_APP=app.py  # Windows
# export FLASK_APP=app.py  # Mac/Linux

# 6. Run migrations
flask db upgrade

# 7. Start the server
python app.py

# 8. Access Swagger Documentation
# Navigate to: http://127.0.0.1:5000/apidocs

# 9. Run tests
python -m unittest discover tests
```

---

## 💡 Usage Examples

### Complete Workflow Example

**1. Register a Customer**
```bash
POST /auth/register
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "secure123",
  "phone": "555-1234",
  "address": "123 Main St",
  "city": "Denver",
  "state": "CO",
  "postal_code": "80201"
}
```

**2. Login to Get Token**
```bash
POST /auth/login
{
  "email": "john@example.com",
  "password": "secure123"
}

Response: { "access_token": "eyJ..." }
```

**3. Add a Vehicle**
```bash
POST /customers/1/vehicles
Authorization: Bearer eyJ...
{
  "vin": "1HGBH41JXMN109186",
  "make": "Honda",
  "model": "Accord",
  "year": 2020,
  "color": "Silver"
}
```

**4. Create a Mechanic**
```bash
POST /mechanics
Authorization: Bearer eyJ...
{
  "full_name": "Mike Johnson",
  "email": "mike@shop.com",
  "phone": "555-5678",
  "salary": 65000,
  "is_active": true
}
```

**5. Add Part to Inventory**
```bash
POST /inventory
Authorization: Bearer eyJ...
{
  "part_number": "OIL-001",
  "name": "Engine Oil Filter",
  "category": "Filters",
  "current_cost_cents": 1200,
  "quantity_in_stock": 50,
  "reorder_level": 10
}
```

**6. Create Service Ticket**
```bash
POST /service-tickets
Authorization: Bearer eyJ...
{
  "vehicle_id": 1,
  "customer_id": 1,
  "status": "open",
  "problem_description": "Oil change needed",
  "odometer_miles": 35000,
  "priority": 2
}
```

**7. Assign Mechanic to Ticket**
```bash
PUT /service-tickets/1/assign-mechanic/1
Authorization: Bearer eyJ...
{
  "role": "Lead Technician",
  "minutes_worked": 0
}
```

**8. Add Part to Ticket**
```bash
POST /service-tickets/1/parts/1
Authorization: Bearer eyJ...
{
  "quantity_used": 1,
  "markup_percentage": 30.0,
  "warranty_months": 6
}
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- Flask documentation and community
- SQLAlchemy for excellent ORM capabilities
- Coding Temple instructors and curriculum
- Dylan Katina for V3 assignment requirements
- All contributors and testers

---

## 📞 Support

For questions, issues, or suggestions:

- Open an issue on GitHub
- Contact via LinkedIn: [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)

---

## 🎓 For Students

If you're a student working on a similar project:

1. Review **PRESENTATION.md** for presentation guidance
2. Study the Swagger documentation implementation
3. Examine the test suite structure and patterns
4. Use this project as a reference, but write your own code
5. Understanding the architecture is more important than copying code

---

**Built with ❤️ by Austin Carlson** | *#growthwithcoding*

**Version 3.0** - Documentation & Testing Focus
