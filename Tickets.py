from db_config import Base
from sqlalchemy import Column, UniqueConstraint, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

class Tickets(Base):
    __tablename__ = 'tickets'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    flight_id = Column(BigInteger(), ForeignKey('flights.id', ondelete='CASCADE'), nullable=False)
    customer_id = Column(BigInteger(), ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)
    __table_args__= (UniqueConstraint('flight_id', 'customer_id', name='una_3'),)
    flights = relationship('Flights', backref=backref('tickets', uselist=True, passive_deletes=True))
    customers = relationship('Customers', backref=backref('tickets', uselist=True, passive_deletes=True))

    def __repr__(self):
        return f'ticket id={self.id} flight id={self.flight_id} customer id={self.customer_id}'

    def __str__(self):
        return f'ticket id={self.id} flight id={self.flight_id} customer id={self.customer_id}'