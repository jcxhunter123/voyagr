from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import os


app = Flask(__name__,static_folder= '/static')
api = Api(app)

class Igsearch(Resource):
    def get(self, username):
        print(username)
        os.system("instagram-scraper "+username+" -d './static/model_inputs/' -n -t image --profile-metada --media-metadata")
        return {'username':username}
 
class Questionnaire(Resource):
    def post(self):
        input_json = request.get_json(force=True) # force=True, above, is necessary if another developer forgot to set the MIME type to 'application/json'
        return jsonify(input_json)

api.add_resource(Igsearch, '/search/<username>')
api.add_resource(Questionnaire, '/questionnaire/answer')

if __name__ == '__main__':
    app.run(debug=True)
