# 🧪 Postman API Testing Guide - Step by Step

**Complete walkthrough for testing the Mechanic Shop API V3**

This guide will walk you through testing every endpoint of the API, one step at a time. Follow each step in order for best results.

---

## 📥 Setup Instructions

### Step 1: Import Collections and Environment

1. **Open Postman**
   - If you don't have Postman, download it from [postman.com](https://www.postman.com/downloads/)

2. **Import the V3 Collection**
   - Click **Import** button (top left)
   - Navigate to the project folder: `k:\Mechanic-Shop-V3\Postman`
   - Select `Mechanic_Shop_API_V3.postman_collection.json`
   - Click **Import**

3. **Import the V3 Environment**
   - Click **Import** again
   - Select `Mechanic_Shop_API_V3.postman_environment.json`
   - Click **Import**

4. **Select the Environment**
   - In the top-right corner, click the environment dropdown
   - Select **"Mechanic Shop V3 - Local"**
   - You should see it highlighted/selected

### Step 2: Start Your API Server

Before testing, make sure your API is running:

```bash
# In your project directory
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

✅ **Ready to Test!** The API is now running and Postman is configured.

---

## 🔐 Phase 1: Authentication Testing

### Test 1: Register Customer 1

**Purpose**: Create a new customer account and receive a JWT token

**Steps**:
1. In Postman, expand **"1. Authentication"** folder
2. Click **"Register Customer 1"**
3. Review the request body (JSON with customer details)
4. Click **"Send"** button

**Expected Response** (Status: `201 Created`):
```json
{
  "access_token": "eyJhbGc...", 
  "customer": {
    "customer_id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "555-1234",
    "address": "123 Main St",
    "city": "Denver",
    "state": "CO",
    "postal_code": "80202",
    "created_at": "2025-10-19T..."
  }
}
```

**What Just Happened**:
- ✅ New customer account created
- ✅ JWT token automatically saved to `{{jwt_token}}` variable
- ✅ Customer ID automatically saved to `{{customer_id}}` variable
- ✅ Rate limiting applied (3 registrations per hour)

**Verify**: 
- Check the **"Tests"** tab - you should see green checkmarks ✅
- Look at the environment variables (eye icon 👁️ in top right) - `jwt_token` and `customer_id` should have values

---

### Test 2: Login Customer

**Purpose**: Login with existing credentials to get a fresh token

**Steps**:
1. Click **"Login Customer"** request
2. Review the body (only email and password)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "access_token": "eyJhbGc...",
  "customer": {
    "customer_id": 1,
    "email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

**What Just Happened**:
- ✅ Logged in successfully
- ✅ New JWT token saved (replaces previous one)
- ✅ Rate limiting applied (5 logins per minute)

**Try This**: Test rate limiting
- Click Send 6 times rapidly
- On the 6th attempt, you should get: `429 Too Many Requests`

---

### Test 3: Get Current User

**Purpose**: Verify authentication is working by getting user info

**Steps**:
1. Click **"Get Current User"** request
2. Notice the **Authorization** header uses `{{jwt_token}}`
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "customer_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "555-1234",
  "address": "123 Main St",
  "city": "Denver",
  "state": "CO",
  "postal_code": "80202",
  "created_at": "2025-10-19T..."
}
```

**What Just Happened**:
- ✅ JWT token verified
- ✅ User information retrieved
- ✅ Authentication system confirmed working

---

## 👥 Phase 2: Customer Management Testing

### Test 4: Get All Customers (Paginated)

**Purpose**: Test pagination feature (V3 Advanced Feature)

**Steps**:
1. Expand **"2. Customers (Paginated)"** folder
2. Click **"Get All Customers (Page 1)"**
3. Notice the URL has query parameters: `?page=1&per_page=10`
4. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "customers": [
    {
      "customer_id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total_customers": 1,
    "total_pages": 1,
    "has_next": false,
    "has_prev": false
  }
}
```

**What Just Happened**:
- ✅ Retrieved paginated customer list
- ✅ Got pagination metadata
- 🆕 **V3 Feature**: Pagination with full metadata

**Try This**: Change pagination parameters
- Edit the URL: `?page=1&per_page=5`
- Notice the `per_page` value changes in response

---

### Test 5: Get Single Customer

**Purpose**: Retrieve specific customer details by ID

**Steps**:
1. Click **"Get Single Customer"** request
2. Notice URL uses `{{customer_id}}` variable
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "customer_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  ...
}
```

