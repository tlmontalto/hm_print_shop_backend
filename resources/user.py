import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict


# first argument is blueprints name
# second argument is it's import_name
# The third argument is the url_prefix so we don't have
# to prefix all our apis with /api/v1
user = Blueprint('hmpusers', 'hmpuser')

@user.route('/register', methods=["POST"])
def register():
    # See request payload anagolous to req.body in express
    # This has all the data like username, email, password
    payload = request.get_json()

    payload['email'] = payload['email'].lower()
    try:
        # Find if the user already exists?
        models.HMPUser.get(models.HMPUser.email == payload['email']) # model query finding by email
        return jsonify(data={}, status={"code": 401, "message": "A user with that name already exists"})
    except models.DoesNotExist:
        payload['password'] = generate_password_hash(payload['password']) # bcrypt line for generating the hash
        user = models.HMPUser.create(**payload) # put the user in the database
         # **payload, is spreading like js (...) the properties of the payload object out

        # starts user session
        login_user(user)

        user_dict = model_to_dict(user)
        print(user_dict)
        print(type(user_dict))
        # delete the password before we return it, because we don't need the client to be aware of it
        del user_dict['password']

        return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    print(payload)
    try:
        user = models.HMPUser.get(models.HMPUser.email == payload['email'])
        user_dict = model_to_dict(user)
        if(check_password_hash(user_dict['password'], payload['password'])):
            del user_dict['password']
            login_user(user)
            return jsonify(data=user_dict, status={'code': 200, 'message': 'Login sucessful'})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Password incorrect'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Email does not exist'})

@user.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return jsonify(data={}, status={"code": 200, "message": "Successful Logout"})

@user.route('/', methods=["GET"])
def get_all_users():
    try:
        users = [model_to_dict(user) for user in models.HMPUser.select()]
        print(users)
        return jsonify(data=users, status={"code": 200, "message": "Success"})
    except models.DoesNotExist:
        return jsonify(data={}, status={"code": 401, "message": "Error getting the resources"})

# Show route
@user.route('/<id>', methods=["GET"])
def get_one_user(id):
    # getting the link from the ID parameter
    user = models.HMPUser.get_by_id(id)
    # printing the link that we got and coverting it to a dictionary
    print(user.__dict__)
    # return JSON object of the link and a status code of 200 since we are successful
    return jsonify(data=model_to_dict(user), status={"code": 200, "message": "successful link"})