from fastapi import APIRouter, HTTPException, Request, Form, Depends
from sqlmodel import select
from fastapi.responses import RedirectResponse
from app.auth.current_user import get_current_user
from db import SessionDep
from models import Cart, CartItem, Product, User
from fastapi.templating import Jinja2Templates
from uuid import UUID

router = APIRouter(prefix="/cart", tags=["Cart"])
templates = Jinja2Templates(directory="templates")



@router.get("/view")
async def view_cart(request: Request, session: SessionDep, user: User = Depends(get_current_user)):

    # Buscar carrito activo
    result = await session.execute(
        select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)
    )
    cart = result.scalars().first()

    if not cart:
        return templates.TemplateResponse(
            "cart.html",
            {"request": request, "items": []}
        )

    # Obtener items
    items_db = await session.execute(
        select(CartItem).where(CartItem.cart_id == cart.id)
    )
    items = items_db.scalars().all()

    data = []
    for item in items:
        product = await session.get(Product, item.product_id)
        if product:
            data.append({
                "product_id": str(item.product.id),
                "name": product.name,
                "price": product.price,
                "img": product.img,
                "quantity": item.quantity
            })

    return templates.TemplateResponse(
        "products_components/cart_component.html",
        {"request": request, "items": data}
    )



@router.get("/", response_model=list[dict])
async def get_cart(session: SessionDep, user: User = Depends(get_current_user)):

    result = await session.execute(
        select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)
    )
    cart = result.scalars().first()

    if not cart:
        cart = Cart(customer_id=user.id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)

    items_result = await session.execute(
        select(CartItem).where(CartItem.cart_id == cart.id)
    )
    items = items_result.scalars().all()

    product_data = []
    for item in items:
        product = await session.get(Product, item.product_id)
        if product:
            product_data.append({
                "product_id": str(product.id),
                "name": product.name,
                "price": product.price,
                "description": product.description,
                "img": product.img,
                "quantity": item.quantity
            })

    return product_data



@router.post("/add/{product_id}")
async def add_to_cart(
    request: Request,
    session: SessionDep,
    product_id: UUID,
    user: User = Depends(get_current_user),
    quantity: int = Form(...),
):

    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")


    result = await session.execute(
        select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)
    )
    cart = result.scalars().first()


    if not cart:
        cart = Cart(customer_id=user.id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)


    result_item = await session.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )
    item = result_item.scalars().first()

    # Actualizar o crear item
    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        session.add(item)

    await session.commit()

    # REDIRIGIR AL CARRITO
    return RedirectResponse(url="/cart/view", status_code=303)

# ------------------------
# ELIMINAR PRODUCTO
# ------------------------
@router.post("/remove/{product_id}")
async def remove_from_cart(
    product_id: UUID,
    session: SessionDep,
    user: User = Depends(get_current_user)
):


    result = await session.execute(
        select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)
    )
    cart = result.scalars().first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    result_item = await session.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == product_id
        )
    )
    item = result_item.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Product not in cart")


    await session.delete(item)
    await session.commit()

    return RedirectResponse("/cart/view", status_code=303)

# ------------------------
# VACIAR CARRITO
# ------------------------
@router.delete("/clear")
async def clear_cart(session: SessionDep, user: User = Depends(get_current_user)):

    # Carrito
    result = await session.execute(
        select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)
    )
    cart = result.scalars().first()

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Items
    items_result = await session.execute(
        select(CartItem).where(CartItem.cart_id == cart.id)
    )
    items = items_result.scalars().all()

    for item in items:
        await session.delete(item)

    await session.commit()
    return {"message": "Cart cleared successfully."}
