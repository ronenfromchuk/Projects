import pytest
from db_config import local_session, config
from DbRepo import DbRepo
from facades.FacadeAnonymous import AnonymousFacade
from tables.Airline_Companies import AirlineCompanies
from tables.Customers import Customers
from tables.Users import Users
from tables.Administrators import Administrators 
from exceptions.ExceptionUserExist import UserAlreadyExists
from exceptions.ExceptionWrongPassword import WrongPassword
from exceptions.ExceptionUndefinedUserId import UndefinedUserID
from exceptions.ExceptionAdminNotFound import AdminNotFound
from exceptions.ExceptionAirlineNotFound import AirlineNotFound
from exceptions.ExceptionCustomerNotFound import CustomerNotFound
from exceptions.ExceptioWrongInput import InvalidInput

repo = DbRepo(local_session)

@pytest.fixture(scope='session')
def admin_facade_object():
    an_facade = AnonymousFacade(repo, config)
    return an_facade.login('ronen', 'uguessit69')

@pytest.fixture(scope='function', autouse=True)
def admin_facade_clean():
    repo.reset_db()

def get_all_customers(admin_facade_object):
    assert admin_facade_object.get_all_customers() == repo.get_all(Customers)

def test_add_administrator(admin_facade_object):
    expected_admin = Administrators(first_name='testronen', last_name='testfromchuk', user_id=8)
    expected_user = Users(username='testr0nen', password='testuguessit69', email='testronen@mcr.com', user_role=1)
    admin_facade_object.add_administrator(expected_admin, expected_user)
    check_admin = repo.get_by_id(Administrators, 3)
    check_user = repo.get_by_id(Users, 8)
    assert check_admin == expected_admin
    assert check_user == expected_user

def test_not_add_administrator(admin_facade_object):
    with pytest.raises(InvalidInput):
        expected_admin = Administrators(first_name='testronen', last_name='testfromchuk', user_id=3)
        expected_user = "Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=1)"
        admin_facade_object.add_administrator(expected_admin, expected_user)
    with pytest.raises(InvalidInput):
        expected_admin = "Administrators(first_name='testronen', last_name='testfromchuk', user_id=3)"
        expected_user = Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=1)
        admin_facade_object.add_administrator(expected_admin, expected_user)
    with pytest.raises(UserAlreadyExists):
        expected_admin = Administrators(first_name='testronen', last_name='testfromchuk', user_id=3)
        expected_user = Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=1)
        admin_facade_object.add_administrator(expected_admin, expected_user)
    with pytest.raises(WrongPassword):
        expected_admin = Administrators(first_name='testlior', last_name='testfromchuk', user_id=8)
        expected_user = Users(username='testr0nen', password='666', email='testronen@mcr.com', user_role=1)
        admin_facade_object.add_administrator(expected_admin, expected_user)
    with pytest.raises(UndefinedUserID):
        expected_admin = Administrators(first_name='testlior', last_name='testfromchuk', user_id=8)
        expected_user = Users(username='testr0nen', password='123123', email='testronen@mcr.com', user_role=3)
        admin_facade_object.add_administrator(expected_admin, expected_user)

def test_add_airline(admin_facade_object):
    expected_airline = AirlineCompanies(name='testel-al', country_id=1, user_id=8)
    expected_user = Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=2)
    admin_facade_object.add_airline(expected_airline, expected_user)
    check_airline = repo.get_by_id(AirlineCompanies, 3)
    check_user = repo.get_by_id(Users, 8)
    assert check_airline == expected_airline
    assert check_user == expected_user

def test_not_add_airline(admin_facade_object):
    with pytest.raises(InvalidInput):
        expected_airline = AirlineCompanies(name='testel-al', country_id=1, user_id=2)
        expected_user = "Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=2)"
        admin_facade_object.add_airline(expected_airline, expected_user)
    with pytest.raises(InvalidInput):
        expected_airline = "AirlineCompanies(name='testel-al', country_id=1, user_id=2)"
        expected_user = Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=2)
        admin_facade_object.add_airline(expected_airline, expected_user)
    with pytest.raises(UserAlreadyExists):
        expected_airline = AirlineCompanies(name='testel-al', country_id=1, user_id=2)
        expected_user = Users(username='testr0nen', password='11111111', email='testronen@mcr.com', user_role=2)
        admin_facade_object.add_airline(expected_airline, expected_user)
    with pytest.raises(WrongPassword):
        expected_airline = AirlineCompanies(name='testel-al', country_id=1, user_id=3)
        expected_user = Users(username='testr0nen', password='123', email='testronen@mcr.com', user_role=2)
        admin_facade_object.add_airline(expected_airline, expected_user)
    with pytest.raises(UndefinedUserID):
        expected_airline = AirlineCompanies(name='testel-al', country_id=1, user_id=3)
        expected_user = Users(username='testr0nen', password='132232', email='testronen@mcr.com', user_role=1)
        admin_facade_object.add_airline(expected_airline, expected_user)

def test_add_customer(admin_facade_object):
    expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=7)
    expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
    admin_facade_object.add_customer(expected_customer, expected_user)
    check_customer = repo.get_by_id(Customers, 4)
    check_user = repo.get_by_id(Users, 8)
    assert check_customer == expected_customer
    assert check_user == expected_user

def test_not_add_customer(admin_facade_object):
    with pytest.raises(InvalidInput):
        expected_customer = "Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)"
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
        admin_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(InvalidInput):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        expected_user = "Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)"
        admin_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(UserAlreadyExists):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
        admin_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(WrongPassword):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
        expected_user = Users(username='testmjackson', password='123', email='testmichael@mcr.com', user_role=3)
        admin_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(UndefinedUserID):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=1)
        admin_facade_object.add_customer(expected_customer, expected_user)
    
def test_remove_administrator(admin_facade_object):
    admin_facade_object.remove_administrator(1)
    assert repo.get_by_id(Administrators, 1) == None
    assert repo.get_by_id(Users, 3) == None

def test_not_remove_administrator(admin_facade_object):
    with pytest.raises(InvalidInput):
        admin_facade_object.remove_administrator('3')
    with pytest.raises(AdminNotFound):
        admin_facade_object.remove_administrator(3)

def test_remove_airline(admin_facade_object):
    expected_airline = AirlineCompanies(name='testel-al', country_id=1, user_id=8)
    expected_user = Users(username='testr0nen', password='11111111', email='ronen@mcr.com', user_role=1)
    admin_facade_object.add_airline(expected_airline, expected_user)
    admin_facade_object.remove_airline(3)
    assert repo.get_by_id(AirlineCompanies, 3) == None
    assert repo.get_by_id(Users, 8) == None

def test_not_remove_airline(admin_facade_object):
    with pytest.raises(InvalidInput):
        admin_facade_object.remove_airline('3')
    with pytest.raises(AirlineNotFound):
        admin_facade_object.remove_airline(3)

def test_remove_customer(admin_facade_object):
    expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
    expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
    admin_facade_object.add_customer(expected_customer, expected_user)
    admin_facade_object.remove_customer(4)
    assert repo.get_by_id(Customers, 4) == None
    assert repo.get_by_id(Users, 8) == None

def test_not_remove_customer(admin_facade_object):
    with pytest.raises(InvalidInput):
        admin_facade_object.remove_customer('4')
    with pytest.raises(CustomerNotFound):
        admin_facade_object.remove_customer(4)