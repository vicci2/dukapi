# The stock API flie; it holds all the endpoints that interact with the stock Model in the D.B
from fastapi import APIRouter,Depends,HTTPException
from typing import List, Dict,Generator
# Binding and sesson initiation:
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
# Attaching schemas that interact with the stock Model
from app.schema import Stocks,AddStock,EditStock,StockUp,Avail,Product
# Attaching target Model:
from app.models.stock import Stock
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

stock_router=APIRouter()
stock_router2=APIRouter()


@stock_router.get("/",
    tags=["STOCK"],
    response_model=List[Stocks],
    summary="all Stocked Items",
    status_code=200
)
def stock(db:Session = Depends(getDb)):
    # querying the database  
    products= db.query(Stock).all() 
    return products

@stock_router.get("/{itemID}",
    tags=["STOCK"],
    response_model=Stocks,
    summary="Get one Stocked Item",
    status_code=200
)
def stock(itemID:int,db:Session = Depends(getDb)):
    # querying the database  
    item= db.query(Stock).filter(Stock.id==itemID).first()
    if not item:
        raise HTTPException(status_code=404,detail=f"Item {itemID}does not exist") 
    # elif
    return item

@stock_router.post("/",
    tags=["STOCK"],
    response_model=Dict[str,str],
    summary="Add a Stock Item",
    status_code=200
)
def stock(payload:AddStock,db:Session = Depends(getDb)):
    # querying the database  
    item=db.query(Stock).filter(Stock.product_name == payload.product_name).first()
    if  item:
        raise HTTPException(status_code=400,detail=f"Sorry product {payload.product_name},is already stocked")    
    server_default=func.now()
    now=server_default
    bP=payload.b_p * payload.quantity
    res:AddStock=Stock(product_name=payload.product_name,quantity=payload.quantity,date=now,b_p=bP)      
    db.add(res)
    db.commit()
    return {"Message":f"Product {payload.product_name} is now in stock"}

@stock_router.put("/",
    tags=["STOCK"],
    response_model=Dict[str,str],
    summary="Change name of a stocked item",
    status_code=200
)
def editstock(itemID:int,payload:EditStock,db:Session = Depends(getDb)):
    # querying the database  
    item= db.query(Stock).filter(Stock.id==itemID).first()
    if not item:
        raise HTTPException(status_code=404,detail=f"Item {itemID}does not exist") 
    elif payload.product_name!=item.product_name:
        raise HTTPException(status_code=400,detail=f"Invalid product name")
    item.product_name=payload.new_name
    db.merge(item)
    db.commit()
    return {"Message":f"New product name:{payload.new_name}"}

@stock_router.put("/{name}",
    tags=["STOCK"],
    response_model=Dict[str,str],
    summary="Increase stocked product quantity",
    status_code=200
)
def stockUp(name:str,payload:StockUp,db:Session = Depends(getDb)):
    # querying the database  
    item=db.query(Stock).filter(Stock.product_name == name).first()
    if not item :
        raise HTTPException(status_code=404,detail=f"Sorry, product doesn't exist")    
    if item.id != payload.id:
        raise HTTPException(status_code=400,detail=f"Sorry product {name},has not been availed")        
    item.quantity=item.quantity + payload.quantity
    db.merge(item)
    db.commit()
    return {"Message":f"Stock Up Successful! "}

@stock_router.delete("/{itemID}",
tags=["STOCK"],
response_model= Dict[str,str],
summary="Delete a specific stocked item",
status_code=200,
)
def deletestock(itemID:int,name:str,db:Session = Depends(getDb)):
    item=db.query(Stock).filter(Stock.id==itemID).first()
    if not item and Stock.product_name!=name:
        raise HTTPException(status_code=400,detail="Invalid entery!")
    elif item.product_name!=name:
        raise HTTPException(status_code=404,detail="No such Product!")
    else:
        db.delete(item)
        db.commit()
        return  {"Message":f"Item {name} successfully removed"}

@stock_router2.post("/",
    tags=["STOCK2"],
    response_model=Dict[str,str],
    summary="Avail a Stocked Item",
    status_code=200
)
def avail(payload:Avail,db:Session = Depends(getDb)):
    # querying the database  
    item=db.query(Stock).filter(Stock.id == payload.id).first()
    if not item:
        raise HTTPException(status_code=400,detail=f"Sorry invalid ID")    
    prd=db.query(Products).filter(Products.name == item.product_name).first()
    if  prd :
        raise HTTPException(status_code=400,detail=f"Sorry product {item.product_name},is already available")    
    if payload.quantity > item.quantity:
        raise HTTPException(status_code=403,detail=f"Sorry  can't avail this much of {item.product_name}")    
    server_default=func.now()
    now=server_default
    res:Product=Products(name=item.product_name,quantity=payload.quantity,date=now,b_p=item.b_p,s_p=payload.selling_price,serial_no=payload.serial_no)          
    item.quantity=item.quantity - payload.quantity
    db.add(res)
    db.merge(item)
    db.commit()
    return {"Message":f"Product {item.product_name} is successfully availed"}