**What Just Happened**:
- ✅ Retrieved specific customer by ID
- ✅ Variables automatically used in URL

---

### Test 6: Update Customer

**Purpose**: Update customer information

**Steps**:
1. Click **"Update Customer"** request
2. Review the body - notice the phone number says "UPDATED"
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "customer_id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "phone": "555-1234-UPDATED",
  ...
}
```

**What Just Happened**:
- ✅ Customer information updated
- ✅ Only authenticated user can update their own info

---

## 🚗 Phase 3: Vehicle Management Testing

### Test 7: Create Vehicle

**Purpose**: Add a vehicle for the customer

**Steps**:
1. Expand **"3. Vehicles"** folder
2. Click **"Create Vehicle"** request
3. Review the body (VIN, make, model, year, color)
4. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "vehicle_id": 1,
  "customer_id": 1,
  "vin": "1HGCM82633A123456",
  "make": "Honda",
  "model": "Accord",
  "year": 2020,
  "color": "Silver"
}
```

**What Just Happened**:
- ✅ New vehicle created
- ✅ Vehicle ID saved to `{{vehicle_id}}` variable
- ✅ Vehicle linked to customer

---

### Test 8: Get Customer Vehicles

**Purpose**: List all vehicles for a customer

**Steps**:
1. Click **"Get Customer Vehicles"** request
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
[
  {
    "vehicle_id": 1,
    "customer_id": 1,
    "vin": "1HGCM82633A123456",
    "make": "Honda",
    "model": "Accord",
    "year": 2020,
    "color": "Silver"
  }
]
```

**What Just Happened**:
- ✅ Retrieved all vehicles for customer
- ✅ Returned as array

---

### Test 9: Update Vehicle

**Purpose**: Update vehicle information

**Steps**:
1. Click **"Update Vehicle"** request
2. Notice model changed from "Accord" to "Accord EX-L"
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "vehicle_id": 1,
  "model": "Accord EX-L",
  "color": "Metallic Silver",
  ...
}
```

**What Just Happened**:
- ✅ Vehicle updated successfully
- ✅ Only vehicle owner can update

---

## 🔧 Phase 4: Mechanics Management (ASSIGNMENT TESTING)

### Test 10: ✅ CREATE Mechanic 1

**Purpose**: Create first mechanic (ASSIGNMENT REQUIREMENT)

**Steps**:
1. Expand **"4. Mechanics - FULL CRUD"** folder
2. Click **"✅ CREATE Mechanic 1"**
3. Review the body (full_name, email, phone, salary, is_active)
4. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "mechanic_id": 1,
  "full_name": "Mike Johnson",
  "email": "mike.johnson@mechanicshop.com",
  "phone": "555-9876",
  "salary": 65000,
  "is_active": true
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: POST /mechanics endpoint working
- ✅ Mechanic ID saved to `{{mechanic_id}}` variable
- ✅ Rate limiting applied (10 per hour)

---

### Test 11: ✅ CREATE Mechanic 2

**Purpose**: Create second mechanic

**Steps**:
1. Click **"✅ CREATE Mechanic 2"**
2. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "mechanic_id": 2,
  "full_name": "Sarah Williams",
  "email": "sarah.williams@mechanicshop.com",
  "phone": "555-5432",
  "salary": 72000,
  "is_active": true
}
```

**What Just Happened**:
- ✅ Second mechanic created
- ✅ ID saved to `{{mechanic_id_2}}` variable

---

### Test 12: ✅ CREATE Mechanic 3

**Purpose**: Create third mechanic (inactive for testing)

**Steps**:
1. Click **"✅ CREATE Mechanic 3"**
2. Notice `is_active: false` in body
3. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "mechanic_id": 3,
  "full_name": "Tom Davis",
  "is_active": false,
  ...
}
```

**What Just Happened**:
- ✅ Third mechanic created (inactive)
- ✅ ID saved to `{{mechanic_id_3}}` variable

---

### Test 13: ✅ GET All Mechanics (CACHED)

