# Testing Documentation - Mechanic Shop API V3

## Overview

This document provides comprehensive information about testing the Mechanic Shop API V3. The test suite uses Python's built-in `unittest` library and covers all API endpoints with both positive and negative test cases.

## Test Structure

```
tests/
├── __init__.py
├── test_auth.py           # Authentication route tests
├── test_customer.py       # Customer route tests
├── test_mechanic.py       # Mechanic route tests
├── test_inventory.py      # Inventory route tests
└── test_service_ticket.py # Service ticket route tests
```

## Running Tests

### Run All Tests

**Windows:**
```bash
python -m unittest discover tests
```

**Mac/Linux:**
```bash
python -m unittest discover tests
```

### Run Specific Test File

**Windows:**
```bash
python -m unittest tests.test_auth
python -m unittest tests.test_customer
python -m unittest tests.test_mechanic
python -m unittest tests.test_inventory
python -m unittest tests.test_service_ticket
```

**Mac/Linux:**
```bash
python -m unittest tests.test_auth
python -m unittest tests.test_customer
python -m unittest tests.test_mechanic
python -m unittest tests.test_inventory
python -m unittest tests.test_service_ticket
```

### Run Specific Test Class

```bash
python -m unittest tests.test_auth.TestAuthRoutes
```

### Run Specific Test Method

```bash
python -m unittest tests.test_auth.TestAuthRoutes.test_register_success
```

### Run with Verbose Output

```bash
python -m unittest discover tests -v
```

## Test Configuration

### ⚠️ Important: Separate Test Database

This project uses **TWO SEPARATE databases**:

1. **`mechanic_shop_v3`** - DEVELOPMENT Database
   - Used when running the API: `python app.py`
   - Uses `seed_sample_data.sql` for manual testing
   - Data persists between runs
   - **DO NOT use this for unit tests!**

2. **`mechanic_shop_v3_test`** - TEST Database
   - Used ONLY for unit tests: `python -m unittest`
   - Tests create/destroy their own temporary data
   - **Does NOT use seed_sample_data.sql**
   - Data is wiped after each test
   - Completely isolated from development data

### Configuration

Tests use the `TestingConfig` configuration from `config.py`:
- Database: `mechanic_shop_v3_test` (separate test database!)
- Testing mode enabled
- Rate limiting disabled for faster tests
- Isolated from development/production databases

**Important:** Create the test database before running tests:

```bash
# Option 1: Use the SQL script
mysql -u root -p < SQL/create_test_database.sql

# Option 2: Create manually
mysql -u root -p
CREATE DATABASE mechanic_shop_v3_test;
```

**Note:** You do NOT need to run migrations or seed data for the test database. Unit tests automatically create tables and test data in the `setUp()` method.

## Test Coverage by Blueprint

### 1. Authentication Tests (`test_auth.py`)

**Routes Tested:**
- `POST /auth/register` - Register new customer
- `POST /auth/login` - Login with credentials
- `GET /auth/me` - Get current user info

**Test Cases:**
- ✅ Successful registration
- ❌ Duplicate email registration
- ❌ Missing required fields
- ❌ Invalid email format
- ❌ No JSON data provided
- ✅ Successful login
- ❌ Invalid password
- ❌ Non-existent email
- ❌ Missing credentials
- ✅ Get current user with valid token
- ❌ Get current user without token
- ❌ Get current user with invalid token

### 2. Customer Tests (`test_customer.py`)

**Routes Tested:**
- `POST /customers` - Create customer (deprecated)
- `GET /customers` - Get all customers (paginated)
- `GET /customers/<id>` - Get specific customer
- `PUT /customers/<id>` - Update customer
- `DELETE /customers/<id>` - Delete customer
- `POST /customers/<id>/vehicles` - Create vehicle
- `GET /customers/<id>/vehicles` - Get customer vehicles
- `GET /customers/<id>/vehicles/<vehicle_id>` - Get specific vehicle
- `PUT /customers/<id>/vehicles/<vehicle_id>` - Update vehicle
- `DELETE /customers/<id>/vehicles/<vehicle_id>` - Delete vehicle

**Test Cases:**
- ✅ Create, read, update, delete operations
- ❌ Unauthorized access attempts
- ❌ Invalid data validation
- ❌ Resource not found errors
- ❌ Duplicate VIN checks
- ✅ Pagination functionality

### 3. Mechanic Tests (`test_mechanic.py`)

**Routes Tested:**
- `POST /mechanics` - Create mechanic
- `GET /mechanics` - Get all mechanics
- `GET /mechanics/by-activity` - Get mechanics by activity
- `GET /mechanics/<id>` - Get specific mechanic
- `PUT /mechanics/<id>` - Update mechanic
- `DELETE /mechanics/<id>` - Delete mechanic

**Test Cases:**
- ✅ CRUD operations for mechanics
- ❌ Duplicate email validation
- ❌ Missing required fields
- ❌ Unauthorized access
- ✅ Activity-based sorting

### 4. Inventory Tests (`test_inventory.py`)

**Routes Tested:**
- `POST /inventory` - Create part
- `GET /inventory` - Get all parts
- `GET /inventory/<id>` - Get specific part
- `PUT /inventory/<id>` - Update part
- `DELETE /inventory/<id>` - Delete part
- `PATCH /inventory/<id>/adjust-quantity` - Adjust quantity

**Test Cases:**
- ✅ CRUD operations for inventory
- ❌ Duplicate part numbers
- ❌ Invalid quantity adjustments
- ❌ Negative quantity prevention
- ✅ Low stock filtering

