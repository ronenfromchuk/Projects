from db_config import Base
from sqlalchemy import Column, UniqueConstraint, BigInteger, Text, ForeignKey
from sqlalchemy.orm import backref, relationship

class Administrators(Base):
    __tablename__ = 'administrators'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    first_name = Column(Text(), nullable=False)
    last_name = Column(Text(), nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    user = relationship("Users", backref=backref("administrators", uselist=False, passive_deletes=True))
    __table_args__= (UniqueConstraint('first_name', 'last_name', name='una_1'),)

    def __repr__(self):
        return f'administrator id={self.id} first name={self.first_name} last name={self.last_name} user id={self.user_id}'

    def __str__(self):
        return f'administrator id={self.id} first name={self.first_name} last name={self.last_name} user id={self.user_id}'