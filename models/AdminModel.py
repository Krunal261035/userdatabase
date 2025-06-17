from sqlalchemy import Column, Integer, String,Text,DateTime,func,DECIMAL,Enum,ARRAY
from sqlalchemy.ext.declarative import declarative_base
import enum
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