from sqlalchemy import Column, Integer, Float
from .database import Base

class cpi(Base):
    __tablename__ = 'cpi'

    date = Column(Integer, primary_key=True, index=True)
    cpi = Column(Float)

    def __repr__(self):
        return f'({self.date}, {self.cpi})\n'

class dxy(Base):
    __tablename__ = 'dxy'

    date = Column(Integer, primary_key=True, index=True)
    dxy = Column(Float)

    def __repr__(self):
        return f'({self.date}, {self.dxy})\n'