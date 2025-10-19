# Mechanic Shop Management API - V2

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

An advanced RESTful API for managing automotive repair shop operations with rate limiting, caching, JWT authentication, and comprehensive inventory management. Built with Flask and SQLAlchemy using the Application Factory Pattern.

## 🎯 Project Overview

This is the **advanced version** of the Mechanic Shop API, implementing sophisticated features including:
- **Rate Limiting** - API protection against abuse
- **Caching** - Performance optimization for frequently accessed data
- **JWT Token Authentication** - Secure customer and mechanic access
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

- [Advanced Features](#-advanced-features-highlights)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Database Setup](#-database-setup)
- [API Endpoints](#-api-endpoints)
- [Rate Limiting & Caching](#-rate-limiting--caching)
- [Authentication](#-authentication)
- [Advanced Queries](#-advanced-queries)
- [Inventory Management](#-inventory-management)
- [Testing with Postman](#-testing-with-postman)
- [Database Schema](#-database-schema)
- [Project Structure](#-project-structure)

---

## ✨ Advanced Features Highlights

### 1. Rate Limiting
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

### 2. Caching
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

### 3. JWT Token Authentication

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

### 4. Advanced Queries

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

### 5. Inventory Management

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
   git clone https://github.com/growthwithcoding/Mechanic-Shop-V2.git
   cd Mechanic-Shop-V2
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
   CREATE DATABASE mechanic_shop_v2;
   ```

5. **Configure environment variables**
   
   Create a `.env` file or set environment variables:
   ```bash
   # Database connection
   DEV_DATABASE_URL=mysql+mysqlconnector://root:your_password@127.0.0.1/mechanic_shop_v2
   
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

---

## ⚙️ Configuration

The application supports multiple environments through `config.py`:

### Development
```python
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@127.0.0.1/mechanic_shop_v2'
```

### Production
```python
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

## 🔌 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Rate Limit | Auth Required |
|--------|----------|-------------|------------|---------------|
| POST | `/auth/register` | Register new customer | 3/hour | No |
| POST | `/auth/login` | Login and get JWT token | 5/min | No |
| GET | `/auth/me` | Get current user info | - | Yes |

**Example: Register**
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "city": "Denver",
    "state": "CO",
    "postal_code": "80201",
    "password": "securepass123"
  }'
```

**Example: Login**
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'
```

### Customer Endpoints

| Method | Endpoint | Description | Pagination | Auth Required |
|--------|----------|-------------|------------|---------------|
| GET | `/customers` | List all customers | Yes | Yes |
| GET | `/customers/<id>` | Get customer details | - | Yes |
| PUT | `/customers/<id>` | Update customer (own account) | - | Yes |
| DELETE | `/customers/<id>` | Delete customer (own account) | - | Yes |
| POST | `/customers/<id>/vehicles` | Add vehicle | - | Yes |
| GET | `/customers/<id>/vehicles` | Get customer vehicles | - | Yes |

**Example: Get Customers with Pagination**
```bash
curl -X GET "http://127.0.0.1:5000/customers?page=1&per_page=10" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Mechanic Endpoints

| Method | Endpoint | Description | Cached | Auth Required |
|--------|----------|-------------|--------|---------------|
| POST | `/mechanics` | Create mechanic | No | Yes |
| GET | `/mechanics` | List all mechanics | Yes (5min) | Yes |
| GET | `/mechanics/<id>` | Get mechanic details | No | Yes |
| GET | `/mechanics/by-activity` | Sort by ticket count | No | Yes |
| PUT | `/mechanics/<id>` | Update mechanic | No | Yes |
| DELETE | `/mechanics/<id>` | Delete mechanic | No | Yes |

**Example: Get Mechanics Sorted by Activity**
```bash
curl -X GET "http://127.0.0.1:5000/mechanics/by-activity?order=desc&active_only=true" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

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

**Example: Create Service Ticket**
```bash
curl -X POST http://127.0.0.1:5000/service-tickets \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vehicle_id": 1,
    "customer_id": 1,
    "status": "open",
    "problem_description": "Engine making strange noise",
    "odometer_miles": 45000,
    "priority": 3
  }'
```

**Example: Bulk Edit Mechanics**
```bash
curl -X PUT http://127.0.0.1:5000/service-tickets/1/edit \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "add_ids": [1, 2],
    "remove_ids": [3],
    "role": "Lead Technician",
    "minutes_worked": 0
  }'
```

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

**Example: Create Part**
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "part_number": "BRK-001",
    "name": "Brake Pad Set",
    "category": "Brakes",
    "current_cost_cents": 4500,
    "quantity_in_stock": 25,
    "reorder_level": 5,
    "manufacturer": "AutoParts Inc",
    "supplier": "Parts Warehouse"
  }'
```

**Example: Add Part to Ticket**
```bash
curl -X POST http://127.0.0.1:5000/service-tickets/1/parts/5 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "quantity_used": 2,
    "markup_percentage": 30.0,
    "warranty_months": 12,
    "installed_by_mechanic_id": 3
  }'
```

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

**Benefits:**
- Reduces payload size
- Improves API performance
- Better user experience
- Scalable for large datasets

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

**Query Parameters:**
- `order`: `desc` (most active first) or `asc` (least active first)
- `active_only`: `true` to filter only active mechanics

**Use Cases:**
- Performance reviews
- Workload balancing
- Identify top performers
- Resource allocation

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

**Usage:**
```bash
PUT /service-tickets/1/edit
{
  "add_ids": [1, 2, 3],
  "remove_ids": [4, 5],
  "role": "Lead Technician",
  "minutes_worked": 0
}
```

**Benefits:**
- Single request for multiple changes
- Atomic operations
- Reduced network overhead
- Better error handling

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
  "reorder_level": 5
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

#### **V2 Collection** (Continuous Testing) ✨ NEW
- **File**: `Mechanic_Shop_API_V2.postman_collection.json`
- **Environment**: `Mechanic_Shop_API_V2.postman_environment.json`
- **Purpose**: Streamlined for continuous testing after V1 presentation with all V2 features

### Import Instructions

1. Open Postman
2. Click **Import**
3. Select **both** collection files and **both** environment files from `/Postman` directory
4. You'll have two collections:
   - **Mechanic Shop API - Complete Collection** (V1)
   - **Mechanic Shop API V2 - Complete Testing Suite** (V2)

### V2 Collection Structure (Recommended for Testing)

**📁 1. Authentication**
- Register Customer 1
- Login Customer
- Get Current User
- 🆕 **V2 Features**: Rate limiting (3/hour register, 5/min login), JWT tokens

**📁 2. Customers (Paginated)**
- Get All Customers (Page 1) - 🆕 **V2**: Pagination with metadata
- Get Single Customer
- Update Customer

**📁 3. Vehicles**
- Create Vehicle
- Get Customer Vehicles
- Update Vehicle
- Delete Vehicle

**📁 4. Mechanics - FULL CRUD** ✅ **ASSIGNMENT**
- ✅ CREATE Mechanic 1, 2, 3
- ✅ GET All Mechanics (CACHED) - 🆕 **V2**: Cached 5 minutes
- ✅ GET Single Mechanic
- 🆕 GET Mechanics by Activity - **V2 ADVANCED**: Sort by ticket count
- ✅ UPDATE Mechanic
- ✅ DELETE Mechanic

**📁 5. Service Tickets - FULL CRUD** ✅ **ASSIGNMENT**
- ✅ CREATE Service Ticket 1, 2
- ✅ GET All Service Tickets
- ✅ GET Single Ticket
- ✅ ASSIGN Mechanic to Ticket
- ✅ ASSIGN Second Mechanic
- ✅ REMOVE Mechanic from Ticket
- 🆕 BULK EDIT Mechanics - **V2 ADVANCED**: Add/remove multiple mechanics
- ✅ UPDATE Service Ticket
- ✅ DELETE Service Ticket

**📁 6. Inventory - Parts** 🆕 **V2 FEATURE**
- CREATE Part (Brake Pads)
- GET All Parts
- GET Low Stock Parts
- GET Single Part
- UPDATE Part
- ADJUST Part Quantity
- ADD Part to Ticket
- DELETE Part

### Environment Variables (V2)

The V2 environment automatically manages:
- `base_url` - API base URL (http://localhost:5000)
- `jwt_token` / `jwt_token_2` - JWT authentication tokens (auto-saved)
- `customer_id` / `customer_id_2` - Customer IDs (auto-saved)
- `mechanic_id` / `mechanic_id_2` / `mechanic_id_3` - Mechanic IDs (auto-saved)
- `vehicle_id` / `vehicle_id_2` - Vehicle IDs (auto-saved)
- `ticket_id` / `ticket_id_2` - Service ticket IDs (auto-saved)
- `part_id` - Part ID (auto-saved)

### V2 Testing Workflow (Continuous Testing)

1. **Select Environment**: Choose "Mechanic Shop V2 - Local"
2. **Run Sequentially**: Execute requests in order from top to bottom
3. **Automatic Saves**: All IDs and tokens are automatically captured
4. **Continuous Testing**: Collection is designed to be run multiple times
5. **No Cleanup Needed**: Each run creates new test data

### Complete Test Sequence (V2)

```
Authentication Flow:
1. Register Customer 1 → Saves jwt_token & customer_id
2. Login Customer → Refreshes jwt_token
3. Get Current User → Verifies authentication

Data Creation:
4. Get All Customers (Paginated) → Test pagination
5. Create Vehicle → Saves vehicle_id
6. Create Mechanic 1 → Saves mechanic_id
7. Create Mechanic 2 → Saves mechanic_id_2
8. Create Mechanic 3 → Saves mechanic_id_3
9. Get All Mechanics (CACHED) → Test caching
10. Get Mechanics by Activity → Test V2 advanced query

Service Tickets:
11. Create Service Ticket 1 → Saves ticket_id
12. Create Service Ticket 2 → Saves ticket_id_2
13. Get All Service Tickets
14. Assign Mechanic to Ticket → Test assignment
15. Assign Second Mechanic → Test multiple assignments
16. Remove Mechanic from Ticket → Test removal
17. Bulk Edit Mechanics → Test V2 bulk operations
18. Update Service Ticket → Test status changes

Inventory Management:
19. Create Part (Brake Pads) → Saves part_id
20. Get All Parts
21. Get Low Stock Parts → Test filtering
22. Adjust Part Quantity → Test inventory updates
23. Add Part to Ticket → Test parts integration

Updates & Deletes:
24. Update Customer, Vehicle, Mechanic, Ticket
25. Delete operations (Vehicle, Mechanic, Ticket, Part)
```

### V2 Features to Demonstrate

1. **Rate Limiting**
   - Try registering more than 3 times

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
Mechanic-Shop-V2/
├── application/                    # Main application package
│   ├── __init__.py                # Application factory
│   ├── extensions.py              # Flask extensions (db, jwt, limiter, cache)
│   ├── models.py                  # SQLAlchemy models (11 models)
│   └── blueprints/                # Feature modules
│       ├── auth/                  # Authentication (register, login)
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── authSchemas.py
│       ├── customer/              # Customer & vehicle management
│       │   ├── __init__.py
│       │   ├── routes.py
│       │   └── customerSchemas.py
│       ├── mechanic/              # Mechanic management
│       │   ├── __init__.py
│       │   ├── routes.py          # Includes caching on GET
│       │   └── mechanicSchemas.py
│       ├── service_ticket/        # Service ticket system
│       │   ├── __init__.py
│       │   ├── routes.py          # Includes part assignment
│       │   └── serviceTicketSchemas.py
│       └── inventory/             # Parts inventory management
│           ├── __init__.py
│           ├── routes.py          # CRUD + quantity adjustment
│           └── inventorySchemas.py
├── migrations/                    # Database migrations
│   ├── versions/                  # Migration scripts
│   └── alembic.ini               # Alembic configuration
├── Postman/                       # API testing collection
│   ├── Mechanic_Shop_API.postman_collection.json
│   └── Mechanic_Shop_API.postman_environment.json
├── app.py                         # Application entry point
├── config.py                      # Configuration settings
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore file
└── README.md                      # This file
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
- **Flask-Marshmallow** - Object serialization/deserialization
- **MySQL 8.0+** - Relational database
- **Werkzeug** - Password hashing

---

## 📝 Assignment Requirements Checklist

### ✅ Rate Limiting & Caching
- [x] Rate limiting applied to registration (3/hour)
- [x] Rate limiting applied to login (5/minute)
- [x] Rate limiting applied to other routes
- [x] Caching implemented on GET /mechanics (5 minutes)
- [x] Flask-Limiter package integrated
- [x] Flask-Caching package integrated

### ✅ Token Authentication
- [x] JWT encode_token function implemented
- [x] login_schema created (email & password only)
- [x] POST /auth/login route created
- [x] Token returned after successful login
- [x] @jwt_required wrapper on protected routes
- [x] Token-protected route for customer's tickets
- [x] python-jose package (via Flask-JWT-Extended)

### ✅ Advanced Queries
- [x] PUT /service-tickets/<id>/edit for mechanic editing
- [x] Accepts remove_ids and add_ids parameters
- [x] GET /mechanics/by-activity sorts by ticket count
- [x] Pagination applied to GET /customers
- [x] Page and per_page parameters supported

### ✅ Inventory Management
- [x] Inventory (Part) model created with required fields
- [x] Many-to-many relationship: Inventory ↔ ServiceTicket
- [x] Junction table (TicketPart) with quantity field
- [x] Inventory blueprint created
- [x] Inventory CRUD routes implemented
- [x] POST route to add part to service ticket

### ✅ Testing
- [x] Postman collection with all endpoints
- [x] Postman environment for local testing
- [x] All routes tested and verified

---

## 🚀 Quick Start Guide

```bash
# 1. Clone and navigate to project
git clone https://github.com/growthwithcoding/Mechanic-Shop-V2.git
cd Mechanic-Shop-V2

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create database
mysql -u root -p
CREATE DATABASE mechanic_shop_v2;
exit;

# 5. Set environment variables
set FLASK_APP=app.py  # Windows
# export FLASK_APP=app.py  # Mac/Linux

# 6. Run migrations
flask db upgrade

# 7. Start the server
python app.py
```

Server runs at `http://127.0.0.1:5000`

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
- All contributors and testers

---

## 📞 Support

For questions, issues, or suggestions:

- Open an issue on GitHub
- Contact via LinkedIn: [Austin Carlson](https://www.linkedin.com/in/austin-carlson-720b65375/)

---

**Built with ❤️ by Austin Carlson** | *#growthwithcoding*
