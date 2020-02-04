import RPi.GPIO as GPIO

#setup board
GPIO.setmode(GPIO.BCM)

#setup pin as input
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)
#var
clickedflag = False

#loop endlessly
while True:

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
                        if (GPIO.input(18) == GPIO.HIGH):
                                GPIO.output(18, GPIO.LOW)
                        elif(GPIO.input(18) == GPIO.LOW):
                                GPIO.output(18, GPIO.HIGH)
