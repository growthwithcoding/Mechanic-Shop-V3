from application.extensions import ma
from marshmallow import fields, validate

class RegisterSchema(ma.Schema):
    """Schema for user registration"""
    first_name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=validate.Length(min=1, max=50))
    address = fields.String(required=True, validate=validate.Length(min=1, max=255))
    city = fields.String(required=True, validate=validate.Length(min=1, max=100))
    state = fields.String(required=True, validate=validate.Length(min=1, max=50))
    postal_code = fields.String(required=True, validate=validate.Length(min=1, max=20))
    password = fields.String(required=True, validate=validate.Length(min=6), load_only=True)

class LoginSchema(ma.Schema):
    """Schema for user login"""
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

# Create schema instances
register_schema = RegisterSchema()
login_schema = LoginSchema()
