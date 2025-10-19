from application.extensions import ma
from application.models import Part
from marshmallow import fields


class PartSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Part (Inventory) serialization and deserialization"""
    class Meta:
        model = Part
        load_instance = True
        include_fk = True
    
    # Custom fields for computed properties
    needs_reorder = fields.Method("get_needs_reorder")
    
    def get_needs_reorder(self, obj):
        """Check if part needs to be reordered"""
        return obj.needs_reorder()


# Single part schema
part_schema = PartSchema()

# Multiple parts schema
parts_schema = PartSchema(many=True)
