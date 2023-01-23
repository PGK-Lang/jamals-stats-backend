from sqlite3 import IntegrityError
import requests
from sqlalchemy import Column, Integer, PickleType, String
from .. import db
from sqlalchemy.exc import IntegrityError

"""
The point of this class is to store the name, team, standings, points, nationality, likes, dislikes, and comments for a driver instance
"""
class Drivers(db.Model):
  __tablename__ = "drivers"

  _id = Column(Integer, primary_key=True)
  _name = Column(String(255))
  _team = Column(String(255))
  _standings = Column(Integer)
  _points = Column(Integer)
  _nationality = Column(String(255))

  _likes = Column(Integer)
  _dislikes = Column(Integer)
  _comments = Column(PickleType)

  def __init__(self, id, driver_name, team_name, position, points, nationality):
    self._id = id
    self._name = driver_name
    self._team = team_name
    self._standings = position
    self._points = points
    self._nationality = nationality

    self._likes = 0
    self._dislikes = 0
    self._comments = []

    """
    example comment
    {
      "name": "Sean"
      "comment": "This driver is insane!!"
    }
    """

  @property
  def name(self):
    return self._name

  @property
  def team(self):
    return self._team

  @property
  def standings(self):
    return self._standings

  @property
  def nationality(self):
    return self._nationality

  @property
  def likes(self) -> int:
    return self._likes

  @property
  def dislikes(self) -> int:
    return self._dislikes

  @property
  def comments(self) -> list:
    return self._comments

  @comments.setter
  def comments(self, comment: dict):
    self._comments = self.comments + [ comment.copy() ]

  def deleteComment(self):
    self._comments = self.comments[:-1].copy()
  
  def like(self):
    self._likes += 1

  def dislike(self):
    self._dislikes += 1
  
  def to_dict(self):
    return {"name": self._name, "team": self._team, "standings": self._standings, "points": self._points, "nationality": self._nationality, "likes": self._likes, "dislikes": self._dislikes, "comments": str(self._comments)}

  def create(self):
        try:
            db.session.add(self)
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

def init_drivers():

  if not len(db.session.query(Drivers).all()) == 0: return

  headers = {
      "X-RapidAPI-Key": "9275b62a1fmsh3b832340dafb492p1abc77jsn58ef554feee6",
   	  "X-RapidAPI-Host": "f1-live-motorsport-data.p.rapidapi.com"
  }

  r = requests.get(
       url="https://f1-live-motorsport-data.p.rapidapi.com/drivers/standings/2022", headers=headers)

  if r.status_code != 200:
    print("API Request failed:", r.status_code)
    exit

  all_drivers = r.json()['results']

  demo_drivers = all_drivers[:4]

  driver_objects = []

  for id, driver in enumerate(demo_drivers):
    driver_objects.append(
        Drivers(id=id, driver_name=driver["driver_name"], team_name=driver["team_name"],
                position=driver["position"], points=driver["points"], nationality=driver["nationality"])
    )

  print("\nTest 4: add comments & likes")
  driver_objects[0].addComment({
      "name": "Dontavious",
      "message": "You're trash!!"
  })
  [driver_objects[0].dislike() for i in range(20)]

  driver_objects[1].addComment({
      "name": "Dontavious",
      "message": "Mid tbh"
  })
  [driver_objects[1].like() for i in range(20)]

  driver_objects[2].addComment({
      "name": "Dontavious",
      "message": "3.0/3.0: Great job! You deserve some seed points."
  })
  [driver_objects[2].like() for i in range(3)]

  [driver.create() for driver in driver_objects]

  db.session.commit()
