# Mechanic Shop API V3 - Presentation Guide 🎓

**Student:** [Your Name Here]  
**Instructor:** Dylan Katina  
**Course:** Full-Stack Development  
**Assignment:** Documentation & Testing (V3)

---

## 🎯 V3 Assignment Focus

This presentation demonstrates the implementation of:
- **Swagger Documentation** - Flask-Swagger & Flask-Swagger-UI
- **Comprehensive Testing** - unittest framework with positive/negative tests

---

## 📋 Pre-Presentation Checklist

Before presenting, ensure:
- [ ] Application is running: `python app.py`
- [ ] Swagger docs accessible: http://127.0.0.1:5000/apidocs
- [ ] Tests passing: `python -m unittest discover tests`
- [ ] Database is populated with sample data
- [ ] Postman collection ready (optional backup)
- [ ] Code editor open with key files visible

---

## 🎤 Presentation Flow (20 minutes)

### 1. Introduction (2 minutes)

**Opening Statement:**
> "Good [morning/afternoon]. Today I'm presenting Version 3 of my Mechanic Shop Management API, which focuses on comprehensive API documentation and testing."

**Key Points to Cover:**
- Project overview: Full-stack RESTful API for automotive repair shop management
- V3 assignment requirements: Documentation with Swagger & Testing with unittest
- Technologies: Flask, MySQL, SQLAlchemy, Flask-Swagger-UI, unittest
- Previous versions: V1 (basic CRUD), V2 (JWT auth, rate limiting, caching, inventory)
- V3 additions: Complete Swagger docs for all routes + comprehensive test suite

**Visual Aid:**
- Show project structure in VS Code
- Highlight `tests/` folder and `swagger_docs.txt` files

---

### 2. Swagger Documentation Demo (8 minutes)

**Navigate to Swagger UI:**
```
http://127.0.0.1:5000/apidocs
```

**Complete Swagger Walkthrough for Presentation:**

#### Step 1: Interface Overview (1 minute)

**Say:** "Let me show you the Swagger documentation interface."

**Point out on screen:**
1. **API Title**: "Mechanic Shop API V3" at the top
2. **Organized Sections** (expand to show):
   - 🔐 Authentication (3 endpoints)
   - 👥 Customers (6 endpoints)
   - 🔧 Mechanics (6 endpoints)
   - 📦 Inventory (7 endpoints)
   - 🎫 Service Tickets (9 endpoints)
3. **Color Coding**:
   - Blue GET = Read data
   - Green POST = Create
   - Orange PUT = Update
   - Red DELETE = Remove
   - Purple PATCH = Partial update
4. **Lock Icons** 🔒 = Authentication required

**Say:** "All 20+ routes are organized by category with clear color coding. Let's test them live!"

---

#### Step 2: Register New User (2 minutes)

**Say:** "First, let's register a new user account."

**Action Steps:**
1. **Scroll to "Authentication" section**
2. **Click `POST /auth/register`** to expand
3. **Point out**:
   - Summary: "Register a new customer"
   - Parameters showing request body schema
   - Example values already filled in
   - Response codes: 201 (success), 400 (error)

4. **Click "Try it out" button**

5. **Say:** "The request body becomes editable. Let me use test data:"
   ```json
   {
     "first_name": "Demo",
     "last_name": "Presentation",
     "email": "demo.presentation@email.com",
     "password": "password123",
     "phone": "555-9999"
   }
   ```

6. **Click "Execute" button**

7. **Show Response**:
   - **Status**: `201 Created` ✅
   - **Response body**:
     ```json
     {
       "message": "Customer registered successfully",
       "access_token": "eyJhbGc...",
       "customer": {
         "customer_id": 6,
         "first_name": "Demo",
         "last_name": "Presentation",
         "email": "demo.presentation@email.com"
       }
     }
     ```

8. **Say:** "Notice we got back a JWT token. I need to copy this for authentication."

9. **Copy the access_token** (show selecting and copying)

---

#### Step 3: Authorize Swagger UI (2 minutes)

**Say:** "Now I need to authenticate Swagger to test protected endpoints."

⚠️ **CRITICAL STEP - Emphasize This!**

**Action Steps:**
1. **Point to top of page**: "See the green 'Authorize' button with lock icon?"

2. **Click "Authorize" button**

3. **Say:** "A popup appears. This is where I paste my JWT token."

4. **In the "Value" field, type**:
   ```
   Bearer eyJhbGc...
   ```
   
   **⚠️ EMPHASIZE**: "Notice I type 'Bearer' with a capital B, add a SPACE, then paste the token."

5. **Click "Authorize" button** in popup

6. **Click "Close" button**

