from sqlalchemy import Column, Integer, String

import database

class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(50), unique=True, index=True)
    passwd = Column(String(100))
    accessToken = Column(String(500), default=None)
