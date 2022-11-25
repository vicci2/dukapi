# Here we explore the useful capabilites of of Fast API (Decoupling):
from fastapi import APIRouter
from .stock import stock_router,stock_router2
from .products import products_router
from .sales import sales_router

router=APIRouter()

router.include_router(stock_router,prefix='/stock',tags=["STOCK"])
router.include_router(stock_router2,prefix='/stock2',tags=["STOCK2"])
router.include_router(products_router,prefix='/products',tags=["PRODUCTS"])
router.include_router(sales_router,prefix='/sales',tags=["SALES"])