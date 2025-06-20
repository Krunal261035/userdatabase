from fastapi import APIRouter,Depends
from models.AdminModel import ProductCategoryModel,ProductModel
from models.models import UserModel
from schemas.products import ProductCategory,ProductSchema,UserResponseSchema
from sqlalchemy.orm import  Session
from database import get_db
from utils import *

product = APIRouter()

@product.post("/productcategory")
def addcategory(body:ProductCategory,db:Session=Depends(get_db),token : UserModel=Depends(get_current_admin)):
    try:
        data = db.query(ProductCategoryModel).filter(ProductCategoryModel.name == body.name).first()
        if data:
            raise HTTPException(status_code=404,detail="Category already exist")

        category = ProductCategoryModel(**body.model_dump())
        db.add(category)
        db.commit()
        db.refresh(category)

        return {"message":"true","body":category}
    except Exception as e:
        return e

@product.post("/Products")
def Product(body:ProductSchema,db:Session=Depends(get_db),token:UserModel = Depends(get_current_admin)):
    try:
        exits = db.query(ProductModel).filter(ProductModel.product_name == body.product_name).first()
        if exits:
            raise HTTPException(status_code=404,detail="product name exits")
        product = ProductModel(**body.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)

        return {"message":"true","body":product}
    except Exception as e:
        print(e)

@product.get("/users",response_model=list[UserResponseSchema])
def user(db:Session = Depends(get_db),token:UserModel=Depends(get_current_admin)):
    user = db.query(UserModel).filter(UserModel.role == "user").all()
    return user