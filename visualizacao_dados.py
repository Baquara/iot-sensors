from sqlalchemy import *
import sys
from PIL import Image, ImageDraw
from flask import Flask,jsonify, render_template, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
from flask_cors import CORS

engine = create_engine('sqlite:///./banco.db?check_same_thread=False')
engine.echo = False
metadata = MetaData(engine)


def dbresults(com):
    data = engine.execute(com)
    if data is not None:
        return [{key: value for key, value in row.items()} for row in data if row is not None]
    else:
        return [{}]


@app.route("/")
def render_page():
    return render_template("index.html")

@app.route("/teste")
def test():
    response = str(dbresults('SELECT * FROM mote WHERE moteid=1 ORDER BY epoch'))
    return response

#Gerar tabela para sensor
@app.route('/data', methods=['POST'])
def post_table():
    sensor = request.json['sensor']
    data = dbresults('SELECT * FROM mote WHERE moteid='+sensor)
    return jsonify(data),200

#Gerar imagem
@app.route('/generate', methods=['POST'])
def post_image():
    data=None
    z = request.json['z']
    data = dbresults('SELECT * FROM mote WHERE moteid='+str(z)+" ORDER BY moteid ASC LIMIT 1")
    for x in data:
        px = float(x['x location'])
        py = float(x['y location'])
        return jsonify({"i":z,"x":px,"y":py}),200


if __name__ == '__main__':
    app.run()
