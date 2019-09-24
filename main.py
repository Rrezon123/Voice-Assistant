from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS=["janary","febrary","march","april","may","june","july","august","september","october","november","december"]
DAYS=["monday","tuesday","wednesday","friday","saturday","sunday"]
DAY_EXTENTIONS=["st","nd","rd","th"]
def speak(text):
    tts = gTTS(text=text, lang='en')
    # sq-shqip,en-english translate assisatant....
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


def get_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception:" + str(e))
    return said


# speak("hello")
# get_audio()
# text=get_audio()
#
# if "hello" or "hi" in text:
#     speak("Hi,What can I do for you")
# text = get_audio()
# if "tell me a joke" in text:
#         speak("What’s the best thing about Switzerland?")
#         # time.clock(10)
#         speak("I don’t know, but the flag is a big plus")






def auth_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service
def get_events(n,service):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

# if __name__ == '__main__':
#     main()
# service=auth_google()
# get_events(2,service)


def get_date(text):
    text=text.lower()
    today=datetime.date.today()

    if text.count("today")>0:
        return today
    day=-1
    day_of_week=-1
    month=-1
    year=today.year

    for word in text.split():
        if word in MONTHS:
            month=MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week=DAYS.index(word)
        elif word.isdigit():
            day=int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found=word.find(ext)
                if found>0:
                    try:
                        day=int(word[:found])
                    except:
                        pass
    if month <today.month and month!=-1:
        year=year+1
    if day< today.day and month==-1 and day!=-1:
        month=month+1
    if month ==-1 and day==-1 and day_of_week!=-1:
        current_day_of_week=today.weekday()
        dif=day_of_week-current_day_of_week

        if dif<0:
            dif+=7
            if text.count("next")>=1:
                dif+=7
        return  today+datetime.timedelta(dif)
    return datetime.date(month=month,day=day,year=year)

text=get_audio().lower()
print(get_date(text))



