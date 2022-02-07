# DONE
from Users import Users
from logger import Logger
from Customers import Customers
from login_token import LoginToken
from FacadeBase import FacadeBase
from FacadeAirline import AirlineFacade
from FacadeCustomer import CustomerFacade
from FacadeAdministrator import AdministratorFacade
from ExceptionUserExist import UserAlreadyExists
from ExceptioWrongInput import InvalidInput
from ExceptionUserNotFound import UsernameNotFound
from ExceptionShortPassword import WrongPassword
from ExceptionWrongPassword import WrongPassword
from ExceptionInvalidUserRole import InvalidUserRole
from ExceptionUndefinedUserId import UndefinedUserID

class AnonymusFacade(FacadeBase):

    def __init__(self, repo):
        super().__init__(repo)
        self.logger = Logger.get_instance()

    def login(self, username, password):
        self.logger.logger.debug('logging in >>>')
        if not isinstance(username, str):
            self.logger.logger.error(f'{InvalidInput}, username should be string!')
            raise InvalidInput('username should be string!')
        elif not isinstance(password, str): 
            self.logger.logger.error(f'{InvalidInput}, password should be string!')
            raise InvalidInput('password should be string!')
        user = self.repo.get_by_column_value(Users, Users.username, username)
        if not self.repo.get_by_column_value(Users, Users.username, username):
            self.logger.logger.error(f'{UsernameNotFound}, user=[{username}], not found!')
            raise UsernameNotFound(f'user=[{username}], not found!')
        elif not self.repo.get_by_column_value(Users, Users.password, password): 
            self.logger.logger.error(f'{WrongPassword}, wrong password for use[{username}]')
            raise WrongPassword(f'wrong password!, user=[{username}]')
        else:
            if user[0].user_role == 1: 
                self.logger.logger.info(f'Hello admin!, {user[0].username}')
                return AdministratorFacade(self.repo, LoginToken(id=user[0].administrators.id, name=user[0].administrators.first_name, role='Administrator'))
            elif user[0].user_role == 2: 
                self.logger.logger.info(f'Hello airline!, {user[0].username}')
                return AirlineFacade(self.repo, LoginToken(id=user[0].airline_companies.id, name=user[0].airline_companies.name, role='Airline'))
            elif user[0].user_role == 3: 
                self.logger.logger.info(f'Hello customer!, {user[0].username}')
                return CustomerFacade(self.repo, LoginToken(id=user[0].customers.id, name=user[0].customers.first_name, role='Customer'))
            else: 
                self.logger.logger.error(f'{InvalidUserRole}, wrong user role provided! user=[{user[0].username}]')
                raise InvalidUserRole

    def add_customer(self, customer, user):
        self.logger.logger.debug('adding a new customer >>>')
        if not isinstance(customer, Customers): 
            self.logger.logger.error(f'{InvalidInput}, customer should be [Customers] obj!')
            raise InvalidInput('customer should be [Customers] object!')
        elif not isinstance(user, Users): 
            self.logger.logger.error(f'{InvalidInput}, user should be [Users] obj!')
            raise InvalidInput('user should be [Users] object!')
        elif self.repo.get_by_id(Users, customer.user_id) != None: 
            self.logger.logger.error(f'{UserAlreadyExists}, user-id=[{customer.user_id}], is occupied!')
            raise UserAlreadyExists(f'user-id=[{customer.user_id}], is occupied!')
        elif len(user.password) < 6: 
            self.logger.logger.error(f'{WrongPassword}, password must be at least 6 characters!')
            raise WrongPassword
        elif user.user_role == 3: 
            super().create_user(user)
            self.logger.logger.info(f'user=[{user.username}], has been created!')
            self.repo.add(customer)
            self.logger.logger.info(f'customer=[{customer.first_name} {customer.last_name}], has been created!')
        else: 
            self.logger.logger.error(f'{UndefinedUserID}, wrong ID for customer creation!')
            raise UndefinedUserID

    def __str__(self):
        return f'{super().__init__}'