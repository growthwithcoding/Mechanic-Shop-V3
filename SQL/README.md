# SQL Scripts for Mechanic Shop V3

This folder contains SQL scripts for database setup and seeding.

## Files

### 1. recreate_database.sql
**Purpose**: Drops and recreates the `mechanic_shop_v3` database

**When to use**: 
- Initial setup
- When you need a fresh database
- After major schema changes

**How to run**:
```bash
mysql -u root -p < SQL/recreate_database.sql
```

**After running**: Execute Flask migrations to create tables
```bash
flask db upgrade
```

---

### 2. seed_sample_data.sql
**Purpose**: Populates the database with sample data for testing

**Includes**:
- 5 Sample Mechanics
- 10 Sample Services
- 12 Sample Parts (Inventory items)
- 8 Specializations
- Mechanic certifications
- Service packages
- Service prerequisites

**When to use**:
- After running migrations
- For testing and development
- To quickly populate a new database

**How to run**:
```bash
# Make sure database and tables exist first
flask db upgrade

# Then seed the data
mysql -u root -p mechanic_shop_v3 < SQL/seed_sample_data.sql
```

**Note**: Customers, Vehicles, and Service Tickets should be created via API endpoints to ensure proper password hashing and validation.

---

### 3. fix_user_permissions.sql
**Purpose**: Grants necessary privileges to database user

**When to use**:
- When you encounter "Access Denied" errors
- After creating a new database user
- If migrations fail due to permissions

**How to run**:
```bash
mysql -u root -p < SQL/fix_user_permissions.sql
```

**Important**: Update the username/host in the script if not using 'root'@'localhost'

---

## Complete Setup Workflow

Follow these steps for a complete database setup:

```bash
# 1. Create/Recreate Database
mysql -u root -p < SQL/recreate_database.sql

# 2. Run Migrations (creates all tables)
set FLASK_APP=app.py  # Windows
flask db upgrade

# 3. Seed Sample Data
mysql -u root -p mechanic_shop_v3 < SQL/seed_sample_data.sql

# 4. (Optional) Fix Permissions if needed
mysql -u root -p < SQL/fix_user_permissions.sql
```

---

## Testing Data via API

After seeding, use these API endpoints to complete the setup:

### 1. Register a Customer
```bash
POST /auth/register
{
  "first_name": "Test",
  "last_name": "User",
  "email": "test@example.com",
  "password": "password123",
  "phone": "555-9999",
  "address": "123 Test St",
  "city": "Denver",
  "state": "CO",
  "postal_code": "80201"
}
```

### 2. Login to Get Token
```bash
POST /auth/login
{
  "email": "test@example.com",
  "password": "password123"
}
```

### 3. Create a Vehicle
```bash
POST /customers/1/vehicles
Authorization: Bearer {token}
{
  "vin": "1HGCM82633A123456",
  "make": "Honda",
  "model": "Accord",
  "year": 2020,
  "color": "Blue"
}
```

### 4. Create a Service Ticket
```bash
POST /service-tickets
Authorization: Bearer {token}
{
  "vehicle_id": 1,
  "customer_id": 1,
  "status": "open",
  "problem_description": "Oil change needed",
  "odometer_miles": 50000,
  "priority": 2
}
```

### 5. Assign Mechanic to Ticket
```bash
PUT /service-tickets/1/assign-mechanic/1
Authorization: Bearer {token}
{
  "role": "Lead Technician",
  "minutes_worked": 0
}
```

### 6. Add Part to Ticket
```bash
POST /service-tickets/1/parts/1
Authorization: Bearer {token}
{
  "quantity_used": 1,
  "markup_percentage": 30.0,
  "warranty_months": 6
}
```

---

## Sample Data Overview

### Mechanics
- **John Smith** - ASE Master, Engine Specialist
- **Sarah Johnson** - Brake Specialist, ASE Master
- **Mike Williams** - Transmission Specialist
- **Emily Davis** - Electrical Systems, Hybrid/EV Certified
- **Robert Brown** - Suspension & Steering Expert

### Services
- Oil Change ($35.00)
- Tire Rotation ($25.00)
- Brake Inspection ($50.00)
- Brake Pad Replacement ($150.00)
- Engine Diagnostic ($85.00)
- And 5 more...

### Parts
- Engine Oil 5W-30 (50 in stock)
- Oil Filter (75 in stock)
- Brake Pad Sets (45 total)
- Brake Rotors (27 total)
- And 8 more...

---

## Troubleshooting

### "Database does not exist"
Run `recreate_database.sql` first

### "Table doesn't exist"
Run `flask db upgrade` after creating database

### "Access denied"
Run `fix_user_permissions.sql` with appropriate user credentials

### "No sample data"
Run `seed_sample_data.sql` after migrations

### "Password authentication failed"
Update database connection string in `config.py` or environment variables

---

For more information, see the main README.md in the project root.
