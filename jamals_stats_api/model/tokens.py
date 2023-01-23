
""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError

class F1Team(db.Model):

    __tablename__ = 'formulaone'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _constructor = db.Column(db.String(255), unique=False, nullable=False)
    _driver = db.Column(db.String(255), unique=True, nullable=False)
    _races = db.Column(db.Integer, unique=False, nullable=False)
    _polePositions = db.Column(db.Integer)
    _qualRate = db.Column(db.Float)
    _numChamps = db.Column(db.Integer)



    def __init__(self, constructor, driver, races, polePositions, qualRate):
        self._constructor = constructor
        self._driver = driver
        self._races = races
        self._polePositions = polePositions
        self._qualRate = qualRate
        self._numChamps = self.retChamps({"Mclaren" : 8, "Ferrari" : 16, "Aston Martin" : 0, "Red Bull" : 5, "Honda" : 6}) # later this would be replaced by an API

    def __str__(self):
        return f"{self.constructor} raced by {self._driver}."   

    def __cmp__(self, other):
        return self._driver == other._driver

    def champComp(self, other): 
        ret = self._numChamps > other._numChamps
        return ret
   

    @property 
    def constructor(self):
        return (self._constructor) 
    
    @constructor.setter
    def constructor(self, qualRate):
        self._constructor = qualRate

    @property 
    def qualRate(self):
        return (self._qualRate*self.races) 
    
    @qualRate.setter
    def qualRate(self, qualRate):
        self._qualRate = qualRate 

    @property 
    def driver(self):
        return (self._driver) 
    
    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @property 
    def races(self):
        return (self._races) 
    
    @races.setter
    def races(self, races):
        self._races = races
    
    @property 
    def polePositions(self):
        return (self._polePositions) 
    
    @polePositions.setter
    def polePositions(self, polePositions):
        self._polePositions = polePositions

    @property 
    def numChamps(self):
        return (self._numChamps) 
    
    @numChamps.setter
    def numChamps(self, numChamps):
        self._numChamps = numChamps

    def retChamps(self, dic):
        try: 
            champs = dic[self._constructor]
            return champs
        except Exception:
            raise KeyError("Constructor Not Recognized")
    
    def create(self): # Create
        try:
            db.session.add(self)
            db.session.commit() 
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self): # Read
        return {
            "id": self.id,
            "constructor": self._constructor,
            "driver": self._driver,
            "qualRate": self._qualRate,
            "numChamps": self._numChamps,
        }


    def update(self, driver="", numChamps="", races=""): # Update
        """only updates values with length"""
        if len(driver) > 0:
            self._driver = driver
        if len(numChamps) > 0:
            self._numChamps += int(numChamps)
        if len(races) > 0:
            self._races += int(races)
        db.session.commit()
        return self

    def delete(self): # Delete
        db.session.delete(self)
        db.session.commit()
        return None

def initTeams():
    db.create_all()
    u1 = F1Team("Mclaren", "Rohin S", 12, 1, 0.23)
    u2 = F1Team("Ferrari", "Advay S", 15, 3, 0.69)
    u3 = F1Team("Aston Martin", "Ryan W", 18, 5, 0.9)
    u4 = F1Team("Honda", "Varalu N", 20, 4, 0.5)

    teams = [u1, u2, u3, u4]

    for team in teams:
        try:
            #''add user/post data to table
            team.create()
        except IntegrityError:
            #fails with bad or duplicate data
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {team._constructor}")

