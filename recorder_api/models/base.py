import re

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """Base class for all database entities"""

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        """Generate database table name automatically.
        Convert CamelCase class name to snake_case db table name.
        """
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    def __repr__(self) -> str:
        attrs = []
        for c in self.__table__.columns:
            attrs.append(f"{c.name}={getattr(self, c.name)}")
        return "{}({})".format(self.__class__.__name__, ', '.join(attrs))


class Recorders(Base):
    recorder_id = mapped_column(sqlalchemy.Integer, primary_key=True)
    recorder_name = mapped_column(sqlalchemy.String, nullable=False)
    recorder_token = mapped_column(sqlalchemy.String, nullable=False)
    created_date = mapped_column(sqlalchemy.DateTime(), server_default=func.now())
