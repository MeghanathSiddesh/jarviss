import pyttsx3
import speech_recognition as sr
import datetime,timedelta
import os
import cv2
from requests import get
import wikipedia
import webbrowser
import pywhatkit
import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
import time
import pyjokes
import threading
import pyautogui
import requests
from email.mime.base import MIMEBase
from email import encoders
import instaloader
import PyPDF2


camera_open = False
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voices',voices[len(voices)-1].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

#converts voice to text
def takecommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold=1
        audio=r.listen(source,timeout=1,phrase_time_limit=20)
    try:
        print("Recogning...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}")
    except Exception as e:
        speak("say that again please...")
        return "None"
    return query

#wish
def wish():
    # jarvis speaking speed should control by user
    hour=int(datetime.datetime.now().hour)
    # tt=time.strftime("%I:%M:%P")
    tt=time.strftime("%I %M:%p")
    if hour>=0 and hour<=12:
        speak(f"good morning!,its {tt}")
    elif hour>12 and hour<18:
        speak(f"good afternoon! {tt} ")
    else:
        speak(f"good evening {tt}")
    speak("i am jarvis sir. please tell me how can i help you")

def open_camera():
    global camera_open
    camera_open = True
    cap = cv2.VideoCapture(0)
    while camera_open:
        ret, img = cap.read()
        cv2.imshow('webcam', img)
        if cv2.waitKey(50) == 27:  # Press ESC to close manually
            break
    cap.release()
    cv2.destroyAllWindows()
    camera_open = False

def handle_query(query):
    global camera_open
    if "close camera" in query.lower():
        print(camera_open)
        if camera_open:
            speak("Okay sir, closing camera")
            camera_open = False  # Set flag to stop camera loop
        else:
            speak("Camera is not open, sir.")
    elif "open camera" in query.lower():
        if not camera_open:
            speak("Okay sir, opening camera")
            camera_thread = threading.Thread(target=open_camera)
            camera_thread.start()
        else:
            speak("Camera is already open, sir.")
