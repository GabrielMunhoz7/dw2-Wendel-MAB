from pydantic import BaseModel
from typing import Optional


class CoinCreate(BaseModel):
    name: str
    period: Optional[str] = None
    region: Optional[str] = None
    material: Optional[str] = None
    denomination: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    image_front: Optional[str] = None
    image_back: Optional[str] = None


class CoinUpdate(BaseModel):
    name: Optional[str] = None
    period: Optional[str] = None
    region: Optional[str] = None
    material: Optional[str] = None
    denomination: Optional[str] = None
    year: Optional[str] = None
    description: Optional[str] = None
    image_front: Optional[str] = None
    image_back: Optional[str] = None


class CoinOut(CoinCreate):
    id: int

    class Config:
        orm_mode = True
