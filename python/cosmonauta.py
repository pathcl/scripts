#!/usr/bin/python
import tweepy
import pywapi
import random
 
CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_KEY=""
ACCESS_SECRET=""
 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)


random = random.randint(0,1000)
weather = pywapi.get_weather_from_weather_com('CIXX0020:1')
tweet = "@Tia_Ivonne It is " + weather['current_conditions']['text'].lower() + " and " + weather['current_conditions']['temperature'] + "C now in Santiago" + " Max " + weather["forecasts"][0]["high"] + " Min " + weather["forecasts"][0]["low"] + " feels like " + weather['current_conditions']['feels_like'] + " your lucky number is: " + str(random) 
api.update_status(tweet)
