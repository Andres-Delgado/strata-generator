from flask import Flask, request

from stratagenerator import StrataGenerator
from fileutils import FileUtils

app: Flask = Flask(__name__)

@app.route('/')
def list_files():
  # curl localhost:5000
  return FileUtils.list_roster_files()

@app.route('/', methods=['POST'])
def process_roster_file():
  # curl -X POST -H "Content-Type: application/json" -d '{"sync": true, "filename": "Tzeentch 2k"}' localhost:5000
  body: dict = request.get_json()
  StrataGenerator.process(body['filename'], body.get('sync', False))
  return body
