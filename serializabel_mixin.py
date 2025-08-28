from datetime import datetime, date

class SerializableMixin:
    def to_dict(self):
        """Convert SQLAlchemy model to dict, handling datetime"""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, (datetime, date)):
                value = value.isoformat()
            result[column.name] = value
        return result