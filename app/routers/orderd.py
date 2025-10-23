from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Cart, CartItem, Order, User
from app.auth.auth_router import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout")
async def checkout(session: SessionDep, user: User = Depends(get_current_user)):
    cart = session.exec(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="No active cart found")

    items = session.exec(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    if not items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    total = sum(item.product.price * item.quantity for item in items if item.product)

    order = Order(customer_id=user.id, total_amount=total)
    session.add(order)

    # Desactivar el carrito
    cart.is_active = False
    session.add(cart)
    session.commit()

    return {"message": "Order placed successfully", "total_amount": total}