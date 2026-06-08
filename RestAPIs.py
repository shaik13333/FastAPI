from fastapi import FastAPI
from pydantic_models.product import Product

app = FastAPI()


products = [
    Product(id="1", name="Laptop", price=999.99, description="A high-performance laptop", in_stock=True),
    Product(id="2", name="Smartphone", price=499.99, description="A powerful smartphone", in_stock=True),
    Product(id="3", name="Headphones", price=199.99, description="Noise-cancelling headphones", in_stock=False)
]

@app.get("/products")
def read_root():
    return products

@app.get("/product/{id}")
def getProduct(id):
    for product in products:
        if(product.id == id):
            return product
    return {"Product not found"}

@app.post("/product")
def createProduct(product: Product):
    products.append(product)

@app.delete("/product/{id}")
def deleteProduct(id: str):
    for product in products:
        if product.id == id:
            products.remove(product)
            return {"message": "Product deleted successfully"}

    return {"message": "Product not found"}

@app.put("/product/{id}")
def updateProduct(id: str, updated_product: Product):
    for product in products:
        if product.id == id:
            product.name = updated_product.name
            product.price = updated_product.price
            product.description = updated_product.description
            product.in_stock = updated_product.in_stock

            return {"message": "Product updated successfully"}

    return {"message": "Product not found"}
