from flask import Flask, request
from flask_cors import CORS
import json
import pprint
import os
app = Flask(__name__)
CORS(app)

@app.route('/update', methods=['POST'])
def post_route():
    try:
        data = request.get_json()
        pprint.pprint(data)
        with open(os.getenv('JSON_DATAVIZ_DATABASE_FILE','database.json'),"w") as f:
            json.dump(data,f)
        # JSON_DATAVIZ_DATABASE_FILE
        return {'STATUS':'SUCCESS'}
    except Exception as e:
        print(str(e))
        return {'STATUS':'FAILED'}

if __name__=="__main__":
  app.run(host='0.0.0.0')