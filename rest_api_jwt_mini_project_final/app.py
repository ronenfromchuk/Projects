from flask import Flask, request, jsonify, make_response
from Customers import Customer
from Users import User
from Logger import Logger
from DataAccess import RestDataAccess
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from functools import wraps
import uuid


app = Flask(__name__)

app.config['SECRET_KEY'] = 'your secret key'

dao = RestDataAccess('DataBaseApi.db')
logger = Logger.get_instance()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer')

        if not token:
            logger.logger.info('user attempted to use function which requires jwt token, token is missing!')
            return jsonify({'message': 'token is missing'}), 401

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
            user = dao.get_user_by_public_id(payload['public_id'])
        except:
            logger.logger.warning("user attempted to use function which requires jwt token, token isn't valid!")
            return jsonify({'message': "token isn't valid"}), 401

        return f(user, *args, **kwargs)
    return decorated


@app.route("/")
def home():
    return '''
        <html>
            <h3>********************************************************************</h3>
            <h1>REST_API_JWT_TOKEN_MINI_PROJECT</h1>
            <h3>********************************************************************</h3>
            <h1 style="color: red;">RONEN FROMCHUK<h1/>
            <h3>***********************************<h3/>
            <h3 style="color: green;">PAGE SUCCESSFULLY LOADED!<h3/>
            <h3>********************************<h3/>
            
        </html>
    '''


@app.route('/customers', methods=['GET', 'POST'])
@token_required
def get_or_post_customer(user):
    if request.method == 'GET':
        search_args = request.args.to_dict()
        customers = dao.get_all_customers(search_args)
        return jsonify(customers)
    if request.method == 'POST':
        customer_data = request.get_json()
        inserted_customer = Customer(id_=None, name=customer_data["name"], location=customer_data["location"])
        answer = dao.insert_new_customer(inserted_customer)
        if answer:
            logger.logger.info(f'new customer=["{inserted_customer}"], has been created by the user "{user}"!')
            return make_response('customer created successfully!', 201)
        else:
            logger.logger.error(f'user=["{user}"], attempted to insert new customer, and didnt provided= ["name"] & '
                                f'["location"]')
            return jsonify({'answer': 'failed'})


@app.route('/customers/<int:id_>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@token_required
def get_customer_by_id(user, id_):
    if request.method == 'GET':
        customer = dao.get_customer_by_id(id_)
        return jsonify(customer)
    if request.method == 'PUT':
        values_dict = request.get_json()
        answer = dao.update_put_customer(id_, values_dict)
        if answer:
            logger.logger.info(f'customer id=[{id_}], has been updated by the user=["{user}"]!')
            return make_response('successful put!', 201)
        else:
            logger.logger.error(f'user=["{user}"], has attempted to update customer id=["{id_}"] '
                                f'not exists in the db.')
            return jsonify({'answer': 'failed'})
    if request.method == 'DELETE':
        answer = dao.delete_customer(id_)
        if answer:
            logger.logger.info(f'customer id=[{id_}], has been deleted by user=["{user}"]! ')
            return make_response('successful delete!', 201)
        else:
            logger.logger.error(f'user=["{user}"], attempted to delete customer id=["{id_}"] '
                                f'not exists in the db.')
            return jsonify({'answer': 'failed'})
    if request.method == 'PATCH':
        values_dict = request.get_json()
        answer = dao.update_patch_customer(id_, values_dict)
        if answer:
            logger.logger.info(f'customer id=[{id_}], has been updated user=["{user}"]!')
            return make_response('successful patch!', 201)
        else:
            logger.logger.info(f'user=["{user}"], attempted to update customer id=["{id_}"] '
                               f'not exists in the db.')
            return jsonify({'answer': 'failed'})


@app.route('/signup', methods=['POST'])
def signup():
    form_data = request.form

    username = form_data.get('username')
    password = form_data.get('password')

    user = dao.get_user_by_username(username)

    if user:
        logger.logger.error(f'anonymous attempted to sign up with username=[{username}], this username already '
                            f'exists in the db')
        return make_response('this username already exist, please try different name!', 202)

    else:
        inserted_user = User(id_=None, public_id=str(uuid.uuid4()), username=username,
                             password=generate_password_hash(password))
        dao.insert_new_user(inserted_user)
        logger.logger.info(f'new user=[{inserted_user}], has been created successfully!')
        return make_response('new user successfully registered!', 201)


@app.route('/login', methods=['POST'])
def login():
    form_data = request.form

    if not form_data or not form_data.get('username') or not form_data.get('password'):
        logger.logger.info('user attempted to login without providing the required data(username, password)')
        return make_response("couldn't verify", 401, {'WWW-Authenticate': 'Basic realm="Login required."'})

    user = dao.get_user_by_username(form_data.get('username'))
    if not user:
        logger.logger.warning(f'user attempted to login, username=[{form_data.get("username")}] '
                              f'does not exist in the db')
        return make_response("couldn't verify", 401, {'WWW-Authenticate': 'Basic realm="Login required."'})

    if not check_password_hash(user.password, form_data.get('password')):
        logger.logger.error(f'user=[{form_data.get("username")}], attempted to login with a wrong password.')
        return make_response("wrong password!", 401, {'WWW-Authenticate': 'Basic realm="Login required."'})

    logger.logger.debug(f' user=[{form_data.get("username")}], logged in successfully!')
    token = jwt.encode({'public_id': user.public_id, 'exp': datetime.now() + timedelta(minutes=30)},
                       app.config['SECRET_KEY'])
    return make_response(jsonify({'token': token.decode('UTF-8')}), 201)


if __name__ == '__main__':
    app.run(debug=True)
