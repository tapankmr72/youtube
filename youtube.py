import time
#import re
#from regex import error
import pytube
from pytube import Playlist, YouTube


from datetime import datetime,timedelta
import json
import urllib.request
import requests
#import os
path = ""
polltime=2
pollgap=2
u2=""
replyto="5560841599"
looper=0
message = ""
updatetext1=0
token="5749368372:AAHGyZqSahxJkKwGi4qMoMfFVgo4Q70yYzY"
headers = {"accept": "application/json","content-type": "application/json"}
#import openpyxl
photourl="https://api.telegram.org/bot"+token+"/sendPhoto"
docurl="https://api.telegram.org/bot"+token+"/sendDocument"
texturl="https://api.telegram.org/bot"+token+"/sendMessage"
meurl ="https://api.telegram.org/bot"+token+"/getMe"
pollurl="https://api.telegram.org/bot"+token+"/getUpdates"
filedownload="https://api.telegram.org/file/bot"+token+"/"
fileurl="https://api.telegram.org/bot"+token+"/getfile"
healthmessage="This is health message of Youtube Downloader BOT. It is running fine and you are receiving this message every 5 minutes "
healthtime = int(time.time())

while looper==0:
    cn = 0
    updatefile = open(path + "updateid.txt", 'r+')
    updatetext = updatefile.read()
    updatefile.close()
    #Starting Long Polling
    lastupdate=int(updatetext)
    payloadpoll = {"offset":lastupdate,"limit": 20,"timeout": pollgap}
    response = requests.post(pollurl, json=payloadpoll, headers=headers)
    f = urllib.request.urlopen(pollurl)
    data=json.load(f)
    b=data

    c=str(b)

    lenc=len(c)
    print(c)
    print(lenc)
    if lenc<50:
        print("No New message "+str(datetime.now().strftime("%H:%M:%S")))
    if lenc>50:
      print("Message received at: "+str(datetime.now().strftime("%H:%M:%S")))
      tempstr = c[0:lenc]
      while cn==0:
       usernametext=""
       usernamepos1=tempstr.find("username")
       if usernamepos1!=-1:
         usernamepos2=tempstr.find("language_code")
         usernametext=tempstr[usernamepos1+12:usernamepos2-4]
       messagepostemp=0
       updatepos1 = tempstr.find("update_id':")
       print("updatepos1",updatepos1)
       if updatepos1==-1:
        break
       namepos = tempstr.find("is_bot': False, 'first_name':")
       namepos1 = tempstr.find("last_name")
       namepos2 = tempstr.find("username")
       namepos3 = tempstr.find("language_code")
       print("namepos", namepos)
       print("namepos1", namepos1)
       numberpos = tempstr.find("from")
       print("numberpos",numberpos)
       datepos = tempstr.find("date':")
       print("datepos",datepos)
       endpos1 = tempstr.find("}}, {")
       print("endpos1",endpos1)
       endpos2 = tempstr.find("}}]}")
       messagepos = tempstr.find("text")
       if messagepos-datepos>20:
         messagepostemp =messagepos
         messagepos=datepos+20
       print("messagepos",messagepos)
       updatetext1 = tempstr[updatepos1 + 12:updatepos1 + 21]
       print(updatetext1)
       numbertext = tempstr[numberpos + 14:numberpos + 24]
       print(numbertext)
       if namepos1 != -1:
           nametext = tempstr[namepos + 31:namepos1 - 4]

       if namepos1 == -1 and namepos2!=-1 :
           nametext = tempstr[namepos + 31:namepos2 - 4]

       if namepos1 == -1 and namepos2 == -1 and namepos3!=-1:
           nametext = tempstr[namepos + 31:namepos3 - 4]


       print("Name: " + nametext)
       datetext = tempstr[datepos + 7:datepos + 17]
       dateconfirm = datetext[2:10]
       datetext=(datetime.fromtimestamp(int(datetext)).strftime('%Y-%m-%d %H:%M:%S'))
       print(datetext)
       if endpos1!=-1:
        messagetext=tempstr[messagepos+8:endpos1-1]
        if messagepostemp-datepos>20:
          messagetext="No Text"
       if endpos1==-1:
        messagetext=tempstr[messagepos+8:endpos2-1]
        if messagepostemp-datepos>20:
          messagetext="No Text"
       #print(messagetext)
       messagetext = messagetext.replace("\\xa0", " ")

       print(messagetext)
       print("----------------")

       print("username: "+usernametext)

       apos=nametext.find(",")
       if apos!=-1:
           u1=nametext[0:apos-1]
       else:
        u1 = nametext

       if u1 != u2:
           alert = u1 + " has just logged in\n\n"
           alert1 = "<a href='tg://user?id=" + numbertext + "'>Click to chat here</a>"
           if usernametext!="":
               alert1=alert1+"\n\nor "+"@"+usernametext
           # print(alert1)
           payloadtext = {"text": alert + alert1, "parse_mode": "html", "disable_web_page_preview": False,
                          "disable_notification": False, "reply_to_message_id": None, "chat_id": replyto}
           response = requests.post(texturl, json=payloadtext, headers=headers)
           u2 = u1
       callbackpos=messagetext.find("'data':")
       callbacktext=messagetext[callbackpos+9:len(messagetext)]
       print("callbacktext:",callbacktext)
       userfile = open(path + "user.txt", 'r',encoding='utf-8', errors='ignore')
       usertext=userfile.read()
       userfile.close
       find1=usertext.find(numbertext)
       if find1==-1:
        userfile = open(path + "user.txt", 'a')
        userfile.write(numbertext+","+datetext+","+nametext+"\n")
        userfile.close()

       if messagetext[0:6] == "/start":
           payloadtext = {"text": "Hello "+nametext +"\n\nWelcome to Youtube Downloader BOT. Just send any Youtube URL to download the Video", "parse_mode": "html",
                          "disable_web_page_preview": True,
                          "disable_notification": False, "reply_to_message_id": None, "chat_id": numbertext}
           response = requests.post(texturl, json=payloadtext, headers=headers)
           break
       elif messagetext[0:15] == "https://youtube" or messagetext[0:13] == "https://youtu":
          spcfind=messagetext.find("entities")
          if spcfind!=-1:
             messagetext=messagetext[0:spcfind-4]
          link = messagetext
          print(messagetext)
          print(link)
          yt = YouTube(link)

          try:
              yt.streams.filter(progressive=True,
                                file_extension="mp4").first().download(output_path=path,
                                                                       filename="video" + ".mp4")
              yt.streams.filter(only_audio=True).first().download(output_path=path,
                                                                       filename="Audio" + ".mp3")
          except pytube.exceptions.RegexMatchError:
              message=("There is some error in this Youtube URL . Please check and send Valid Youtube URL only")
              payloadtext = {"text": message + nametext, "disable_web_page_preview": True,
                             "disable_notification": False, "reply_to_message_id": None, "chat_id": numbertext}
              response = requests.post(texturl, json=payloadtext, headers=headers)
              break
          message="Successfully Dowloaded.Now sending it to you in a moment..."
          payloadtext = {"text": message + nametext, "disable_web_page_preview": True,
                         "disable_notification": False, "reply_to_message_id": None, "chat_id": numbertext}
          response = requests.post(texturl, json=payloadtext, headers=headers)
          file = path +"video"+ ".mp4"
          files = {'document': open(file, 'rb')}
          response = requests.post(docurl + "?chat_id={}".format(numbertext), files=files)
          print(response.text)
          file2 = path + "Audio" + ".mp3"
          files = {'document': open(file2, 'rb')}
          response = requests.post(docurl + "?chat_id={}".format(numbertext), files=files2)
          print(response.text)
          break


       elif messagetext[0:15] != "https://youtube":
           payloadtext = {"text": "What, "+nametext,"disable_web_page_preview": True,
                          "disable_notification": False, "reply_to_message_id": None, "chat_id": numbertext}
           response = requests.post(texturl, json=payloadtext, headers=headers)
           break

       tempstr = tempstr[endpos1+4 :lenc]


    if int(updatetext1)>=int(updatetext):
      updatefile = open(path + "updateid.txt", 'w')
      updatetext = int(updatetext1)+1
      updatefile.write(str(updatetext))
      updatefile.close()

    healthtime1 = int(time.time())
    # print(healthtime1)
    if healthtime1 - healthtime > 300:
        payloadtext = {"text": healthmessage, "parse_mode": "html", "disable_web_page_preview": False,
                       "disable_notification": False, "reply_to_message_id": None, "chat_id": replyto}
        response = requests.post(texturl, json=payloadtext, headers=headers)
        healthtime = healthtime1

    print("Offset ID in Text File updated succesfully")
