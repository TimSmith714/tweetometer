# Tweet-o-meter adapted from MagPi version to use
# three LEDS
#https://github.com/topshed/tweetometer

import time, sys
from textblob import TextBlob
from twython import TwythonStreamer
import RPi.GPIO as GPIO

# Twitter App tokens and secret keys
APP_KEY = 'APP KEY HERE'
APP_SECRET = 'APP SECRET HERE'
OAUTH_TOKEN = 'TOKEN'
OAUTH_TOKEN_SECRET = 'TOKEN SEPARATE'

# Set the Pins

RED = 22
YELLOW = 17
GREEN = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

#Set the totals
totals = {'pos': 0, 'neg': 0, 'neu': 0}

def shineLED(colour):
    if colour == 'green':
        GPIO.output(RED, False)
        GPIO.output(YELLOW, False)
        GPIO.output(GREEN, True)
    elif colour == 'yellow':
        GPIO.output(RED, False)
        GPIO.output(YELLOW, True)
        GPIO.output(GREEN, False)
    elif colour == 'red':
        GPIO.output(RED, True)
        GPIO.output(YELLOW, False)
        GPIO.output(GREEN, False)


class MyStreamer(TwythonStreamer):
    def on_success(self,data): #When we get valid data
        if 'text' in data: # If the tweet has a text field
            tweet = data['text'].encode('utf-8')
            print(tweet) #display each tweet
            tweet_pro = TextBlob(data['text']) #Calculate sentiment
            #Adjust value below to tune setiment sensitivity
            if tweet_pro.sentiment.polarity > 0.1: #positive
                print('Positive')
                shineLED('green')# SHOW GREEN LED
                totals['pos']+=1
            elif tweet_pro.sentiment.polarity < -0.1: #negative
                print('Negative')
                # SHOW RED LED
                shineLED('red')
                totals['neg']+=1
            else:
                print('Neutral')
                # SHOW YELLOW LED
                shineLED('yellow')
                totals['neu']+=1
            overall_sentiment = max(totals.keys(),key=(lambda k: totals[k]))
            # Show the status LED colour
            print(totals)
            print('winning: ' + overall_sentiment)
            time.sleep(0.5) # Throttling

        def on_error(self, status_code, data): # catch and display Twython Errors
            print("Error: ")
            print( status_code)
            # FLASH RED LED

    # Start processing the stream
stream2 = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
while True: # Endless loop may want to adjust
    try:
        stream2.statuses.filter(track='BankHolidayMonday') # Change for a different keyword
    except KeyboardInterrupt: # Exit on Ctrl+C
        GPIO.cleanup()
        sys.exit()
    except: # Ignore all other errors
        continue
