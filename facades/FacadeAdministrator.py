from logger import Logger
from FacadeBase import FacadeBase
from tables.Users import Users
from tables.Customers import Customers
from tables.Administrators import Administrators
from tables.Airline_Companies import AirlineCompanies
from exceptions.ExceptionUserExist import UserAlreadyExists
from exceptions.ExceptionUnvalidToken import InvalidToken
from exceptions.ExceptioWrongInput import InvalidInput
from exceptions.ExceptionShortPassword import WrongPassword
from exceptions.ExceptionAdminNotFound import AdminNotFound
from exceptions.ExceptionAirlineNotFound import AirlineNotFound
from exceptions.ExceptionCustomerNotFound import CustomerNotFound
from exceptions.ExceptionUndefinedUserId import UndefinedUserID

class AdministratorFacade(FacadeBase):

    def __init__(self, repo, config, login_token):
        super().__init__(repo, config)
        self.login_token = login_token
        self.logger = Logger.get_instance()
        self.admin_role_number = self.config["user_roles"]["admin"]
        self.airline_role_number = self.config["user_roles"]["airline"]
        self.customer_role_number = self.config["user_roles"]["customer"]
        self.password_length = self.config["limits"]["password_length"]

    def get_all_customers(self):
        self.logger.logger.debug(f'getting all customers >>>')
        if self.login_token.role != 'Administrator': raise InvalidToken
        else: 
            self.logger.logger.info(f'customers has been displayed!')
            return self.repo.get_all(Customers)

    def add_administrator(self, administrator, user):
        self.logger.logger.debug('adding new administrator >>>')
        if not isinstance(administrator, Administrators): 
            self.logger.logger.error(f'{InvalidInput}, input should be [Administrators] object!')
            raise InvalidInput('input should be [Administrators] object!')
        elif not isinstance(user, Users): 
            self.logger.logger.error(f'{InvalidInput},input user should be [Users] object!')
            raise InvalidInput('input user should be [Users] object!')
        elif self.login_token.role != 'Administrator': raise InvalidToken
        elif self.repo.get_by_id(Users, administrator.user_id) != None: 
            self.logger.logger.error(f'{UserAlreadyExists}, user id=[{administrator.user_id}] is occupied!')
            raise UserAlreadyExists
        elif user.user_role == int(self.admin_role_number): 
            self.create_user(user)
            self.logger.logger.info(f'user=[{user.username}], has been created!')
            self.repo.add(administrator)
            self.logger.logger.info(f'administrator=[{administrator.first_name} {administrator.last_name}], has been created!')
        else: 
            self.logger.logger.error(f'{UndefinedUserID}, wrong ID for Administrator creation!')
            raise UndefinedUserID

    def add_airline(self, airline, user):
        self.logger.logger.debug('adding an airline >>>')
        if not isinstance(airline, AirlineCompanies): 
            self.logger.logger.error(f'{InvalidInput}, airline should be [AirlineCompanies] object!')
            raise InvalidInput('input for airline should be [AirlineCompanies] object!')
        elif not isinstance(user, Users): 
            self.logger.logger.error(f'{InvalidInput}, user should be [Users] object!')
            raise InvalidInput('input for user should be [Users] object!')
        elif self.login_token.role != 'Administrator': raise InvalidToken
        elif self.repo.get_by_id(Users, airline.user_id) != None: 
            self.logger.logger.error(f'{UserAlreadyExists}, user id=[{airline.user_id}], is occupied!')
            raise UserAlreadyExists
        elif user.user_role == int(self.airline_role_number):  
            self.create_user(user)
            self.logger.logger.info(f'user=[{user.username}], has been created!')
            self.repo.add(airline)
            self.logger.logger.info(f'administrator=[{airline.name}], has been created!')
        else: 
            self.logger.logger.error(f'{UndefinedUserID}, wrong USER-ID for "airline" creation!')
            raise UndefinedUserID

    def add_customer(self, customer, user):
        self.logger.logger.debug('adding a customer >>>')
        if not isinstance(customer, Customers): 
            self.logger.logger.error(f'{InvalidInput}, customer should be [Customers] object!')
            raise InvalidInput('input for customer should be [Customers] object!')
        elif not isinstance(user, Users): 
            self.logger.logger.error(f'{InvalidInput}, user should be [Users] object!')
            raise InvalidInput('input for user should be [Users] object!')
        elif self.login_token.role != 'Administrator': raise InvalidToken
        elif self.repo.get_by_id(Users, customer.user_id) != None: 
            self.logger.logger.error(f'{UserAlreadyExists}, user id=[{customer.user_id}], is occupied!')
            raise UserAlreadyExists
        elif len(user.password) < int(self.password_length): 
            self.logger.logger.error(f'{WrongPassword}, your password must be 6 characters at least!')
            raise WrongPassword
        elif user.user_role == int(self.customer_role_number): 
            self.create_user(user)
            self.logger.logger.info(f'user=[{user.username}], has been created!')
            self.repo.add(customer)
            self.logger.logger.info(f'customer=[{customer.first_name} {customer.last_name}], has been created!')
        else: 
            self.logger.logger.error(f'{UndefinedUserID}, wrong ID for "customer" creation!')
            raise UndefinedUserID
    
    def remove_administrator(self, administrator):
        self.logger.logger.debug(f'Removing administrator >>>')
        if not isinstance(administrator, int): raise InvalidInput('input should be integer!')
        elif self.login_token.role != 'Administrator': raise InvalidToken
        admin = self.repo.get_by_id(Administrators, administrator)
        if admin == None: raise AdminNotFound
        else: 
            admin_user_id = admin.user_id
            self.repo.delete_by_id(Administrators, Administrators.id, administrator)
            self.repo.delete_by_id(Users, Users.id, admin_user_id)

    def remove_airline(self, airline):
        self.logger.logger.debug(f'removing airline=[{airline}] >>>')
        if not isinstance(airline, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be integer!')
            raise InvalidInput('input should be integer!')
        elif self.login_token.role != 'Administrator': raise InvalidToken
        airline1 = self.repo.get_by_id(AirlineCompanies, airline)
        if airline1 == None: 
            self.logger.logger.error(f'{AirlineNotFound}airline=[{airline}] wasnt found!')
            raise AirlineNotFound
        else: 
            airline_user_id = airline1.user_id
            self.repo.delete_by_id(AirlineCompanies, AirlineCompanies.id, airline)
            self.logger.logger.info(f'airline=[{airline}], has been deleted!')
            self.repo.delete_by_id(Users, Users.id, airline_user_id)
            self.logger.logger.info(f'user=[{airline_user_id}], has been deleted!')

    def remove_customer(self, customer):
        self.logger.logger.debug(f'removing customer[{customer}] >>>')
        if not isinstance(customer, int): 
            self.logger.logger.error(f'{InvalidInput}, input should be integer!')
            raise InvalidInput('input should be integer!')
        elif self.login_token.role != 'Administrator': raise InvalidToken
        customer1 = self.repo.get_by_id(Customers, customer)
        if customer1 == None: 
            self.logger.logger.error(f'{CustomerNotFound}, customer=[{customer}] wasnt found!')
            raise CustomerNotFound
        else: 
            customer1_user_id = customer1.user_id
            self.repo.delete_by_id(Customers, Customers.id, customer)
            self.logger.logger.info(f'customer=[{customer}], has been deleted!')
            self.repo.delete_by_id(Users, Users.id, customer1_user_id)
            self.logger.logger.info(f'user=[{customer1_user_id}], has been deleted!')


    def __str__(self):
        return f'facade_administrator={self.logger}, token id={self.login_token.id}, name={self.login_token.name}, role={self.login_token.role}'
