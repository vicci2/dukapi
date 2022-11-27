# Here we explore the useful capabilites of of Fast API (Decoupling):
from fastapi import APIRouter
from .stock import stock_router,stock_router2
from .products import products_router,products_router2
from .sales import sales_router,sales_router2

router=APIRouter()

router.include_router(stock_router,prefix='/stock',tags=["STOCK"])
router.include_router(stock_router2,prefix='/stock2',tags=["STOCK2"])
router.include_router(products_router,prefix='/products',tags=["PRODUCTS"])
router.include_router(products_router2,prefix='/products2',tags=["PRODUCTS2"])
router.include_router(sales_router,prefix='/sales',tags=["SALES"])
router.include_router(sales_router2,prefix='/sales2',tags=["SALES2"])