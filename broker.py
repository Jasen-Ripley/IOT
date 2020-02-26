from influxdb import InfluxDBClient
import paho.mqtt.client as mqtt
import datetime
import RPi.GPIO as GPIO


#setup board
GPIO.setmode(GPIO.BCM)

#setup pin as input
GPIO.setup(18, GPIO.OUT)

broker_address="192.168.0.34" #broker address (your pis ip address)

def on_message(client, userdata, message):
               print(message.topic + " " + str(message.payload))
               if message.topic == '/light':
                   lightvalue = message.payload.decode('ascii')
                   receiveTime = datetime.datetime.utcnow()
                   json_body = [{
                       "measurement": 'light',
                       "time": receiveTime,
                       "fields": {
                           "value": float(lightvalue)
                       }
                   }]
                   dbclient.write_points(json_body)
                   
               if message.topic == '/piled':
                              if message.payload.decode('ascii') == "on":
                                             GPIO.output(18, GPIO.HIGH)
                              else:
                                             GPIO.output(18, GPIO.LOW)
# Set up a client for InfluxDB
dbclient = InfluxDBClient('0.0.0.0', 8086, 'root', 'root', 'mydb')                        
        
client = mqtt.Client() #create new mqtt client instance

client.connect(broker_address) #connect to broker

client.on_message = on_message

client.subscribe("/light") #subscribe to topic

client.subscribe("/piled") #subscribe to topic

client.loop_start() #start client

#loop endlessly
try:
	while True:   # wait for ctrl-c
               pass
except KeyboardInterrupt:
	pass

client.loop_stop() #stop client
GPIO.cleanup()