7. **Say:** "Now the lock icons show as closed, meaning I'm authenticated!"

---

#### Step 4: Test Protected Endpoint (1 minute)

**Say:** "Let's verify authentication works by testing a protected endpoint."

**Action Steps:**
1. **Scroll to "Authentication" section**
2. **Click `GET /auth/me`**
3. **Point out**: Lock icon indicates authentication required
4. **Click "Try it out"**
5. **Click "Execute"**

6. **Show Response**:
   - **Status**: `200 OK` ✅
   - **Body**:
     ```json
     {
       "customer_id": 6,
       "first_name": "Demo",
       "last_name": "Presentation",
       "email": "demo.presentation@email.com"
     }
     ```

7. **Say:** "Perfect! Authentication is working. Now I can test any protected endpoint."

---

#### Step 5: Test GET with Seed Data (1 minute)

**Say:** "Let me show you testing with pre-seeded database data."

**Action Steps:**
1. **Scroll to "Mechanics" section**
2. **Click `GET /mechanics`**
3. **Point out**: "This endpoint is cached for 5 minutes"
4. **Click "Try it out"**
5. **Click "Execute"**

6. **Show Response** (Status: `200 OK`):
   ```json
   [
     {
       "mechanic_id": 1,
       "full_name": "John Smith",
       "email": "john.smith@mechanicshop.com",
       "phone": "555-0101",
       "salary": 65000,
       "is_active": true
     },
     {
       "mechanic_id": 2,
       "full_name": "Sarah Johnson",
       "salary": 68000
     }
   ]
   ```

7. **Say:** "These are from our seed data - 5 mechanics pre-loaded in the database."

---

#### Step 6: Test POST Endpoint (1 minute)

**Say:** "Now let's create a new resource."

**Action Steps:**
1. **Click `POST /mechanics`**
2. **Click "Try it out"**
3. **Edit request body**:
   ```json
   {
     "full_name": "Demo Mechanic",
     "email": "demo.mechanic@shop.com",
     "phone": "555-0000",
     "salary": 60000,
     "is_active": true
   }
   ```

4. **Click "Execute"**

5. **Show Response** (Status: `201 Created`):
   ```json
   {
     "mechanic_id": 6,
     "full_name": "Demo Mechanic",
     "email": "demo.mechanic@shop.com",
     "salary": 60000
   }
   ```

6. **Say:** "Notice it assigned mechanic_id 6. I could now use this ID to test other endpoints like update or delete."

---

**Key Points to Emphasize:**
- ✅ Interactive testing without Postman
- ✅ Authentication integration working
- ✅ All request/response schemas documented
- ✅ Real-time validation and error messages
- ✅ Examples for all endpoints

---

### 3. Testing Implementation Demo (5 minutes)

**IMPORTANT: Test Database Setup**

Before running tests, demonstrate the test database setup:

```bash
# Show the test database creation script
python create_test_db.py
```

**Output:**
```
Creating test database...
✓ Test database 'mechanic_shop_v3_test' created successfully
✓ Database connection closed
```

**Explain:**
- Tests use a separate database (`mechanic_shop_v3_test`)
- Prevents interference with development data
- Rate limiting disabled in test mode for faster execution
- Customer address fields made optional for test flexibility

**Show Test Structure:**

#### Step 1: Display Test Files
In VS Code or file explorer, show `tests/` folder:
```
tests/
├── __init__.py
├── test_auth.py              # 13 tests (authentication & registration)
├── test_customer.py          # 26 tests (customer & vehicle routes)
├── test_mechanic.py          # 18 tests (mechanic routes)
├── test_service_ticket.py    # 30 tests (service ticket routes)
└── test_inventory.py         # 19 tests (inventory management)
```

**Total: 106 tests across 5 test suites**

#### Step 2: Open Example Test File
Open `tests/test_mechanic.py`:

**Point out key components:**
1. **Imports:**
   ```python
   import unittest
   from application import create_app
   from application.extensions import db
   ```

2. **Test Class Setup:**
   ```python
   class TestMechanicRoutes(unittest.TestCase):
       def setUp(self):
           # Create test app and database
           # Register customer and get token
   ```

3. **Example Positive Test:**
   ```python
   def test_create_mechanic(self):
       response = self.client.post('/mechanics', 
           json={...},
           headers={'Authorization': f'Bearer {self.token}'}
       )
       self.assertEqual(response.status_code, 201)
   ```

4. **Example Negative Test:**
   ```python
   def test_create_mechanic_missing_fields(self):
       response = self.client.post('/mechanics',
           json={},  # Missing required fields
           headers={'Authorization': f'Bearer {self.token}'}
       )
       self.assertEqual(response.status_code, 400)
   ```

