import pytest
from db_config import local_session, config
from DbRepo import DbRepo
from facades.FacadeAnonymous import AnonymousFacade
from tables.Tickets import Tickets
from tables.Customers import Customers 
from exceptions.ExceptionNoMoreTickets import NoMoreTicketsLeft
from exceptions.ExceptionFlightNotFound import FlightNotFound
from exceptions.ExceptionCustomerNotFound import CustomerNotFound
from exceptions.ExceptionTicketNotFound import TicketNotFound
from exceptions.ExceptioWrongInput import InvalidInput
from exceptions.ExceptionUnvalidToken import InvalidToken

repo = DbRepo(local_session)

@pytest.fixture(scope='session')
def customer_facade_object():
    an_facade = AnonymousFacade(repo, config)
    return an_facade.login('bibi', 'sarahmalka')

@pytest.fixture(scope='function', autouse=True)
def customer_facade_clean():
    repo.reset_db()

def test_update_customer(customer_facade_object):
    customer_facade_object.update_customer({'first_name': 'Benjamin'}, 1) 
    check_customer = repo.get_by_id(Customers, 1)
    assert check_customer.first_name == 'Benjamin'

def test_not_update_customer(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.update_customer({'first_name': 'Benjamin'}, 'mu')
    with pytest.raises(InvalidInput):
        customer_facade_object.update_customer("{'first_name': 'Benjamin'}", 66)
    with pytest.raises(CustomerNotFound):
        customer_facade_object.update_customer({'first_name': 'Benjamin'}, 66) 
    with pytest.raises(InvalidToken):
        customer_facade_object.update_customer({'first_name': 'Benjamin'}, 2)

def test_add_ticket(customer_facade_object):
    customer_facade_object.add_ticket(Tickets(id=619, flight_id=3, customer_id=1))
    check_ticket = repo.get_by_id(Tickets, 619)
    assert check_ticket.flight_id == 3
    assert check_ticket.customer_id == 3
    
def test_not_add_ticket(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.add_ticket('Tickets(flight_id=3, customer_id=3)')
    with pytest.raises(FlightNotFound):
        customer_facade_object.add_ticket(Tickets(flight_id=3, customer_id=3))
    with pytest.raises(NoMoreTicketsLeft):
        customer_facade_object.add_ticket(Tickets(flight_id=1, customer_id=1))

def test_remove_ticket(customer_facade_object):
    customer_facade_object.remove_ticket(3)
    check_customer = repo.get_by_id(Tickets, 3)
    assert check_customer == None

def test_not_remove_ticket(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.remove_ticket({'66':'7'})
    with pytest.raises(TicketNotFound):
        customer_facade_object.remove_ticket(66)
    with pytest.raises(InvalidToken):
        customer_facade_object.remove_ticket(2)

def test_get_ticket_by_customer(customer_facade_object):
    assert repo.get_by_column_value(Tickets, Tickets.customer_id, 1) == customer_facade_object.get_ticket_by_customer(1)

def test_not_get_ticket_by_customer(customer_facade_object):
    with pytest.raises(InvalidInput):
        customer_facade_object.get_ticket_by_customer('7')
    with pytest.raises(CustomerNotFound):
        customer_facade_object.get_ticket_by_customer(7)
    with pytest.raises(InvalidToken):
        customer_facade_object.get_ticket_by_customer(1)
