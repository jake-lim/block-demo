from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import jsonpickle

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'transaction.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(120), unique=True)

    def __init__(self, username, email, token):
        self.username = username
        self.email = email
        self.token = token


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('username', 'email', 'token')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# endpoint to create new user
@app.route("/transaction", methods=["POST"])
def add_user():
    username = request.json['username']
    email = request.json['email']
    token = request.json['token']
    
    new_user = User(username, email, token)

    db.session.add(new_user)
    db.session.commit()

    return jsonpickle.encode(new_user)

# endpoint to show all users
@app.route("/transaction", methods=["GET"])
def get_user():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)


# endpoint to get user detail by id
@app.route("/transaction/<id>", methods=["GET"])
def user_detail(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# endpoint to update user
@app.route("/transaction/<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    username = request.json['username']
    email = request.json['email']
    token = request.token['token']

    user.email = email
    user.username = username
    user.token = token

    db.session.commit()
    return user_schema.jsonify(user)


# endpoint to delete user
@app.route("/transaction/<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
