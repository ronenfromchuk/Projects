from sqlalchemy.orm import backref, relationship
from db_config import Base
from sqlalchemy import Column, Integer, BigInteger, Text, ForeignKey

class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    username = Column(Text(), nullable=False, unique=True)
    password = Column(Text(), nullable=False)
    email = Column(Text(), nullable=False, unique=True)

    def __repr__(self):
        return f'user id={self.id} username={self.username} password={self.password} email={self.email}'

    def __str__(self):
        return f'user id={self.id} username={self.username} password={self.password} email={self.email}'