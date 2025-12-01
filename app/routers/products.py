from fastapi import APIRouter, Request, HTTPException, status, File, UploadFile, Form
from sqlmodel import select
from db import SessionDep
from models import Product, CreateProduct
from typing import Optional
from uuid import UUID
from supa_impt.supa_bucket import upload_to_bucket
#Templates response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
router = APIRouter( tags=["Products"])
templates = Jinja2Templates(directory="templates")

@router.get("/",response_class=HTMLResponse,status_code=status.HTTP_200_OK)
async def list_products(request: Request,session: SessionDep):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return templates.TemplateResponse("home.html",{"request": request, "products": products})
@router.get("/products/new",response_class=HTMLResponse,status_code=status.HTTP_200_OK)
async def show_create(request: Request,session: SessionDep):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return templates.TemplateResponse("products_components/crud_products.html",{"request": request , "products": products})
@router.get("/products/update/{product_id}",response_class=HTMLResponse,status_code=status.HTTP_200_OK)
async def show_update(request: Request,session: SessionDep, product_id: UUID):
    product = await session.get(Product, product_id)
    return templates.TemplateResponse("products_components/update.html",{"request": request , "product": product})


@router.get("/products",response_class=HTMLResponse,status_code=status.HTTP_200_OK)
async def show_cards(request: Request,session: SessionDep):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return templates.TemplateResponse("home.html",{"request": request, "products": products})
@router.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
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

@router.get("/products",response_class=HTMLResponse, status_code=status.HTTP_200_OK)
async def list_products(request:Request,session: SessionDep):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    return templates.TemplateResponse("products_components/crud_products.html",{"request": request, "products": products})

@router.post("/products/update/{product_id}", response_model=Product)
async def update_product(
    request: Request,
    session: SessionDep,
    product_id: UUID,

    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    stock: Optional[int] = Form(None),
    img: Optional[UploadFile] = File(None),

):
    # Buscar producto
    db_product = await session.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")



    # Actualizar los campos enviados
    if name :
        db_product.name = name
    if description :
        db_product.description = description
    if price :

        db_product.price = price
    if stock :
        db_product.stock = stock
    if img and img.filename:
        img_url = await upload_to_bucket(img)
        db_product.img = img_url


    session.add(db_product)
    await session.commit()
    await session.refresh(db_product)
    return RedirectResponse(url="/products/new", status_code=status.HTTP_302_FOUND)
@router.post("/products/{product_id}")
async def delete_product(product_id: UUID, session: SessionDep):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
    return RedirectResponse(url="/products/new", status_code=status.HTTP_302_FOUND)