from pydantic import BaseModel

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class cpi(OurBaseModel):
    date: int
    cpi: float

class dxy(OurBaseModel):
    date: int
    dxy: float