from datetime import datetime, date
from sqlalchemy.orm import class_mapper

class SerializableMixin:
    def to_dict(self, include_relationships=False):
        """Convert SQLAlchemy model to dict, handling datetime"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            result[column.name] = value
            
        if include_relationships:
            for relation in class_mapper(self.__class__).relationships:
                value = getattr(self, relation.key)
                if value is None:
                    result[relation.key] = None
                elif isinstance(value, list):  # one-to-many
                    result[relation.key] = [item.to_dict() for item in value]
                else:  # many-to-one or one-to-one
                    result[relation.key] = value.to_dict()
                    
        return result