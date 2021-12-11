import sqlite3
from Customer import Customer

class CustomerDataAccess:

    def __init__(self, data_path):
        self.con = sqlite3.connect(data_path)
        self.data_path = data_path
        self.cursor = self.con.cursor()

    def print_all_customers(self):
        self.cursor.execute("select * from customer")
        for row in self.cursor:
            print(row)

    def check_customer(self, _input):
        self.cursor.execute('SELECT * FROM customer')
        _l = [row[0] for row in self.cursor]
        return _input in _l

    def insert_customer(self, customer):
        if self.check_customer(int(customer.id)): return 'id occupied'
        self.cursor.execute(f'INSERT INTO customer VALUES ({customer.id}, "{customer.fname}", "{customer.lname}", "{customer.address}", {customer.mobile})')
        self.con.commit()
        return f'customer {customer.fname} {customer.lname} has been added!'

    def delete_customer(self, id):
        if not self.check_customer(int(id)): return "wrong id"
        self.cursor.execute(f"DELETE FROM customer WHERE id = {id}")
        self.con.commit()
        return f'customer id: {id} deleted!'

    def get_all_customers(self):
        self.cursor.execute("SELECT * FROM customer")
        return [f'{row[1]} {row[2]}' for row in self.cursor]

    def get_customers_by_id(self, id):
        if not self.check_customer(int(id)) : return 'wrong id!'
        else:
            self.cursor.execute("SELECT * FROM customer WHERE" + \
                                f' id = {id}')
            return [f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}' for row in self.cursor]

    def update_customer(self, id, customer):
        self.cursor.execute(f"UPDATE customer SET id = {customer.id} WHERE id = {id} ")
        self.cursor.execute(f"UPDATE customer SET fname = '{customer.fname}' WHERE fname = {id} ")
        self.cursor.execute(f"UPDATE customer SET lname = '{customer.lname}' WHERE id = {id} ")
        self.cursor.execute(f"UPDATE customer SET address = '{customer.address}' WHERE id = {id} ")
        self.cursor.execute(f"UPDATE customer SET mobile = {customer.mobile} WHERE id = {id} ")
        self.con.commit()
        return f'customer {customer.fname} {customer.lname} has been updated!'

    def __repr__(self):
        return f'CustomerDataAccess({self.data_path})'

    def __str__(self):
        return f'CustomerDataAccess: data_base_path: {self.data_path}'
