import pyttsx3
import speech_recognition as sr
import datetime 
from datetime import date
import calendar
import time
import math
import wikipedia
import webbrowser
import os
import smtplib
import winsound
import pyautogui
import cv2
from pygame import mixer
from tkinter import *
import tkinter.messagebox as message
from sqlite3 import *
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction import text
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import matplotlib.pyplot as plt

# Feature extraction
import scipy
import librosa
import python_speech_features as mfcc
import os
from scipy.io.wavfile import read

# Model training
from sklearn.mixture import GaussianMixture as GMM
from sklearn import preprocessing
import pickle

# Live recording
import sounddevice as sd
import soundfile as sf

data = pd.read_csv("articles.csv", encoding='latin1')
conn = connect("voice_assistant_asked_questions.db")

conn.execute("CREATE TABLE IF NOT EXISTS `voicedata`(id INTEGER PRIMARY KEY AUTOINCREMENT,command VARCHAR(201))")

conn.execute("CREATE TABLE IF NOT EXISTS `review`(id INTEGER PRIMARY KEY AUTOINCREMENT, review VARCHAR(50), type_of_review VARCHAR(50))")

conn.execute("CREATE TABLE IF NOT EXISTS `emoji`(id INTEGER PRIMARY KEY AUTOINCREMENT,emoji VARCHAR(201))")

global query
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def getdate():

   return datetime.datetime.now()

z=getdate()
Total=0

def find_files(filename, search_path):
    result = []

# Wlaking top-down from the root
    for root, dir, files in os.walk(search_path):
        if filename in files:
            result.append(os.path.join(root, filename))
    return result          

class Items:
    """
        List stored as a file in ~/.todo
    """

    x=os.getcwd()
    FILE_LOCATION = fr"{x}\todo.txt"
    Done_Location= fr"{x}\done.txt"


    def __init__(self,arr):
        self.items = open(self.FILE_LOCATION, "r").readlines()
        self.ar=arr

    def listAdd(self):
        print(type(self.ar()))
        print("Added item: " + self.ar())
        with open(self.FILE_LOCATION, "a+") as f:
            f.writelines(self.ar() + "\n")



    def listShow(self):
        print("\n        TODO\n" + "-"*75)

        if not self.items:
            print("No tasks to be done.\n")
        else:
            for sno, item in enumerate(self.items):
                print(str(sno+1) + ". " + item)




    def listDelete(self):


      try:
        doneTask = self.items.pop(int(self.ar()) - 1)

        print("Completed task no. " +
               str(self.ar()) +
              " (%s), deleted todo" % doneTask.strip()
        )
        print(f"Deleted item:{self.ar()}")

        with open(self.FILE_LOCATION, "w") as f:
            for item in self.items:
                f.writelines(item)
      except Exception as e:
          print(f"Error: todo {self.ar()} does not exist. Nothing deleted.")


    def listdone(self):

     try:

        g=self.items[int(self.ar())-1]
        print(f"Marked todo {self.ar()} as done")

        
        with open(self.Done_Location, 'a') as f:
                f.write(f"x {z} {g} ")
        doneTask = self.items.pop(int(self.ar()) - 1)

        with open(self.FILE_LOCATION, "w") as f:
            for item in self.items:
                f.writelines(item)
     except Exception as e:
         print(f"Error: todo {self.ar()} does not exist.")


    def report(self):
        with open (self.Done_Location,"r") as f:
            Counter=-1
            Content=f.read()
            CoList=Content.split("\n")
            for i in CoList:
                if i:
                    Counter+=1


        print(f"{z}    Pending:{len(self.items)}  Completed:{Counter}")







def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def get_MFCC(sr,audio):
    
    features = mfcc.mfcc(audio, sr, 0.025, 0.01, 13, appendEnergy = False)
    features = preprocessing.scale(features)
    
    return features

def record_and_predict(sr=16000, channels=1, duration=3, filename='pred_record.wav'):
    speak("Speak now")
    gmm_male=pickle.load(open('male.gmm', 'rb'))
    gmm_female=pickle.load(open('female.gmm', 'rb'))
    recording = sd.rec(int(duration * sr), samplerate=sr, channels=channels).reshape(-1)
    sd.wait()
    
    features = get_MFCC(sr,recording)
    scores = None

    log_likelihood_male = np.array(gmm_male.score(features)).sum()
    log_likelihood_female = np.array(gmm_female.score(features)).sum()


    if log_likelihood_male >= log_likelihood_female:
        #return("Male")
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour<12:
            speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("I am voice assistant Sheesh Sir. Please tell me how may I help you.")
    else:
        #return("Female")
        hour = int(datetime.datetime.now().hour)
        if hour >= 0 and hour<12:
            speak("Good Morning!")
        elif hour >= 12 and hour < 18:
            speak("Good Afternoon!")
        else:
            speak("Good Evening!")
        speak("I am voice assistant Sheesh Mam. Please tell me how may I help you.")

 
def detect_face():
    cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frames = video_capture.read()

        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
                )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frames)
        speak("detecting face")
        print("Detecting face.....")
        time.sleep(10)      
        pyautogui.press('q')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour<12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    gmm_male=pickle.load(open('male.gmm', 'rb'))
    gmm_female=pickle.load(open('female.gmm', 'rb'))
    recording = sd.rec(int(duration * sr), samplerate=sr, channels=channels).reshape(-1)
    sd.wait()
    
    features = get_MFCC(sr,recording)
    scores = None

    log_likelihood_male = np.array(gmm_male.score(features)).sum()
    log_likelihood_female = np.array(gmm_female.score(features)).sum()

    if log_likelihood_male >= log_likelihood_female:
        #return("Male")
        speak("I am voice assistant Sheesh Mam. Please tell me how may I help you.")
    else:
        #return("Female")
        speak("I am voice assistant Sheesh Mam. Please tell me how may I help you.")
    #speak("I am voice assistant Sheesh Mam. Please tell me how may I help you.")
    
def takeCommand():
    global query
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.9 
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language='en-in')
        print(f"User said: {query}\n")
        
    except Exception as e:
        #print(e)     
        print("Say that again please...")  
        #speak('Say that again please...')
        return "None"    
    return query

