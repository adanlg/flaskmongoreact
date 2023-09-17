from flask import Flask, jsonify, request
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

# Instantiation
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/juan'
mongo = PyMongo(app)

# Settings
CORS(app)

# Database
collection = mongo.db.luis  # Use 'collection' directly for MongoDB operations

# Routes
@app.route('/users', methods=['POST'])
def createUser():
    print(request.json)
    data = {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }

    result = collection.insert_one(data)
    inserted_id = result.inserted_id

    return jsonify(str(inserted_id))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in collection.find({}):
        users.append({
            '_id': str(doc['_id']),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = collection.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User Deleted'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    print(request.json)
    collection.update_one({'_id': ObjectId(id)}, {"$set": {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({'message': 'User Updated'})

if __name__ == "__main__":
    app.run(debug=True)
