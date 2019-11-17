from flask import Flask, request, jsonify, abort
from JsonFileOperator import JsonFileOperator
from ProjectEnums import *
from Helpers import Helpers

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    # request
    if not request.json or not ('username' in request.json and 'password' in request.json):
        abort(400)
        
#   Read from users Json file
    jsonOpObj = JsonFileOperator(USERS_FILE, 'r')
    users = jsonOpObj.Read()
    if len(users):
        new_user_id =   users[-1]['id'] + 1
    else:
        new_user_id =  1
    additional_params = {'id' :  new_user_id}
    user_model = Helpers.PopulateModel(request, CREATE_USER_PARAMS, additional_params)
    users.append(user_model)
    
#   Write to users Json file
    jsonOpObj = JsonFileOperator(USERS_FILE, 'w')
    jsonOpObj.Write(users)
    return jsonify({'user_id': str(user_model['id'])}), 201



@app.route('/login', methods=['POST'])
def login():
    # request
    ...

@app.route('/properties', methods=['GET'])
def properties():
#   Read from properties Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'r')
    users_properties = jsonOpObj.Read()
    return jsonify({'properties': users_properties})


@app.route('/property', methods=['POST'])
def property():
    # request
    if not request.json or not 'id' in request.json:
        abort(400)

    search_id = request.json["id"]
#   Read from properties Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'r')
    users_properties = jsonOpObj.Read()
    found_property = next((item for item in users_properties if item["id"] == search_id), None)
    return jsonify({'property': found_property})


@app.route('/property/create', methods=['POST'])
def property_create():
    if not request.json or not 'name' in request.json:
        abort(400)
        
#   Read from properties Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'r')
    users_properties = jsonOpObj.Read()
    if len(users_properties):
        new_property_id =   users_properties[-1]['id'] + 1
    else:
        new_property_id =  1
    additional_params = {'id' :  new_property_id}
    property_model = Helpers.PopulateModel(request, CREATE_PROPERTY_PARAMS, additional_params)
    users_properties.append(property_model)
    
#   Write to Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'w')
    jsonOpObj.Write(users_properties)
    return jsonify({'property_id': str(property_model['id'])}), 201


@app.route('/property/update', methods=['POST'])
def property_update():
    # request
    ...


@app.route('/property/delete', methods=['DELETE'])
def property_delete():
    # request
    ...


if __name__ == '__main__':
    app.run(port = 5000)
