from sqlmodel import SQLModel, Field,Relationship
from typing import Optional,List
import datetime
import uuid
from pydantic import BaseModel, EmailStr, field_validator
from db import  init_db
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class UserBase(SQLModel):
    username: str | None = Field(description="User name")
    email: EmailStr = Field(default=None, unique = True)
    password: str
    role: RoleEnum = Field(default=RoleEnum.CUSTOMER)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    date: datetime.datetime | None = Field(default_factory=datetime.datetime.now)
    is_active: bool = Field(default=True)


    products: List["Product"] = Relationship(back_populates="owner")
    orders: List["Order"] = Relationship(back_populates="customer")
    cart: Optional["Cart"] = Relationship(back_populates="customer")

class ProductBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    owner_id: uuid.UUID = Field(foreign_key="user.id")
    img : str | None = None

    owner: Optional["User"] = Relationship(back_populates="products")
# -----------------------------
# PEDIDOS
# -----------------------------
class OrderBase(SQLModel):
    total_amount: float

class Order(OrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="user.id")

    customer: Optional[User] = Relationship(back_populates="orders")

# -----------------------------
# CARRITO DE COMPRAS
# -----------------------------
class Cart(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="user.id")
    is_active: bool = Field(default=True)

    customer: Optional[User] = Relationship(back_populates="cart")
    items: List["CartItem"] = Relationship(back_populates="cart")


class CartItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    cart_id: uuid.UUID = Field(foreign_key="cart.id")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    quantity: int = Field(default=1, ge=1)

    cart: Optional[Cart] = Relationship(back_populates="items")
    product: Optional[Product] = Relationship()
class CreateUser(UserBase):
    pass
class UpdateUser(UserBase):
    pass
class CreateProduct(ProductBase):
    pass