**Purpose**: Retrieve all mechanics (ASSIGNMENT + V3 CACHING)

**Steps**:
1. Click **"✅ GET All Mechanics (CACHED)"**
2. Click **"Send"**
3. Note the response time
4. Click **"Send"** again immediately
5. Compare response times

**Expected Response** (Status: `200 OK`):
```json
[
  {
    "mechanic_id": 1,
    "full_name": "Mike Johnson",
    ...
  },
  {
    "mechanic_id": 2,
    "full_name": "Sarah Williams",
    ...
  },
  {
    "mechanic_id": 3,
    "full_name": "Tom Davis",
    "is_active": false,
    ...
  }
]
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: GET /mechanics endpoint working
- 🆕 **V3 Feature**: Response cached for 5 minutes
- ✅ Second request should be much faster (cached)

---

### Test 14: ✅ GET Single Mechanic

**Purpose**: Retrieve specific mechanic by ID (ASSIGNMENT)

**Steps**:
1. Click **"✅ GET Single Mechanic"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "mechanic_id": 1,
  "full_name": "Mike Johnson",
  "email": "mike.johnson@mechanicshop.com",
  "phone": "555-9876",
  "salary": 65000,
  "is_active": true,
  "ticket_count": 0
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: GET /mechanics/<id> endpoint working
- ✅ Includes ticket count in response

---

### Test 15: 🆕 GET Mechanics by Activity

**Purpose**: Sort mechanics by ticket count (V3 ADVANCED FEATURE)

**Steps**:
1. Click **"🆕 GET Mechanics by Activity"**
2. Notice query parameters: `?order=desc&active_only=false`
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
[
  {
    "mechanic_id": 1,
    "full_name": "Mike Johnson",
    "email": "mike.johnson@mechanicshop.com",
    "phone": "555-9876",
    "salary": 65000,
    "is_active": true,
    "ticket_count": 0
  },
  ...
]
```

**What Just Happened**:
- 🆕 **V3 ADVANCED**: Mechanics sorted by activity level
- ✅ Custom sorting using relationship counts
- ✅ Filtering options (active_only parameter)

**Try This**: Test filtering
- Change URL to: `?order=desc&active_only=true`
- Tom Davis (inactive) should not appear

---

### Test 16: ✅ UPDATE Mechanic

**Purpose**: Update mechanic information (ASSIGNMENT)

**Steps**:
1. Click **"✅ UPDATE Mechanic"**
2. Notice full_name changed to "Mike Johnson Sr."
3. Notice salary increased to 70000
4. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "mechanic_id": 1,
  "full_name": "Mike Johnson Sr.",
  "salary": 70000,
  ...
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: PUT /mechanics/<id> endpoint working
- ✅ Mechanic information updated

---

### Test 17: ✅ DELETE Mechanic

**Purpose**: Delete a mechanic (ASSIGNMENT)

**Steps**:
1. Click **"✅ DELETE Mechanic"**
2. Notice it uses `{{mechanic_id_3}}` (Tom Davis - inactive)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Mechanic id: 3, successfully deleted."
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: DELETE /mechanics/<id> endpoint working
- ✅ Mechanic removed from database

**Verify**: Run "GET All Mechanics" again - Tom Davis should be gone

---

## 🎫 Phase 5: Service Tickets Management (ASSIGNMENT TESTING)

### Test 18: ✅ CREATE Service Ticket 1

**Purpose**: Create first service ticket (ASSIGNMENT)

**Steps**:
1. Expand **"5. Service Tickets - FULL CRUD"** folder
2. Click **"✅ CREATE Service Ticket 1"**
3. Review the body (vehicle_id, customer_id, status, problem_description, etc.)
4. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "ticket_id": 1,
  "vehicle_id": 1,
  "customer_id": 1,
  "status": "open",
  "problem_description": "Engine making strange noise and check engine light on",
  "odometer_miles": 45000,
  "priority": 3,
  "opened_at": "2025-10-19T...",
  "closed_at": null
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: POST /service_tickets endpoint working
- ✅ Ticket ID saved to `{{ticket_id}}` variable
- ✅ Rate limiting applied (10 per hour)

---

### Test 19: ✅ CREATE Service Ticket 2

**Purpose**: Create second ticket

