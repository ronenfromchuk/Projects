# DONE
import pytest
from Countries import Countries
from db_config import local_session
from DbRepo import DbRepo
from datetime import datetime
from facades.FacadeAnonymous import anonymousFacade
from Airline_Companies import AirlineCompanies
from Customers import Customers
from Users import Users
from Flights import Flights
from Administrators import Administrators 
from exceptions.ExceptionUserExist import UserAlreadyExists
from exceptions.ExceptionShortPassword import WrongPassword
from exceptions.ExceptionUndefinedUserId import UndefinedUserID
from exceptions.ExceptionAdminNotFound import AdminNotFound
from exceptions.ExceptionAirlineNotFound import AirlineNotFound
from exceptions.ExceptionCustomerNotFound import CustomerNotFound
from exceptions.ExceptioWrongInput import InvalidInput
from exceptions.ExceptionFlightNotFound import FlightNotFound
from exceptions.ExceptionWrongCountry import InvalidCountry

repo = DbRepo(local_session)
anonymous_facade = anonymousFacade(repo)

@pytest.fixture(scope='session')
def base_facade_object():
    an_facade = anonymous_facade
    return an_facade

@pytest.fixture(scope='function', autouse=True)
def anonymous_facade_clean():
    repo.reset_db()

def test_get_all_flights(base_facade_object):
    assert base_facade_object.get_all_flights() == repo.get_all(Flights)

def test_get_flight_by_id(base_facade_object):
    assert base_facade_object.get_flight_by_id(1) == repo.get_by_id(Flights,1)

def test_not_get_flight_by_id(base_facade_object):
    with pytest.raises(InvalidInput):
        base_facade_object.get_flight_by_id('1')
    with pytest.raises(FlightNotFound):
        base_facade_object.get_flight_by_id(888)

def test_get_flights_by_parameters(base_facade_object):
    sample = base_facade_object.get_flights_by_parameters(1,2,datetime(2022, 4, 1, 12, 00, 00))
    expected = repo.get_by_condition(Flights, lambda query: query.filter(Flights.origin_country_id == 1, Flights.destination_country_id == 2, Flights.departure_time == datetime(2022, 4, 1, 12, 00, 00)))
    assert expected == sample

def test_not_get_flights_by_parameters(base_facade_object):
    with pytest.raises(InvalidInput):
        base_facade_object.get_flights_by_parameters('3',2,datetime(2022, 4, 1, 12, 00, 00))
    with pytest.raises(InvalidInput):
        base_facade_object.get_flights_by_parameters(3,'2',datetime(2022, 4, 1, 12, 00, 00))
    with pytest.raises(InvalidInput):
        base_facade_object.get_flights_by_parameters(1,2,'datetime(2022, 4, 1, 12, 00, 00)')
    with pytest.raises(FlightNotFound):
        base_facade_object.get_flights_by_parameters(3,1,datetime(2022, 4, 1, 12, 00, 00))

def test_get_all_airlines(base_facade_object):
    assert base_facade_object.get_all_airlines() == repo. get_all(AirlineCompanies)

def test_get_airline_by_id(base_facade_object):
    assert base_facade_object.get_airline_by_id(1) == repo.get_by_id(AirlineCompanies, 1)

def test_not_get_airline_by_id(base_facade_object):
    with pytest.raises(InvalidInput):
        base_facade_object.get_airline_by_id('1')
    with pytest.raises(AirlineNotFound):
        base_facade_object.get_airline_by_id(123)

def test_get_all_countries(base_facade_object):
    assert base_facade_object.get_all_countries() == repo. get_all(Countries)

def test_get_country_by_id(base_facade_object):
    assert base_facade_object.get_country_by_id(1) == repo.get_by_id(Countries, 1)

def test_not_get_country_by_id(base_facade_object):
    with pytest.raises(InvalidInput):
        base_facade_object.get_country_by_id('1')
    with pytest.raises(InvalidCountry):
        base_facade_object.get_country_by_id(123)

def test_create_user(base_facade_object):
    base_facade_object.create_user(Users(username='cristi7no', password='siuuuuuu', email='cr7@mcr.com', user_role=3))
    assert repo.get_by_column_value(Users, Users.username, 'cristi7no') != None

def test_not_create_user(base_facade_object):
    with pytest.raises(InvalidInput):
        base_facade_object.create_user('3')
    with pytest.raises(WrongPassword):
        base_facade_object.create_user(Users(username='cristi7no', password='7777777', email='siuuu@mcr.com', user_role=3))
