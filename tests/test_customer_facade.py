# DONE
import pytest
from db_config import local_session
from DbRepo import DbRepo
from FacadeAnonymous import AnonymusFacade
from Tickets import Tickets
from Customers import Customers 
from ExceptionNoMoreTickets import NoMoreTicketsLeft
from ExceptionFlightNotFound import FlightNotFound
from ExceptionCustomerNotFound import CustomerNotFound
from ExceptionTicketNotFound import TicketNotFound
from ExceptioWrongInput import InvalidInput

repo = DbRepo(local_session)
anonymus_facade = AnonymusFacade(repo)

@pytest.fixture(scope='session')
def customer_facade_object():
    an_facade = AnonymusFacade(repo)
    return an_facade.login('bibi', 'sarahmalka')

@pytest.fixture(scope='function', autouse=True)
def customer_facade_clean():
    repo.reset_db()

def test_update_customer(customer_facade_object):
    customer_facade_object.update_customer({'first_name': 'Benjamin'}, 1) 
    assert repo.get_by_column_value(Customers, Customers.first_name, 'Benjamin') != None

def test_not_update_customer(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.update_customer({'first_name': 'Benjamin'}, 'mu')
    with pytest.raises(InvalidInput):
        customer_facade_object.update_customer("{'first_name': 'Benjamin'}", 66)
    with pytest.raises(CustomerNotFound):
        customer_facade_object.update_customer({'first_name': 'Samuel'}, 55) 
    
def test_add_ticket(customer_facade_object):
    customer_facade_object.add_ticket(Tickets(id=619, flight_id=3, customer_id=1))
    assert repo.get_by_id(Tickets, 619) != None
    
def test_not_add_ticket(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.add_ticket('Tickets(flight_id=3, customer_id=3)')
    with pytest.raises(FlightNotFound):
        customer_facade_object.add_ticket(Tickets(flight_id=3, customer_id=3))
    with pytest.raises(NoMoreTicketsLeft):
        customer_facade_object.add_ticket(Tickets(flight_id=1, customer_id=1))

def test_remove_ticket(customer_facade_object):
    customer_facade_object.remove_ticket(3)
    assert repo.get_by_id(Tickets, 3) == None

def test_not_remove_ticket(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.remove_ticket({'66':'7'})
    with pytest.raises(TicketNotFound):
        customer_facade_object.remove_ticket(66)

def test_get_ticket_by_customer(customer_facade_object):
    assert repo.get_by_column_value(Tickets, Tickets.customer_id, 1) == customer_facade_object.get_ticket_by_customer(1)

def test_not_get_ticket_by_customer(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.get_ticket_by_customer('7')
    with pytest.raises(CustomerNotFound):
        customer_facade_object.get_ticket_by_customer(7)
