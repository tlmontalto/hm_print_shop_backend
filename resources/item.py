from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

import models

from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError


# Creating an instance of the Blueprint class (Flask version of a controller)
# param 1: Name of the Blueprint
# param 2: The name for importing this Blueprint into another file
item = Blueprint('items', 'item')


"""
curl 'http://localhost:5000/api/v1/items/'
"""
@item.route('/', methods=['GET'])
# @login_required
def get_all_items():
    # if not current_user.email.endswith('edu'):
    #     return jsonify(data={}, status={"code": 403, "message": "Not authorized"})

    try:
        # db_links = models.Link.select()
        # links = []
        
        # for link in db_links:
        #     print(link)
        #     print(model_to_dict(link))
        #     links.append(model_to_dict(link))

        items = [model_to_dict(item) for item in models.Item.select()]
        
        print(items)
        return jsonify(data=items, status={'code': 200, 'message': 'Success'})

    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resource'})


"""
Invalid Request:
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"test":"test"}' \
    'http://localhost:5000/api/v1/link/'

Valid Request:    
curl -X POST \
    -H 'Content-Type: application/json' \
    -d '{"username": "Tamir", "description": "Coffee Bookend", "file_url": "https://www.thingiverse.com/thing:1837114"}' \
    'http://localhost:5000/api/v1/link/'
"""
@item.route('/', methods=['POST'])
def create_item():
    payload = request.get_json()
    print(payload)

    try:
        item = models.Item.create(name=payload['name'], description=payload['description'], file_url=payload['file_url'], img_url=payload['img_url'], price=payload['price'])

        print(item.__dict__)

        return jsonify(data=model_to_dict(item), status={'code': 201, 'message': 'Success'})
    except IntegrityError:
        print('Invalid Schema was sent')

        return jsonify(data={}, status={'code': 401, 'message': 'Invalid item schema'})

# Show route
@item.route('/<id>', methods=["GET"])
def get_one_item(id):
    # getting the link from the ID parameter
    item = models.Item.get_by_id(id)
    # printing the link that we got and coverting it to a dictionary
    print(item.__dict__)
    # return JSON object of the link and a status code of 200 since we are successful
    return jsonify(data=model_to_dict(item), status={"code": 200, "message": "successful link"})

# Update route
@item.route('/<id>', methods=["PUT"])
def update_item(id):
    # storing the data from the request body
    payload = request.get_json()
    # the first step of updating the found link with new data
    query = models.Item.update(**payload).where(models.Item.id == id)
    # execute the query
    query.execute()
    # return the updated link and status code of 200 for success!!!
    return jsonify(data=model_to_dict(models.Item.get_by_id(id)), status={"code": 200, "message": "successfully updated item"})


# Delete route
@item.route('/<id>', methods=["DELETE"])
def delete_item(id):
    # find the link to delete
    query = models.Item.delete().where(models.Item.id == id)
    # actually delete the link
    query.execute()
    # return a response of success if the link is deleted
    return jsonify(data="item successfully deleted", status={"status": 200, "message": "item successfully deleted"})