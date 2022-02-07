from db_config import Base
from sqlalchemy import Column, BigInteger, Text

class Countries(Base):
    __tablename__ = 'countries'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False, unique=True)

    def __repr__(self):
        return f'country id={self.id} name={self.name}'

    def __str__(self):
        return f'country id={self.id} name={self.name}>'