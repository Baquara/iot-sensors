from sqlalchemy import *
import sys
from PIL import Image, ImageDraw
from flask import Flask,jsonify, render_template, request
from flask_cors import CORS
from statistics import mode
from numpy import mean


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
    voltagens = []
    umidade = []
    temperaturas = []
    luminosidades = []
    modavol = 0
    modaumidade =0
    modatemperaturas = 0
    modaluz = 0
    tamanho = 0
    for x in data:
        try:
            voltagens.append(float(x["voltage"]))
        except:
            voltagens.append(0)
        try:
            umidade.append(float(x["humidity"]))
        except:
            umidade.append(0)
        try:
            temperaturas.append(float(x["temperature"]))
        except:
            temperaturas.append(0)
        try:
            luminosidades.append(float(x["light"]))
        except:
            luminosidades.append(0)
        tamanho+=1
    import matplotlib.pyplot as plt
    plt.plot(voltagens, 'r--',umidade, 'b--',temperaturas,'g--',luminosidades,'y--')
    plt.savefig('chart.png')
    from PIL import Image
    image = Image.open('chart.png')
    image.show()
    modavol = mode(voltagens)
    modaumidade = mode(umidade)
    modatemperaturas = mode(temperaturas)
    modaluz = mode(luminosidades)
    print("Moda voltagem: "+str(modavol))
    print("Moda umidade: "+str(modaumidade))
    print("Moda temperaturas: "+str(modatemperaturas))
    print("Moda luz: "+str(modaluz))
    #for x in data:
        #input(str(x["epoch"]) + " "+(x["voltage"]))
        #if(int(x["voltage"]) is not modavol):
            #print("Elemento de epoch "+str(x["epoch"])+" apresenta voltagem divergente.")
        #if( (int(float(x["humidity"])) - modahumidades) > 10 or (int(float(x["humidity"])) - modahumidades) < -10):
            #print("Elemento de epoch "+str(x["epoch"])+" apresenta humidade divergente. Humidade comum ="+str(modahumidades)+", humidade do elemento: "+str(x["humidity"]))
        #if((int(float(x["temperature"])) - modatemperaturas) > 100):
            #print("Elemento de epoch "+str(x["epoch"])+" apresenta temperatura divergente. Temperatura comum ="+str(modatemperaturas)+", temperatura do elemento: "+str(x["temperature"]))

    return jsonify(data,{"Moda_voltagem":modavol,"Moda_umidade":modaumidade,"Moda_temperaturas":modatemperaturas,"Moda_luminosidade":modaluz}),200

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
