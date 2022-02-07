# DONE
import pytest
from datetime import datetime
from db_config import local_session
from DbRepo import DbRepo
from FacadeAnonymous import AnonymusFacade
from Flights import Flights
from Airline_Companies import AirlineCompanies
from ExceptionInvalidTime import InvalidTime
from ExceptionWrongLocation import InvalidLocation
from ExceptionNoMoreTickets import NoMoreTicketsLeft
from ExceptionAirlineNotFound import AirlineNotFound
from ExceptionFlightNotFound import FlightNotFound
from ExceptioWrongInput import InvalidInput

repo = DbRepo(local_session)
anonymus_facade = AnonymusFacade(repo)

@pytest.fixture(scope='session')
def airline_facade_object():
    an_facade = AnonymusFacade(repo)
    return an_facade.login('d33zn1ts', 'buyaka619')

@pytest.fixture(scope='function', autouse=True)
def airline_facade_clean():
    repo.reset_db()

def test_get_flights_by_airline(airline_facade_object):
    assert airline_facade_object.get_flights_by_airline(1) == repo.get_by_column_value(Flights, Flights.airline_company_id, 1)

def test_not_get_flights_by_airline(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.get_flights_by_airline('e')
    with pytest.raises(AirlineNotFound):
        airline_facade_object.get_flights_by_airline(2)

def test_add_flight(airline_facade_object):
    flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2022, 4, 1, 12, 00, 00), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
    airline_facade_object.add_flight(flight)
    assert repo.get_by_id(Flights, 3) != None

def test_not_add_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        flight = 'Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2027, 1, 3, 10, 10, 10), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)'
        airline_facade_object.add_flight(flight)
    with pytest.raises(InvalidTime):
        flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2026, 1, 2, 10, 10, 10), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
        airline_facade_object.add_flight(flight)
    with pytest.raises(NoMoreTicketsLeft):
        flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2025, 2, 2, 12, 00, 00), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=-44)
        airline_facade_object.add_flight(flight)   
    with pytest.raises(InvalidLocation):
        flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=1, departure_time=datetime(2024, 3, 2, 12, 00, 00), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
        airline_facade_object.add_flight(flight)

def test_update_airline(airline_facade_object):
    airline_update = {'name':'DEEZ NUTS'}
    airline_facade_object.update_airline(airline_update, 1)
    assert repo.get_by_column_value(AirlineCompanies, AirlineCompanies.name, 'EEZ NUTS') != None

def test_not_update_airline(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_update = "{'name':'EEZ NUTS'}"
        airline_facade_object.update_airline(airline_update, 1)
    with pytest.raises(InvalidInput):
        airline_update = {'name':'EEZ NUTS'}
        airline_facade_object.update_airline(airline_update, 'c')
    with pytest.raises(AirlineNotFound):
        airline_update = {'name':'EEZ NUTS'}
        airline_facade_object.update_airline(airline_update, 21)

def test_update_flight(airline_facade_object):
    flight_update = {'remaining_tickets':12132}
    airline_facade_object.update_flight(flight_update, 1)
    assert repo.get_by_column_value(Flights, Flights.remaining_tickets, 12132) != None

def test_not_update_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.update_flight("{'remaining_tickets':0}", 1)
    with pytest.raises(InvalidInput):
        airline_facade_object.update_flight({'remaining_tickets':-2}, 'np')
    with pytest.raises(NoMoreTicketsLeft):
        airline_facade_object.update_flight({'remaining_tickets':21}, 2)
    with pytest.raises(FlightNotFound):
        airline_facade_object.update_flight({'remaining_tickets':2}, 33)

def test_remove_flight(airline_facade_object):
    airline_facade_object.remove_flight(1)
    assert repo.get_by_id(Flights, 1) == None

def test_not_remove_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.remove_flight('na')
    with pytest.raises(FlightNotFound):
        airline_facade_object.remove_flight(77)