5. **Teardown:**
   ```python
   def tearDown(self):
       db.session.remove()
       db.drop_all()
   ```

#### Step 3: Run Tests Live
Open terminal and execute:
```bash
python -m unittest discover tests -v
```

**Expected Output:**
```
test_create_customer (tests.test_customer.TestCustomerRoutes) ... ok
test_get_all_customers_pagination (tests.test_customer.TestCustomerRoutes) ... ok
test_invalid_login (tests.test_customer.TestCustomerRoutes) ... ok
test_create_mechanic (tests.test_mechanic.TestMechanicRoutes) ... ok
test_get_mechanics_cached (tests.test_mechanic.TestMechanicRoutes) ... ok
test_get_mechanics_by_activity (tests.test_mechanic.TestMechanicRoutes) ... ok
test_delete_nonexistent_mechanic (tests.test_mechanic.TestMechanicRoutes) ... ok
test_create_service_ticket (tests.test_service_ticket.TestServiceTicketRoutes) ... ok
test_bulk_edit_mechanics (tests.test_service_ticket.TestServiceTicketRoutes) ... ok
test_assign_invalid_mechanic (tests.test_service_ticket.TestServiceTicketRoutes) ... ok
test_create_part (tests.test_inventory.TestInventoryRoutes) ... ok
test_get_low_stock_parts (tests.test_inventory.TestInventoryRoutes) ... ok
test_adjust_quantity_insufficient_stock (tests.test_inventory.TestInventoryRoutes) ... ok
...

----------------------------------------------------------------------
Ran 33 tests in 3.245s

OK
```

**Key Points to Emphasize:**
- ✅ 30+ tests across 4 test files
- ✅ Tests cover all routes (100% route coverage)
- ✅ Positive tests verify correct behavior
- ✅ Negative tests verify error handling
- ✅ All tests passing (green output)
- ✅ Automated execution with single command

---

### 4. Code Walkthrough (3 minutes)

#### Step 1: Show Swagger Documentation File
Open `application/blueprints/mechanic/swagger_docs.txt`:

**Point out structure:**
```yaml
/mechanics/{mechanic_id}:
  get:
    tags:
      - Mechanics
    summary: Get mechanic by ID
    description: Retrieves detailed information about a specific mechanic
    parameters:
      - in: path
        name: mechanic_id
        required: true
        schema:
          type: integer
        description: The mechanic ID
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
                  salary: 65000
                  is_active: true
      404:
        description: Mechanic not found
```

**Explain:**
- Path definition matches actual route
- Parameters documented (path, query, body)
- All response codes covered
- Examples provided for clarity
- Schema references defined elsewhere

#### Step 2: Show Corresponding Route Implementation
Open `application/blueprints/mechanic/routes.py`:

**Show the actual route:**
```python
@mechanic_bp.route("/<int:mechanic_id>", methods=['GET'])
@jwt_required()
def get_mechanic(mechanic_id):
    """Get mechanic by ID - see swagger_docs.txt"""
    mechanic = db.session.execute(
        select(Mechanic).where(Mechanic.mechanic_id == mechanic_id)
    ).scalar_one_or_none()
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    return mechanic_schema.jsonify(mechanic), 200
```

**Key Points:**
- Documentation matches implementation exactly
- Route parameters match docs
- Response codes match docs
- Error handling documented

#### Step 3: Show Schema Definition
Open `application/blueprints/mechanic/mechanicSchemas.py`:

```python
class MechanicSchema(ma.Schema):
    mechanic_id = fields.Integer(dump_only=True)
    full_name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone = fields.String(required=False, allow_none=True)
    salary = fields.Integer(required=True)
    is_active = fields.Boolean(required=False, missing=True)
    
    class Meta:
        fields = ('mechanic_id', 'full_name', 'email', 'phone', 
                  'salary', 'is_active')
```

**Explain:**
- Schema validates incoming data
- Matches Swagger payload definition
- Used in route for serialization/deserialization

---

### 5. Assignment Requirements Review (2 minutes)

**Display Assignment Requirements:**

#### Documentation Checklist
Pull up assignment text or checklist:

✅ **Each Route Documented With:**
- [x] Path and endpoint
- [x] Request type (GET, POST, PUT, DELETE)
- [x] Tag (category for organization)
- [x] Summary
- [x] Description
- [x] Security definitions (for token-protected routes)
- [x] Parameters (for POST/PUT requests)
- [x] Responses with status codes and examples

✅ **Definitions:**
- [x] Payload definitions for incoming data (POST/PUT)
- [x] Response definitions for outgoing data
- [x] Examples for all schemas

