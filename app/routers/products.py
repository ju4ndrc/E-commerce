from fastapi import APIRouter, Request, HTTPException, status, File, UploadFile, Form
from sqlmodel import select
from starlette.responses import RedirectResponse

from db import SessionDep
from models import Product, CreateProduct
from typing import Optional
from uuid import UUID
from supa_impt.supa_bucket import upload_to_bucket
#Templates response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
router = APIRouter(prefix="/products", tags=["Products"])
templates = Jinja2Templates(directory="templates")

@router.get("/new",response_class=HTMLResponse,status_code=status.HTTP_200_OK)
async def show_create(request: Request):
    return templates.TemplateResponse("products_components/crud_products.html",{"request": request})

@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    request: Request,
    session: SessionDep,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    img:Optional[UploadFile] = File(...),


):
    img_url = None
    if img:
        try:
            img_url = await upload_to_bucket(img)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        try:
            new_product = CreateProduct(name=name,description=description, price=price, stock=stock, img=img_url)
            product = Product.model_validate(new_product)
            session.add(product)
            await session.commit()
            await session.refresh(product)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    return RedirectResponse(url="/products/new", status_code=status.HTTP_302_FOUND)

@router.get("/",response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def list_products(request:Request,session: SessionDep):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return templates.TemplateResponse("products_components/show_products.html",
                                      {"request": request, "products": products})
@router.patch("/{product_id}", response_model=Product)
async def update_product(
    product_id: UUID,
    session: SessionDep,
    name: str = Form(None),
    description: str = Form(None),
    price: float = Form(None),
    stock: int = Form(None),
    img: Optional[UploadFile] = File(...),

):
    # Buscar producto
    db_product = await session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")


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
    await session.commit()
    await session.refresh(db_product)
    return db_product
@router.delete("/{product_id}")
async def delete_product(product_id: UUID, session: SessionDep):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return {"message": "Product deleted successfully"}