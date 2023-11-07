from config.db import db
from fastapi import APIRouter, status
from schemas.user import user_entity, users_entity
from fastapi.responses import JSONResponse
from bson.objectid import ObjectId
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# @router.get("/")
# async def read_users():
#     users_data = db.users.find({})

#     if not users_data or users_data == []:
#         return JSONResponse(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             content={"message": "user not found"}
#         )
#
#     users = users_entity(users_data)
#     return users


@router.get("/")
async def read_user_by_email(email: str):
    user_data = db.users.find_one({"email": email})

    if not user_data or user_data == {}:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "user not found"}
        )

    user = user_entity(user_data)
    return user


@router.get("/{id}")
async def read_user(id: str):
    user_data = db.users.find_one({"_id":  ObjectId(id)})

    if not user_data or user_data == {}:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "user not found"}
        )

    user = user_entity(user_data)
    return user


@router.post("/")
async def create_user(user: User):
    new_user = db.users.insert_one({
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "password": user.password,
        "dob": str(user.dob),
        "gender": user.gender,
        "university": user.university,
        "mobile": user.mobile,
        "country": user.country
    })

    find_user = db.users.find_one({"_id":  new_user.inserted_id})

    return user_entity(find_user)


@router.put("/{id}")
async def update_user(id: str, user: User):
    db.users.find_one_and_update({"_id": ObjectId(id)}, {
        "$set": {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password,
            "dob": str(user.dob),
            "gender": user.gender,
            "university": user.university,
            "mobile": user.mobile,
            "country": user.country
        }
    })

    return {"message": "User updated successfully"}


@router.delete("/{id}")
async def delete_user(id: str):
    db.users.find_one_and_delete({"_id": ObjectId(id)})

    return {"message": "User deleted successfully"}
