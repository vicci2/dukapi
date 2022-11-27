# The products API flie; it holds all the endpoints that interact with the sales Model in the D.B
from fastapi import APIRouter,Depends, HTTPException
from typing import List, Dict,Generator
# Binding and sesson initiation:
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
# Attaching schemas that interact with the sales Model
from app.schema import *
# Attaching target Model:
from app.models.sales import Sales
from app.models.products import Products
# Others:
from sqlalchemy import func
    
# Dependency injection:
def getDb() -> Generator:
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close

sales_router=APIRouter()
sales_router2=APIRouter()

@sales_router.get("/",
    tags=["SALES"],
    # response_model=List[Sale],
    summary="all sales",
    status_code=200
)
def sales(db:Session = Depends(getDb)):
    # querying the database    
    return db.query(Sales).all()

@sales_router2.get("/",
    tags=["SALES2"],
    # response_model=List[Sale],
    summary="Get sales of a particular item",
    status_code=200
)
def sales(payload:ViewSales,db:Session = Depends(getDb)):
    # querying the database  
    # sale=db.query(Sales).filter(Sales.id==payload.id).first()
    # if not sale:
    #     raise HTTPException(status_code=404,detail=f"Sorry, no such sale")
    # else:
    #     # view=
        return db.query(Sales).filter(Sales.id==payload.id).all()