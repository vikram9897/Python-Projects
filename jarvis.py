import pyttsx3 #download pip
import pyaudio #download pyaudio
import datetime
import speech_recognition as sr #download speech recognition
import wikipedia
import webbrowser
import os
import smtplib
import numpy as np
import cv2
engine  = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning Sir")
    elif hour>=12 and hour <18:
        speak("Good Afternoon Sir")
    else:
        speak("Good Evening Sir")
def face_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
   
    cap = cv2.VideoCapture(0)

    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows() 

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source,duration=2)
        #,phrase_time_limit=5
        #, duration=1
        audio=r.listen(source,phrase_time_limit=5)
    try:
        print("Recognizing...")
        #query=r.recognize_google(audio,Language='en-in')
        query=r.recognize_google(audio)
        #print(f"User said: {query}\n")
        print("User said: {}".format(query))
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query
def sendEmail():
    speak("To whom I should send mail ? Enter mail")
    to=input("enter mail:")
    speak("What should I send for you ")
    content=takeCommand()
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    f=open('D:/B.Sc.(IT)','r')
    pas=f.readline()
    f.close()
    server.login("@gmail.com",pas)
    server.sendmail("@gmail.com",to,content)
    server.close()
if __name__ == "__main__":
    wishMe()
    speak(" hello how are you. This is Vikram")
    speak("how may i help you")
    while True:
        query=takeCommand().lower()
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query=query.replace("wikipedia", "")
            results=wikipedia.summary(query,sentences=2)
            speak("Acording to wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'play music' in query:
            music_dir='D:\\vikram\\Videos' #File Path
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[3]))
        elif 'mail' in query:
            try:
                sendEmail()
                speak("Email has been sent")
            except Exception as e:
                print(e)
        elif 'face' in query:
            face_detection()
        elif 'thank you' in query:
            speak("Welcome Have a nice day") 
            break

