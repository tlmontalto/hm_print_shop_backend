from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

import models

from playhouse.shortcuts import model_to_dict
from peewee import IntegrityError


# Creating an instance of the Blueprint class (Flask version of a controller)
# param 1: Name of the Blueprint
# param 2: The name for importing this Blueprint into another file
link = Blueprint('links', 'link')


"""
curl 'http://localhost:5000/api/v1/links/'
"""
@link.route('/', methods=['GET'])
@login_required
def get_all_links():
    # if not current_user.email.endswith('edu'):
    #     return jsonify(data={}, status={"code": 403, "message": "Not authorized"})

    try:
        # db_links = models.Link.select()
        # links = []
        
        # for link in db_links:
        #     print(link)
        #     print(model_to_dict(link))
        #     links.append(model_to_dict(link))

        links = [model_to_dict(link) for link in current_user.link]
        
        print(links)
        return jsonify(data=links, status={'code': 200, 'message': 'Success'})

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
@link.route('/', methods=['POST'])
def create_link():
    payload = request.get_json()
    print(payload)

    try:
        link = models.Link.create(username=payload['name'], description=current_user.id, file_url=payload['breed'])

        print(link.__dict__)

        return jsonify(data=model_to_dict(link), status={'code': 201, 'message': 'Success'})
    except IntegrityError:
        print('Invalid Schema was sent')

        return jsonify(data={}, status={'code': 401, 'message': 'Invalid link schema'})

# Show route
@link.route('/<id>', methods=["GET"])
def get_one_link(id):
    # getting the link from the ID parameter
    link = models.Link.get_by_id(id)
    # printing the link that we got and coverting it to a dictionary
    print(link.__dict__)
    # return JSON object of the link and a status code of 200 since we are successful
    return jsonify(data=model_to_dict(link), status={"code": 200, "message": "successful link"})

# Update route
@link.route('/<id>', methods=["PUT"])
def update_link(id):
    # storing the data from the request body
    payload = request.get_json()
    # the first step of updating the found link with new data
    query = models.Link.update(**payload).where(models.Link.id == id)
    # execute the query
    query.execute()
    # return the updated link and status code of 200 for success!!!
    return jsonify(data=model_to_dict(models.Link.get_by_id(id)), status={"code": 200, "message": "successfully updated link"})


# Delete route
@link.route('/<id>', methods=["DELETE"])
def delete_link(id):
    # find the link to delete
    query = models.Link.delete().where(models.Link.id == id)
    # actually delete the link
    query.execute()
    # return a response of success if the link is deleted
    return jsonify(data="link successfully deleted", status={"status": 200, "message": "link successfully deleted"})