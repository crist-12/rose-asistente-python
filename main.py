from __future__ import print_function
import datetime
import os.path
from google import auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import pytz
import pyttsx3
from gtts import gTTS
import playsound
import speech_recognition as sr
import subprocess


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
DAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)


    subprocess.Popen(["TextEdit.app", file_name])

note("Ola k ase")
"""
def speak2(text):
    tts = gTTS(text=text, lang="es")
    filename = "voice2.mp3"
    tts.save(filename)
    playsound.playsound(filename)

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="es-HN")
            print(said)
        except Exception as e:
            print("Exception :", e)

    return said


text = "k ase"

if "Hola" in text:
    speak("¡Hola!, ¿cómo estás?")

if "Cuál es tu nombre" in text:
    speak("Mi nombre es Rose")


def authenticate_google():

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service

def get_events(day,service):

    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax = end_date.isoformat(),
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak2("No tienes ningún evento programado")
    for event in events:
        speak2(f"Tienes {len(events)} eventos ese día.")
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        start_time = str(start.split("T")[1].split("-")[0])
        if int(start_time.split(":")[0]) < 12:
            start_time += "am"
        else:
            start_time = str(int(start_time.split(":")[0])-12)
            start_time += "pm"
        speak2(event["summary"] + " a las " + start_time)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    
    day = -1
    day_of_the_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_the_week = DAYS.index(word) + 1
        elif word.isdigit():
            day = int(word)

    if month < today.month and month != -1:
        year += 1
    
    if day < today.day and month == -1 and day != -1:
        month += 1

    if month == -1 and day == -1 and day_of_the_week != -1:
        current_day_of_the_week = today.weekday()
        dif = day_of_the_week - current_day_of_the_week

        if dif < 0:
            dif += 7
            if text.count("siguiente") >= 1 or text.count("próxima") >= 1:
                dif += 7
    
        return today + datetime.timedelta(dif)
    
    if month == -1 or day == -1:
        return None

    return datetime.date(month=month, day=day, year=year)


service = authenticate_google()
text = get_audio().lower()
#print(get_date(text))
#speak("Hola, Chris, ¿cómo estás?")


CALENDAR_STR = ["eventos para", "evento para", "tengo algo para", "estoy libre el", "actividades para", "agenda para", "estoy ocupado"]
for frase in CALENDAR_STR:
    if frase in CALENDAR_STR:
        if frase in text:
            date = get_date(text)
            if date:
                get_events(date, service)
            else:
                speak2("No te entendí muy bien, repite plox")

                """