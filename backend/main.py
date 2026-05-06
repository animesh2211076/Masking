from fastapi import FastAPI, HTTPException, Depends

from file_utils import  write_masked_log
from masking import mask_user_object
# import json
from database import sessionLocal
import schemas
from sqlalchemy.orm import Session
from schemas import User as UserORM
from models import UserCreate, UserResponse


schemas.Base.metadata.create_all(bind=sessionLocal().bind)

app = FastAPI(title="Masking using FastAPI + Presidio")


def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()
# all users masked data returned
@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserORM).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    # ORM → Pydantic
    user_schemas = [UserResponse.model_validate(user) for user in users]

    # Mask response
    masked_users = [
        mask_user_object(user.model_dump(), role="user")
        for user in user_schemas
    ]

    # Masked logging
    write_masked_log(
        role="user",
        route="/users",
        masked_payload=masked_users
    )

    return masked_users
    # masked_user = mask_user_object(
    #     user_schema.model_dump(),
    #     role="user"
    # )

    # # Masked logging
    # write_masked_log(
    #     role="user",
    #     route=f"/users/{user_id}",
    #     masked_payload=masked_user
    # )

    # return masked_user

#     users = read_users_from_file()
#     masked_users = [mask_user_object(u, role="user") for u in users]

#     write_masked_log(role="user", route="/users", masked_payload=masked_users)
#     return masked_users

# particular user masked data returned
@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserORM, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ORM → Pydantic
    user_schema = UserResponse.model_validate(user)

    # Mask response
    masked_user = mask_user_object(
        user_schema.model_dump(),
        role="user"
    )

    # Masked logging
    write_masked_log(
        role="user",
        route=f"/users/{user_id}",
        masked_payload=masked_user
    )

    return masked_user


    # raise HTTPException(status_code=404, detail="User not found")

# masked data for support role but less than user
@app.get("/support")
def support_view(db: Session = Depends(get_db)):
    users = db.query(UserORM).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    # ORM → Pydantic
    user_schemas = [UserResponse.model_validate(user) for user in users]

    # Mask response
    masked_users = [
        mask_user_object(user.model_dump(), role="support")
        for user in user_schemas
    ]

    # Masked logging
    write_masked_log(
        role="user",
        route="/users",
        masked_payload=masked_users
    )

    return masked_users

#     users = read_users_from_file()
#     masked_users = [mask_user_object(u, role="support") for u in users]

#     write_masked_log(role="support", route="/support", masked_payload=masked_users)
#     return masked_users


# full data for admin role but logs still masked
@app.get("/admin")
def admin_view(db: Session = Depends(get_db)):
    users = db.query(UserORM).all()

    if not users:
        raise HTTPException(status_code=404, detail="No users found")

    # ORM → Pydantic
    user_schemas = [UserResponse.model_validate(user) for user in users]

    # Mask response
    masked_users = [
        mask_user_object(user.model_dump(), role="support")
        for user in user_schemas
    ]

    # Masked logging
    write_masked_log(
        role="admin",
        route="/admin",
        masked_payload=masked_users
    )

    return user_schemas

#     users = read_users_from_file()



#     response_data = users

#     masked_for_logs = [mask_user_object(u, role="support") for u in users]
#     write_masked_log(role="admin", route="/admin", masked_payload=masked_for_logs)

#     return response_data

@app.post("/upload_users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Pydantic → ORM
    db_user = UserORM(**user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # ORM → Pydantic (for response)
    return UserResponse.model_validate(db_user)
    # users = read_users_from_file()
    # users.append(new_user.model_dump())

    # Write back to the user data file
    # with open("user_data.txt", "w", encoding="utf-8") as f:
    #     json.dump(users, f, indent=2)

    # masked_user = mask_user_object(new_user.model_dump(), role="user")
    # write_masked_log(role="user", route="/users", masked_payload=masked_user)

    # return db_user
