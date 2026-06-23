from pydantic import BaseModel, Field, field_validator, EmailStr
import string
from typing import List

class User(BaseModel):
    username: str = Field(..., min_length=2, max_length=15)
    email: EmailStr
    full_name:  str = Field(min_length=3, max_length=15)
    disabled: bool = Field()
    roles: list[str] = Field()

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=15)
    email: EmailStr
    full_name:  str = Field(min_length=3, max_length=15)
    password: str 

    @field_validator('password')
    def validate_password_strength(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit.")
        if not any(c in string.punctuation for c in value):
            raise ValueError("Password must contain at least one special character.")
        return value

class Ticker(BaseModel):
    ticker: str =Field(..., min_length=2, max_length=10)

    @field_validator("ticker")
    def validate_symbol(cls, v):
        return v.upper()  # Always store symbols in uppercase

class PortfolioEntry(BaseModel):
    symbol: str = Field(..., min_length=2, max_length=10)
    amount: float = Field(..., gt=0)
    buy_price: float = Field(..., gt=0)

    @field_validator("symbol")
    def validate_symbol(cls, v):
        return v.upper()  # Always store symbols in uppercase

    class Config:
        orm_mode = True

class PortfolioResponse(BaseModel):
    id: int
    symbol: str
    amount: float
    buy_price: float
    current_price: float
    invested_value: float
    current_value: float
    profit_loss: float

class PortfolioListResponse(BaseModel):
    portfolio: List[PortfolioResponse]

class Config:
    from_attributes = True