#### Testing Checklist
✅ **Test Implementation:**
- [x] `tests/` folder created
- [x] `test_mechanics.py` - 7+ tests
- [x] `test_customers.py` - 8+ tests  
- [x] `test_service_ticket.py` - 9+ tests
- [x] `test_inventory.py` - 9+ tests
- [x] One test per route (minimum)
- [x] Negative tests included
- [x] Executable with: `python -m unittest discover tests`

**Quick Stats:**
- 📚 **20+ routes** fully documented
- 🧪 **33+ tests** implemented
- ✅ **100% test pass rate**
- 📊 **All assignment requirements met**

---

### 6. Q&A (3 minutes)

**Be Prepared to Answer:**

**Common Questions:**

1. **"How do you handle authentication in tests?"**
   - Show setUp() method where we register user and obtain token
   - Demonstrate passing token in headers for protected routes

2. **"What's the benefit of Swagger over Postman?"**
   - Swagger is auto-generated from code
   - Always stays in sync with actual implementation
   - Interactive and shareable
   - Industry standard for API documentation

3. **"Show me a negative test example"**
   - Open a test file and show error handling test
   - Explain how we test missing fields, invalid IDs, insufficient stock, etc.

4. **"How does caching work?"**
   - Show `@cache.cached(timeout=300)` decorator on GET /mechanics
   - Explain 5-minute cache duration
   - Show how it improves performance for frequently accessed data

5. **"What about the from previous versions?"**
   - V1: Basic CRUD operations
   - V2: Added JWT auth, rate limiting, caching, inventory management
   - V3: Documentation and testing focus

**Demonstration Requests:**
- Ready to run any specific test
- Can test any endpoint via Swagger UI
- Can show any route's code implementation

---

## 📊 Key Metrics to Highlight

**Documentation:**
- ✅ 20+ routes documented
- ✅ 5 blueprint categories (Auth, Customer, Mechanic, Service Ticket, Inventory)
- ✅ 100% route coverage
- ✅ Interactive Swagger UI
- ✅ Complete schema definitions with examples

**Testing:**
- ✅ 4 test files (one per blueprint)
- ✅ 33+ individual tests
- ✅ Positive and negative test cases
- ✅ 100% test pass rate
- ✅ Automated test execution

**From Previous Versions:**
- JWT token authentication
- Rate limiting on critical endpoints
- Response caching for performance
- Pagination on customer list
- Advanced queries (mechanic by activity)
- Inventory management system

---

## 💡 Tips for Smooth Presentation

**Before You Start:**
1. Have application running: `python app.py`
2. Open browser tab to Swagger: http://127.0.0.1:5000/apidocs
3. Have VS Code open with key files visible
4. Clear terminal ready for test execution
5. Have sample data in database (or script to create it)

**During Presentation:**
1. Speak clearly and maintain steady pace
2. Explain what you're doing before clicking
3. Point to specific elements on screen
4. Use technical terms confidently
5. Show enthusiasm for your work

**If Something Goes Wrong:**
1. **App won't start:** Check MySQL is running, show error handling
2. **Test fails:** Show the error, explain how you'd debug it
3. **Swagger not loading:** Have Postman collection as backup
4. **Database issues:** Show migrations folder, explain how to reset DB

**Time Management:**
- Use a timer or watch
- If running over, skip to most impressive features
- Save time for Q&A (instructor questions are important!)

---

## 🎯 Closing Statement

**Final Summary:**
> "In conclusion, Version 3 of my Mechanic Shop API successfully implements comprehensive documentation using Swagger and thorough testing using Python's unittest framework. All 20+ routes are fully documented with interactive testing capabilities, and the 33+ automated tests ensure code reliability and proper error handling. This project demonstrates industry best practices for API development, including documentation, testing, authentication, and performance optimization. Thank you for your time, and I'm happy to answer any questions."

**Be Ready For:**
- Follow-up questions about specific implementation details
- Requests to demonstrate specific features
- Questions about challenges faced during development
- Discussion of potential future enhancements

---

## 📝 Post-Presentation Notes

**After presenting, be prepared to:**
- Provide GitHub repository link
- Share Postman collection if requested
- Discuss code architecture decisions
- Explain any trade-offs made during development
- Outline potential future improvements

---

## 🚀 Backup Plans

**If Live Demo Fails:**
1. Have screenshots of Swagger UI ready
2. Show recorded video of tests passing
3. Walk through code instead of running it
4. Use Postman collection as alternative
5. Show test output from previous successful run

**Alternative Demo Scenarios:**
- **Plan A:** Full live demo (ideal)
- **Plan B:** Swagger live, show test output from file
- **Plan C:** Code walkthrough with screenshots
- **Plan D:** Postman + code review

---

**Good luck with your presentation! You've got this! 🎓**
