from fastapi import FastAPI, Depends, HTTPException,APIRouter,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import  Session
from models.models import UserModel,AddressModel
from schemas.schema import UserSchema,AddressSchema,UpdateUserSchema,AddressSchemaDisplay,AddToCartSchema
from database import get_db
from utils import *
from models.AdminModel import ProductModel,CartModel,CartitemsModel
# FastAPI App
router = APIRouter()


# Routes

@router.post("/create_user")
def add(body:UserSchema,db:Session = Depends(get_db)):
    try:

        password_hash = get_password_hash(body.password_hash)

        user = UserModel(username = body.username,email = body.email,password_hash = password_hash,full_name = body.full_name,is_active = body.is_active,role= body.role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"body":user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_token(data={"sub": str(user.id), "role": user.role,"username":user.username,"email":user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.patch("/update_user")
def update_user(
    body: UpdateUserSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    try:
        updated = False

        # Compare values – only update if they are different
        if body.username == current_user.username:
            current_user.username = body.username
            updated = True

        if body.email == current_user.email:
            current_user.email = body.email
            updated = True

        if body.full_name == current_user.full_name:
            current_user.full_name = body.full_name
            updated = True

        if updated:
            db.commit()
            db.refresh(current_user)
            return {
                "message": "Profile updated.",
                "user": {
                    "username": current_user.username,
                    "email": current_user.email,
                    "full_name": current_user.full_name
                }
            }
        else:
            return {
                "message": "No changes detected.",
                "user": {
                    "username": current_user.username,
                    "email": current_user.email,
                    "full_name": current_user.full_name
                }
            }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_account")
def delete_account(db:Session= Depends(get_db),token:UserModel=Depends(get_current_user)):
    try:

        user = db.query(UserModel).filter(UserModel.id == token.id).first()
        print(user)
        db.delete(user)
        db.commit()
        return {"Message":"True","user":"Deleted successfully"}
    except Exception as e:
        return e
# @app.get("/user/dashboard")
# def user_dashboard(user: UserModel = Depends(get_current_user)):
#     return {"message": f"Hello {user.username}, this is your dashboard!"}


# @app.get("/admin/dashboard")
# def admin_dashboard(admin: UserModel = Depends(get_current_admin)):
#     return {"message": f"Welcome Admin {admin.username}!"}


@router.post("/Address")
def add_address(body:AddressSchema,db:Session = Depends(get_db),token :UserModel=Depends(get_current_user)):
    try:
        user = AddressModel(**body.model_dump(),user_id = token.id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return {"message":"true","body":user}
    except Exception as e:
        return {"detail":str(e)}
    
@router.get("/Get_address",response_model=list[AddressSchemaDisplay])
def get_address(db:Session = Depends(get_db),token:UserModel=Depends(get_current_user)):
    user = db.query(AddressModel).filter(AddressModel.user_id == token.id).all()
    return user

@router.put("/update_Address/{id}")
def update_address(id: int,body:AddressSchema,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    try:
        address = db.query(AddressModel).filter(AddressModel.id==id).first()
        if  not address:
            raise HTTPException(status_code=404,detail="Address not found")
        for key,value in body.model_dump(exclude_unset=True).items():
            setattr(address,key,value)
        db.commit()
        db.refresh(address)
        return {"message":"Address Updated","address":address}
    except Exception as e:
        return e
    
@router.delete("/Address/{id}")
def deleteaddress(id:int,db: Session = Depends(get_db), token: UserModel = Depends(get_current_user)):
    try:
        address = db.query(AddressModel).filter(AddressModel.user_id == token.id).first()
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        
        db.delete(address)
        db.commit()
        return {"detail": "Address deleted successfully"}
    except Exception as e:
        return {"detail": str(e)}

@router.get("/Products")
def products(db:Session=Depends(get_db)):
    products = db.query(ProductModel).all()
    return {"body": products}

@router.post("/add_Cart")
def cart(body:AddToCartSchema,db:Session= Depends(get_db),token:UserModel= Depends(get_current_user)):
    try:
        cart = db.query(CartModel).filter_by(user_id = token.id).first()
        if not cart:
            cart = CartModel(user_id = token.id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        
        existing_items = db.query(CartitemsModel).filter_by(id= cart.id,product_id = body.product_id).first()
        if existing_items:
            existing_items.quantity += body.quantity
            db.commit()
            db.refresh(existing_items)
            return existing_items
        
        new_items = CartitemsModel(cart_id = cart.id,product_id = body.product_id,quantity = body.quantity)
        db.add(new_items)
        db.commit()
        db.refresh(new_items)
        return new_items
    except Exception as e:
        return e


@router.get("/cart/total")
def total_cart(db:Session = Depends(get_db),token:UserModel=Depends(get_current_user)):
    results = (
        db.query(
            UserModel.username,
            ProductModel.product_name,
            CartitemsModel.quantity,
            ProductModel.price,
            (CartitemsModel.quantity * ProductModel.price).label("total")
        )
        .join(CartModel, CartModel.user_id == UserModel.id)
        .join(CartitemsModel, CartitemsModel.cart_id == CartModel.id)
        .join(ProductModel, ProductModel.id == CartitemsModel.product_id)
        .all()
    )
    return [
        {
            "username": row.username,
            "product_name": row.product_name,
            "quantity": row.quantity,
            "price": float(row.price),
            "total": float(row.total)
        }
        for row in results
    ]