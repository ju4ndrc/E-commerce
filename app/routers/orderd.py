from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from sqlmodel import select
from db import SessionDep
from models import Cart, CartItem, Order, User
from fastapi.templating import Jinja2Templates
router = APIRouter(prefix="/orders", tags=["Orders"])
templates = Jinja2Templates(directory="templates")
@router.get("/checkout")
async def checkout_page(request: Request, session: SessionDep, user: User):


    # Obtener carrito activo
    cart_query = await session.execute(
        select(Cart).where(
            Cart.customer_id == user.id,
            Cart.is_active == True
        )
    )
    cart = cart_query.scalars().first()

    if not cart:
        raise HTTPException(404, "No active cart found")

    # Obtener items
    items_query = await session.execute(
        select(CartItem).where(CartItem.cart_id == cart.id)
    )
    items = items_query.scalars().all()

    if not items:
        raise HTTPException(400, "Your cart is empty")

    # Calcular total
    total = sum(item.product.price * item.quantity for item in items if item.product)

    return templates.TemplateResponse(
        "components/payment.html",
        {
            "request": request,
            "items": items,
            "total": total
        }
    )


@router.post("/checkout")
async def checkout_process(
    request: Request,
    session: SessionDep,
    user: User,
    full_name: str = Form(...),
    email: str = Form(...),
    address: str = Form(...),
    phone: str = Form(...)
):

    cart_query = await session.execute(
        select(Cart).where(
            Cart.customer_id == user.id,
            Cart.is_active == True
        )
    )
    cart = cart_query.scalars().first()

    if not cart:
        raise HTTPException(404, "No active cart found")

    items_query = await session.execute(
        select(CartItem).where(CartItem.cart_id == cart.id)
    )
    items = items_query.scalars().all()

    if not items:
        raise HTTPException(400, "Your cart is empty")

    total = sum(item.product.price * item.quantity for item in items if item.product)

    # Crear la orden
    order = Order(
        customer_id=user.id,
        total_amount=total,
        full_name=full_name,
        email=email,
        address=address,
        phone=phone
    )

    session.add(order)

    # Desactivar carrito
    cart.is_active = False
    session.add(cart)

    await session.commit()

    return templates.TemplateResponse(
        "components/payment.html",
        {
            "request": request,
            "order": order,
            "total": total,
            "success": True
        }
    )