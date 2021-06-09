from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import os
import tcase as t

app = Flask(__name__)

@app.route('/mybot', methods = ['POST'] )

def mybot():
    incoming_msg = request.values.get('Body','').lower()
    resp = MessagingResponse()
    msg = resp.message()
    pin_code="000000"
    date ="00-00-0000"
    responded = False
    if (incoming_msg in ['hi','hello','hey','hlo','hlow','who are you','may i know you','hy']):
        msg.body("Hello, I am *COVID VACCINE TRACKER BOT* \nI will let you know whether vaccine doses for your age group is available or not in your area. \n\nPlease select the option: \n1. Yes, I want to continue \n2. No, I don't want to continue \n*Hint: Please type the option number to proceed*")
    
    elif('2' in incoming_msg and len(incoming_msg)==1):
        msg.body("Thanks...")
    
    elif('1' in incoming_msg and len(incoming_msg)==1):
        msg.body("What is your District pin code ? (eg Delhi pin 110001)")
    
    elif(len(incoming_msg)==6 and incoming_msg.isdigit()):
        pin_code = incoming_msg
        date = datetime.datetime.today()
        date = date.strftime("%d-%m-%Y")
        
        ndata = t.find_avail(pin_code,date)
        msg.body(ndata)
        with open('abc.txt','w') as file:
            file.write('')
        responded = True

    elif(len(incoming_msg)>6 or incoming_msg.isalnum()):
        msg.body("*Type the correct Pin Code*")

    else:
        msg.body("This is *COVID VACCINE TRACKER BOT*\nGreet the bot with *Hi* or *Hello* to initiate the conversation.")
    return str(resp)

if __name__=='__main__':
    app.run()


