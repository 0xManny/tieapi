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

class spy(Base):
    __tablename__ = 'spy'

    date = Column(Integer, primary_key=True, index=True)
    spy = Column(Float)

    def __repr__(self):
        return f'({self.date}, {self.spy})\n'

class dji(Base):
    __tablename__ = 'dji'

    date = Column(Integer, primary_key=True, index=True)
    dji = Column(Float)

    def __repr__(self):
        return f'({self.date}, {self.dji})\n'

class fedfunds(Base):
    __tablename__ = 'fedfunds'

    date = Column(Integer, primary_key=True, index=True)
    fedfunds = Column(Float)

    def __repr__(self):
        return f'({self.date}, {self.fedfunds})\n'