import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO

#setup board
GPIO.setmode(GPIO.BCM)

#setup pin as input
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)
#var
clickedflag = False
arduinoled = GPIO.LOW

broker_address="192.168.0.34" #broker address (your pis ip address)

def on_message(client, userdata, message):
                if ("on" in message.payload.decode('ascii')):
                                GPIO.output(18, GPIO.LOW) #pi off
                                print("off")
                else:
                                GPIO.output(18, GPIO.HIGH) #pi on
                                print("on")
                
                        
        
client = mqtt.Client() #create new mqtt client instance

client.connect(broker_address) #connect to broker

client.on_message = on_message

client.subscribe("/PI") #subscribe to topic

client.loop_start() #start client

#loop endlessly
try:
	while True:   # wait for ctrl-c
		#get button state
                buttonstate = GPIO.input(21)

                #if the button is pressed and was not previously clicked
                if (buttonstate and not clickedflag):
                        #set as clicked
                        clickedflag = True;

                #if button is not clicked and was previously not clicked
                if (not buttonstate and clickedflag):

                                #set as not clicked
                        clickedflag = False;
                        if (arduinoled == GPIO.HIGH):
                                arduinoled = GPIO.LOW
                                #GPIO.output(18, GPIO.LOW)
                                client.publish("/aled","off") #send message
                        elif(arduinoled == GPIO.LOW):
                                arduinoled = GPIO.HIGH
                                #GPIO.output(18, GPIO.HIGH)
                                client.publish("/aled","on") #send message

except KeyboardInterrupt:
	pass

client.loop_stop() #stop client