**Steps**:
1. Click **"✅ CREATE Service Ticket 2"**
2. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "ticket_id": 2,
  "problem_description": "Brake pads need replacement",
  ...
}
```

**What Just Happened**:
- ✅ Second ticket created
- ✅ ID saved to `{{ticket_id_2}}` variable

---

### Test 20: ✅ GET All Service Tickets

**Purpose**: Retrieve all tickets (ASSIGNMENT)

**Steps**:
1. Click **"✅ GET All Service Tickets"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
[
  {
    "ticket_id": 1,
    "status": "open",
    ...
  },
  {
    "ticket_id": 2,
    "status": "open",
    ...
  }
]
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: GET /service_tickets endpoint working
- ✅ All tickets retrieved

---

### Test 21: ✅ GET Single Ticket

**Purpose**: Retrieve specific ticket by ID

**Steps**:
1. Click **"✅ GET Single Ticket"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "ticket_id": 1,
  "vehicle_id": 1,
  "customer_id": 1,
  "status": "open",
  "problem_description": "Engine making strange noise...",
  "mechanics": [],
  "parts": [],
  ...
}
```

**What Just Happened**:
- ✅ Retrieved specific ticket
- ✅ Includes related mechanics and parts

---

### Test 22: ✅ ASSIGN Mechanic to Ticket

**Purpose**: Assign mechanic to service ticket (ASSIGNMENT)

**Steps**:
1. Click **"✅ ASSIGN Mechanic to Ticket"**
2. Review body (role, minutes_worked)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Mechanic 1 successfully assigned to ticket 1",
  "ticket_id": 1,
  "mechanic_id": 1,
  "role": "Lead Technician",
  "minutes_worked": 0
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: PUT /<ticket_id>/assign-mechanic/<mechanic_id> working
- ✅ Mechanic assigned to ticket
- ✅ Junction table (TicketMechanic) entry created

**Verify**: Run "GET Single Ticket" - Mike Johnson should be in mechanics array

---

### Test 23: ✅ ASSIGN Second Mechanic

**Purpose**: Assign multiple mechanics to same ticket

**Steps**:
1. Click **"✅ ASSIGN Second Mechanic"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Mechanic 2 successfully assigned to ticket 1",
  "ticket_id": 1,
  "mechanic_id": 2,
  "role": "Assistant Technician",
  "minutes_worked": 0
}
```

**What Just Happened**:
- ✅ Second mechanic assigned to same ticket
- ✅ Multiple mechanics can work on one ticket

**Verify**: Run "GET Single Ticket" - Both mechanics should appear

---

### Test 24: ✅ REMOVE Mechanic from Ticket

**Purpose**: Remove mechanic from ticket (ASSIGNMENT)

**Steps**:
1. Click **"✅ REMOVE Mechanic from Ticket"**
2. Notice it removes mechanic_id_2 (Sarah)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Mechanic 2 successfully removed from ticket 1",
  "ticket_id": 1,
  "mechanic_id": 2
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: PUT /<ticket_id>/remove-mechanic/<mechanic_id> working
- ✅ Mechanic removed from ticket
- ✅ Junction table entry deleted

**Verify**: Run "GET Single Ticket" - Only Mike Johnson should remain

---

### Test 25: 🆕 BULK EDIT Mechanics

**Purpose**: Add/remove multiple mechanics in one request (V3 ADVANCED)

**Steps**:
1. Click **"🆕 BULK EDIT Mechanics"**
2. Review body: `add_ids: [1, 2]`, `remove_ids: []`
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Ticket mechanics updated successfully",
  "ticket_id": 1,
  "added_mechanics": [1, 2],
  "removed_mechanics": [],
  "errors": []
}
```

**What Just Happened**:
- 🆕 **V3 ADVANCED**: Bulk operations endpoint
- ✅ Multiple mechanics added in single request
- ✅ Efficient batch processing

**Try This**: Test removal
- Change body to: `"add_ids": [], "remove_ids": [2]`
- Sarah should be removed

---

### Test 26: ✅ UPDATE Service Ticket

**Purpose**: Update ticket information (ASSIGNMENT)

