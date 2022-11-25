# This file is used to scalulpt the Products Model/Table in the system Database:

from sqlalchemy import Column,Integer,String,DateTime,NUMERIC,func
from sqlalchemy.orm import relationship

# We need to make sure that this model also meets our set specs in the db.base file Base class..... si:
from app.db.base import Base

# The Products Model:
class Products(Base):
    # attaching a prefered tablename:
    __tablename__='products'
    # Column defination:
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False,unique=True)
    quantity=Column(NUMERIC,nullable=False)
    b_p=Column(NUMERIC,nullable=False)
    s_p=Column(NUMERIC,nullable=False)
    serial_no=Column(String,nullable=False,unique=True)
    date=Column(DateTime(timezone=False),server_default=func.now())

    sales=relationship("Sales",back_populates="products")# relationship defination:
    