### 5. Service Ticket Tests (`test_service_ticket.py`)

**Routes Tested:**
- `POST /service_tickets` - Create ticket
- `GET /service_tickets` - Get all tickets
- `GET /service_tickets/<id>` - Get specific ticket
- `PUT /service_tickets/<id>` - Update ticket
- `DELETE /service_tickets/<id>` - Delete ticket
- `PUT /service_tickets/<id>/assign-mechanic/<mechanic_id>` - Assign mechanic
- `PUT /service_tickets/<id>/remove-mechanic/<mechanic_id>` - Remove mechanic
- `PUT /service_tickets/<id>/edit` - Edit ticket mechanics
- `POST /service_tickets/<id>/parts/<part_id>` - Add part to ticket

**Test Cases:**
- ✅ CRUD operations for tickets
- ✅ Mechanic assignment/removal
- ✅ Part addition to tickets
- ❌ Insufficient inventory checks
- ❌ Invalid mechanic/part references
- ❌ Unauthorized access

## How Unit Tests Work

### Data Isolation

Each test is completely isolated:

1. **Before Each Test** (`setUp()`):
   - `db.create_all()` creates fresh tables
   - Test-specific data is created
   - Example: Register a test user with `test@example.com`

2. **During Test**:
   - Test performs its operations
   - Assertions verify expected behavior

3. **After Each Test** (`tearDown()`):
   - `db.session.remove()` closes the session
   - `db.drop_all()` destroys all tables
   - Database is completely clean for next test

4. **Result**: Each test starts with a blank database

### Why Seed Data is NOT Used

Unit tests **do not use `seed_sample_data.sql`** because:
- Tests need predictable, controlled data
- Each test creates only the data it needs
- Tests must be independent and repeatable
- Seed data would cause conflicts and unpredictable results

### Development vs Test Credentials

**Development Database** (after running seed_sample_data.sql):
- Email: `alice.johnson@email.com`
- Password: `password123`
- Has 5 pre-seeded customers, mechanics, parts, etc.

**Test Database** (during unit tests):
- Email: `test@example.com` (or similar test-specific emails)
- Password: `TestPass123!` (or similar test-specific passwords)
- Data created fresh for each test
- No relationship to seed data

---

## Test Patterns

### Setup and Teardown

Each test class uses the following pattern:

```python
class TestExample(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        cls.app = create_app('testing')
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
    
    def setUp(self):
        """Run before each test"""
        db.create_all()
        # Create test data
    
    def tearDown(self):
        """Run after each test"""
        db.session.remove()
        db.drop_all()
    
    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        cls.app_context.pop()
```

### Authentication Helper

Tests that require authentication use this pattern:

```python
def setUp(self):
    db.create_all()
    
    # Register and get token
    register_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "TestPass123!",
        "phone": "555-000-0000"
    }
    response = self.client.post(
        '/auth/register',
        data=json.dumps(register_data),
        content_type='application/json'
    )
    self.token = json.loads(response.data)['access_token']
    self.headers = {'Authorization': f'Bearer {self.token}'}
```

### Negative Testing

All test files include negative tests to verify proper error handling:

```python
def test_example_negative(self):
    """Test with invalid data (negative test)"""
    response = self.client.post(
        '/endpoint',
        data=json.dumps(invalid_data),
        content_type='application/json'
    )
    
    self.assertEqual(response.status_code, 400)
    json_data = json.loads(response.data)
    self.assertIn('error', json_data)
```

## Best Practices

1. **Test Independence**: Each test should be independent and not rely on other tests
2. **Clean State**: Database is recreated for each test
3. **Descriptive Names**: Test method names clearly describe what is being tested
4. **Assertions**: Multiple assertions per test when appropriate
5. **Error Messages**: Tests include descriptive docstrings
6. **Coverage**: Both success and failure scenarios are tested

## Continuous Integration

To integrate these tests into a CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python -m unittest discover tests -v
```

## Troubleshooting

### Database Connection Errors

If tests fail with database connection errors:
1. Ensure MySQL is running
2. Verify test database exists: `CREATE DATABASE mechanic_shop_v3_test;`
3. Check credentials in `config.py`

### Import Errors

If you encounter import errors:
1. Ensure you're in the project root directory
2. Activate virtual environment
3. Install all dependencies: `pip install -r requirements.txt`

### JWT Token Errors

If JWT-related tests fail:
1. Verify JWT_SECRET_KEY is set in config
2. Check token expiration time
3. Ensure Flask-JWT-Extended is properly installed

## Test Results Example

```
test_create_mechanic_success (tests.test_mechanic.TestMechanicRoutes) ... ok
test_create_mechanic_duplicate_email (tests.test_mechanic.TestMechanicRoutes) ... ok
test_create_mechanic_no_auth (tests.test_mechanic.TestMechanicRoutes) ... ok
test_delete_mechanic_success (tests.test_mechanic.TestMechanicRoutes) ... ok
test_get_all_mechanics_success (tests.test_mechanic.TestMechanicRoutes) ... ok
test_login_success (tests.test_auth.TestAuthRoutes) ... ok
test_register_success (tests.test_auth.TestAuthRoutes) ... ok

----------------------------------------------------------------------
Ran 50 tests in 5.234s

OK
```

## Next Steps

1. Add integration tests for complex workflows
2. Implement performance testing
3. Add code coverage reporting with `coverage.py`
4. Create load testing scenarios
5. Add API contract testing

## Resources

- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Flask Testing Documentation](https://flask.palletsprojects.com/en/latest/testing/)
- [API Testing Best Practices](https://www.software testinghelp.com/api-testing/)