**Steps**:
1. Click **"✅ UPDATE Service Ticket"**
2. Notice status changed from "open" to "in_progress"
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "ticket_id": 1,
  "status": "in_progress",
  "problem_description": "Engine noise - Diagnostic complete",
  ...
}
```

**What Just Happened**:
- ✅ **ASSIGNMENT**: PUT /service_tickets/<id> endpoint working
- ✅ Ticket status updated

---

### Test 27: ✅ DELETE Service Ticket

**Purpose**: Delete a service ticket

**Steps**:
1. Click **"✅ DELETE Service Ticket"**
2. Notice it uses `{{ticket_id_2}}` (second ticket)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Service ticket id: 2, successfully deleted."
}
```

**What Just Happened**:
- ✅ Ticket deleted from database
- ✅ Related associations also removed

---

## 📦 Phase 6: Inventory Management (V3 FEATURE)

### Test 28: CREATE Part (Brake Pads)

**Purpose**: Add part to inventory (V3 FEATURE)

**Steps**:
1. Expand **"6. Inventory - Parts"** folder
2. Click **"CREATE Part (Brake Pads)"**
3. Review body (part_number, name, category, cost, quantity, etc.)
4. Click **"Send"**

**Expected Response** (Status: `201 Created`):
```json
{
  "part_id": 1,
  "part_number": "BRK-001",
  "name": "Brake Pad Set",
  "description": "Premium ceramic brake pads",
  "category": "Brakes",
  "manufacturer": "AutoParts Inc",
  "current_cost_cents": 4500,
  "quantity_in_stock": 25,
  "reorder_level": 5,
  "supplier": "Parts Warehouse"
}
```

**What Just Happened**:
- 🆕 **V3 FEATURE**: Inventory system active
- ✅ Part ID saved to `{{part_id}}` variable
- ✅ Cost stored in cents for precision

---

### Test 29: GET All Parts

**Purpose**: List all inventory parts

**Steps**:
1. Click **"GET All Parts"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
[
  {
    "part_id": 1,
    "part_number": "BRK-001",
    "name": "Brake Pad Set",
    "quantity_in_stock": 25,
    ...
  }
]
```

**What Just Happened**:
- ✅ All parts retrieved
- ✅ Full inventory visible

---

### Test 30: GET Low Stock Parts

**Purpose**: Filter parts needing reorder (V3 FEATURE)

**Steps**:
1. Click **"GET Low Stock Parts"**
2. Notice URL: `?low_stock=true`
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
[]
```

Currently empty because part has 25 in stock (above reorder level of 5).

**What Just Happened**:
- 🆕 **V3 FEATURE**: Low stock filtering
- ✅ Automatic reorder alerts

---

### Test 31: GET Single Part

**Purpose**: Retrieve specific part details

**Steps**:
1. Click **"GET Single Part"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "part_id": 1,
  "part_number": "BRK-001",
  "name": "Brake Pad Set",
  "quantity_in_stock": 25,
  ...
}
```

---

### Test 32: UPDATE Part

**Purpose**: Update part information

**Steps**:
1. Click **"UPDATE Part"**
2. Notice name changed to "Brake Pad Set - Premium"
3. Notice price increased to 4800 cents
4. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "part_id": 1,
  "name": "Brake Pad Set - Premium",
  "current_cost_cents": 4800,
  ...
}
```

**What Just Happened**:
- ✅ Part information updated
- ✅ Price history maintained

---

### Test 33: ADJUST Part Quantity

**Purpose**: Increase/decrease inventory quantity (V3 FEATURE)

**Steps**:
1. Click **"ADJUST Part Quantity"**
2. Review body: `"adjustment": 10` (adds 10)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Quantity adjusted successfully",
  "part": {
    "part_id": 1,
    "quantity_in_stock": 35,
    ...
  },
  "adjustment": 10,
  "previous_quantity": 25,
  "new_quantity": 35
}
```

**What Just Happened**:
- 🆕 **V3 FEATURE**: Inventory adjustment tracking
- ✅ Quantity increased by 10 (25 → 35)

**Try This**: Test negative adjustment
- Change body to: `"adjustment": -5`
- Quantity should decrease

---

### Test 34: ADD Part to Ticket

**Purpose**: Install part on service ticket (V3 FEATURE)

**Steps**:
1. Click **"ADD Part to Ticket"**
2. Review body (quantity_used, markup_percentage, warranty, mechanic)
3. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Part successfully added to ticket",
  "ticket_id": 1,
  "part_id": 1,
  "part_name": "Brake Pad Set - Premium",
  "quantity_used": 1,
  "unit_cost_cents": 4800,
  "total_cost": 62.40,
  "remaining_stock": 34
}
```

