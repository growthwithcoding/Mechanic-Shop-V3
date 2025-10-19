from marshmallow import Schema, fields, validate


class MechanicSchema(Schema):
    mechanic_id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True)
    email = fields.Str(required=True, validate=validate.Email())
    phone = fields.Str(required=True)
    salary = fields.Int(required=True)
    is_active = fields.Bool(load_default=True)
    
    # Optional: Include ticket count when sorting by popularity
    ticket_count = fields.Int(dump_only=True)


# Initialize schema instances
mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
