import RPi.GPIO as GPIO
import random
import time
import spotipy
import spotipy.util as util
import datetime


#setup board
GPIO.setmode(GPIO.BCM)

light = [18,23,24,25]
button = [12,16,20,21]
#setup pin as input
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(light, GPIO.OUT)

#var
redclickedflag = False
blueclickedflag = False
level = 1
code = []
end = 3
year = []
day = []
month = []
hour = []
minute = []
numofalarm = 0
delete = 0
global first
first = 1

SPOTIPY_CLIENT_ID = '0057d6cc4ee04588b5965d9267cf973d'
SPOTIPY_CLIENT_SECRET = '0b5c72001cb64ddb97cf4d014c934117'
SPOTIPY_REDIRECT_URI = 'https://example.com/callback/'
scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state'
username = 'jasenripley'

playlists = ['spotify:playlist:3yWqySvWxg31ojLk1uANtq', 'spotify:playlist:0uqtYzb1wrhKpJ4MSdoLtO','spotify:playlist:4SvKX5rQ5zZ9LW4YUKFtG7', 'spotify:playlist:4Z95CkcAeidsIQxUDXslOQ', 'spotify:playlist:7dvT2tFRRsMyGepnAD0vZP', 'spotify:playlist:7dvT2tFRRsMyGepnAD0vZP', 'spotify:playlist:7dvT2tFRRsMyGepnAD0vZP']
token = util.prompt_for_user_token(username, scope , client_id = SPOTIPY_CLIENT_ID, client_secret = SPOTIPY_CLIENT_SECRET ,redirect_uri = SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

def getinput():
                redclickedflag = False
                blueclickedflag = False
                greenclickedflag = False
                yellowclickedflag = False
                while True:
                                switchred = GPIO.input(button[0])
                                switchblue = GPIO.input(button[1])
                                switchgreen = GPIO.input(button[2])
                                switchyellow = GPIO.input(button[3])
                                if (switchred and not redclickedflag):
                                                #set as clicked
                                                redclickedflag = True;
                                if (not switchred and redclickedflag):
                                                #set as not clicked
                                                redclickedflag = False;
                                                return(0)
                                
                                if (switchblue and not blueclickedflag):
                                                #set as clicked
                                                blueclickedflag = True;
                                if (not switchblue and blueclickedflag):
                                                #set as not clicked
                                                blueclickedflag = False;
                                                return(1)
                                if (switchgreen and not greenclickedflag):
                                                #set as clicked
                                                greenclickedflag = True;
                                if (not switchgreen and greenclickedflag):
                                                #set as not clicked
                                                greenclickedflag = False;
                                                return(2)
                                
                                if (switchyellow and not yellowclickedflag):
                                                #set as clicked
                                                yellowclickedflag = True;
                                if (not switchyellow and yellowclickedflag):
                                                #set as not clicked
                                                yellowclickedflag = False;
                                                return(3)
                

def startgame(level, code):
                if level == 1:
                                print("press a button to start Simon Says!")
                                getinput()

                nextlight = random.randint(0,3)
                code.append(nextlight)
                for x in code:
                                GPIO.output(light[x], GPIO.HIGH)
                                time.sleep(.5)
                                GPIO.output(light[x], GPIO.LOW)
                                time.sleep(.25)
                for x in code:
                                print("press a button")
                                guess = getinput()
                                if x == guess:
                                                print("Correct!")
                
                                else:
                                                print("Incorrect!")
                                                level = 1
                                                code = []
                                                startgame(1, code)
                if (level == end):
                                level = 1
                                code = []
                                sp.pause_playback(device_id = '3ca9457b4cec4b390aba0107e0d43f639c857457')
                                return
                print()
                print("New Level")
                startgame(level + 1, code)

alarm = 1
while alarm != 0:
                year.append(input("year(xxxx): "))
                month.append(input("month(xx): "))
                day.append(input("day(xx): "))
                hour.append(input("hour(in military time, xx): "))
                minute.append(input("minutes: "))
                alarm = input("would you like to add another alarm? (y/n)")
                numofalarm = numofalarm + 1
                if alarm == 'y':
                                alarm = 1
                else:
                                alarm = 0

#date = datetime.date(int(year),int(month),int(day))
while alarm == 0:
                now = time.localtime()
                for i in range(0, numofalarm):
                                if (int(year[i]) == now[0]) & (int(month[i]) == now[1]) & (int(day[i]) == now[2]) & (int(hour[i]) == now[3]) & (int(minute[i]) == now[4]):
                                                date = datetime.date(int(year[i]),int(month[i]),int(day[i]))
                                                delete = i
                                                alarm = 1
                                                if first == 1:
                                                                sp.shuffle(state=True, device_id = '3ca9457b4cec4b390aba0107e0d43f639c857457' )
                                                                sp.start_playback(device_id = '3ca9457b4cec4b390aba0107e0d43f639c857457', context_uri = playlists[date.weekday()])
                                                                first = 0
                                                startgame(1, [])
                if alarm == 1:
                                del year[delete]
                                del day[delete]
                                del month[delete]
                                del hour[delete]
                                del minute[delete]
                                first = 1
                                numofalarm = numofalarm - 1
                                if year != []:
                                                alarm = 0
