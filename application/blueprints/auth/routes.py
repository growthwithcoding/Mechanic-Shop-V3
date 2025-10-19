from typing import Any, Dict, cast
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from application.blueprints.auth import auth_bp
from application.blueprints.auth.authSchemas import register_schema, login_schema
from application.blueprints.customer.customerSchemas import customer_schema
from application.models import Customer
from application.extensions import db, limiter


# REGISTER - POST /auth/register
# Rate limiting applied: Prevents spam account creation
@auth_bp.route("/register", methods=['POST'])
@limiter.limit("3 per hour")
def register():
    """
    Register a new customer account
    Creates a new customer with hashed password and returns JWT token
    """
    # Check if request has JSON data
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        # Validate and deserialize input
        customer_data = cast(Dict[str, Any], register_schema.load(request.json))
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if email already exists
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query).scalars().first()
    if existing_customer:
        return jsonify({"error": "Email already registered"}), 400
    
    # Extract password and remove from customer_data
    password = customer_data.pop('password')
    
    # Create new customer
    new_customer = Customer(**customer_data)
    new_customer.set_password(password)
    
    db.session.add(new_customer)
    db.session.commit()
    
    # Create JWT access token (identity must be a string)
    access_token = create_access_token(identity=str(new_customer.customer_id))
    
    return jsonify({
        "message": "Customer registered successfully",
        "access_token": access_token,
        "customer": customer_schema.dump(new_customer)
    }), 201


# LOGIN - POST /auth/login
# Rate limiting applied: Prevents brute force attacks
@auth_bp.route("/login", methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """
    Login with email and password
    Returns JWT token if credentials are valid
    """
    # Check if request has JSON data
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        # Validate and deserialize input
        login_data = cast(Dict[str, Any], login_schema.load(request.json))
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Find customer by email
    query = select(Customer).where(Customer.email == login_data['email'])
    customer = db.session.execute(query).scalars().first()
    
    # Check if customer exists and password is correct
    if not customer or not customer.check_password(login_data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Create JWT access token (identity must be a string)
    access_token = create_access_token(identity=str(customer.customer_id))
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "customer": customer_schema.dump(customer)
    }), 200


# GET CURRENT USER - GET /auth/me
# JWT required: Returns the currently authenticated user's information
@auth_bp.route("/me", methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user information
    Requires valid JWT token in Authorization header
    """
    # Get customer ID from JWT token (convert from string back to int)
    current_customer_id = int(get_jwt_identity())
    
    # Fetch customer from database
    customer = db.session.get(Customer, current_customer_id)
    
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    return customer_schema.jsonify(customer), 200
