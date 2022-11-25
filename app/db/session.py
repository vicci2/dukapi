# This file isused to bind the API to a database of choise and initiate a session upon connection or transaction:
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URI.
SQLALCHEMY_DATABASE_URL = "sqlite:///./dukapi.db"
# Binding the database URI to that of the app:
# engine=create_engine("postgresql://gsluscwvsxtaxi:4fcb45e3778720583c178db061a85a6be5eec19b7a32e46a6489e2b540bb6b5c@ec2-52-211-232-23.eu-west-1.compute.amazonaws.com:5432/d6op78lg3m8k3")
# engine=create_engine("postgresql://postgres:vicciSQL@localhost:5432/fast_duka_api")
engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
