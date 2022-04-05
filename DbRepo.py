from logger import Logger
from datetime import datetime
from sqlalchemy import asc
from Users import Users



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
        self.local_session.commit()

    def create_all_sp(self, file):
            try:
                with open(file, 'r') as sp_file:
                    queries = sp_file.read().split('|||')
                for query in queries:
                    self.local_session.execute(query)
                self.local_session.commit()
                self.logger.logger.debug(f'all SP were created!, from file=[{file}]')
            except FileNotFoundError:
                self.logger.logger.critical(f'file=[{file}] wasnt found')

    def reset_all_tables_auto_inc(self):
        self.reset_auto_inc(Users)


    def reset_db(self):
        self.reset_auto_inc(Users)


        self.add_all([  Users(username='ronen', password='uguessit69', email='ronen@mcr.com', public_id='test1', user_role=1),       #1 ---> user_id
                        Users(username='bbntyahho', password='case10000', email='bbn@mcr.com', public_id='test2', user_role=1),      #2 ---> user_id
                        Users(username='jesse', password='jlingz14', email='jesse@mcr.com', user_role=2),         #3 ---> user_id # airline
                        Users(username='paulpogba', password='pp666666', email='pp6@mcr.com', user_role=2),       #4 ---> user_id # airline
                        Users(username='jadon25', password='jsancho25', email='jadon@mcr.com', public_id='test5', user_role=3),      #5 ---> user_id
                        Users(username='l0llel', password='trolllel123', email='troll@mcr.com', public_id='test6', user_role=3),     #6 ---> user_id
                        Users(username='ajoshua', password='aj2022', email='anthony@mcr.com', public_id='test7', user_role=3),       #7 ---> user_id
                        Users(username='tonyparker', password='tp1999', email='tonyp@mcr.com', public_id='test8', user_role=3),      #8 ---> user_id
                        Users(username='andyc0l3', password='ac1999', email='andyc0le@mcr.com', public_id='test9', user_role=3),     #9 ---> user_id
                        Users(username='mjackson', password='justd01t', email='mjackson@mcr.com', public_id='test10', user_role=3)])  #10 --> user_id
