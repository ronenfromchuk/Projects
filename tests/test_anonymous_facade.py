import pytest
from db_config import local_session, config
from DbRepo import DbRepo
from facades.FacadeAnonymous import AnonymousFacade
from tables.Customers import Customers
from tables.Users import Users
from exceptions.ExceptionUserExist import UserAlreadyExists
from exceptions.ExceptionShortPassword import WrongPassword
from exceptions.ExceptionUndefinedUserId import UndefinedUserID
from exceptions.ExceptionUserNotFound import UsernameNotFound
from exceptions.ExceptionWrongPassword import WrongPassword
from exceptions.ExceptioWrongInput import InvalidInput

repo = DbRepo(local_session)

@pytest.fixture(scope='session')
def anonymus_facade_object():
    an_facade = AnonymousFacade(repo, config)
    return an_facade

@pytest.fixture(scope='function', autouse=True)
def anonymous_facade_clean():
    repo.reset_db()

def test_login(anonymous_facade_object):
    assert anonymous_facade_object.login('ronen', 'uguessit69') != None

def test_not_login(anonymous_facade_object):
    with pytest.raises(InvalidInput):
        anonymous_facade_object.login('we6682', 87)
    with pytest.raises(InvalidInput):
        anonymous_facade_object.login(533, 'uguessit69')
    with pytest.raises(UsernameNotFound):
        anonymous_facade_object.login('we6682', 'uguessit69')
    with pytest.raises(WrongPassword):
        anonymous_facade_object.login('b0r1s', 'we562')

def test_add_customer(anonymous_facade_object):
    expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
    expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
    anonymous_facade_object.login('testmjackson', 'testjustd01t')
    anonymous_facade_object.add_customer(expected_customer, expected_user)
    check_customer = repo.get_by_id(Customers, 4)
    check_user = repo.get_by_id(Users, 8)
    assert check_customer == expected_customer
    assert check_user == expected_user

def test_not_add_customer(anonymous_facade_object):
    with pytest.raises(InvalidInput):
        expected_customer = "Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)"
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
        anonymous_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(InvalidInput):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        expected_user = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        anonymous_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(UserAlreadyExists):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=3)
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=3)
        anonymous_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(WrongPassword):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
        expected_user = Users(username='testmjackson', password='123', email='testmichael@mcr.com', user_role=3)
        anonymous_facade_object.add_customer(expected_customer, expected_user)
    with pytest.raises(UndefinedUserID):
        expected_customer = Customers(first_name='testmichael', last_name='testjackson', address='London oxford st.', phone_number='test0506666666', credit_card_number='test6806668882', user_id=8)
        expected_user = Users(username='testmjackson', password='testjustd01t', email='testmichael@mcr.com', user_role=1)
        anonymous_facade_object.add_customer(expected_customer, expected_user)