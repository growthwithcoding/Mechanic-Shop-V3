from typing import Any, Dict, cast
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from flask_jwt_extended import jwt_required
from application.blueprints.inventory import inventory_bp
from application.blueprints.inventory.inventorySchemas import part_schema, parts_schema
from application.models import Part
from application.extensions import db, limiter


# CREATE - POST /inventory
@inventory_bp.route("", methods=['POST'])
@jwt_required()
@limiter.limit("20 per hour")
def create_part():
    """Create a new part in inventory"""
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        part_data = cast(Dict[str, Any], part_schema.load(request.json))
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # Check if part_number already exists
    query = select(Part).where(Part.part_number == part_data.part_number)
    existing_part = db.session.execute(query).scalars().first()
    if existing_part:
        return jsonify({"error": "Part number already exists"}), 400
    
    new_part = part_data
    db.session.add(new_part)
    db.session.commit()
    return jsonify(part_schema.dump(new_part)), 201


# READ ALL - GET /inventory
@inventory_bp.route("", methods=['GET'])
@jwt_required()
def get_parts():
    """Get all parts in inventory with optional filtering"""
    # Query parameters for filtering
    low_stock = request.args.get('low_stock', 'false').lower() == 'true'
    category = request.args.get('category')
    
    query = select(Part)
    
    # Apply filters if provided
    if category:
        query = query.where(Part.category == category)
    
    parts = db.session.execute(query).scalars().all()
    
    # Filter for low stock items if requested
    if low_stock:
        parts = [part for part in parts if part.needs_reorder()]
    
    return jsonify(parts_schema.dump(parts)), 200


# READ ONE - GET /inventory/<id>
@inventory_bp.route("/<int:part_id>", methods=['GET'])
@jwt_required()
def get_part(part_id):
    """Get a specific part by ID"""
    part = db.session.get(Part, part_id)
    
    if part:
        return jsonify(part_schema.dump(part)), 200
    return jsonify({"error": "Part not found"}), 404


# UPDATE - PUT /inventory/<id>
@inventory_bp.route("/<int:part_id>", methods=['PUT'])
@jwt_required()
def update_part(part_id):
    """Update a part in inventory"""
    part = db.session.get(Part, part_id)
    
    if not part:
        return jsonify({"error": "Part not found"}), 404
    
    if not request.json:
        return jsonify({"error": "No JSON data provided"}), 400
    
    try:
        part_data = cast(Dict[str, Any], part_schema.load(request.json))
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    # If part_number is being changed, check if new part_number already exists
    if hasattr(part_data, 'part_number') and part_data.part_number != part.part_number:
        query = select(Part).where(Part.part_number == part_data.part_number)
        existing_part = db.session.execute(query).scalars().first()
        if existing_part:
            return jsonify({"error": "Part number already exists"}), 400
    
    # Update part attributes
    for key, value in part_schema.dump(part_data).items():
        if hasattr(part, key) and key != 'part_id':
            setattr(part, key, value)
    
    db.session.commit()
    return jsonify(part_schema.dump(part)), 200


# DELETE - DELETE /inventory/<id>
@inventory_bp.route("/<int:part_id>", methods=['DELETE'])
@jwt_required()
def delete_part(part_id):
    """Delete a part from inventory"""
    part = db.session.get(Part, part_id)
    
    if not part:
        return jsonify({"error": "Part not found"}), 404
    
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": f'Part id: {part_id}, successfully deleted'}), 200


# ADJUST QUANTITY - PATCH /inventory/<id>/adjust-quantity
@inventory_bp.route("/<int:part_id>/adjust-quantity", methods=['PATCH'])
@jwt_required()
def adjust_part_quantity(part_id):
    """
    Adjust the quantity of a part in inventory
    
    Request body:
    {
        "adjustment": 10    # Positive to add, negative to subtract
    }
    """
    part = db.session.get(Part, part_id)
    
    if not part:
        return jsonify({"error": "Part not found"}), 404
    
    if not request.json or 'adjustment' not in request.json:
        return jsonify({"error": "adjustment field is required"}), 400
    
    adjustment = request.json['adjustment']
    
    try:
        adjustment = int(adjustment)
    except (ValueError, TypeError):
        return jsonify({"error": "adjustment must be an integer"}), 400
    
    new_quantity = part.quantity_in_stock + adjustment
    
    if new_quantity < 0:
        return jsonify({"error": "Adjustment would result in negative quantity"}), 400
    
    part.quantity_in_stock = new_quantity
    db.session.commit()
    
    return jsonify({
        "message": "Quantity adjusted successfully",
        "part": part_schema.dump(part),
        "adjustment": adjustment,
        "previous_quantity": part.quantity_in_stock - adjustment,
        "new_quantity": part.quantity_in_stock
    }), 200
