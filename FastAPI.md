FAST API :- 


--> Initially we learned how to install fastAPI, uvicorn and setup the uvicorn server.
     
    INSIDE main.py:-

    from fastapi import FastAPI
    app = FastAPI()
    
    uvicorn filename.objectname --reload
    ex:- uvicorn main(filename).app --reload
    
--> Created rest api's for all http methods. Used pydantic models

   from pydantic import BaseModel

   class Product(BaseModel):
       id: str
       name: str
       price: float
       description: str
       in_stock: bool

--> FastAPI uses Pydantic models to validate and convert incoming JSON into Python objects. FastAPI automatically converts returned Python objects into JSON responses.It also acts as dto    and we can also add validation inside pydantic model.

--> For REST api's refer main.py in FASTAPI folder (/documents/FASTAPI)


================================================================================================================================

1) Lets create database config class to connect with database, We are using SQLlite

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///products.db"  --> DB url

engine = create_engine(DATABASE_URL)  --> connection with database

SessionLocal = sessionmaker( ---> Creates database sessions used for CRUD operations
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()  ---> any class extending this will act as DB table. It is same as @Entity in java.

----------------------------------------------------


2) We have also created a model:-

from sqlalchemy import Column, String, Float, Boolean
from database import Base

class Product(Base):

    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    in_stock = Column(Boolean)

----------------------------------------------------

3) Now main file where we will write the rest api's

from fastapi import FastAPI

from database import Base, engine
from database_models.product import Product

app = FastAPI()

Base.metadata.create_all(bind=engine)

--> This is a very important line.
--> Before calling this method, we import all the models/entities in the application.
--> SQLAlchemy scans all classes that extend Base.
--> It generates CREATE TABLE statements for those entities.
--> If the database file (products.db) does not exist, SQLite creates it automatically.
--> If the tables do not exist, SQLAlchemy creates them automatically.

Example:

class Product(Base)
class User(Base)

will generate:

CREATE TABLE products(...)
CREATE TABLE users(...)

inside products.db.

@app.get("/")
def read_root():
    return "Welcome to the Product API!"


==================================================================================================================================================
--------------------> We have practised all the CRUD api's, REFER \Documents\FastAPI\main_db.py (IT CONTAINS ALL THE API's) <---------------------
--> Know lets discuss each and every method we used in CRUD API's

1) db = SessionLocal()   --> To establish a connection with DB and to perform the CRUD operation
2) db.add(product)       --> Registers an object with SQLAlchemy and marks it to be inserted into the database during the next commit (still not inserted). Insert statement is generated
                             and it is executed when we call commit()
3) db.commit()           --> Permanently saves all pending changes (insert, update, delete) to the database by executing the generated SQL.
4) db.query(Product)     --> Starts building a SELECT query for the Product table but does not execute it yet.
5) filter()              --> Adds a WHERE condition to restrict which rows should be returned.
6) .first()              --> Executes the query and returns only the first matching row (or None if no row exists).
7) .all()                --> Executes the query and returns all matching rows as a list.
8) .delete()             --> deletes record from the table

---------------------------------------------------------

-> We have established a single connectionand reused it, but its not the practical way used in production system.


DEPENDS() IN FASTAPI

Purpose:

Depends() is FastAPI's Dependency Injection mechanism.

It tells FastAPI:

"Before executing this API method, execute another function, obtain its result, and inject that result into the method."

Database Example:- 

     def get_db():-

     db = SessionLocal()

     try:
        yield db

     finally:
        db.close()
-------------------------------------------

USE IN API:-

     @app.get("/products")
     def getProducts(
       db = Depends(get_db)
     ):
     return db.query(Product).all()
-------------------------------------------

FUNCTION OF "yield db":-

1) Give db object to FastAPI.
2) Pause execution.
3) Wait for API method to finish.
4) Continue execution after yield.
5) Execute cleanup code (db.close()).


====================================================================================================================

Response Model:- 

This is an important concept left in API's


ENTITY:-
class Product(Base):
    id
    name
    price
    supplier_cost
    internal_notes


RESPONSE MODEL:-
class ProductResponse(BaseModel):
    id: str
    name: str
    price: float


API:-
@app.get(
    "/product/{id}",
    response_model=ProductResponse
)
def getProduct():
    return product


--> OUTPUT contains only the fields present in RESPONSE MODEL

{
  "id": 10,
  "name": value,
  "price": 100
}
