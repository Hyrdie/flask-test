from flask import Flask
from flask import request
from sqlalchemy.orm import Session
from orm import db
from orm.db_setup import engine
from repository.user import insert, get_by_id, get_all, update, delete
from schema.user import User, UserResponse
import requests
from pydantic import ValidationError
from settings import settings

app = Flask("AKASIA Test")

db.metadata.create_all(engine)

@app.route("/")
def get_info():
    return "services for user akasia"


@app.route("/user/fetch", methods=['GET'])
def get_user():
    response = []
    page = request.args.get('page', 0)
    if not page:
        return "Missing page param", 400

    raw_data_from_api = requests.get(f"https://reqres.in/api/users?page={page}")
    data_from_api = raw_data_from_api.json()
    data = data_from_api.get('data')

    with Session(engine) as session:
        for value in data:
            user_database = get_by_id(session, value.get('id')).fetchone()
            if not user_database:
                user = User(
                    email=value.get('email'),
                    first_name=value.get('first_name'),
                    last_name=value.get('last_name'),
                    avatar=value.get('avatar'),
                )
                insert(session, user)
        
        get_all_user = get_all(session)
        for data_user in get_all_user:
            user = UserResponse(
                    id=data_user.id,
                    email=data_user.email,
                    first_name=data_user.first_name,
                    last_name=data_user.last_name,
                    avatar=data_user.avatar,
                )
            response.append(dict(user))

    return {"data":response}

@app.route("/user/<int:id>", methods=['GET'])
def get_user_by_id(id):
    with Session(engine) as session:
        data = get_by_id(session, id).fetchone()
    resp = UserResponse(
        id=data.id,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        avatar=data.avatar
    )
    return {"data":dict(resp)}

@app.route("/user", methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = User(
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            avatar=data.get('avatar')
        )
        with Session(engine) as session:
            insert(session, user)
        return {"data":dict(user)}
    except ValidationError as e:
        return e.errors(), 400

@app.route("/user/<int:id>", methods=['PUT'])
def update_user(id):
    try:
        with Session(engine) as session:
            get_user = get_by_id(session, id).fetchone()
            data = request.get_json()
            user = User(
                email=data.get('email', get_user.email),
                first_name=data.get('first_name', get_user.first_name),
                last_name=data.get('last_name', get_user.last_name),
                avatar=data.get('avatar', get_user.avatar)
            )
            update(session, id, user)
        return {"data":dict(user)}
    except ValidationError as e:
        return e.errors(), 400

@app.route("/user/<int:id>", methods=['DELETE'])
def delete_user(id):
    auth_header = request.headers.get('authorization')
    if auth_header != settings.TOKEN:
        return "token is not valid", 401
    try:
        with Session(engine) as session:
            delete(session, id)
        return {"message":f"deleted user with id : {id}"}
    except ValidationError as e:
        return e.errors(), 400
    