from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import  Session
from models.models import UserModel,AddressModel
from schemas.schema import UserSchema,AddressSchema,UpdateUserSchema,AddressResponseSchema
from database import get_db
from utils import *
import uuid, random
from models.AdminModel import ProductModel

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
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
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


@router.delete("/delete_account/")
def delete_account(db:Session= Depends(get_db),token:UserModel=Depends(get_current_user)):
    try:

        user = db.query(UserModel).filter(UserModel.id == token.id).first()
        print(user)
        db.delete(user)
        db.commit()
        # db.refresh(user)
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
    
@router.get("/Get_address")
def get_address(db:Session = Depends(get_db),token:UserModel=Depends(get_current_user)):
    user = db.query(AddressModel).filter(AddressModel.user_id == token.id).all()
    return {"body":user}

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