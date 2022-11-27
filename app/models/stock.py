# This file is used to scalulpt the Stock Model/Table in the system Database:

# We need to make sure that this model also meets our set specs in the db.base file Base class..... so:
from app.db.base import Base
from sqlalchemy import Column,Integer,String,DateTime,NUMERIC,func
# The Stock Model:
class Stock(Base):
    # attaching a prefered tablename:
    __tablename__='stock'
    # Column defination:
    id=Column(Integer,primary_key=True,index=True)
    product_name=Column(String,nullable=False,unique=True)
    desc=Column(String,nullable=False)
    quantity=Column(NUMERIC,nullable=False)
    b_p=Column(NUMERIC,nullable=False)
    date=Column(DateTime(timezone=False),server_default=func.now())