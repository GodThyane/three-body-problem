from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import cross_origin, CORS
from simulation import ThreeBody
from simulation import ImgThreeBody
import os

app = Flask(__name__)
# Se inicializan los CORS para evitar problemas al momento de hacer peticiones al backend
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = 'secret'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')


@socketio.on('event')
@cross_origin()
def handleMessage(message):
    body = message['body']

    three = ThreeBody(body['masseRef'], body['disRef'], body['velRef'], body['tRef'], body['masses'],
                      body['positions'], body['velocities'], body['t'],
                      str(body['id']))
    three.Simulation()
    emit("event", {"isGif": True, "res": three.gif()})
    strGif = "threeBody" + str(body['id']) + ".gif"
    os.remove(strGif)
    return 'OK'


@socketio.on('img')
@cross_origin()
def handleMessage(message):
    body = message['body']

    three = ImgThreeBody(body['masses'], body['positions'])
    emit("event", {"isGif": False, "res": three.GetImg()})
    return 'OK'


if __name__ == '__main__':
    socketio.run(app)
