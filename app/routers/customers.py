from fastapi import APIRouter, HTTPException,Request
from sqlmodel import select
from db import SessionDep
from models import Cart, CartItem, Product, User

from uuid import UUID

router = APIRouter(prefix="/cart", tags=["Cart"])

# Obtener el carrito activo del usuario
@router.get("/", response_model=list[dict])
async def get_cart(session: SessionDep, user: User):
    cart = await session.execute(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()


    if not cart:
        cart = Cart(customer_id=user.id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)

    # Traer productos del carrito
    items = await session.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    products = items.scalars().all()


    product_data = []
    for item in products:
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


# Agregar producto al carrito
@router.post("/add/{product_id}")
async def add_to_cart(
    request: Request,
    product_id: UUID,
    quantity: int,
    session: SessionDep
):
    product = await session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    cart = await session.execute(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()

    if not cart:
        cart = Cart(customer_id=user.id)
        session.add(cart)
        await session.commit()
        await session.refresh(cart)

    item = await session.execute(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)

    session.add(item)
    await session.commit()
    await session.refresh(item)

    return {"message": f"Added {quantity} {product.name} to your cart."}


# Eliminar producto del carrito
@router.delete("/remove/{product_id}")
async def remove_from_cart(product_id: UUID, session: SessionDep):
    cart = await session.execute(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    item = await session.execute(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == product_id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Product not in cart")

    await session.delete(item)
    await session.commit()
    return {"message": "Product removed from cart."}


# Vaciar carrito
@router.delete("/clear")
async def clear_cart(session: SessionDep):
    cart = await session.execute(select(Cart).where(Cart.customer_id == user.id, Cart.is_active == True)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    items = await session.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    products = items.scalars().all()
    for item in items:
        session.delete(item)

    await session.commit()
    return {"message": "Cart cleared successfully."}