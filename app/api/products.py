# The products API flie; it holds all the endpoints that interact with the products Model in the D.B
from fastapi import APIRouter,Depends,HTTPException
from typing import List, Dict,Generator
from app.models.sales import Sales
# Binding and sesson initiation:
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
# Attaching schemas that interact with the products Model
from app.schema import MakeSale, Productinfo, StockProduct,EditProduct,Product
# Attaching target Model:
from app.models.products import Products
from app.models.stock import Stock
# Others:
from sqlalchemy import func
    
# Dependency injection:
def getDb() -> Generator:
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close

products_router=APIRouter()
products_router2=APIRouter()

@products_router.get("/",
    tags=["PRODUCTS"],
    # response_model=List[Product],
    summary="all inventory Products",
    status_code=200
)
def products(db:Session = Depends(getDb)):
    # querying the database    
    products= db.query(Products).all() 
    return products

@products_router.get("/{itemID}",
    tags=["PRODUCTS"],
    # response_model=Productinfo,
    summary="Get one inventory Item",
    status_code=200
)
def stock(itemID:int,db:Session = Depends(getDb)):
    # querying the database  
    item= db.query(Products).filter(Products.id==itemID).first()
    if not item:
        raise HTTPException(status_code=404,detail=f"Item {itemID} does not exist") 
    return item

@products_router.post("/",
    tags=["PRODUCTS"],
    response_model=Dict[str,str],
    summary="Increase quantity of an Inventory Item",
    status_code=200
)
def stock(payload:StockProduct,db:Session = Depends(getDb)):
    # querying the database  
    item=db.query(Products).filter(Products.id == payload.id).first()
    prd=db.query(Stock).filter(Stock.product_name==payload.name).first()
    print(prd)        
    if not item :
        raise HTTPException(status_code=404,detail=f"Sorry, product doesn't exist")    
    if item.name != payload.name:
        raise HTTPException(status_code=400,detail=f"Sorry product {payload.name},has not been availed")            
    if prd.quantity < payload.quantity:
        raise HTTPException(status_code=400,detail=f"Sorry cant avail this much of {item.name}")        
    item.quantity=item.quantity + payload.quantity
    prd.quantity=prd.quantity - payload.quantity
    db.merge(item)
    db.merge(prd)
    db.commit()
    return {"Message":f"{payload.quantity} more {payload.name} are now avalable"}

@products_router.put("/",
    tags=["PRODUCTS"],
    response_model=Dict[str,str],
    summary="Change the selling price of a product in Inventory",
    status_code=200
)
def editproduct(payload:EditProduct,db:Session = Depends(getDb)):
    # querying the database  
    item= db.query(Products).filter(Products.id==payload.id).first()
    if not item:
        raise HTTPException(status_code=404,detail=f"Item {payload.id} does not exist") 
    if payload.name!=item.name:
        raise HTTPException(status_code=400,detail=f"Invalid product name")
    # item.name=payload.newName
    item.s_p=payload.sp
    db.merge(item)
    db.commit()
    return {"Message":f"New selling Price:{payload.sp}"}

@products_router2.post("/",
    tags=["PRODUCTS2"],
    # response_model=MakeSale,
    summary="Sell an item",
    status_code=200
)
def makeSale(payload:MakeSale,db:Session = Depends(getDb)):
    # querying the database  
    item=db.query(Products).filter(Products.id == payload.id).first()       
    if not item :
        raise HTTPException(status_code=404,detail=f"Sorry, product doesn't exist")           
    if item.quantity < payload.quantity or payload.quantity <0 or payload.quantity==0 :
        raise HTTPException(status_code=400,detail=f"Sorry, can't sale this much of {payload.name}")         
    if item.name!=payload.name :
        raise HTTPException(status_code=404,detail=f"Sorry, product doesn't exist")            
    item.quantity =item.quantity - payload.quantity
    prf=int(item.s_p - item.b_p)
    sale:MakeSale=Sales(product_id=payload.id,name=item.name,b_p=item.b_p,s_p=item.s_p,quantity=payload.quantity,profit=prf)
    db.add(sale)
    db.merge(item)
    db.commit()
    return {"Message":f"Purchase successful. {payload.quantity} {payload.name} have been sold"}

@products_router.delete("/{itemID}",
tags=["PRODUCTS"],
response_model= Dict[str,str],
summary="Delete a specific product in inveventory item",
status_code=200,
)
def deleteproduct(itemID:int,name:str,db:Session = Depends(getDb)):
    item=db.query(Products).filter(Products.id==itemID).first()
    if not item:
        raise HTTPException(status_code=400,detail="Invalid entery!")
    elif item.name!=name:
        raise HTTPException(status_code=404,detail="No such Product!")
    else:
        db.delete(item)
        db.commit()
        return  {"Message":f"Item {name} successfully removed"}
