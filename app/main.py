from fastapi import FastAPI
# import sentry_sdk
from fastapi.middleware.cors import CORSMiddleware
# APIRouter
from .api.api import router
# db configs
from .db.base import Base
from .db.session import engine
# table creation
Base.metadata.create_all(bind=engine)

# sentry_sdk.init(
#     dsn="https://e76ab2001f45482cb634a4e3a859f60a@o1410536.ingest.sentry.io/6748054",
 
#     # Set traces_sample_rate to 1.0 to capture 100%
#     # of transactions for performance monitoring.
#     # We recommend adjusting this value in production,
#     traces_sample_rate=1.0,
# )
# instance of the fastAPI
app = FastAPI(
    title="Vicci Shop API",
    description="A sample VicciShop Inventory Management System API",
    version="0.1.0",
    docs_url="/viccishop/docs",
    redoc_url="/viccishop/redoc",
    contact={
        "name":"Vicci",
        "email":"vicci2regia@gmail.com",
        "tel":"0728893493"
    }    
)
# CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Custom request responses
app.include_router(router,responses={
     200: {'description': 'Ok'},
                       201: {'description': 'Created'},
                       202: {'description': 'Accepted'},
                       400: {"description": "Bad Request"},
                       401: {"description": "Unauthorized"},
                       403: {"description": "Forbidden"},
                       404: {"description": "Not found"},
                       405: {"description": "Method not allowed"}
                       })
