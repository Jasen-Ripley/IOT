from flask import Flask, request, json
from flask_restful import Resource, Api
from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import datetime
import RPi.GPIO as GPIO

broker_address="192.168.0.34" #broker address (your pis ip address)

client = mqtt.Client() #create new mqtt client instance

client.connect(broker_address) #connect to broker

dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')  

app = Flask(__name__)
api = Api(app)

class Test(Resource):
        def post(self):
                value = request.get_data()
                value = json.loads(value)
                print("post" + str(value))
                if value['device'] == "pi":
                        client.publish("/piled", value['state'])
                else:
                        client.publish("/arduino", value['state'])
        def get(self):
                #database query
                query = 'select mean("value") from "light" where "time" > now()-10s'
                #make query
                result = dbclient.query(query)
                mean = list(result.get_points(measurement='light'))[0]['mean']
                return {'avg':mean}
	
api.add_resource(Test, '/test')

app.run(host='0.0.0.0', debug=True)
