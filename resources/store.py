from flask_restful import Resource, reqparse
from models.user import SubmissionStore
from flask import request

class SubmissionList(Resource):
    def post(self):
        username=request.values.get('username')
        return {
            'submissions': [submission.json() for submission in SubmissionStore.find_by_username(username)]}
