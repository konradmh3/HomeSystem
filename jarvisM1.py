#################################################################################################################
# Because i really want to build on this program for a while...im going to take a break in adding more commands #
# For now, i will improve the commands i have such as the spotify app, the inconsistant voices                  #
# And lastly introduce jarvis to spotify with spotify api so that he can play music for me on voice command     #
#################################################################################################################

from __future__ import print_function


# import the necessary libraries
import datetime
import os.path
import os
import speech_recognition as sr
from playsound import playsound
import random
import requests
# from time import sleep


# Add LIFX Authorization
token = "c07545722e208de4d94b41b0d7497aaebe7b0cfc73c32bf5d76241b54fd37b39"
headers = {
    "Authorization": "Bearer %s" %token ,
    }

# Add Spotipy Authorization
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# credentials
client_id = "96ce87edae0949aaaeec8e5b82678a3d"
client_secret = "0cf5e905b5024144a7e58c1062590571"
redirect_uri = "http://localhost:8080" # this has to match uri in spotify developer dashboard
scope = "user-modify-playback-state" # this scope allows us to play music and control playback
# Use the SpotifyOAuth object to authenticate with the Spotify API and get a token that can adjust playback
# token is cached in the .cache file
spotify_oauth = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope)
sp = spotipy.Spotify(client_credentials_manager=spotify_oauth)
# we can now use sp to make calls to the spotify api


# Create a dictionary of possible input phrases and their corresponding commands
commands = {
    "lights on": ["turn on the lights", "lights on", "turn on lights", "turn on the light", "light on"],
    "lights off": ["turn off the lights", "lights off", "turn off lights", "turn off the light", "light off"],
    "play": ["play", "on spotify"],
    "give date and time": ["what time is it", "what is the time", "time", "tell me the time", "what's the time", "what is the date", "what date is it", "date", "tell me the date", "what's the date"],
    "list commands": ["help", "list commands", "list command", "commands", "command", "list", "list all commands", "list all command"],
    "stop": ["nevermind", "never mind", "cancel", "stop", "quit", "exit", "close", "end"],
    "kill": ["kill", "die"]
}

############################################# RESPONSE CHOOSER ################################################# NEEDS TO BE FIXED AS THE PATH IS WRONG CONFIRMED
def returnRandomSound(foldername):
                path = foldername
                files = os.listdir(path)
                randomFile = random.choice(files)
                return foldername + "/" + randomFile

# Now lets make a function to listen for speech and convert it to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        audio = r.listen(source, phrase_time_limit=4) 
    ###### just added the phrase_time_limit=4, ^, we MAY have to come back later and connect commands that are cut off by this ######
        try:
            text = r.recognize_google(audio).lower()
            print(text)
            # if "jarvis" not in text: we want to return nothing if the wake word is not in the text
            if "jarvis" in text:
                return text
            else:
                print("couldn't understand or no wake word, pls try again")
                return ""
        except:
            print("couldn't understand or no wake word, pls try again")
            return ""
            # the above try and except is to catch any errors that may occur when listening for speech
            # this is because sometimes the speech recognition library will not be able to understand what the user is saying
            # so we will just return an empty string instead of an error crashing the program

# Now lets make a function to perform the command
def perform_command(command, text):
    if command == "lights on":
        # now we can run the command to turn on the lights
        # we can do this by running a bash script
        payload = {
            "power": "on",
            }
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)       
        # print(response.text)
        # playsound(returnRandomSound("lightsOnSounds"))
    elif command == "lights off":
        # now we can run the command to turn off the lights
        payload = {
            "power": "off",
            }
        response = requests.put('https://api.lifx.com/v1/lights/all/state', data=payload, headers=headers)       
        # print(response.text)
        # playsound(returnRandomSound("lightsOffSounds"))
    elif command == "play":
        # first we need to get the song name from the text
        try:
            song_name = text.split("play")[1].strip()
            print("playing " + song_name)
            results = sp.search(q=song_name, type="track")
            track = results["tracks"]["items"][0]
            uri = track["uri"]
            url = track["external_urls"]["spotify"]
            # play the song
            sp.start_playback(uris=[uri])
        except:
            pass
    elif command == "give date and time":
        # now we can give the current date and time
        now = datetime.datetime.now()
        print("The current date and time is " + now.strftime("%m-%d-%Y %H:%M:%S"))
    elif command == "list commands":
        # now we can list all the available commands
        print("Here is a list of available commands:")
        for key in commands.keys():
            print("- " + key)
    elif command == "stop":
        # lets also stop spotify playback if playing
        try:
            sp.pause_playback()
        except:
            pass
        # now we can exit the program
        print("stopping...")
    elif command == "kill":
        # now we can kill the program
        print("Killing program...")
        exit()


# Now we can loop indefinitely to listen for and perform commands
while True:
    text = listen()
    for key in commands.keys():
        if any(input_phrase in text for input_phrase in commands[key]):
            perform_command(key, text)
            break

# This code uses a dictionary to store the different input phrases and their corresponding commands,
# and then uses a single function (perform_command()) to handle all the different types of commands.
# The while loop at the end of the code listens for input phrases and then calls the perform_command()
# function to perform the corresponding command. This rewritten code is more efficient and easier to 
# maintain than the original code.