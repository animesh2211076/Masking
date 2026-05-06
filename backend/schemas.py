from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
Base=declarative_base()


class User(Base):
    __tablename__ = "users"
    id =Column(Integer, primary_key=True, index=True)

    name= Column(String) 

    phone= Column(String,unique=True)  

    email= Column(String,unique=True)  
    pan= Column(String,unique=True)  

    ifsc= Column(String,unique=True)  

    upi= Column(String,unique=True) 
    account= Column(String,unique=True)  
    balance= Column(Float)  