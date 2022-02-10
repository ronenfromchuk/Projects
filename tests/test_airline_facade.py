# DONE
import pytest
from datetime import datetime
from db_config import local_session
from DbRepo import DbRepo
from facades.FacadeAnonymous import anonymousFacade
from Flights import Flights
from Airline_Companies import AirlineCompanies
from exceptions.ExceptionInvalidTime import InvalidTime
from exceptions.ExceptionWrongLocation import InvalidLocation
from exceptions.ExceptionNoMoreTickets import NoMoreTicketsLeft
from exceptions.ExceptionAirlineNotFound import AirlineNotFound
from exceptions.ExceptionFlightNotFound import FlightNotFound
from exceptions.ExceptioWrongInput import InvalidInput

repo = DbRepo(local_session)
anonymous_facade = anonymousFacade(repo)

@pytest.fixture(scope='session')
def airline_facade_object():
    an_facade = anonymousFacade(repo)
    return an_facade.login('d33zn1ts', 'buyaka619')

@pytest.fixture(scope='function', autouse=True)
def airline_facade_clean():
    repo.reset_db()

def test_get_flights_by_airline(airline_facade_object):
    assert airline_facade_object.get_flights_by_airline(2) == repo.get_by_column_value(Flights, Flights.airline_company_id, 2)

def test_not_get_flights_by_airline(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.get_flights_by_airline('e')
    with pytest.raises(AirlineNotFound):
        airline_facade_object.get_flights_by_airline(3)

def test_add_flight(airline_facade_object):
    flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2022, 4, 1, 12, 00, 00), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
    airline_facade_object.add_flight(flight)
    assert repo.get_by_id(Flights, 3) != None

def test_not_add_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        flight = 'Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2023, 1, 4, 10, 10, 10), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)'
        airline_facade_object.add_flight(flight)
    with pytest.raises(InvalidTime):
        flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2023, 1, 4, 10, 10, 10), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
        airline_facade_object.add_flight(flight)
    with pytest.raises(NoMoreTicketsLeft):
        flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=2, departure_time=datetime(2022, 4, 1, 12, 00, 00), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=-44)
        airline_facade_object.add_flight(flight)   
    with pytest.raises(InvalidLocation):
        flight = Flights(airline_company_id=2, origin_country_id=1, destination_country_id=1, departure_time=datetime(2022, 4, 1, 12, 00, 00), landing_time=datetime(2022, 1, 24, 10, 29, 1), remaining_tickets=44)
        airline_facade_object.add_flight(flight)

def test_update_airline(airline_facade_object):
    airline_update = {'name':'Up Yours LTD'}
    airline_facade_object.update_airline(airline_update, 1)
    assert repo.get_by_column_value(AirlineCompanies, AirlineCompanies.name, 'Up Yours LTD') != None

def test_not_update_airline(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_update = "{'name':'Up Yours LTD'}"
        airline_facade_object.update_airline(airline_update, 2)
    with pytest.raises(InvalidInput):
        airline_update = {'name':'Up Yours LTD'}
        airline_facade_object.update_airline(airline_update, 'b')
    with pytest.raises(AirlineNotFound):
        airline_update = {'name':'Up Yours LTD'}
        airline_facade_object.update_airline(airline_update, 33)

def test_update_flight(airline_facade_object):
    flight_update = {'remaining_tickets':12132}
    airline_facade_object.update_flight(flight_update, 1)
    assert repo.get_by_column_value(Flights, Flights.remaining_tickets, 12132) != None

def test_not_update_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.update_flight("{'remaining_tickets':-2}", 1)
    with pytest.raises(InvalidInput):
        airline_facade_object.update_flight({'remaining_tickets':-2}, 'ty')
    with pytest.raises(NoMoreTicketsLeft):
        airline_facade_object.update_flight({'remaining_tickets':-2}, 1)
    with pytest.raises(FlightNotFound):
        airline_facade_object.update_flight({'remaining_tickets':22}, 52)

def test_remove_flight(airline_facade_object):
    airline_facade_object.remove_flight(1)
    assert repo.get_by_id(Flights, 1) == None

def test_not_remove_flight(airline_facade_object):
    with pytest.raises(InvalidInput):
        airline_facade_object.remove_flight('ea')
    with pytest.raises(FlightNotFound):
        airline_facade_object.remove_flight(77)
