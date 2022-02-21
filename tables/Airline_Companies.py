from sqlalchemy.orm import backref, relationship
from db_config import Base
from sqlalchemy import Column, BigInteger, Text, ForeignKey

class AirlineCompanies(Base):
    __tablename__ = 'airline_companies'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    name = Column(Text(), nullable=False, unique=True)
    country_id = Column(BigInteger(), ForeignKey('countries.id', ondelete='CASCADE'), unique=False, nullable=False)
    user_id = Column(BigInteger(), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    country = relationship("Countries", backref=backref("airline_companies", uselist=True, passive_deletes=True))
    user = relationship("Users", backref=backref("airline_companies", uselist=False, passive_deletes=True))

    def __repr__(self):
        return f'airline company id={self.id} name={self.name} country id={self.country_id} user id={self.user_id}'

    def __str__(self):
        return f'airline company id={self.id} name={self.name} country id={self.country_id} user id={self.user_id}'