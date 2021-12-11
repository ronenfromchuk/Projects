import sqlite3
from Customer import Customer
from CustomerDataAccess import CustomerDataAccess

con = sqlite3.connect('hanukkah.db')
cur = con.execute('SELECT * FROM customer')
c = CustomerDataAccess('hanukkah.db')

_input = input('Choose one of the following options: \n1. Get all customers'
               '\n2. Get customer by id\n3. Insert customer\n4. Delete customer'
               '\n5. Update customer\n6. Exit\ninsert your choise: ')

if _input == '1':
    print(c.print_all_customers())
if _input == '2':
    print(c.get_all_customers())
if _input == '3':
    new_customer = Customer(id=int(input('id: ')),fname=input('first name: '),lname=input('last name: '),address=input('address: '),mobile=input('mobile: '))
    print(c.insert_customer(new_customer))
if _input == '4':
    print(c.delete_customer(id=input('id: ')))
if _input == '5':
    _input_id = input('Choose customer to update by his id: ')
    if not c.check_customer(int(_input_id)) : print('id does not exist!')
    else:
        update_customer = Customer(id=input('id:'),fname=input('First Name: '), lname=input('Last Name: '), address=input('Address: '), mobile=input('Mobile: '))
        print(c.update_customer(_input_id, update_customer))

if _input == '6':
    print('you have chose to exit!')