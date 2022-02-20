from flask import Flask, render_template
import json

app = Flask(__name__)

customers = [{'id': 1, 'name': 'danny', 'address': 'tel-aviv'},
             {'id': 2, 'name': 'marina', 'address': 'beer-sheva'},
             {'id': 3, 'name': 'david', 'address': 'herzeliya'}]

administrators = [{'id': 1, 'name': 'jonny', 'address': 'tel-aviv'},
             {'id': 2, 'name': 'marcus', 'address': 'beer-sheva'},
             {'id': 3, 'name': 'andy', 'address': 'herzeliya'}]

users = [{'id': 1, 'name': 'jeses', 'address': 'Manchester'},
             {'id': 2, 'name': 'Anthony', 'address': 'Salford'},
             {'id': 3, 'name': 'Patrice', 'address': 'London'}]

countries = [{'id': 1, 'name': 'Israel', 'address': 'Middle-East'},
             {'id': 2, 'name': 'England', 'address': 'United-Kingdom'},
             {'id': 3, 'name': 'Netherlands', 'address': 'Europe'}]

flights = [{'id': 1, 'name': 'EL-AL', 'Origin': 'Tel-Aviv', 'destination': 'Kingston'},
             {'id': 2, 'name': 'British-Airways', 'Origin': 'Manchester', 'destination': 'Tel-Aviv'},
             {'id': 3, 'name': 'Easy-Jet', 'Origin': 'Manchester', 'destination': 'Ibiza'}]

tickets = [{'id': 1, 'name': 'one', 'destination': 'tel-aviv'},
             {'id': 2, 'name': 'two', 'destination': 'beer-sheva'},
             {'id': 3, 'name': 'three', 'destination': 'herzeliya'}]

user_roles = [{'id': 1, 'name': 'jonny', 'user_role': 'administrator'},
             {'id': 2, 'name': 'British-Airways', 'user_role': 'airline-company'},
             {'id': 3, 'name': 'andy', 'user_role': 'customer'}]

airlines = [{'id': 1, 'name': 'EL-AL', 'Origin': 'Tel-Aviv'},
             {'id': 2, 'name': 'British-Airways', 'Origin': 'Manchester'},
             {'id': 3, 'name': 'Easy-Jet', 'Origin': 'Manchester'}]

# localhost:5000/
# static page
# dynamic page
@app.route("/")
def home():
    print('hi')
    return '''
        <html>
            Hello main page!
            <button><a href="/ajax">show post</a></button>
        </html>
    '''

@app.route("/ajax")
def ajax():
    print('hi')
    return render_template('home.html')

@app.route('/customers', methods = ['GET'])    
def get_customers():
    return json.dumps(customers)

@app.route('/customers/<int:id>', methods = ['GET'])
def get_customer_by_id(id):
    for c in customers:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/conutries', methods = ['GET'])    
def get_conutries():
    return json.dumps(countries)

@app.route('/conutries/<int:id>', methods = ['GET'])
def get_conutry_by_id(id):
    for c in countries:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/administrators', methods = ['GET'])    
def get_administrators():
    return json.dumps(administrators)

@app.route('/administrators/<int:id>', methods = ['GET'])
def get_administrator_by_id(id):
    for c in administrators:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/users', methods = ['GET'])    
def get_users():
    return json.dumps(users)

@app.route('/users/<int:id>', methods = ['GET'])
def get_user_by_id(id):
    for c in users:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/flights', methods = ['GET'])    
def get_flights():
    return json.dumps(flights)

@app.route('/flights/<int:id>', methods = ['GET'])
def get_flight_by_id(id):
    for c in flights:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/tickets', methods = ['GET'])    
def get_tickets():
    return json.dumps(tickets)

@app.route('/conutries/<int:id>', methods = ['GET'])
def get_ticket_by_id(id):
    for c in tickets:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/user_roles', methods = ['GET'])    
def get_user_roles():
    return json.dumps(user_roles)

@app.route('/conutries/<int:id>', methods = ['GET'])
def get_user_role_by_id(id):
    for c in user_roles:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

@app.route('/airlines', methods = ['GET'])    
def get_airlines():
    return json.dumps(airlines)

@app.route('/airlines/<int:id>', methods = ['GET'])
def get_airline_by_id(id):
    for c in airlines:
        if c["id"] == id:
            return json.dumps(c)
    return '{}'

app.run()

