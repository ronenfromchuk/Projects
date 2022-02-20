from flask import Flask, render_template
import json

app = Flask(__name__)

customers = [{'id': 1, 'name': 'danny', 'address': 'tel-aviv'},
             {'id': 2, 'name': 'marina', 'address': 'beer-sheva'},
             {'id': 3, 'name': 'david', 'address': 'herzeliya'}]

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

app.run()