**What Just Happened**:
- 🆕 **V3 FEATURE**: Parts integrated with tickets
- ✅ Inventory automatically decremented (35 → 34)
- ✅ Cost with markup calculated (48.00 + 30% = 62.40)
- ✅ Warranty tracking enabled

**Verify**: 
- Run "GET Single Part" - quantity should be 34
- Run "GET Single Ticket" - part should appear in parts array

---

### Test 35: DELETE Part

**Purpose**: Remove part from inventory

**Steps**:
1. Click **"DELETE Part"**
2. Click **"Send"**

**Expected Response** (Status: `200 OK`):
```json
{
  "message": "Part id: 1, successfully deleted"
}
```

**What Just Happened**:
- ✅ Part removed from inventory

---

## ✅ Testing Complete!

### What You've Tested:

**✅ ASSIGNMENT REQUIREMENTS:**
- Full CRUD for Mechanics (Create, Read, Update, Delete)
- Full CRUD for Service Tickets (Create, Read, Update, Delete)
- Mechanic Assignment to Tickets
- Mechanic Removal from Tickets

**🆕 V3 ADVANCED FEATURES:**
- Rate Limiting (Registration, Login)
- JWT Authentication
- Caching (Mechanics list)
- Pagination (Customers)
- Advanced Queries (Sort mechanics by activity)
- Bulk Operations (Edit multiple mechanics)
- Complete Inventory Management
- Parts Integration with Service Tickets

---

## 🎓 Additional Testing Exercises

### Exercise 1: Test Authentication Flow
1. Create a second customer
2. Login as second customer
3. Try to update first customer's info
4. **Expected**: Should get `403 Forbidden` (users can only update themselves)

### Exercise 2: Test Rate Limiting
1. Try registering 4 times in one hour
2. **Expected**: 4th attempt should fail with `429 Too Many Requests`
3. Try logging in 6 times rapidly
4. **Expected**: 6th attempt should fail

### Exercise 3: Test Caching
1. Run "GET All Mechanics" and note response time
2. Wait 1 minute and run again - should be instant (cached)
3. Update a mechanic
4. Run "GET All Mechanics" again - cache should still be active
5. Wait 5 minutes and run again - fresh data loaded

