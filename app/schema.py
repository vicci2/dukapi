# This file holds the basic blueprint of the API'S UI 
from pydantic import BaseModel
from typing import Optional
# from sqlalchemy import number
from datetime import datetime

# stock schema
class StockBase(BaseModel):
    product_name:str
    desc:str
    quantity:int
    b_p:int    

class AddStock(StockBase):
    pass

class Stocks(StockBase):
    id:int
    date:datetime
    class Config:
        orm_mode=True

class EditStock(BaseModel):
    product_name:Optional[str]
    new_name:Optional[str]

class StockUp(BaseModel):
    name:str
    id:int
    quantity:int

class Avail(BaseModel):
    id:int
    quantity:int
    selling_price:int
    serial_no:str

# sales schema
class SalesBase(BaseModel):
    name:str
    quantity:int    

class MakeSale(SalesBase):
    id:int    

class Salesinfo(SalesBase):    
    class Config:
        orm_mode=True

class ViewSales(BaseModel):
    id:int
    name:str

# these classes use the relationships established
class SaleInDb(SalesBase):
    id:int
    date:datetime
    class Config:
        orm_mode=True

# inventories schema
class ProductBase(BaseModel):
    name:str
    quantity:int
    bp:int
    sp:int
    serial_no:str

class StockProduct(BaseModel):
    id:int
    name:str
    quantity:Optional[int]
    pass

class EditProduct(BaseModel):
    id:int
    name:str
    # newName:Optional[str]
    sp:Optional[int]

class Product(ProductBase):
    class Config:
        orm_mode=True

class Productinfo(ProductBase):
    # id:int
    class Config:
        orm_mode=True

# these classes use the relationships established
class ProductInDb(ProductBase):
    id:int
    date:datetime
    sale:list[MakeSale]
    product:Productinfo
    class Config:
        orm_mode=True