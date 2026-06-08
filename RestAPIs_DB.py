from fastapi import Depends, FastAPI

from database import Base, SessionLocal, engine
from database_models.product import Product
from pydantic_models.productDto import ProductDto
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def get_db():
     db = SessionLocal()
     try:
        yield db
     finally:
        db.close()


@app.get("/")
def read_root():
    return "Welcome to the Product API!"

@app.post("/product")
def addProduct(productDto: ProductDto, db: Session = Depends(get_db)):
    #In Python params with default values must come after params without default values.
    product = Product(
        id=productDto.id,
        name=productDto.name,
        price=productDto.price,
        description=productDto.description,
        in_stock=productDto.in_stock
    )
    db.add(product)
    db.commit()
    return {"message": "Product added successfully"}

@app.get("/getProducts")
def fetchProducts():
   data = db.query(Product).all()
   return data

@app.get("/getProduct/{id}")
def fetchProduct(id):
    data = db.query(Product).filter(Product.id == id).first()
    if data is None:
        return {"message": "Product not found"}
    return data

@app.put("/product/{id}")
def updateProduct(id: str, dto: ProductDto):
    product = db.query(Product)\
                .filter(Product.id == id)\
                .first()

    if product is None:
        return {"message": "Product not found"}
    product.id = dto.id
    product.name = dto.name
    product.price = dto.price
    product.description = dto.description
    product.in_stock = dto.in_stock
    db.commit()

    return {"message": "Updated successfully"}



@app.delete("/product/{id}")
def deleteProduct(id: str):

    product = db.query(Product)\
                .filter(Product.id == id)\
                .first()

    if product is None:
        return {"message": "Product not found"}

    db.delete(product)
    db.commit()

    return {"message": "Product deleted successfully"}
