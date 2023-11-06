from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+mysqlconnector://root:root123@localhost/loginApp")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine, autoflush=False, )