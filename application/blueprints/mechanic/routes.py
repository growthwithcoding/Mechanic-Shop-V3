from typing import Any, Dict, cast
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from flask_jwt_extended import jwt_required
from application.blueprints.mechanic import mechanic_bp
from application.blueprints.mechanic.mechanicSchemas import mechanic_schema, mechanics_schema
from application.models import Mechanic
from application.extensions import db, limiter, cache


# CREATE - POST /mechanics
@mechanic_bp.route("", methods=['POST'])
@jwt_required()
@limiter.limit("10 per hour")
def create_mechanic():
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        mechanic_data = cast(Dict[str, Any], mechanic_schema.load(request.json))
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if email already exists
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    existing_mechanic = db.session.execute(query).scalars().first()
    if existing_mechanic:
        return jsonify({"error": "Email already associated with a mechanic."}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return jsonify(mechanic_schema.dump(new_mechanic)), 201


# READ ALL - GET /mechanics
# Caching applied: Results are cached for 5 minutes to reduce database load
@mechanic_bp.route("", methods=['GET'])
@jwt_required()
@cache.cached(timeout=300)
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return jsonify(mechanics_schema.dump(mechanics)), 200


# GET MECHANICS BY POPULARITY - GET /mechanics/by-activity
# This endpoint returns mechanics sorted by the number of tickets they've worked on
# Demonstrates using relationship attributes and custom sorting with lambda functions
@mechanic_bp.route("/by-activity", methods=['GET'])
@jwt_required()
def get_mechanics_by_activity():
    """
    Returns mechanics sorted by the number of tickets they've worked on (descending order).
    
    This endpoint demonstrates:
    1. Accessing related data through SQLAlchemy relationships (ticket_mechanics)
    2. Using len() on relationship lists to count related records
    3. Custom sorting with lambda functions based on relationship data
    4. Creating insightful queries that reveal business metrics
    
    Query parameters:
    - order: 'desc' (default) for most active first, 'asc' for least active first
    - active_only: 'true' to filter only active mechanics (default: 'false')
    """
    # Get query parameters
    order = request.args.get('order', 'desc').lower()
    active_only = request.args.get('active_only', 'false').lower() == 'true'
    
    # Build query
    query = select(Mechanic)
    if active_only:
        query = query.where(Mechanic.is_active == True)
    
    mechanics = db.session.execute(query).scalars().all()
    
    # Convert to list for sorting (SQLAlchemy result is not directly sortable)
    mechanics_list = list(mechanics)
    
    # Sort mechanics by the number of tickets they've worked on
    # Using lambda function to define custom sorting key
    # The key function accesses the ticket_mechanics relationship and counts the items
    mechanics_list.sort(
        key=lambda mechanic: len(mechanic.ticket_mechanics),
        reverse=(order == 'desc')
    )
    
    # Prepare response with ticket counts included
    result = []
    for mechanic in mechanics_list:
        mechanic_dict = {
            'mechanic_id': mechanic.mechanic_id,
            'full_name': mechanic.full_name,
            'email': mechanic.email,
            'phone': mechanic.phone,
            'salary': mechanic.salary,
            'is_active': mechanic.is_active,
            'ticket_count': len(mechanic.ticket_mechanics)  # Count of tickets worked on
        }
        result.append(mechanic_dict)
    
    return jsonify(result), 200


# READ ONE - GET /mechanics/<id>
@mechanic_bp.route("/<int:mechanic_id>", methods=['GET'])
@jwt_required()
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if mechanic:
        # Include ticket count in single mechanic response
        mechanic_dict = cast(Dict[str, Any], mechanic_schema.dump(mechanic))
        return jsonify({**mechanic_dict, 'ticket_count': len(mechanic.ticket_mechanics)}), 200
    return jsonify({"error": "Mechanic not found."}), 404


# UPDATE - PUT /mechanics/<id>
@mechanic_bp.route("/<int:mechanic_id>", methods=['PUT'])
@jwt_required()
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        mechanic_data = cast(Dict[str, Any], mechanic_schema.load(request.json))
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Update mechanic attributes
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 200


# DELETE - DELETE /mechanics/<id>
@mechanic_bp.route("/<int:mechanic_id>", methods=['DELETE'])
@jwt_required()
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f'Mechanic id: {mechanic_id}, successfully deleted.'}), 200
