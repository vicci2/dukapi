# The products API flie; it holds all the endpoints that interact with the sales Model in the D.B
from fastapi import APIRouter,Depends, HTTPException
from typing import List, Dict,Generator
# Binding and sesson initiation:
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
# Attaching schemas that interact with the sales Model
from app.schema import MakeSale
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

@sales_router.get("/",
    tags=["SALES"],
    # response_model=List[Sale],
    summary="all sales",
    status_code=200
)
def sales(db:Session = Depends(getDb)):
    # querying the database    
    return db.query(Sales).all()

@sales_router.get("/{saleID}",
    tags=["SALES"],
    # response_model=List[Sale],
    summary="Get a particular sale item",
    status_code=200
)
def sales(itemID:int,db:Session = Depends(getDb)):
    # querying the database  
    sale=db.query(Sales).filter(Sales.id==itemID).first()
    if not sale:
        raise HTTPException(status_code=404,detail=f"Sorry, no such sale")
    return sale

@sales_router.get("/{productID}",
    tags=["SALES"],
    summary="View all the salesof an item",
    status_code=200
)
def viewsales(productID:int,db:Session = Depends(getDb)):
    # querying the database  
    sales=db.query(Sales).filter(Sales.product_id==productID).first()    
    if not sales:
        raise HTTPException(status_code=400,detail="Invalid product ID!")
    return sales