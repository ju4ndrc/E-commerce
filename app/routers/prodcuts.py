from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlmodel import select
from db import SessionDep
from models import Product, User

import os
import shutil
from uuid import UUID
router = APIRouter(prefix="/products", tags=["Products"])
UPLOAD_DIR = "app/static/img"
os.makedirs(UPLOAD_DIR, exist_ok=True)
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    image: UploadFile = File(...),


):
    image_url = None

    if image:
        # Guardar imagen físicamente
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/static/img/{image.filename}"

    # Crear producto
    product = Product(name=name,description=description, price=price, stock=stock, img=image_url,owner_id = user.id)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/", response_model=list[Product])
async def list_products(session: SessionDep,user: User ):
    return session.exec(select(Product)).all()

@router.patch("/{product_id}", response_model=Product)
async def update_product(
    product_id: UUID,
    session: SessionDep,
    name: str = Form(None),
    description: str = Form(None),
    price: float = Form(None),
    stock: int = Form(None),
    image: UploadFile = File(None),

):
    # Buscar producto
    db_product = session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Actualizar imagen si se envía una nueva
    if image:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_product.img = f"/static/img/{image.filename}"

    # Actualizar los campos enviados
    if name is not None:
        db_product.name = name
    if description is not None:
        db_product.description = description
    if price is not None:
        db_product.price = price
    if stock is not None:
        db_product.stock = stock

    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product
@router.delete("/{product_id}")
async def delete_product(product_id: UUID, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}