def news():
    main_url='https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=80301fbf81a3406d973788bddfead685'
    main_page=requests.get(main_url).json()
    articles=main_page["articles"]
    head=[]
    day=["first","second","third","fourth","fifth","sixth","seventh","eigth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"today's {day[i]} news is: {head[i]}")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def pdf_reader():
    try:
        book_path = 'C:\\app\\hellof.pdf'
        book = open(book_path, 'rb')
        pdfReader = PyPDF2.PdfReader(book)
        pages = len(pdfReader.pages)
        
        speak(f"Total number of pages in this PDF is {pages}")
        speak("Sir, please enter the page number I have to read")
        
        pg = int(input("Please enter the page number: "))
        if pg < 0 or pg >= pages:
            raise ValueError("Page number out of range.")
        
        page = pdfReader.pages[pg]
        text = page.extract_text()  # Use extract_text() instead of extractText()
        speak(text)
        
    except FileNotFoundError:
        speak("The specified file was not found.")
    except ValueError as e:
        speak(str(e))
    except Exception as e:
        speak("An error occurred.")
        print(e)





    


if __name__ == "__main__":
    wish()
    # takecommand()
    # speak("This is advance jarvis")
    while True:
    # if 1:
        query=takecommand().lower()
        #logic building for tasks
        if "open notepad" in query:
            npath='C:\\Windows\\System32\\notepad.exe'
            os.startfile(npath)
        # elif "open adobe reader" in query:
        #     apath=""

        elif 'open command prompt' in query:
            os.system("start cmd")
        elif 'open camera' in query:
            handle_query(query)
        elif 'close camera' in query:
            handle_query(query)


        elif "play music" in query:
            music_dir="C:\\Users\\punit\\Music\\haadu"
            songs=os.listdir(music_dir)
            # rd=random.choice(songs)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir,song))

        elif  "ip address" in query:
            ip=get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia...")
            query=query.replace("wikipedia","")
            results=wikipedia.summary(query,sentences=2)
            speak("according to wikipedia")
            speak(results)
            print(results)

        elif "take a screenshot" in query or "take screenshot" in query:
            speak("sir,please tell me the name for this screenshot file")
            name=takecommand().lower()
            speak("sir please hold the screen for few seconds i am taking screen shot")
            time.sleep(3)
            img=pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("i am done sir, screenshot is saved in our main folder")

        elif "open youtube" in query:
            webbrowser.open("youtube.com")

        elif "open facebook" in query:
            webbrowser.open("facebook.com")

        elif "open instagram" in query:
            webbrowser.open("instagram.com")

        elif "open stack overflow" in query:
            webbrowser.open("https://stackoverflow.com")

        elif "open google" in query:
            speak("sir,what should i search on google")
            cm=takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={cm.replace(' ', '+')}")

        elif "open chat gpt" in query.lower():
            webbrowser.open("https://chatgpt.com")

        elif "send message" in query:
            pywhatkit.sendwhatmsg("+919513430636", "college hogthya lowde", 8, 12)

        elif "on youtube" in query:
            query=query.replace("on youtube","")
            pywhatkit.playonyt(query)
            #play songs on spotify

        elif "you can sleep" in query:
            speak("thanks for using me, Have a Good day")
            sys.exit()

        elif "close notepad" in query:
            speak("okay sir,closing notepad")
            os.system("taskkill /f /im notepad.exe")
        elif "switch window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        # elif "where i am" or "where are we":
        #     speak("wait sir, let me check")
        #     try:
        #         ipAdd=requests.get('https://api.ipify.org').text
        #         print(ipAdd)
        #         url='https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
        #         get_georequests=requests.get(url)
        #         geo_data=get_georequests.json()
        #         # print(geo_data)
        #         city=geo_data['city']
        #         country=geo_data['country']
        #         speak(f"sir, iam not sure but i think we are in {city} city of {country} country")
        #     except Exception as e:
        #         speak("sir do to network issue i can't find where we are")
        #         pass

        # elif "instagram profile" in query or "profile on instagram" in query:
        #     speak("sir,please enter your username correctly")
        #     name=input("enter your username")
        #     webbrowser.open(f"www.instagram.com/{name}")
        #     # speak(f"sir,here is the profile of your username {name}")
        #     time.sleep(5)
        #     speak(f"sir would you like to download the profile picture of this account")
        #     condition=takecommand().lower()
        #     if "yes do it" in condition:
        #         mod=instaloader.Instaloader()
        #         x=mod.download_profile(name,profile_pic_only=True)
        #         speak("i am done sir,profile picture is saved in our main folder. now i am ready")
        #         print(x)
        #     else:
        #         pass


        


        # elif "close facebook" in query:
        #     speak("okay sir,closing facebook")
        #     os.system("taskkill /f /im facebook.exe")
        
        # elif "close notepad" in query:
        #     speak("okay sir,closing notepad")
        #     os.system("taskkill /f /im notepad.exe")

        elif "set alarm" in query:
            nn=int(datetime.datetime.now().hour)
            if nn==10:
                music_dir="C:\\Users\\punit\\Music\\haadu"
                songs=os.listdir(music_dir)
                os.startfile(os.path.join(music_dir,songs[0]))

        elif "tell me a joke" in query:
            joke=pyjokes.get_joke()
            speak(joke)

        elif "restart the system" in query:
            os .system("shutdown /r /t 5")

        elif "shutdown the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep 0,1,0")
        elif 'switch the window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
        elif 'tell me news' in query:
            speak("please wait, fetching the latest news")
            news()
        # elif 'email':
        #     speak("sir what should i say?")
        #     query=takecommand().lower()
        #     if "send a file" in query:
        #         email='letsmailmeghnath@gmail.com'
        #         password='ddgt dslq qxoe luar'
        #         send_to_email='letsmailmeghnath@gmail.com'
        #         speak('okay sir, what is the subject for this email')            
        #         query=takecommand().lower()
        #         subject=query
        #         speak('and sir, what is the message for this email')
        #         query2=takecommand().lower()
        #         message=query2
        #         speak('sir please enter the correct path of the file into the shell')
        #         file_location=input('please enter the path here')

        #         speak("please wait, i am sending email now")

        #         msg=MIMEMultipart()
        #         msg['From']=email
        #         msg['To']=send_to_email
        #         msg['Subject']=subject

        #         msg.attach(MIMEText(message,'plain'))

        #         filename=os.path.basename(file_location)
        #         attachment=open(file_location,"rb")
        #         part=MIMEBase('application','octet-stream')
        #         part.set_payload(attachment.read())
        #         encoders.encode_base64(part)
        #         part.add_header('Content-Disposition',"attachment; filename= %s" % filename)

        #         msg.attach(part)

        #         server=smtplib.SMTP('smtp.gmail.com',587)
        #         server.starttls()
        #         server.login(email,password)
        #         text=msg.as_string()
        #         server.sendmail(email,send_to_email,text)
        #         server.quit()
        #         speak("email has been sent successfully")
        elif "read pdf" in query:
            pdf_reader()
        elif "hide all files" in query or "hide this folder" in query or "visible for everyone" in query:
            speak("sir please tell you want to hide this folder or make it visible for everyone")
            condition=takecommand().lower()
            if "hide" in condition:
                os.system("attrib +h /s /d")
                speak("sir, all the files in this folder are hidden")
            elif "visible" in query:
                os.system("attrib -h /s /d")
                speak("sir,all the files in this folder are visible to everyone")
            elif "leave it" in query or "leave for now" in query:
                speak("ok sir")

        






        speak("sir,do you have any other work")
        #to cloase any application
       