### Exercise 4: Test Pagination
1. Create multiple customers (you'd need to modify the collection)
2. Test: `GET /customers?page=1&per_page=5`
3. Test: `GET /customers?page=2&per_page=5`
4. Verify pagination metadata is correct

### Exercise 5: Test Inventory Workflow
1. Create a part with 10 items in stock and reorder level of 8
2. Add the part to a ticket 3 times (use different quantities)
3. Check remaining stock - should be decremented
4. Run "GET Low Stock Parts" - your part should appear
5. Adjust quantity back up
6. Verify it's no longer in low stock list

### Exercise 6: Test Mechanic Activity Sorting
1. Assign Mechanic 1 to 3 different tickets
2. Assign Mechanic 2 to 1 ticket
3. Run "GET Mechanics by Activity"
4. **Expected**: Mechanic 1 should be listed first (more tickets)

### Exercise 7: Test Bulk Operations
1. Create 3 mechanics
2. Create 1 service ticket
3. Use Bulk Edit to add all 3 mechanics at once
4. Verify all 3 are assigned
5. Use Bulk Edit to remove 2 mechanics
6. Verify only 1 remains

---

## 🐛 Troubleshooting

### Problem: "401 Unauthorized" errors
**Solution**: 
- Your JWT token may have expired (1 hour expiration)
- Run "Login Customer" again to get a fresh token
- Check that the environment is selected (top-right dropdown)

### Problem: "404 Not Found" errors
**Solution**:
- Check that the API server is running (`python app.py`)
- Verify the base_url in environment is `http://localhost:5000`
- Ensure you've run prerequisite tests (e.g., create vehicle before creating ticket)

### Problem: Environment variables not saving
**Solution**:
- Check the "Tests" tab in each request - scripts should be present
- Ensure correct environment is selected
- Try re-importing the environment file

### Problem: "Rate limit exceeded" errors
**Solution**:
- This is expected! It means rate limiting is working
- Wait for the time period to reset (check error message)
- For testing, you can temporarily disable rate limiting in the code

### Problem: Foreign key constraint errors
**Solution**:
- Ensure you create resources in the correct order:
  1. Customer (via registration)
  2. Vehicle (requires customer_id)
  3. Mechanic
  4. Service Ticket (requires vehicle_id and customer_id)
  5. Assign mechanics to tickets
  6. Add parts to tickets

---

## 📊 Testing Checklist

Use this checklist to track your testing progress:

### Phase 1: Authentication ✅
- [ ] Register Customer
- [ ] Login Customer  
- [ ] Get Current User
- [ ] Test rate limiting on registration
- [ ] Test rate limiting on login

### Phase 2: Customers ✅
- [ ] Get All Customers (paginated)
- [ ] Get Single Customer
- [ ] Update Customer
- [ ] Test pagination with different parameters

### Phase 3: Vehicles ✅
- [ ] Create Vehicle
- [ ] Get Customer Vehicles
- [ ] Update Vehicle
- [ ] Delete Vehicle

### Phase 4: Mechanics (ASSIGNMENT) ✅
- [ ] CREATE Mechanic (multiple)
- [ ] GET All Mechanics (verify caching)
- [ ] GET Single Mechanic
- [ ] GET Mechanics by Activity
- [ ] UPDATE Mechanic
- [ ] DELETE Mechanic

### Phase 5: Service Tickets (ASSIGNMENT) ✅
- [ ] CREATE Service Ticket (multiple)
- [ ] GET All Service Tickets
- [ ] GET Single Ticket
- [ ] ASSIGN Mechanic to Ticket
- [ ] ASSIGN Multiple Mechanics
- [ ] REMOVE Mechanic from Ticket
- [ ] BULK EDIT Mechanics
- [ ] UPDATE Service Ticket
- [ ] DELETE Service Ticket

### Phase 6: Inventory (V3 FEATURE) ✅
- [ ] CREATE Part
- [ ] GET All Parts
- [ ] GET Low Stock Parts
- [ ] GET Single Part
- [ ] UPDATE Part
- [ ] ADJUST Part Quantity
- [ ] ADD Part to Ticket (verify stock decrement)
- [ ] DELETE Part

### Assignment Verification ✅
- [ ] All Mechanic CRUD endpoints working
- [ ] All Service Ticket CRUD endpoints working
- [ ] Mechanic assignment working
- [ ] Mechanic removal working
- [ ] Proper authentication on all routes
- [ ] Marshmallow schemas validating data

### V3 Features Verification ✅
- [ ] Rate limiting functioning
- [ ] Caching working (faster 2nd request)
- [ ] JWT tokens auto-saving
- [ ] Pagination with metadata
- [ ] Advanced sorting (mechanics by activity)
- [ ] Bulk operations working
- [ ] Inventory system functional
- [ ] Parts integrate with tickets

---

## 🎉 Congratulations!

You've successfully tested the complete Mechanic Shop API V3!

### What You've Learned:
- ✅ How to test RESTful API endpoints
- ✅ Working with JWT authentication
- ✅ Using Postman environments and variables
- ✅ Testing CRUD operations
- ✅ Verifying rate limiting and caching
- ✅ Testing complex relationships (many-to-many)
- ✅ Working with pagination and filtering
- ✅ Testing bulk operations

### Next Steps:
1. **Documentation**: Review the main README.md for detailed API documentation
2. **Code Review**: Explore the source code to understand implementation
3. **Custom Tests**: Create your own test scenarios
4. **Error Handling**: Try invalid requests to see error responses
5. **Performance**: Test with larger datasets to see pagination benefits

---

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review the main README.md file
3. Verify your database is set up correctly
4. Check that all migrations have run
5. Ensure environment variables are configured

---

**Happy Testing! 🚀**

*This testing guide covers all assignment requirements plus advanced V3 features for the Mechanic Shop Management API.*
