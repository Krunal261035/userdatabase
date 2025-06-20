from sqlalchemy import Column, Integer, String,Text,DateTime,func,DECIMAL,Enum,ARRAY,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy.orm import relationship
Base = declarative_base()

class ProductCategoryModel(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String,index=True)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class SizeEnum(str, enum.Enum):
    M = "M"
    L = "L"
    XL = "XL"

class ProductModel(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String,index=True)
    price = Column(DECIMAL(10,2),index=True)
    size = Column(Enum(SizeEnum, name="size", create_type=False), nullable=False)
    image = Column(ARRAY(Text),index=True)
    stock = Column(Integer,index=True)
    description = Column(String,index=True)
    category_id = Column(Integer,index=True)


class CartModel(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="SET NULL"))
    created_at = Column(DateTime, server_default=func.now())


class CartitemsModel(Base):
    __tablename__ = "cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer,index=True)
    added_at = Column(DateTime, server_default=func.now())


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,index=True)
    orderdate = Column(DateTime, server_default=func.now())

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer,index=True)
    product_id = Column(Integer,index=True)
    quantity = Column(Integer,index=True)
    price = Column(Integer,index=True)