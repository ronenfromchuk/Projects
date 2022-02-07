# DONE
import pytest
from db_config import local_session
from DbRepo import DbRepo
from FacadeAnonymous import AnonymusFacade
from Customers import Customers
from Users import Users
from ExceptionUserExist import UserAlreadyExists
from ExceptionShortPassword import WrongPassword
from ExceptionUndefinedUserId import UndefinedUserID
from ExceptionUserNotFound import UsernameNotFound
from ExceptionWrongPassword import WrongPassword
from ExceptioWrongInput import InvalidInput

repo = DbRepo(local_session)
anonymus_facade = AnonymusFacade(repo)

@pytest.fixture(scope='session')
def anonymus_facade_object():
    an_facade = anonymus_facade
    return an_facade

@pytest.fixture(scope='function', autouse=True)
def anonymus_facade_clean():
    repo.reset_db()

def test_login(anonymus_facade_object):
    assert anonymus_facade_object.login('ronen', 'uguessit69') != None

def test_not_login(anonymus_facade_object):
    with pytest.raises(InvalidInput):
        anonymus_facade_object.login('we6682', 87)
    with pytest.raises(InvalidInput):
        anonymus_facade_object.login(533, 'uguessit69')
    with pytest.raises(UsernameNotFound):
        anonymus_facade_object.login('we6682', 'uguessit69')
    with pytest.raises(WrongPassword):
        anonymus_facade_object.login('b0r1s', 'we562')

def test_add_customer(anonymus_facade_object):
    expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
    expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
    anonymus_facade_object.add_customer(expected_customer, expected_user)
    assert repo.get_by_column_value(Customers, Customers.first_name, 'testmichael') != None
    assert repo.get_by_column_value(Users, Users.username, 'testmjackson') != None

def test_not_add_customer(anonymus_facade_object):
    with pytest.raises(InvalidInput):
        expected_customer = "Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)"
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
        anonymus_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(InvalidInput):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        expected_user = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        anonymus_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(UserAlreadyExists):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
        anonymus_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(WrongPassword):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
        expected_user = Users(username='testmjackson', password='123', email='testmichael@mcr.com', user_role=3)
        anonymus_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(UndefinedUserID):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=1)
        anonymus_facade_object.add_customer(expected_customer, expected_user)