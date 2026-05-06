from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user"
    )

    phone: str = Field(
        ...,
        pattern=r"^[6-9]\d{9}$",
        description="Indian mobile number (10 digits)"
    )

    email: EmailStr = Field(
        ...,
        description="Valid email address"
    )

    pan: str = Field(
        ...,
        pattern=r"^[A-Z]{5}[0-9]{4}[A-Z]$",
        description="PAN number (e.g. ABCDE1234F)"
    )

    ifsc: str = Field(
        ...,
        pattern=r"^[A-Z]{4}0[A-Z0-9]{6}$",
        description="Bank IFSC code"
    )

    upi: Optional[str] = Field(
        None,
        description="UPI ID (e.g. name@bank)"
    )

    account: str = Field(
        ...,
        min_length=9,
        max_length=18,
        description="Bank account number"
    )

    balance: float = Field(
        0.0,
        ge=0,
        description="Account balance (cannot be negative)"
    )

class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True 