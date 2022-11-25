# This file is used to declare certain features that all models in this system must conform to:
from typing import Any
from sqlalchemy.ext.declarative import as_declarative,declared_attr

# using the declarative as adecorator:
@as_declarative()
class Base:
    id:Any
    # __name__:strGenerate __tablename__automatically
    @declared_attr
    def __tablename__(cls)->str:
        return __name__.lower()
