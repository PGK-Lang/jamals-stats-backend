from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.schedule import Schedule

# variable name, prefix, and name to match variable
schedule_api = Blueprint('schedule_api', __name__,
                   url_prefix='/api/f1schedule/')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(schedule_api)

class UserAPI:        
    class _Create(Resource): # alter to support your needs
        def post(self):
            pass

    class _Read(Resource):
        def get(self):
            schedules = Schedule.query.all()    # read/extract all users from database
            json_ready = [schedule.read() for schedule in schedules]  # prepare output in json
            return jsonify(json_ready)
    
    class _Update(Resource):
            def update(self):
                body = request.get_json()
                id = body.get('circuit')
                driver = ''
                numChamps = ''
                races = ''
                try:
                    driver = body.get("date")
                except:
                    pass
                try:
                    numChamps = body.get("location")
                except:
                    pass
                try: 
                    races = body.get("raceName")
                except:
                    pass
                team = Schedule.query.get(id)
                team.update(driver, numChamps, races)
        
    class _Delete(Resource):
            def delete(self):
                body = request.get_json()
                id = body.get('id')
                team = Schedule.query.get(id)
                team.delete()
                return f"{team.read()} Has been deleted"
# building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')