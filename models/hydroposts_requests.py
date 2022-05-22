from pydantic import BaseModel, EmailStr, validator
from fastapi import HTTPException
import re

class CreateHydropostRequest(BaseModel):
    id: int
    region: str
    river: str
    latitude: float
    longitude: float
