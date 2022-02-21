from sqlalchemy.orm import backref, relationship
from db_config import Base
from sqlalchemy import Column, Integer, DateTime, BigInteger, ForeignKey

class Flights(Base):
    __tablename__ = 'flights'

    id = Column(BigInteger(), primary_key=True, autoincrement=True)
    airline_company_id = Column(BigInteger(), ForeignKey('airline_companies.id', ondelete='CASCADE'), nullable=False)
    origin_country_id = Column(BigInteger(), ForeignKey('countries.id', ondelete='CASCADE'), unique=False, nullable=False)
    destination_country_id = Column(BigInteger(), ForeignKey('countries.id', ondelete='CASCADE'), unique=False, nullable=False)
    departure_time = Column(DateTime(), unique=False, nullable=False)
    landing_time = Column(DateTime(), unique=False, nullable=False)
    remaining_tickets= Column(Integer())
    company = relationship("AirlineCompanies", backref=backref("flights", uselist=True, passive_deletes=True))
    origin = relationship("Countries", foreign_keys = [origin_country_id], uselist=True, passive_deletes=True)
    destination = relationship("Countries", foreign_keys = [destination_country_id] , uselist=True, passive_deletes=True)

    def __repr__(self):
        return f'flight id={self.id} airline company id={self.airline_company_id} origin country id={self.origin_country_id} desitnation country id={self.destination_country_id} departure time={self.departure_time} landing time={self.landing_time} remaining tickets={self.remaining_tickets}'

    def __str__(self):
        return f'flight id={self.id} airline company id={self.airline_company_id} origin country id={self.origin_country_id} desitnation country id={self.destination_country_id} departure time={self.departure_time} landing time={self.landing_time} remaining tickets={self.remaining_tickets}'
