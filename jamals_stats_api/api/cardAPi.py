from flask import Blueprint, request, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
import requests  # used for testing 
import random
import wikipediaapi
card_api = Blueprint('card_api', __name__,
                   url_prefix='/api/')

# API generator https://flask-restful.readthedocs.io/en/latest/api.html#id1
api = Api(card_api)

'''
I combined both in order to support both endpoints on the same area. may allow us to pivot should it be necessary
basically tricks the server into running both ends
'''
class UsrAPI:
    def serialize(name):
        wiki_wiki = wikipediaapi.Wikipedia('en') # make a wikipedia api object

        page_py = wiki_wiki.page(name) # init to wikipedia by default for default page, otherwise check name
        thisdict = {} # create a dictionary
        thisdict["url"] = page_py.fullurl 
        thisdict["summary"] = page_py.summary
        for i in page_py.sections:
            thisdict[i.title] = i.text
              # init values
            

        return thisdict

    local_dic = {} # Stores all the users and IDs
    def card(front, back, diction):
        user_id = str(len(diction))
        diction[user_id] = {'title':front, "substance":back}
    def delete_all(query, diction):
        if query == "true":
            diction = {}
            return {"message" : "operation successful"}
        else:
            return {"message" : "operation failure"}

    class _Create(Resource):
        def post(self, front, back): # simply creates the endpoint, dne otherwise
            UsrAPI.card(front, back, UsrAPI.local_dic)
            return {"message" : f"{front} and {back} added"}
        
    # getJokes()
    class _Read(Resource):
        def get(self):
            return jsonify(UsrAPI.local_dic) # init wikipedia by default

    class _Update(Resource):
        def put(self, nid):
            lst = []
            id = str(nid)
            body = request.get_json()
            UsrAPI.local_dic[id] = body
            return {"message" : f"{body} added"}

    class _WikiRead(Resource):
        def get(self):
            return jsonify(UsrAPI.serialize('wikipedia')) # init wikipedia by default

    # getJoke(id)
    class _ReadWithName(Resource): # read when url have name query satisfied
        def get(self, name):
            return jsonify(UsrAPI.serialize(name))# otherwise check with name
    class _Delete(Resource):
        def get(self, id):
            key = UsrAPI.local_dic.pop(id, None)
            return jsonify({"message": f" {key} deleted"})

    
    # getJoke(id)
   # class _ReadWithName(Resource): # read when url have name query satisfied
    #    def get(self, name):
     #       return jsonify()# otherwise check with name

    # getRandomJoke()
    #class _ReadRandom(Resource):
     #   def get(self):
      #      return jsonify() # this exists for some reason
    

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Create, '/card/create/<string:front>_<string:back>')
    api.add_resource(_Read, '/card/')
    api.add_resource(_WikiRead, '/wiki/')
    api.add_resource(_ReadWithName, '/wiki/<string:name>')
    api.add_resource(_Delete, 'card/delete/<string:id>')
    api.add_resource(_Update, 'card/update/<string:nid>')