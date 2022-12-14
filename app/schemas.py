from pydantic import BaseModel

class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

class cpi(OurBaseModel):
    date: str
    cpi: float

class dxy(OurBaseModel):
    date: int
    dxy: float

class spy(OurBaseModel):
    date: int
    spy: float

class dji(OurBaseModel):
    date: int
    dji: float

class fedfunds(OurBaseModel):
    date: str
    fedfunds: float