# Class implementation

from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.tokens import F1Team

f1_api = Blueprint('f1_api', __name__,
                   url_prefix='/api/tokens')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(f1_api)

class F1API:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            nconstructor = body.get('constructor')
            if nconstructor is None or len(nconstructor) < 2:
                return {'message': f'Constructor is incorrect'}, 210
            # validate uid
            ndriver = body.get('driver')
            if ndriver is None or len(ndriver) < 2:
                return {'message': f'Driver is missing, or is less than 2 characters'}, 210
            # look for password and dob
            nraces = body.get('races')
            nqualRate = body.get('qualRate')
            npolePositions = body.get('polePositions')

            ''' #1: Key code block, setup USER OBJECT '''
            f1dude = F1Team(constructor=constructor, driver=ndriver, races=nraces, polePositions=npolePositions,qualRate=nqualRate)
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            dude = f1dude.create()
            # success returns json of user
            if dude:
                return jsonify(f1dude.read())
            # failure returns error
            return {'message': "err"}, 210

    class _Read(Resource):
        def get(self):
            teams = F1Team.query.all()    # read/extract all users from database
            json_ready = [team.read() for team in teams]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')