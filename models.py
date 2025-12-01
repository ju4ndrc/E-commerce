from sqlmodel import SQLModel, Field,Relationship
from typing import Optional,List
import datetime
import uuid
from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"

class Token(SQLModel):
    access_token: str
    token_type: str


class UserBase(SQLModel):
    username: str | None = Field(description="User name")
    email: str = Field(default=None, unique = True)
    password: str
    status: bool = Field(default=True)
    img : Optional[str] = Field(description="User image", default=None)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory = uuid.uuid4, primary_key=True, index=True)
    date: datetime.datetime | None = Field(default_factory=datetime.datetime.now)
    role: RoleEnum = Field(default=RoleEnum.CUSTOMER)



    orders: List["Order"] = Relationship(back_populates="customer")
    cart: Optional["Cart"] = Relationship(back_populates="customer")

class ProductBase(SQLModel):
    name: str| None = Field(description="Product name")
    description:str | None = Field(description="Product Description")
    price: float | None = Field(description="Product Price")
    stock: int | None = Field(description="Product Stock")
    img : Optional[str] = Field(description="Product image")

class Product(ProductBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
#    owner_id: uuid.UUID = Field(foreign_key="user.id")

#    owner: Optional["User"] = Relationship(back_populates="products")

# PEDIDOS

class OrderBase(SQLModel):
    total_amount: float

class Order(OrderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    customer_id: uuid.UUID = Field(foreign_key="user.id")

    customer: Optional[User] = Relationship(back_populates="orders")


# CARRITO DE COMPRAS

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