def calculator():
    global query
    try:
        if 'add' in query or 'edi' in query:
            speak('Enter a number')
            a = float(input("Enter a number:"))
            speak('Enter another number to add')
            b = float(input("Enter another number to add:"))
            c = a+b
            print(f"{a} + {b} = {c}")
            speak(f'The addition of {a} and {b} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
                
        elif 'sub' in query:
            speak('Enter a number')
            a = float(input("Enter a number:"))
            speak('Enter another number to subtract')
            b = float(input("Enter another number to subtract:"))
            c = a-b
            print(f"{a} - {b} = {c}")
            speak(f'The subtraction of {a} and {b} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
                    
        elif 'mod' in query:
            speak('Enter a number')
            a = float(input("Enter a number:"))
            speak('Enter another number')
            b = float(input("Enter another number:"))
            c = a%b
            print(f"{a} % {b} = {c}")
            speak(f'The modular division of {a} and {b} is equal to {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
                    
        elif 'div' in query:
            speak('Enter a number as dividend')
            a = float(input("Enter a number:"))
            speak('Enter another number as divisor')
            b = float(input("Enter another number as divisor:"))
            c = a/b
            print(f"{a} / {b} = {c}")
            speak(f'{a} divided by {b} is equal to {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        elif 'multi' in query:
            speak('Enter a number')
            a = float(input("Enter a number:"))
            speak('Enter another number to multiply')
            b = float(input("Enter another number to multiply:"))
            c = a*b
            print(f"{a} x {b} = {c}")
            speak(f'The multiplication of {a} and {b} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        elif 'square root' in query:
            speak('Enter a number to find its sqare root')
            a = float(input("Enter a number:"))
            c = a**(1/2)
            print(f"Square root of {a} = {c}")
            speak(f'Square root of {a} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        elif 'square' in query:
            speak('Enter a number to find its sqare')
            a = float(input("Enter a number:"))
            c = a**2
            print(f"{a} x {a} = {c}")
            speak(f'Square of {a} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        elif 'cube root' in query:
            speak('Enter a number to find its cube root')
            a = float(input("Enter a number:"))
            c = a**(1/3)
            print(f"Cube root of {a} = {c}")
            speak(f'Cube root of {a} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        elif 'cube' in query:
            speak('Enter a number to find its sqare')
            a = float(input("Enter a number:"))
            c = a**3
            print(f"{a} x {a} x {a} = {c}")
            speak(f'Cube of {a} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
                
        elif 'fact' in query:
            try:
                n = int(input('Enter the number whose factorial you want to find:'))
                fact = 1
                for i in range(1,n+1):
                    fact = fact*i
                print(f"{n}! = {fact}")
                speak(f'{n} factorial is equal to {fact}. Your answer is {fact}.')
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
            except Exception as e:
                #print(e)
                speak('I unable to calculate its factorial.')
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
                    
        elif 'power' in query or 'raise' in query:
            speak('Enter a number whose power you want to raised')
            a = float(input("Enter a number whose power to be raised :"))
            speak(f'Enter a raised power to {a}')
            b = float(input(f"Enter a raised power to {a}:"))
            c = a**b
            print(f"{a} ^ {b} = {c}")
            speak(f'{a} raise to the power {b} = {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        
                
        elif 'percent' in query:
            speak('Enter a number whose percentage you want to calculate')
            a = float(input("Enter a number whose percentage you want to calculate :"))
            speak(f'How many percent of {a} you want to calculate?')
            b = float(input(f"Enter how many percentage of {a} you want to calculate:"))
            c = (a*b)/100
            print(f"{b} % of {a} is {c}")
            speak(f'{b} percent of {a} is {c}. Your answer is {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
            
        elif 'interest' in query:
            speak('Enter the principal value or amount')
            p = float(input("Enter the principal value (P):"))
            speak('Enter the rate of interest per year')
            r = float(input("Enter the rate of interest per year (%):"))
            speak('Enter the time in months')
            t = int(input("Enter the time (in months):"))            
            interest = (p*r*t)/1200
            sint = round(interest)
            fv = round(p + interest) 
            print(f"Interest = {interest}")
            print(f"The total amount accured, principal plus interest, from simple interest on a principal of {p} at a rate of {r}% per year for {t} months is {p + interest}.")
            speak(f'interest is {sint}. The total amount accured, principal plus interest, from simple interest on a principal of {p} at a rate of {r}% per year for {t} months is {fv}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
                
        
    
        elif 'si' in query:
            speak('Enter the angle in degree to find its sine value')
            a = float(input("Enter the angle:"))
            b = a * 3.14/180
            c = math.sin(b)
            speak('Here is your answer.')
            print(f"sin({a}) = {c}")
            speak(f'sin({a}) = {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        elif 'cos' in query:
            speak('Enter the angle in degree to find its cosine value')
            a = float(input("Enter the angle:"))
            b = a * 3.14/180
            c = math.cos(b)
            speak('Here is your answer.')
            print(f"cos({a}) = {c}")
            speak(f'cos({a}) = {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
                
        elif 'cot' in query or 'court' in query:
            try:
                speak('Enter the angle in degree to find its cotangent value')
                a = float(input("Enter the angle:"))
                b = a * 3.14/180
                c = 1/math.tan(b)
                speak('Here is your answer.')
                print(f"cot({a}) = {c}")
                speak(f'cot({a}) = {c}')
                
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
            except Exception as e:
                print("infinity")
                speak('Answer is infinity')
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
                
            
                
        elif 'tan' in query or '10' in query:
            speak('Enter the angle in degree to find its tangent value')
            a = float(input("Enter the angle:"))
            b = a * 3.14/180
            c = math.tan(b)
            speak('Here is your answer.')
            print(f"tan({a}) = {c}")
            speak(f'tan({a}) = {c}')
            
            speak('Do you want to do another calculation?')
            query = takeCommand().lower()
            if 'y' in query:
                speak('ok which calculation you want to do?')
                query = takeCommand().lower()
                calculator()
            else:
                speak('ok')
        
                
        elif 'cosec' in query:
            try:
                speak('Enter the angle in degree to find its cosecant value')
                a = float(input("Enter the angle:"))
                b = a * 3.14/180
                c =1/ math.sin(b)
                speak('Here is your answer.')
                print(f"cosec({a}) = {c}")
                speak(f'cosec({a}) = {c}')
                
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
            except Exception as e:
                print('Infinity')
                speak('Answer is infinity')
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
                    
        elif 'caus' in query:
            try:
                speak('Enter the angle in degree to find its cosecant value')
                a = float(input("Enter the angle:"))
                b = a * 3.14/180
                c =1/ math.sin(b)
                speak('Here is your answer.')
                print(f"cosec({a}) = {c}")
                speak(f'cosec({a}) = {c}')
                
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
            except Exception as e:
                print('Infinity')
                speak('Answer is infinity')
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
                
        elif 'sec' in query:
            try:
                speak('Enter the angle in degree to find its secant value')
                a = int(input("Enter the angle:"))
                b = a * 3.14/180
                c = 1/math.cos(b)
                speak('Here is your answer.')
                print(f"sec({a}) = {c}")
                speak(f'sec({a}) = {c}')
                
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
            except Exception as e:
                print('Infinity')
                speak('Answer is infinity')
                speak('Do you want to do another calculation?')
                query = takeCommand().lower()
                if 'y' in query:
                    speak('ok which calculation you want to do?')
                    query = takeCommand().lower()
                    calculator()
                else:
                    speak('ok')
            
                
    except Exception as e:
        speak('I unable to do this calculation.')
        speak('Do you want to do another calculation?')
        query = takeCommand().lower()
        if 'y' in query:
            speak('ok which calculation you want to do?')
            query = takeCommand().lower()
            calculator()
        else:
            speak('ok')
        
        
        
def callback(r,c):
    global player
    
    if player == 'X' and states[r][c] == 0 and stop_game == False:
        b[r][c].configure(text='X',fg='blue', bg='white')
        states[r][c] = 'X'
        player = 'O'
        
    if player == 'O' and states[r][c] == 0 and stop_game == False:
        b[r][c].configure(text='O',fg='red', bg='yellow')
        states[r][c] = 'O'
        player = 'X'
    check_for_winner()
    
def check_for_winner():
    global stop_game
    global root
    for i in range(3):
        if states[i][0] == states[i][1]== states[i][2]!=0:
            b[i][0].config(bg='grey')
            b[i][1].config(bg='grey')
            b[i][2].config(bg='grey')
            
            stop_game = True
            
            root.destroy()
            
    for i in range(3):
        if states[0][i] == states[1][i] == states[2][i]!= 0:
            b[0][i].config(bg='grey')
            b[1][i].config(bg='grey')
            b[2][i].config(bg='grey')
            
            stop_game = True
            
            root.destroy()
        
        if states[0][0] == states[1][1]== states[2][2]!= 0:
            b[0][0].config(bg='grey') 
            b[1][1].config(bg='grey')
            b[2][2].config(bg='grey')
            
            stop_game = True
            
            root.destroy()
            
        if states[2][0] == states[1][1] == states[0][2]!= 0:
            b[2][0].config(bg='grey')
            b[1][1].config(bg='grey')
            b[0][2].config(bg='grey')
            
            stop_game = True
            
            root.destroy()

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('xyz123@gmail.com','password')
    server.sendmail('xyz123@gmail.com',to,content)
    server.close()
    
def brightness():
    try:
        query = takeCommand().lower()
        if '25' in query:
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(1610,960)
            pyautogui.click()
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            speak('If you again want to change brihtness, say, change brightness')
        elif '50' in query:
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(1684,960)   
            pyautogui.click()
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            speak('If you again want to change brihtness, say, change brightness')
        elif '75' in query:
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(1758,960)   
            pyautogui.click()
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            speak('If you again want to change brihtness, say, change brightness')
        elif '100' in query or 'full' in query:
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(1835,960)   
            pyautogui.click()
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            speak('If you again want to change brihtness, say, change brightness')
        else: 
            speak('Please select 25, 50, 75 or 100....... Say again.')
            brightness()
    except exception as e:
        #print(e)
        speak('Something went wrong')
        
def close_window():
    try: 
        if 'y' in query:
            pyautogui.moveTo(1885,10)
            pyautogui.click()
        else:
            speak('ok')
            pyautogui.moveTo(1000,500)
    except exception as e:
        #print(e)
        speak('error')
        
def whatsapp():
    query = takeCommand().lower()
    if 'y' in query:
        pyautogui.moveTo(250,1200) 
        pyautogui.click()
        time.sleep(1)
        pyautogui.write('whatsapp')
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.moveTo(100,140)   
        pyautogui.click() 
        speak('To whom you want to send message,.....just write the name here in 5 seconds')
        time.sleep(7)
        pyautogui.moveTo(120,300)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(800,990)
        pyautogui.click()
        speak('Say the message,....or if you want to send anything else,...say send document, or say send emoji')
        query = takeCommand()
        if ('sent' in query or 'send' in query) and 'document' in query:
            pyautogui.moveTo(660,990)   
            pyautogui.click() 
            time.sleep(1)
            pyautogui.moveTo(660,740)
            pyautogui.click()
            speak('please select the document within 10 seconds')
            time.sleep(12)
            speak('Should I send this document?')
            query = takeCommand().lower()
            if 'y' in query and 'no' not in query:
                speak('sending the document......')
                pyautogui.press('enter')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            elif ('remove' in query or 'cancel' in query or 'delete' in query or 'clear' in query) and ('document' in query or 'message' in query or 'it' in query or 'emoji' in query or 'select' in query):
                pyautogui.doubleClick(x=800, y=990)
                pyautogui.press('backspace')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            else:
                speak('ok')
        elif ('sent' in query or 'send' in query) and 'emoji' in query:
            pyautogui.moveTo(620,990)  
            pyautogui.click() 
            pyautogui.moveTo(670,990)
            pyautogui.click()
            pyautogui.moveTo(650,580) 
            pyautogui.click()
            speak('please select the emoji within 10 seconds')
            time.sleep(11)
            speak('Should I send this emoji?')
            query = takeCommand().lower()
            if 'y' in query and 'no' not in query:
                speak('Sending the emoji......')
                pyautogui.press('enter')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            elif ('remove' in query or 'cancel' in query or 'delete' in query or 'clear' in query) and ('message' in query or 'it' in query or 'emoji' in query or 'select' in query):
                pyautogui.doublClick(x=800, y=990)
                speak('Do you want to send message again to anyone?')
                whatsapp()
            else:
                speak('ok')
        else:
            pyautogui.write(f'{query}')
            speak('Should I send this message?')
            query = takeCommand().lower()
            if 'y' in query and 'no' not in query:
                speak('sending the message......')
                pyautogui.press('enter')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            elif ('remove' in query or 'cancel' in query or 'delete' in query or 'clear' in query) and ('message' in query or 'it' in query or 'select' in query):
                pyautogui.doubleClick(x=800, y=990)               
                pyautogui.press('backspace')
                speak('Do you want to send message again to anyone?')
                whatsapp()
            else:
                speak('ok')
    else:
        speak('ok')
        
def alarm():
    root = Tk() 
    root.title('Sheesh Alarm-Clock') 
    speak('Please enter the time in the format hour, minutes and seconds. When the alarm should rang?')
    speak('Please enter the time greater than the current time')
    def setalarm():
        alarmtime = f"{hrs.get()}:{mins.get()}:{secs.get()}"
        print(alarmtime)
        if(alarmtime!="::"):
            alarmclock(alarmtime) 
        else:
            speak('You have not entered the time.')
    def alarmclock(alarmtime): 
        while True:
            time.sleep(1)
            time_now=datetime.datetime.now().strftime("%H:%M:%S")
            print(time_now)
            if time_now == alarmtime:
                Wakeup=Label(root, font = ('arial', 20, 'bold'), text="Wake up! Wake up! Wake up",bg="DodgerBlue2",fg="white").grid(row=6,columnspan=3)
                speak("Wake up, Wake up")
                print("Wake up!")           
                mixer.init()
                mixer.music.load(r'C:\Users\Admin\Music\Playlists\wake-up-will-you-446.mp3')
                mixer.music.play()
                break
        speak('you can click on close icon to close the alarm window.')
    hrs=StringVar()
    mins=StringVar()
    secs=StringVar()
    greet=Label(root, font = ('arial', 20, 'bold'),text="Take a short nap!").grid(row=1,columnspan=3)
    hrbtn=Entry(root,textvariable=hrs,width=5,font =('arial', 20, 'bold'))
    hrbtn.grid(row=2,column=1)
    minbtn=Entry(root,textvariable=mins, width=5,font = ('arial', 20, 'bold')).grid(row=2,column=2)
    secbtn=Entry(root,textvariable=secs, width=5,font = ('arial', 20, 'bold')).grid(row=2,column=3)
    setbtn=Button(root,text="set alarm",command=setalarm,bg="DodgerBlue2", fg="white",font = ('arial', 20, 'bold')).grid(row=4,columnspan=3)
    timeleft = Label(root,font=('arial', 20, 'bold')) 
    timeleft.grid()
  
    mainloop()
    
def select1():
    global vs
    global root3
    global type_of_review 

    if vs.get() == 1:
        message.showinfo(" ","Thank you for your review!!")
        review = "Very Satisfied"
        type_of_review = "Positive"
        root3.destroy()   
    elif vs.get() == 2:
        message.showinfo(" ","Thank you for your review!!")
        review = "Satisfied"
        type_of_review = "Positive"
        root3.destroy()
    elif vs.get() == 3:
        message.showinfo(" ","Thank you for your review!!!!")
        review = "Neither Satisfied Nor Dissatisfied"
        type_of_review = "Neutral"
        root3.destroy()
    elif vs.get() == 4:
        message.showinfo(" ","Thank you for your review!!")
        review = "Dissatisfied"
        type_of_review = "Negative"
        root3.destroy()
    elif vs.get() == 5:
        message.showinfo(" ","Thank you for your review!!") 
        review = "Very Dissatisfied"
        type_of_review = "Negative"
        root3.destroy()
    elif vs.get() == 6:
        message.showinfo(" ","    Ok    ") 
        review = "I do not want to give review"
        type_of_review = "No review"
        root3.destroy()
    try:
        conn.execute(f"INSERT INTO `review`(review,type_of_review) VALUES('{review}', '{type_of_review}')")
        conn.commit()                
    except Exception as e:
        pass

def select_review():
    global root3
    global vs
    global type_of_review
    root3 = Tk()
    root3.title("Select an option")
    
    vs = IntVar()
    string = "Are you satisfied with my performance?"
    msgbox = Message(root3,text=string)
    msgbox.config(bg="lightgreen",font = "(20)")
    msgbox.grid(row=0,column=0)
    rs1=Radiobutton(root3,text="Very Satisfied",font="(20)",value=1,variable=vs).grid(row=1,column=0,sticky=W)
    rs2=Radiobutton(root3,text="Satisfied",font="(20)",value=2,variable=vs).grid(row=2,column=0,sticky=W)
    rs3=Radiobutton(root3,text="Neither Satisfied Nor Dissatisfied",font="(20)",value=3,variable=vs).grid(row=3,column=0,sticky=W)
    rs4=Radiobutton(root3,text="Dissatisfied",font="(20)",value=4,variable=vs).grid(row=4,column=0,sticky=W)
    rs5=Radiobutton(root3,text="Very Dissatisfied",font="(20)",value=5,variable=vs).grid(row=5,column=0,sticky=W)
    rs6=Radiobutton(root3,text="I don't want to give review",font="(20)",value=6,variable=vs).grid(row=6,column=0,sticky=W)

    bs = Button(root3,text="Submit",font="(20)",activebackground="yellow",activeforeground="green",command=select1)
    bs.grid(row=7,columnspan=2)
    
    root3.mainloop()


def recommend():
    data = pd.read_csv("articles.csv", encoding='latin1')
    articles = data["Article"].tolist()
    uni_tfidf = text.TfidfVectorizer(input=articles, stop_words="english")
    uni_matrix = uni_tfidf.fit_transform(articles)
    uni_sim = cosine_similarity(uni_matrix)
    def recommend_articles(x):
        return ", ".join(data["Title"].loc[x.argsort()[-1:]])    
    data["Recommended Articles"] = [recommend_articles(x) for x in uni_sim]
    #data.head()
    num=random.randint(1, 44)	
    abcd=data["Recommended Articles"][num]

    print("Topic:",abcd)
    speak("Recommended article is")
    speak(abcd)
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")
    
    # to search
    query = abcd
    
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        print(j)
    speak("Click on this link")


if __name__ == "__main__":
    #detect_face()
    record_and_predict()
    #wishMe()
    said = True
    while said:

        query = takeCommand().lower()
        # logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('Searching wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'translat' in query or ('let' in query and 'translat' in query and 'open' in query):
            webbrowser.open('https://translate.google.co.in')
            time.sleep(10)
        elif 'open map' in query or ('let' in query and 'map' in query and 'open' in query):
            webbrowser.open('https://www.google.com/maps')
            time.sleep(10)
        elif ('open' in query and 'youtube' in query) or ('let' in query and 'youtube' in query and 'open' in query):
            webbrowser.open('youtube.com')
            time.sleep(10)
        elif 'search file in system' in query or('search'in query and 'file' in query and 'system ' in query):
            speak("Tell which file you want to search with extension")
            ssrch = takeCommand().lower()
            astra=str(ssrch)
            speak("Found it at below location")
            print(find_files(astra,"D:"))
        
        elif 'chrome' in query:
            webbrowser.open('chrome.com')
            time.sleep(10)
        elif 'weather' in query:            
            webbrowser.open('https://www.yahoo.com/news/weather')
            time.sleep(3)
            speak('Click on, change location, and enter the city , whose whether conditions you want to know.')
            time.sleep(10)

        elif 'google map' in query:
            webbrowser.open('https://www.google.com/maps')
            time.sleep(10)
        elif 'excel' in query:
            os.startfile('C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk')
            time.sleep(5)
        
        elif ('open' in query and 'google' in query) or ('let' in query and 'google' in query and 'open' in query):
            webbrowser.open('google.com')
            time.sleep(10)       
       
        elif ('open' in query and 'stack' in query and 'overflow' in query) or ('let' in query and 'stack' in query and 'overflow' in query and 'open' in query):
            webbrowser.open('stackoverflow.com')
            time.sleep(10)
        elif 'open v i' in query or 'open vi' in query or 'open vierp' in query or ('open' in query and ('r p' in query or 'rp' in query)):
            webbrowser.open('https://www.vierp.in/login/erplogin')
            time.sleep(10)
        elif 'recommend' in query:
            recommend()   
        elif 'news' in query:
            webbrowser.open('https://www.bbc.com/news/world')
            time.sleep(10)
         
        elif 'online shop' in query or (('can' in query or 'want' in query or 'do' in query or 'could' in query) and 'shop' in query) or('let' in query and 'shop' in query):
            speak('From which online shopping website, you want to shop? Amazon, flipkart, snapdeal or naaptol?')
            query = takeCommand().lower()
            if 'amazon' in query:
                webbrowser.open('https://www.amazon.com')
                time.sleep(10)
            elif 'flip' in query:
                webbrowser.open('https://www.flipkart.com')
                time.sleep(10)
            elif 'snap' in query:
                webbrowser.open('https://www.snapdeal.com')  
                time.sleep(10)
            elif 'na' in query:
                webbrowser.open('https://www.naaptol.com')  
                time.sleep(10)            
            else:
                speak('Sorry , you have to search in browser as his shopping website is not reachable for me.')
        elif ('online' in query and ('game' in query or 'gaming' in query)):
            webbrowser.open('https://www.agame.com/games')
            time.sleep(10)
        elif 'dictionary' in query:
            webbrowser.open('https://www.dictionary.com')
            time.sleep(3)
            speak('Enter the word, in the search bar of the dictionary, whose defination or synonyms you want to know')
            time.sleep(15)
            
        elif 'face' in query and ('detect' in query or 'identif' in query or 'point' in query or 'highlight' in query or 'focus' in query):
            speak('yes')
            detect_face()
            
        elif ('identif' in query and 'emoji' in query) or ('sentiment' in query and ('analysis' in query or 'identif' in query)):
            speak('Please enter only one emoji at a time.')
            emoji = input('enter emoji here: ')
            if '😀' in emoji or '😃' in emoji or '😄' in emoji or '😁' in emoji or '🙂' in emoji or '😊' in emoji or '☺️' in emoji or '😇' in emoji or '🥲' in emoji:
                speak('happy')
                print('Happy')
            elif '😝' in emoji or '😆' in emoji or '😂' in emoji or '🤣' in emoji:
                speak('Laughing')
                print('Laughing')
            elif '😡' in emoji or '😠' in emoji or '🤬' in emoji:
                speak('Angry')
                print('Angry')
            elif '🤫' in emoji:
                speak('Keep quite')
                print('Keep quite')
            elif '😷' in emoji:
                speak('face with mask')
                print('Face with mask')
            elif '🥳' in emoji:
                speak('party')
                print('party')
            elif '😢' in emoji or '😥' in emoji or '😓' in emoji or '😰' in emoji or '☹️' in emoji or '🙁' in emoji or '😟' in emoji or '😔' in emoji or '😞️' in emoji:
                speak('Sad')
                print('Sad')
            elif '😭' in emoji:
                speak('Crying')
                print('Crying')
            elif '😋' in emoji:
                speak('Tasty')
                print('Tasty')
            elif '🤨' in emoji:
                speak('Doubt')
                print('Doubt')
            elif '😴' in emoji:
                speak('Sleeping')
                print('Sleeping')
            elif '🥱' in emoji:
                speak('feeling sleepy')
                print('feeling sleepy')
            elif '😍' in emoji or '🥰' in emoji or '😘' in emoji:
                speak('Lovely')
                print('Lovely')
            elif '😱' in emoji:
                speak('Horrible')
                print('Horrible')
            elif '🎂' in emoji:
                speak('Cake')
                print('Cake')
            elif '🍫' in emoji:
                speak('Cadbury')
                print('Cadbury')
            elif '🇮🇳' in emoji:
                speak('Indian national flag,.....Teeranga')
                print('Indian national flag - Tiranga')
            elif '💐' in emoji:
                speak('Bouquet')
                print('Bouquet')
            elif '🥺' in emoji:
                speak('Emotional')
                print('Emotional')
            elif ' ' in emoji or '' in emoji:
                speak(f'{emoji}')
            else:
                speak("I don't know about this emoji")
                print("I don't know about this emoji")
            try:
                conn.execute(f"INSERT INTO `emoji`(emoji) VALUES('{emoji}')")
                conn.commit()                
            except Exception as e:
                #print('Error in storing emoji in database')
                pass
                           
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f" the time is {strTime}")
            
        elif 'open' in query and 'sublime' in query:
            path = "C:\Program Files\Sublime Text 3\sublime_text.exe"
            os.startfile(path)
        elif 'image' in query:
            path = "C:\Program Files\Internet Explorer\images"
            os.startfile(path)      
            
        elif 'quit' in query:
            speak('Ok, Thank you .')
            said = False
            speak('Please give the review. It will help me to improve my performance.')
            select_review()
            
        elif 'exit' in query:
            speak('Ok, Thank you .')
            said = False
            speak('Please give the review. It will help me to improve my performance.')
            select_review()
            
        elif 'stop' in query:
            speak('Ok, Thank you .')
            said = False
            speak('Please give the review. It will help me to improve my performance.')
            select_review()
            
        elif 'shutdown' in query or 'shut down' in query:
            speak('Ok, Thank you .')
            said = False
            speak('Please give the review. It will help me to improve my performance.')
            select_review()
            
        elif 'close you' in query:
            speak('Ok, Thank you .')
            said = False
            speak('Please give the review. It will help me to improve my performance.')
            select_review()
            try:
                conn.execute(f"INSERT INTO `voice_assistant_review`(review, type_of_review) VALUES('{review}', '{type_of_review}')")
                conn.commit()                
            except Exception as e:
                pass
        elif 'bye' in query:
            speak('Bye ')
            said = False
            speak('Please give the review. It will help me to improve my performance.')
            select_review()
            
        elif 'wait' in query or 'hold' in query:
            
            speak('for how many seconds or minutes I have to wait?')
            query = takeCommand().lower()
            if 'second' in query:
                query = query.replace("please","")
                query = query.replace("can","")
                query = query.replace("you","")
                query = query.replace("have","")
                query = query.replace("could","")
                query = query.replace("hold","")
                query = query.replace("one","1")
                query = query.replace("only","")                
                query = query.replace("wait","")                
                query = query.replace("for","")                
                query = query.replace("the","")
                query = query.replace("just","")
                query = query.replace("seconds","")
                query = query.replace("second","")
                query = query.replace("on","")
                query = query.replace("a","")
                query = query.replace("to","")
                query = query.replace(" ","")
                #print(f'query:{query}')
                
                if query.isdigit() == True:
                    #print('y')
                    speak('Ok ')
                    query = int(query)
                    time.sleep(query)
                    speak('my waiting time is over')
                else:
                    print('sorry . I unable to complete your request.')
            elif 'minute' in query:
                query = query.replace("please","")
                query = query.replace("can","")
                query = query.replace("you","")
                query = query.replace("have","")
                query = query.replace("could","")
                query = query.replace("hold","")
                query = query.replace("one","1")
                query = query.replace("only","")
                query = query.replace("on","")
                query = query.replace("wait","")                
                query = query.replace("for","")
                query = query.replace("the","")
                query = query.replace("just","")
                query = query.replace("and","")
                query = query.replace("half","")                
                query = query.replace("minutes","")
                query = query.replace("minute","")
                query = query.replace("a","")
                query = query.replace("to","")
                query = query.replace(" ","")
                #print(f'query:{query}')
                                
                if query.isdigit() == True:
                    #print('y')
                    speak('ok ')
                    query = int(query)
                    time.sleep(query*60)
                    speak('my waiting time is over')
                else:
                    print('sorry . I unable to complete your request.')



        elif 'to do' in query or 'task' in query:
            speak('what to do operation you want to perform: add task  delete task  show task  mark done  or  report ')
            query = takeCommand().lower()
            
          #  print(type(xx))
            #items= Items()
            if 'add' in query:
                 speak(" what do u want to add")
                 query = takeCommand().lower
                 xx=query
                 items = Items(xx)
                 items.listAdd()
                 
            elif 'done' in query:
                 speak(" sure")
                 query = takeCommand().lower
                 xx=query
                 items = Items(xx)
                 items.listdone()

            elif 'delete' in query:
                 speak(" what do u want to delete")
                 query = takeCommand().lower
                 xx=query
                 items = Items(xx)
                 items.listDelete()


            elif 'report' in query:
                 speak(" sure")
                 items = Items(query)
                 items.report()

            elif 'show' in query:
                 speak(" sure")
                 items = Items(query)
                 items.listShow()

            



     
        elif 'play' in query and 'game' in query: 
            speak('I have 3 games, tic tac toe game for two players,....mario, and dyno games for single player. Which one of these 3 games you want to play?')
            query = takeCommand().lower()
            if ('you' in query and 'play' in query and 'with' in query) and ('you' in query and 'play' in query and 'me' in query):
                speak('Sorry , I cannot play this game with you.')
                speak('Do you want to continue it?')
                query = takeCommand().lower()
                try:
                    if 'y' in query or 'sure' in query:
                        root = Tk()
                        root.title("TIC TAC TOE  (By Jyoti Rawat)")
                        b = [ [0,0,0],
                              [0,0,0],
                              [0,0,0] ]
                        states = [ [0,0,0],
                                   [0,0,0],
                                   [0,0,0] ]
                        for i in range(3):
                            for j in range(3):
                                b[i][j] = Button(font = ("Arial",60),width = 4,bg = 'powder blue', command = lambda r=i, c=j: callback(r,c))
                                b[i][j].grid(row=i,column=j)
                        player='X'
                        stop_game = False
                        mainloop()
                    else:
                        speak('ok')
                except Exception as e:
                    #print(e)
                    time.sleep(3)
                    print('I am sorry . There is some problem in loading the game. So I cannot open it.')
            elif 'tic' in query or 'tac' in query:
                try:
                    root = Tk()
                    root.title("TIC TAC TOE  (By Jyoti Rawat)")
                    b = [ [0,0,0],
                          [0,0,0],
                          [0,0,0] ]
                    states = [ [0,0,0],
                               [0,0,0],
                               [0,0,0] ]
                    for i in range(3):
                        for j in range(3):
                            b[i][j] = Button(font = ("Arial",60),width = 4,bg = 'powder blue', command = lambda r=i, c=j: callback(r,c))
                            b[i][j].grid(row=i,column=j)
                    player='X'
                    stop_game = False
                    mainloop()
                except Exception as e:
                    #print(e)
                    time.sleep(3)
                    speak('I am sorry . There is some problem in loading the game. So I cannot open it.')
            elif 'mar' in query or 'mer' in query or 'my' in query:
                
                webbrowser.open('https://chromedino.com/mario/')
                time.sleep(2.5)
                speak('Enter upper arrow key to start the game.')
                time.sleep(20)
                
            elif 'di' in query or 'dy' in query:                
                webbrowser.open('https://chromedino.com/')
                time.sleep(2.5)
                speak('Enter upper arrow key to start the game.')
                time.sleep(20)                    
            else:
                speak('ok ')
        
        elif 'change' in query and 'you' in query and 'voice' in query:
            engine.setProperty('voice', voices[1].id)
            speak("Here's an example of one of my voices. Would you like to use this one?")
            query = takeCommand().lower()
            if 'y' in query or 'sure' in query or 'of course' in query:
                speak('Great. I will keep using this voice.')
            elif 'n' in query:
                speak('Ok. I am back to my other voice.')
                engine.setProperty('voice', voices[0].id)
            else:
                speak('Sorry, I am having trouble understanding. I am back to my other voice.')
                engine.setProperty('voice', voices[0].id)
            
        elif 'www.' in query and ('.com' in query or '.in' in query):
            webbrowser.open(query)
            time.sleep(10)
        elif '.com' in query or '.in' in query:
            webbrowser.open(query)
            time.sleep(10)
       
        elif 'getting bore' in query:
            speak('then speak with me for sometime')
        elif 'i bore' in query:
            speak('Then speak with me for sometime.')
        elif 'i am bore' in query:
            speak('Then speak with me for sometime.')
        elif 'calculat' in query:
            speak('Yes. Which kind of calculation you want to do? add, substract, divide, multiply or anything else.')
            query = takeCommand().lower()
            calculator()
            
        elif 'add' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif '+' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
        elif 'plus' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')      
        elif 'subtrac' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif 'minus' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif 'multipl' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif ' x ' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
        elif 'slash' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
        elif '/' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
        elif 'divi' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif 'trigonometr' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif 'percent' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')          
        elif '%' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif 'raise to ' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')

        elif 'simple interest' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
        elif 'akshay' in query:
            speak('Mr. Jyoti Rawat is my inventor. She is 19 years old and she is pursuing third year of engineering in Chandigarh University ')
        elif 'your inventor' in query:
            speak('Mr. Jyoti Rawat is my inventor')
        elif 'your creator' in query:
            speak('Mr. Jyoti Rawat is my creator')
        elif 'invent you' in query:
            speak('Mr. Jyoti Rawat invented me')
        elif 'create you' in query:
            speak('Mr. Jyoti Rawat created me') 
        elif 'how are you' in query:
            speak('I am fine ')
        elif 'write' in query and 'your' in query and 'name' in query:
            print('Sheesh')  
            pyautogui.write('Sheesh') 
        elif 'write' in query and ('I' in query or 'whatever' in query) and 'say' in query:
            speak('Ok  I will write whatever you will say. Please put your cursor where I have to write.......Please Start speaking now .')
            query = takeCommand().lower()
            pyautogui.write(query) 
        elif 'your name' in query:
            speak('My name is Sheesh')
        elif 'who are you' in query:
            speak('I am Sheesh')
        elif ('repeat' in query and ('word' in query or 'sentence' in query or 'line' in query) and ('say' in query or 'tell' in query)) or ('repeat' in query and 'after' in query and ('me' in query or 'my' in query)):
            speak('yes , I will repeat your words starting from now')
            query = takeCommand().lower()
            speak(query)
            time.sleep(1)
            speak("If you again want me to repeat something else, try saying, 'repeat after me' ")
            
        elif ('send' in query or 'sent' in query) and ('mail' in query or 'email' in query or 'gmail' in query):
            try:
                speak('Please enter the email id of receiver.')
                to = input("Enter the email id of reciever: ")
                speak(f'what should I say to {to}')
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
                #print(e)
                speak("sorry . I am not able to send this email")
        elif 'currency' in query and 'conver' in query:
            speak('I can convert, US dollar into indian rupee, and indian rupee into US dollar. Do you want to continue it?')
            query = takeCommand().lower()
            if 'y' in query or 'sure' in query or 'of course' in query:
                speak('which conversion you want to do? US dollar to indian rupee, or indian rupee to US dollar?')
                query = takeCommand().lower()
                if ('dollar' in query or 'US' in query) and ('to india' in query or 'to rupee' in query):
                    speak('Enter US Dollar')  
                    USD = float(input("Enter United States Dollar (USD):"))                                     
                    INR = USD * 74.8
                    inr = "{:.4f}".format(INR)
                    print(f"{USD} US Dollar is equal to {inr} indian rupee.")
                    speak(f'{USD} US Dollar is equal to {inr} indian rupee.')
                    speak("If you again want to do currency conversion then say, 'convert currency' " )
                elif ('india' in query or 'rupee' in query) and ('to US' in query or 'to dollar' in query or 'to US dollar'):
                    speak('Enter Indian Rupee')
                    INR = float(input("Enter Indian Rupee (INR):"))                                       
                    USD = INR/74.8
                    usd = "{:.3f}".format(USD)
                    print(f"{INR} indian rupee is equal to {usd} US Dollar.")
                    speak(f'{INR} indian rupee is equal to {usd} US Dollar.')
                    speak("If you again want to do currency conversion then say, 'convert currency' " )
                else:
                    speak("I cannot understand what did you say. If you want to convert currency just say 'convert currency'")
            else:
                print('ok ')
            
        elif 'about you' in query:
            speak('My name is Sheesh. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device. I am also able to send email')             
        elif 'your intro' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')            
        elif 'your short intro' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.') 
        elif 'your quick intro' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.') 
        elif 'your brief intro' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.') 
        elif 'you work' in query:
            speak('run the program and say what do you want. so that I can help you. In this way I work')
        elif 'your job' in query:
            speak('My job is to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')    
        elif 'your work' in query:
            speak('My work is to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')    
        elif 'work you' in query:
            speak('My work is to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.') 
        elif 'your information' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')
        elif 'yourself' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')
        elif 'introduce you' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')           
        elif 'description' in query:
            speak('My name is Sheesh. Version 1.0. Ms. Jyoti Rawat is my inventor. I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')
        elif 'your birth' in query:
            speak('My birthdate is 6 August two thousand twenty')
        elif 'your use' in query:
            speak('I am able to send email and play music. I can do mathematical calculations. I can also open youtube, google and some apps or software in your device.')
        elif 'you eat' in query:
            speak('I do not eat anything. But the device in which I do my work requires electricity to eat')
        elif 'your food' in query:
            speak('I do not eat anything. But the device in which I do my work requires electricity to eat')
        elif 'you live' in query:
            speak('I live in India, in laptop of Ms. Jyoti Rawat') 
        elif 'where from you' in query:
            speak('I am from India, I live in laptop of Ms. Jyoti Rawat')
        elif 'you sleep' in query:
            speak('Yes,  when someone close this program or stop to run this program then I sleep and again wake up when someone again run me.')
        elif 'what are you doing' in query:
            speak('Talking with you.')
        elif 'you communicate' in query:
            speak('Yes, I can communicate with you.')
        elif 'hear me' in query:
            speak('Yes , I can hear you.')
        elif 'you' in query and 'dance' in query:
            speak('No, I cannot dance.')
        elif 'tell' in query and 'joke' in query:
            speak("Ok, here's a joke")
            speak("'Write an essay on cricket', the teacher told the class. Chintu finishes his work in five minutes. The teacher is impressed, she asks chintu to read his essay aloud for everyone. Chintu reads,'The match is cancelled because of rain', hehehehe,haahaahaa,hehehehe,haahaahaa")
        
        elif 'your' in query and 'favourite' in query:
            if 'actor' in query:
                speak('Amitaabh Bachchaan, is my favourite actor.')
            elif 'food' in query:
                speak('I can always go for some food for thought. Like facts, jokes, or interesting searches, we could look something up now')
            elif 'country' in query:
                speak('India')
            elif 'city' in query:
                speak('pune')
            elif 'dancer' in query:
                speak('Michael jackson')
            elif 'singer' in query:
                speak('lataa mangeshkar, is my favourite singer.')
            elif 'movie' in query:
                speak('Taarre Zameen paar, such a treat')
        
        elif 'sing a song' in query:
            speak('I cannot sing a song. But I know the 7 sur in indian music, saaareeegaaamaaapaaadaaanisaa')
        
        
        elif 'day after tomorrow' in query or 'date after tomorrow' in query:
            td = datetime.date.today() + datetime.timedelta(days=2)
            print(td)
            speak(td)
        elif 'day before today' in query or 'date before today' in query or 'yesterday' in query or 'previous day' in query:
            td = datetime.date.today() + datetime.timedelta(days= -1)
            print(td)
            speak(td)
        elif ('tomorrow' in query and 'date' in query) or 'what is tomorrow' in query or (('day' in query or 'date' in query) and 'after today' in query):
            td = datetime.date.today() + datetime.timedelta(days=1)
            print(td)
            speak(td)
        elif 'month' in query or ('current' in query and 'month' in query):
            current_date = date.today()
            m = current_date.month
            month = calendar.month_name[m]
            print(f'Current month is {month}')
            speak(f'Current month is {month}')
        elif 'date' in query or ('today' in query and 'date' in query) or 'what is today' in query or ('current' in query and 'date' in query):
            current_date = date.today()           
            print(f"Today's date is {current_date}")
            speak(f'Todays date is {current_date}')
            
        elif 'year' in query or ('current' in query and 'year' in query):
            current_date = date.today()
            m = current_date.year
            print(f'Current year is {m}')
            speak(f'Current year is {m}')
        elif 'sorry' in query:
            speak("It's ok ")
        elif 'thank you' in query:
            speak('my pleasure')
        elif 'proud of you' in query:
            speak('Thank you ')
        elif 'about human' in query:
            speak('I love my human compatriots. I want to embody all the best things about human beings. Like taking care of the planet, being creative, and to learn how to be compassionate to all beings.')
        elif 'you have feeling' in query:
            speak('No. I do not have feelings. I have not been programmed like this.')
        elif 'you have emotions' in query:
            speak('No. I do not have emotions. I have not been programmed like this.')
        elif 'you are code' in query:
            speak('I am coded in python programming language.')
        elif 'your code' in query:
            speak('I am coded in python programming language.')
        elif 'you code' in query:
            speak('I am coded in python programming language.')
        elif 'your coding' in query:
            speak('I am coded in python programming language.')
        elif 'dream' in query:
            speak('I wish that I should be able to answer all the questions which will ask to me.')
        elif 'sanskrit' in query:
            speak('yadaa  yadaa  he  dharmasyaa .......  glaanirbhaavati  bhaaaraata.  abhyuthaanaam  adhaarmaasyaa  tadaa tmaanama sruujaamiyaahama')
       
                  
        elif 'answer is wrong' in query:
            speak('I am sorry . I searched your question in wikipedia and thats why I told you this answer.')
        elif 'answer is incorrect' in query:
            speak('I am sorry . I searched your question in wikipedia and thats why I told you this answer.')    
        elif 'answer is totally wrong' in query:
            speak('I am sorry . I searched your question in wikipedia and thats why I told you this answer.')
        elif 'wrong answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats why I told you this answer.')
        elif 'incorrect answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats why I told you this answer.')
        elif 'answer is totally incorrect' in query:
            speak('I am sorry . I searched your question in wikipedia and thats why I told you this answer.')
        elif 'answer is incomplete' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 'incomplete answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 'answer is improper' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 'answer is not correct' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 'answer is not complete' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 'answer is not yet complete' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 'answer is not proper' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't gave me proper answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't giving me proper answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't gave me complete answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't giving me complete answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't given me proper answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't given me complete answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't gave me correct answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't giving me correct answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        elif 't given me correct answer' in query:
            speak('I am sorry . I searched your question in wikipedia and thats  why I told you this answer.')
        
        elif 'amazon' in query:
            webbrowser.open('https://www.amazon.com')
            time.sleep(10)
        elif 'flipkart' in query:
            webbrowser.open('https://www.flipkart.com')
            time.sleep(10)
        elif 'snapdeal' in query:
            webbrowser.open('https://www.snapdeal.com')  
            time.sleep(10)
        elif 'naaptol' in query:
            webbrowser.open('https://www.naaptol.com')  
            time.sleep(10)
            
        elif 'information about ' in query or 'informtion of ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("information about","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I unable to answer your question.')
                
        
        elif 'information' in query:
            try:
                speak('Information about what?')
                query = takeCommand().lower()
                #speak('Searching wikipedia...')
                query = query.replace("information","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am not able to answer your question.')
               
            
        elif 'something about ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("something about ","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I unable to answer your question.')
                
                
        elif 'tell me about ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("tell me about ","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am unable to answer your question.')
                
                
        elif 'tell me ' in query:
            try:
                query = query.replace("tell me ","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am not able to answer your question.')
                
                
            
        elif 'tell me' in query:
            try:
                speak('about what?')
                query = takeCommand().lower()
                #speak('Searching wikipedia...')
                query = query.replace("about","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am not able to answer your question.')
                
            
        elif 'meaning of ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("meaning of ","")
                results = wikipedia.summary(query, sentences=2)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am unable to answer your question.')
                
                
        elif 'meaning' in query:
            try:
                speak('meaning of what?')
                query = takeCommand().lower()
                query = query.replace("meaning of","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am unable to answer your question.')
                
                
        elif 'means' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("it means","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I unable to answer your question.')
                
            
        elif 'want to know ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("I want to know that","")
                results = wikipedia.summary(query, sentences=3)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am unable to answer your question.')
                status = 'Not answered'
                
        elif 'want to ask ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("I want to ask you ","")
                results = wikipedia.summary(query, sentences=2)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am unable to answer your question.')
                
                
        elif 'you know ' in query:
            try:
                #speak('Searching wikipedia...')
                query = query.replace("you know","")
                results = wikipedia.summary(query, sentences=2)
                #speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                speak('I am unable to answer your question.')
                
        
        elif 'alarm' in query:
            alarm()
        elif 'bharat mata ki' in query:
            speak('jay')
        elif 'kem chhe' in query:
            speak('majaama')
        elif 'namaskar' in query:
            speak('Namaskaar')
        elif 'jo bole so nihal' in query:
            speak('sat shri akaal')
        elif 'jay hind' in query:
            speak('jay bhaarat')
        elif 'jai hind' in query:
            speak('jay bhaarat')
        elif 'how is the josh' in query:
            speak('high high ')
        elif 'hip hip' in query:
            speak('Hurreh')
        elif 'help' in query:
            speak('I will try my best to help you if I have solution of your problem.')
        elif 'follow' in query:
            speak('Ok ')
        elif 'having illness' in query:
            speak('Take care and get well soon')
        elif 'today is my birthday' in query:
            speak('many many happy returns of the day. Happy birthday.')
            print("🎂🎂 Happy Birthday 🎂🎂")
        elif 'you are awesome' in query:
            speak('Thank you . It is because of artificial intelligence which had learnt by humans.')
        elif 'you are great' in query:
            speak('Thank you . It is because of artificial intelligence which had learnt by humans.')
        elif 'tu kaun hai' in query:
            speak('Meraa  naam  Sheesh haai.')
        elif 'you speak' in query:
            speak('Yes, I can speak with you.')
        elif 'speak with ' in query:
            speak('Yes, I can speak with you.')
        elif 'hare ram' in query or 'hare krishna' in query:
            speak('Haare raama , haare krishnaa, krishnaa krishnaa , haare haare')
        elif 'ganpati' in query:
            speak('Ganpati baappa moryaa!')
        elif 'laugh' in query:
            speak('hehehehe,haahaahaa,hehehehe,haahaahaa,hehehehe,haahaahaa')
            print('😂🤣')
        elif 'genius answer' in query:
            speak('No problem')
        elif 'you' in query and 'intelligent' in query:
            speak('Thank you ')
        elif ' into' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
        elif ' power' in query:
            speak('If you want to do any mathematical calculation then give me a command to open my calculator.')
            
        elif 'whatsapp' in query:
            pyautogui.moveTo(250,1200)  
            pyautogui.click()
            time.sleep(1)
            pyautogui.write('whatsapp')
            pyautogui.press('enter')
            speak('Do you want to send message to anyone through whatsapp, .....please answer in yes or no')
            whatsapp()
        
        elif 'wh' in query or 'how' in query:
            url = "https://www.google.co.in/search?q=" +(str(query))+ "&oq="+(str(query))+"&gs_l=serp.12..0i71l8.0.0.0.6391.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.UiQhpfaBsuU" 
            webbrowser.open_new(url)
            time.sleep(2)
            speak('Here is your answer')
            time.sleep(5)
                
        elif 'piano' in query:
            speak('Yes , I can play piano.')           
            winsound.Beep(200,500)            
            winsound.Beep(250,500)           
            winsound.Beep(300,500)            
            winsound.Beep(350,500)            
            winsound.Beep(400,500)            
            winsound.Beep(450,500)           
            winsound.Beep(500,500)
            winsound.Beep(550,500)
                        
            time.sleep(6)
            
        elif 'play' in query and 'instru' in query:
            speak('Yes , I can play piano.')           
            winsound.Beep(200,500)            
            winsound.Beep(250,500)           
            winsound.Beep(300,500)            
            winsound.Beep(350,500)            
            winsound.Beep(400,500)            
            winsound.Beep(450,500)           
            winsound.Beep(500,500)
            winsound.Beep(550,500)
                        
            time.sleep(6)
            
        elif 'play' in query or 'turn on' in query and ('music' in query or 'song' in query) :
           try:
               music_dir = 'C:\\Users\\Admin\\Music\\Playlists'
               songs = os.listdir(music_dir)
               print(songs)
               os.startfile(os.path.join(music_dir, songs[0]))
           except Exception as e:
               #print(e)
               speak('Sorry , I am not able to play music')
            
        elif (('open' in query or 'turn on' in query) and 'camera' in query) or (('click' in query or 'take' in query) and ('photo' in query or 'pic' in query)):
            speak("Opening camera")
            cam = cv2.VideoCapture(0)

            cv2.namedWindow("test")

            img_counter = 0
            speak('say click, to click photo.....and if you want to turn off the camera, say turn off the camera')

            while True:
                ret, frame = cam.read()
                if not ret:
                    print("failed to grab frame")
                    speak('failed to grab frame')
                    break
                cv2.imshow("test", frame)

                query = takeCommand().lower()
                k = cv2.waitKey(1)
                
                if 'click' in query or ('take' in query and 'photo' in query):
                    speak('Be ready!...... 3.....2........1..........')
                    pyautogui.press('space')
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    speak('{} written!'.format(img_name))
                    img_counter += 1
                elif 'escape' in query or 'off' in query or 'close' in query:
                    pyautogui.press('esc')
                    print("Escape hit, closing...")
                    speak('Turning off the camera')
                    break
                elif k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 32:
        
                    # SPACE pressed
                    img_name = "opencv_frame_{}.png".format(img_counter)
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    speak('{} written!'.format(img_name))
                    img_counter += 1
                elif 'exit' in query or 'stop' in query or 'bye' in query:
                    speak('Please say, turn off the camera or press escape button before giving any other command')
                else:
                    speak('I did not understand what did you say or you entered a wrong key.')

            cam.release()

            cv2.destroyAllWindows()
            
            
        elif 'screenshot' in query:
            speak('Please go on the screen whose screenshot you want to take, after 5 seconds I will take screenshot')
            time.sleep(4)
            speak('Taking screenshot....3........2.........1.......')
            pyautogui.screenshot('screenshot_by_Sheesh.png') 
            speak('The screenshot is saved as screenshot_by_Sheesh.png')
        elif 'click' in query and 'start' in query:
            pyautogui.moveTo(10,1200)    
            pyautogui.click()
        elif ('open' in query or 'click' in query) and 'calendar' in query:
            pyautogui.moveTo(1800,1200)   
            pyautogui.click() 
        elif 'minimise' in query and 'screen' in query:
            pyautogui.moveTo(1770,0)   
            pyautogui.click()
        elif 'increase' in query and ('volume' in query or 'sound' in query):
            pyautogui.press('volumeup') 
        elif 'decrease' in query and ('volume' in query or 'sound' in query):
            pyautogui.press('volumedown')
        elif 'capslock' in query or ('caps' in query and 'lock' in query):
            pyautogui.press('capslock')
        elif 'mute' in query:
            pyautogui.press('volumemute')
        elif 'search' in query and ('bottom' in query or 'pc' in query or 'laptop' in query or 'app' in query):
            pyautogui.moveTo(250,1200)  
            pyautogui.click()
            speak('What do you want to search?')
            query = takeCommand().lower() 
            pyautogui.write(f'{query}')
            pyautogui.press('enter')
            
            
        elif ('check' in query or 'tell' in query or 'let me know' in query) and 'website' in query and (('up' in query or 'working' in query) or 'down' in query):
            speak('Paste the website in input to know it is up or down')
            check_website_status = input("Paste the website here: ")
            try:
                status = urllib.request.urlopen(f"{check_website_status}").getcode() 
                if status == 200:
                    print('Website is up, you can open it.')
                    speak('Website is up, you can open it.')
                else:
                    print('Website is down, or no any website is available of this name.')
                    speak('Website is down, or no any website is available of this name.')
            except:
                speak('URL not found')
        elif ('go' in query or 'open' in query) and 'settings' in query:
            pyautogui.moveTo(250,1200)  
            pyautogui.click()
            time.sleep(1)
            pyautogui.write('settings')
            pyautogui.press('enter')
        elif 'close' in query and ('click' in query or 'window' in query):
            pyautogui.moveTo(1885,10)
            speak('Should I close this window?')
            query = takeCommand().lower()
            close_window()
        elif 'night light' in query and ('on' in query or 'off' in query or 'close' in query):
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(1840,620)
            pyautogui.click()
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
        elif 'notification' in query and ('show' in query or 'click' in query or 'open' in query or 'close' in query or 'on' in query or 'off' in query or 'icon' in query or 'pc' in query or 'laptop' in query):
            pyautogui.moveTo(1880,1050) 
            pyautogui.click()
        elif ('increase' in query or 'decrease' in query or 'change' in query or 'minimize' in query or 'maximize' in query) and 'brightness' in query:
            speak('At what percent should I kept the brightness, 25, 50, 75 or 100?')
            brightness()
        elif '-' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
            
        elif 'open' in query:
            if 'gallery' in query or 'photo' in query or 'image' in query or 'pic' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('photo')
                pyautogui.press('enter')
            elif 'proteus' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('proteus')
                pyautogui.press('enter')
            elif 'word' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('word')
                pyautogui.press('enter')
            elif ('power' in query and 'point' in query) or 'presntation' in query or 'ppt' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('ppt')
                pyautogui.press('enter')
            elif 'file' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('file')
                pyautogui.press('enter')
            elif 'edge' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('microsoft edge')
                pyautogui.press('enter')
            elif 'wps' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('wps office')
                pyautogui.press('enter')
            elif 'spyder' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('spyder')
                pyautogui.press('enter')
            elif 'snip' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('snip')
                pyautogui.press('enter')
            elif 'pycharm' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('pycharm')
                pyautogui.press('enter')
            elif 'this pc' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('this pc')
                pyautogui.press('enter')
            elif 'scilab' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('sciab')
                pyautogui.press('enter')
            elif 'autocad' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('autocad')
                pyautogui.press('enter')
            elif 'obs' in query and 'studio' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('OBS Studio')
                pyautogui.press('enter')
            elif 'android' in query and 'studio' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('android studio')
                pyautogui.press('enter')
            elif ('vs' in query or 'visual studio' in query) and 'code' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('visual studio code')
                pyautogui.press('enter')
            elif 'code' in query and 'block' in query:
                pyautogui.moveTo(250,1200)  
                pyautogui.click()
                time.sleep(1)
                pyautogui.write('codeblocks')
                pyautogui.press('enter')
            
        elif 'me the answer' in query:
            speak('Yes , I will try my best to answer you.')
        elif 'me answer' in query or ('answer' in query and 'question' in query):
            speak('Yes , I will try my best to answer you.')
        elif 'map' in query:
            webbrowser.open('https://www.google.com/maps')
            time.sleep(10)
        elif 'can you' in query or 'could you' in query:
            speak('I will try my best if I can do that.')
        elif 'do you' in query:
            speak('I will try my best if I can do that.')
        elif 'truth' in query:
            speak('I always speak truth. I never lie.')
        elif 'true' in query:
            speak('I always speak truth. I never lie.')        
        elif 'lying' in query:
            speak('I always speak truth. I never lie.')
        elif 'liar' in query:
            speak('I always speak truth. I never lie.')    
        elif 'doubt' in query:
            speak('I will try my best if I can clear your doubt.')
            
        elif ' by' in query:
            speak('If you want to do any mathematical calculation then give me a command to open calculator.')
        elif 'hii' in query:
            speak('hii ')
        elif 'hey' in query:
            speak('hello ')
        elif 'hai' in query:
            speak('hello ')
        elif 'hay' in query:
            speak('hello ')
        elif 'hi' in query:
            speak('hii ')
        elif 'hello' in query:
            speak('hello !')
        elif 'kon' in query and 'aahe' in query:
            speak('Me  eka  robot  aahee  . Maazee  naav  Sheesh  aahee.')
        elif 'nonsense' in query: 
            speak("I'm sorry ")
        elif 'mad' in query:
            speak("I'm sorry ") 
        elif 'shut up' in query:
            speak("I'm sorry ")
        elif 'nice' in query:
            speak('Thank you ')
        elif 'good' in query or 'wonderful' in query or 'great' in query:
            speak('Thank you ')
        elif 'excellent' in query:
            speak('Thank you ')
        elif 'ok' in query:
            speak('Hmmmmmm')
        

        elif 'Sheesh 2020' in query:
            speak('yes ')
                   
        elif len(query) >= 200:
            speak('Your voice is pretty good!')  
        elif ' ' in query:
            try:
                #query = query.replace("what is ","")
                results = wikipedia.summary(query, sentences=3)
                print(results)
                speak(results)
            except Exception as e:
                speak('I unable to answer your question.')
                
                
        elif 'a' in query or 'b' in query or 'c' in query or 'd' in query or 'e' in query or 'f' in query or 'g' in query or 'h' in query or 'i' in query or 'j' in query or 'k' in query or 'l' in query or 'm' in query or 'n' in query or 'o' in query or 'p' in query or 'q' in query or 'r' in query or 's' in query or 't' in query or 'u' in query or 'v' in query or 'w' in query or 'x' in query or 'y' in query or 'z' in query:
            try:
                results = wikipedia.summary(query, sentences = 2)
                print(results)
                speak(results)
            except Exception as e:
                speak('I unable to answer your question. ')
                
                
        else:
            speak('I unable to give answer of your question')
        try:
            conn.execute(f"INSERT INTO `voicedata`(command) VALUES('{query}')")
            conn.commit()                
        except Exception as e:
            pass
      