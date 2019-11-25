import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
    type=str,
    required=True,
    help="This field cannot be blank."
)

_user_parser.add_argument('password',
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument('phoneNo',
    type=str,
    required=False,
    help="This field cannot be blank."
)


class UserRegister(Resource):
    def post(self):
        username=request.values.get('username')
        password=request.values.get('password')
        phoneNo=request.values.get('phoneNo')
        print(username,password,phoneNo)
        if UserModel.find_by_username(username):
            return {"error":True,
                    "username":False,
                    "message": "A user with that username already exists"}, 400

        user = UserModel(username,password,phoneNo)
        user.save_to_db()

        return {"message": "User created successfully.","error":False}, 200

class User(Resource):
    @classmethod
    def get(cls, username):
        user = UserModel.find_by_id(username)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()
    
    @classmethod
    def delete(cls, username):
        user = UserModel.find_by_id(username)
        if not user:
            return {'message': 'User not found'}, 404
        
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        username=request.values.get('username')
        password=request.values.get('password')

        # find user in database
        user = UserModel.find_by_username(username)

        if user and safe_str_cmp(user.password, password):
            return {
                'error':False,
                'username':user.username,
                'phoneNo':user.phoneNo,
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserUpdate(Resource):
    def post(self):
        username=request.values.get('username')
        
        if request.values.get('NumberUpdate')=="True":
            phoneNo=request.values.get('phoneNo')
            user = UserModel.find_by_username(username)
            if user:
                password=user.password
                user.delete_from_db()
                User=UserModel(username,password,phoneNo)
                User.save_to_db()
                return {'message':'Profile Updated','error':'false'}, 200
            return {'error':True,'message':'Some erros have occured during the process'}, 400
        else:
            user = UserModel.find_by_username(username)
            currentPassword=request.values.get('currentPassword')
            newPassword=request.values.get('newPassword')
            if user and safe_str_cmp(user.password, currentPassword):
                user.password=newPassword
                user.save_to_db()
                return {'message':'Profile Updated','error':'false'}, 200
            return {'error':True,'message':'Some erros have occured during the process'}, 400

class CheckPhoneNumber(Resource):
    def post(self):
        phoneNo=request.values.get('phoneNo')
        user = UserModel.find_by_phoneNo(phoneNo)
        if user:
            return {'error':True, 'message':'The provided number already exists'}, 400
        else:
            return {'error':False},200

class ForgetPassword(Resource):
    def post(self):
        phoneNo=request.values.get('phoneNo')
        user=UserModel.find_by_phoneNo(phoneNo)
        if user:
            return {'error':False,'username':user.username},200
        else:
            return {'error':True, 'message':'This number is not associated with any account'}, 400


class setNewPassword(Resource):
    def post(self):
        username=request.values.get('username')
        password=request.values.get('password')
        user=UserModel.find_by_username(username)
        if user:
            user.password=password
            user.save_to_db()
            return {'error':False, 'message':'Password Updated'},200
        else:
            return {'error':True, 'message':"Your process couldn\'t be completed due to some error.'}, 400


