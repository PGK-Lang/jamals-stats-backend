from random import randrange
from datetime import date
import os, base64
import json
from __init__ import app, db
from sqlalchemy.exc import IntegrityError



class Schedule(db.Model):
    __tablename__ = 'f1schedule'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _raceName = db.Column(db.String(255), unique=True, nullable=False)
    _date = db.Column(db.String, unique=False, nullable=False)
    _circuit = db.Column(db.String(255), unique=False, nullable=False)
    _location = db.Column(db.String(255), unique=False, nullable=False)


    def __init__(self, raceName, date, circuit, location):
        self._raceName = raceName
        self._date = date
        self._circuit = circuit
        self._location = location

    def __str__(self):
        return f"{self.raceName} on {self._date} at {self._circuit} in {self._location}."   

    def __cmp__(self, other):
        return self._raceName == other._raceName

    @property 
    def raceName(self):
        return (self._raceName) 

    @raceName.setter
    def raceName(self, raceName):
        self._raceName = raceName

    @property 
    def date(self):
        return (self._date) 

    @date.setter
    def date(self, date):
        self._date = date

    @property 
    def circuit(self):
        return (self._circuit) 

    @circuit.setter
    def circuit(self, circuit):
        self._circuit = circuit

    @property 
    def location(self):
        return (self._location) 

    @location.setter
    def location(self, location):
        self._location = location

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
            "raceName": self._raceName,
            "date": self._date,
            "circuit": self._circuit,
            "location": self._location,
        }

    def update(self, raceName="", date="", circuit="", location=""): # Update
        """only updates values with length"""
        if len(raceName) > 0:
            self._raceName = raceName
        if len(date) > 0:
            self._date = date
        if len(circuit) > 0:
            self._circuit = circuit
        if len(location) > 0:
            self._location = location
        db.session.commit()
        return self

    def delete(self): # Delete
        db.session.delete(self)
        db.session.commit()

def initSchedule():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = Schedule('Monaco Grand Prix', '(2023,5,28)', 'Monaco Circuit', 'Monaco')
    u2 = Schedule('Singapore Grand Prix', '(2023,9,17)','Marina Bay Street Circuit', 'Singapore')
    u3 = Schedule('Bahrain Grand Prix', '(2023,3,31)','Bahrain International Circuit','Bahrain') 
    u4 = Schedule('Australian Grand Prix','(2023,3,24)','Albert Park Circuit', 'Melbourne')
    
    # raceName, date, circuit, location

    users = [u1, u2, u3, u4]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            '''add user/post data to table'''
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.uid}")
            