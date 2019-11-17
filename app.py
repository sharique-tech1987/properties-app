from flask import Flask, request, jsonify, abort
from flask_httpauth import HTTPBasicAuth
from JsonFileOperator import JsonFileOperator
from ProjectEnums import *
from Helpers import Helpers

auth = HTTPBasicAuth()
app = Flask(__name__)

@auth.get_password
def get_pw(username):
#   Read from users Json file
    jsonOpObj = JsonFileOperator(USERS_FILE, 'r')
    users = jsonOpObj.Read()
    found_user = next((item for item in users if item["username"] == username), None)
    if found_user:
        return found_user['password']
    return None

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
@auth.login_required
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
        
#   Read from users Json file
    jsonOpObj = JsonFileOperator(USERS_FILE, 'r')
    users = jsonOpObj.Read()
    found_user = next((item for item in users if item["username"] == auth.username()), None)

    additional_params = {'id':new_property_id, 'user_id':found_user['id']}
    property_model = Helpers.PopulateModel(request, CREATE_PROPERTY_PARAMS, additional_params)
    users_properties.append(property_model)
    
#   Write to Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'w')
    jsonOpObj.Write(users_properties)
    return jsonify({'property_id': str(property_model['id'])}), 201


@app.route('/property/update', methods=['POST'])
@auth.login_required
def property_update():
    # request
    ...


@app.route('/property/delete', methods=['DELETE'])
@auth.login_required
def property_delete():
    # request
    if not request.json or not 'property_id' in request.json:
        abort(400)
        
#   Read from properties Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'r')
    users_properties = jsonOpObj.Read()
    
#   Read from users Json file
    jsonOpObj = JsonFileOperator(USERS_FILE, 'r')
    users = jsonOpObj.Read()
    found_user = next((item for item in users if item["username"] == auth.username()), None)
    
    property_id = request.json["property_id"]
    user_id = found_user['id']
    
    property_index = -1
    for index, item in enumerate(users_properties):
        if item["id"] == property_id and item["user_id"] == user_id:
            property_index = index
            break 
    if property_index != -1:
        done_op = True
        del users_properties[property_index] 
    else:
        done_op = False
        
#   Write to Json file
    jsonOpObj = JsonFileOperator(PROPERTIES_FILE, 'w')
    jsonOpObj.Write(users_properties)

    return jsonify(done_op)


if __name__ == '__main__':
    app.run(port = 5000)
