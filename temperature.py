#!/usr/bin/env/python3
import RPi.GPIO as GPIO
import time, datetime
import Adafruit_DHT
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from template import *


gmail_sender = 'cilabtemperature@gmail.com'
gmail_passwd = 'Password00?!'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(gmail_sender, gmail_passwd)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.HIGH)

def Rounding():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
        temperature = round(temperature,2)
        humidity = round(humidity,2)
    except:
        pass
    return temperature, humidity

'''
temp <26: ext-krzysztof.heigel@here.com, ext-bartosz.bialobrzeski@here.com, 
temp >26: ext-krzysztof.heigel@here.com, ext-bartosz.bialobrzeski@here.com, marco-kimpfler@here.com, oleg.tydynyan@here.com
temp >32: ext-krzysztof.heigel@here.com, ext-bartosz.bialobrzeski@here.com, security.berlin@here.com
'''

def EmailSend(TEXT, SUBJECT, recipients, temp):
    server.set_debuglevel(1)
    message = MIMEMultipart('related')
    message.attach(MIMEText(TEXT, 'html'))
    img = '1.jpg'
    if (temp<26):
        img = '1.jpg'
    elif (temp>=26 and temp<32):
        img = '2.jpg'
    elif (temp>=32):
        img = '3.jpg'
    
    with open(img, 'rb') as image_file:
        image = MIMEImage(image_file.read())
    image.add_header('Content-ID', '<picture@example.com>')
    image.add_header('Content-Disposition', 'inline', filename=img)
    message.attach(image)
    
    message['Subject'] = SUBJECT
    message['From'] = gmail_sender
    message['To'] = ", ".join(recipients)
    server.sendmail(gmail_sender, recipients, message.as_string())
    
while True:
    temperature,humidity = Rounding()
    recipients = ['ext-krzysztof.heigel@here.com']
    EmailSend(TEXTOK.format(temperature), SUBJECTOK, recipients, temperature)
    while temperature<26:
        temperature,humidity = Rounding()
        #time.sleep(30)
        print("Temperature: {}C  below 26 Humidity: {}% Date and Time: {}".format(temperature, humidity, datetime.datetime.now()))
        if temperature>=26:
            recipients = ['ext-krzysztof.heigel@here.com']
            EmailSend(TEXT26.format(temperature), SUBJECT26, recipients, temperature)
    while temperature>=26 and temperature<32:
        temperature,humidity = Rounding()
        #time.sleep(30)
        print("Temperature: {}C below 32 Humidity: {}% Date and Time: {}".format(temperature, humidity, datetime.datetime.now()))
        if temperature>=32:
            recipients = ['ext-krzysztof.heigel@here.com']
            EmailSend(TEXT32.format(temperature), SUBJECT32, recipients, temperature)
    
    
    
    
    
    
