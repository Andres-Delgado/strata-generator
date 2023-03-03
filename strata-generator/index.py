from flask import Flask, jsonify, request
from stratagenerator import StrataGenerator

app: Flask = Flask(__name__)

@app.route('/')
def hello_world():
  return 'ayooo\n'

@app.route('/', methods=['POST'])
def process_roster_file():

  # curl -X POST -H "Content-Type: application/json" -d '{"sync": true, "filename": "Tzeentch 2k"}' http://localhost:5000/

  StrataGenerator.process()
  return request.get_json()