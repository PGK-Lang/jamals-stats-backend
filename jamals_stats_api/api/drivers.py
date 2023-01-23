from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from .. import db
from ..model.drivers import Drivers

driver_blueprint = Blueprint("drivers", __name__)
driver_api = Api(driver_blueprint)

class DriverAPI(Resource):
  def get(self):
    id = request.args.get("id")
    driver = db.session.query(Drivers).get(id)
    if driver:
      return driver.to_dict()
    return {"message": "driver not found"}, 404

  def post(self):
    parser = reqparse.RequestParser()
    parser.add_argument("id", required=True, type=int)
    parser.add_argument("name", required=True, type=str)
    parser.add_argument("comment", required=True, type=str)
    args = parser.parse_args()

    try:
      driver = db.session.query(Drivers).get(args["id"])
      if driver:
        driver.comments = {
          "name": args["name"],
          "comment": args["comment"]
        }
        db.session.commit()
      else:
          return {"message": "driver not found"}, 404
    except Exception as e:
      db.session.rollback()
      return {"message": f"server error: {e}"}, 500
  
  def delete(self):
    id = request.args.get("id")
    driver = db.session.query(Drivers).get(id)

    if driver:
      driver.deleteComment()
      db.session.commit()
      return driver.to_dict()
    return {"message": "driver not found"}, 404

class LikesAPI(Resource):
  def put(self):
    id = request.args.get("id")
    driver = db.session.query(Drivers).get(id)

    if driver:
      driver.like()
      db.session.commit()
      return driver.likes
    return {"message": "driver not found"}, 404

class DislikesAPI(Resource):
  def put(self):
    id = request.args.get("id")
    driver = db.session.query(Drivers).get(id)

    if driver:
      driver.dislike()
      db.session.commit()
      return driver.dislikes
    return {"message": "driver not found"}, 404

class ListDriversAPI(Resource):
  def get(self):
    drivers = db.session.query(Drivers).all()
    return [driver.to_dict() for driver in drivers]

driver_api.add_resource(DriverAPI, "/drivers")
driver_api.add_resource(LikesAPI, "/like")
driver_api.add_resource(DislikesAPI, "/dislike")
driver_api.add_resource(ListDriversAPI, "/drivers-list")