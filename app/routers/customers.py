from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from db import SessionDep
from models import Cart, CartItem, Product, User

from uuid import UUID

router = APIRouter(prefix="/cart", tags=["Cart"])

# Obtener el carrito activo del usuario
@router.get("/", response_model=list[dict])
async def get_cart(session: SessionDep):
    cart = session.exec(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()

    if not cart:
        cart = Cart(customer_id=user.id)
        session.add(cart)
        session.commit()
        session.refresh(cart)

    # Traer productos del carrito
    items = session.exec(select(CartItem).where(CartItem.cart_id == cart.id)).all()

    product_data = []
    for item in items:
        product = session.get(Product, item.product_id)
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


# Agregar producto al carrito
@router.post("/add/{product_id}")
async def add_to_cart(
    product_id: UUID,
    quantity: int,
    session: SessionDep
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = session.exec(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()

    if not cart:
        cart = Cart(customer_id=user.id)
        session.add(cart)
        session.commit()
        session.refresh(cart)

    item = session.exec(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)

    session.add(item)
    session.commit()
    session.refresh(item)

    return {"message": f"Added {quantity} {product.name} to your cart."}


# Eliminar producto del carrito
@router.delete("/remove/{product_id}")
async def remove_from_cart(product_id: UUID, session: SessionDep):
    cart = session.exec(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = session.exec(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product not in cart")

    session.delete(item)
    session.commit()
    return {"message": "Product removed from cart."}


# Vaciar carrito
@router.delete("/clear")
async def clear_cart(session: SessionDep):
    cart = session.exec(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = session.exec(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    for item in items:
        session.delete(item)

    session.commit()
    return {"message": "Cart cleared successfully."}