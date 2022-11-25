# This file is used to scalulpt the Sales Model/Table in the system Database:

from sqlalchemy import Column,Integer,DateTime,NUMERIC,func,ForeignKey
from sqlalchemy.orm import relationship

# We need to make sure that this model also meets our set specs in the db.base file Base class..... si:
from app.db.base import Base

# The Sales Model:
class Sales(Base):
    # attaching a prefered tablename:
    __tablename__='sales'
    # Column defination:
    id=Column(Integer,primary_key=True,index=True)
    product_id=Column(Integer,ForeignKey("products.id"))
    quantity=Column(NUMERIC,nullable=False)
    b_p=Column(NUMERIC,nullable=False)
    s_p=Column(NUMERIC,nullable=False)   
    profit=Column(NUMERIC,nullable=False)   
    date=Column(DateTime(timezone=False),server_default=func.now())
    
    products=relationship("Products",back_populates="sales")# relationship defination:
