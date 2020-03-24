from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os


app = Flask(__name__)
api = Api(app)

class Igsearch(Resource):
    def get(self, username):
        # os.system("instagram-scraper "+username)
        return {'username':username}
 
class Questionnaire(Resource):
    def post(self):
        input_json = request.get_json(force=True) # force=True, above, is necessary if another developer forgot to set the MIME type to 'application/json'
        return jsonify(input_json)

api.add_resource(Igsearch, '/search/<username>')
api.add_resource(Questionnaire, '/questionnaire/answer')

if __name__ == '__main__':
    app.run(debug=True)
