from logger import Logger
from datetime import datetime
from sqlalchemy import asc
from Users import Users
from Flights import Flights
from Tickets import Tickets
from Customers import Customers
from Countries import Countries
from User_Roles import UserRoles
from Administrators import Administrators
from Airline_Companies import AirlineCompanies


class DbRepo:
    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = Logger.get_instance()

    def get_all(self, table_class):
        return self.local_session.query(table_class).all()

    def get_all_limit(self, table_class, limit_num):
        return self.local_session.query(table_class).limit(limit_num).all()

    def get_all_order_by(self, table_class, column_name, direction=asc):
        return self.local_session.query(table_class).order_by(direction(column_name)).all()

    def get_by_column_value(self, table_class, column_name, value):
        return self.local_session.query(table_class).filter(column_name == value).all()

    def get_by_id(self, table_class, id):
        return self.local_session.get(table_class,id)

    def get_by_condition(self, table_class, cond):
        return cond(self.local_session.query(table_class)).all()

    def get_by_ilike(self,table_class, column_name, exp):
        return self.local_session.query(table_class).filter(column_name.ilike(exp)).all()

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()
        print('row has been added!')

    def add_all(self, rows_list):
        self.local_session.add_all(rows_list)
        self.local_session.commit()
        print('rows list added!')

    def delete_by_id(self, table_class, id_column_name, id):
        self.local_session.query(table_class).filter(id_column_name == id).delete(synchronize_session=False)
        self.local_session.commit()
        self.logger.logger.warning(f'deleting from table {table_class}.')
        print(f'deleted by id={id}')

    def delete_table(self, table_name):
        self.logger.logger.warning(f'deleting table {table_name}.')
        self.local_session.execute(f'drop TABLE if exists {table_name} cascade')
        self.local_session.commit()
        print(f'table={table_name}, has been deleted')

    def delete_all_tables(self):
        self.logger.logger.warning('deleting all the tables >>>')
        self.delete_table('airline_companies')
        self.delete_table('administrators')
        self.delete_table('customers')
        self.delete_table('users')
        self.delete_table('user_roles')
        self.delete_table('countries')
        self.delete_table('flights')
        self.delete_table('tickets')


    def update_by_id(self, table_class, id_column_name, id, data):
        self.local_session.query(table_class).filter(id_column_name == id).update(data)
        self.local_session.commit()
        print(f'updated by id={id}')

    def reset_auto_inc(self, table_class):
        self.local_session.execute(f'TRUNCATE TABLE {table_class.__tablename__} RESTART IDENTITY CASCADE')

    def create_all_sp(self, file):
            try:
                with open(file, 'r') as sp_file:
                    queries = sp_file.read().split('---')
                for query in queries:
                    self.local_session.execute(query)
                self.local_session.commit()
                self.logger.logger.debug(f'all SP were created!, from file=[{file}]')
            except FileNotFoundError:
                self.logger.logger.critical(f'file=[{file}] wasnt found')

    def reset_db(self):
        self.reset_auto_inc(Countries)
        self.reset_auto_inc(Users)
        self.reset_auto_inc(AirlineCompanies)
        self.reset_auto_inc(Customers)
        self.reset_auto_inc(Flights)
        self.reset_auto_inc(Tickets)
        self.reset_auto_inc(Administrators)
        self.reset_auto_inc(UserRoles)
        self.add_all([  Countries(name='israel'),Countries(name='england'),
                        Countries(name='thailand'),Countries(name='jamaica'),
                        Countries(name='norway'),Countries(name='ukraine'),])
        self.add_all([  UserRoles(role_name='administrator'),
                        UserRoles(role_name='airline company'),
                        UserRoles(role_name='customer')])
        self.add_all([  Users(username='ronen', password='uguessit69', email='ronen@mcr.com', user_role=1),       #1 ---> user_id
                        Users(username='bbntyahho', password='case10000', email='bbn@mcr.com', user_role=1),      #2 ---> user_id
                        Users(username='jesse', password='jlingz14', email='jesse@mcr.com', user_role=2),         #3 ---> user_id # airline
                        Users(username='paulpogba', password='pp666666', email='pp6@mcr.com', user_role=2),       #4 ---> user_id # airline
                        Users(username='jadon25', password='jsancho25', email='jadon@mcr.com', user_role=3),      #5 ---> user_id
                        Users(username='l0llel', password='trolllel123', email='troll@mcr.com', user_role=3),     #6 ---> user_id
                        Users(username='ajoshua', password='aj2022', email='anthony@mcr.com', user_role=3),       #7 ---> user_id
                        Users(username='tonyparker', password='tp1999', email='tonyp@mcr.com', user_role=3),      #8 ---> user_id
                        Users(username='andyc0l3', password='ac1999', email='andyc0le@mcr.com', user_role=3),     #9 ---> user_id
                        Users(username='mjackson', password='justd01t', email='mjackson@mcr.com', user_role=3)])  #10 --> user_id
        self.add_all([  AirlineCompanies(name='el-al', country_id=1, user_id=1),
                        AirlineCompanies(name='british airways', country_id=2, user_id=2)])
        self.add_all([  Administrators(first_name='ronen', last_name='fromchuk', user_id=1),
                        Administrators(first_name='jadon', last_name='sancho', user_id=5)])
        self.add_all([  Customers(first_name='anthony', last_name='parker', address='ny 11 st.', phone_number='011111111', credit_card_number='6809002442', user_id=5),
                        Customers(first_name='andy', last_name='cole', address='manchester m4a1', phone_number='0161777777', credit_card_number='6807008882', user_id=6),
                        Customers(first_name='michael', last_name='jackson', address='London oxford st.', phone_number='0506666666', credit_card_number='6806668882', user_id=7)])
        self.add_all([  Flights(airline_company_id=1, origin_country_id=1, destination_country_id=2, departure_time=datetime(2022, 4, 1, 12, 00, 00), landing_time=datetime(2022, 4, 1, 15, 30, 0), remaining_tickets=3),
                        Flights(airline_company_id=2, origin_country_id=2, destination_country_id=1, departure_time=datetime(2022, 5, 1, 10, 1, 1), landing_time=datetime(2022, 5, 1, 23, 0, 1), remaining_tickets=1),
                        Flights(airline_company_id=2, origin_country_id=3, destination_country_id=2, departure_time=datetime(2022, 6, 1, 15, 00, 00), landing_time=datetime(2022, 6, 1, 20, 0, 0), remaining_tickets=10)])
        self.add_all([  Tickets(flight_id=1, customer_id=1),
                        Tickets(flight_id=2, customer_id=2),
                        Tickets(flight_id=3, customer_id=3)])