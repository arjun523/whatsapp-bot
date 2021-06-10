from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
import datetime
import tcase as t

app = Flask(__name__)

@app.route('/mybot', methods = ['GET','POST'] )

def mybot():
    incoming_msg = request.values.get('Body','').lower()
    resp = MessagingResponse()
    msg = resp.message()
    age='00'
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
        URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin_code,date)
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        string =''
        counter=0
        result = requests.get(URL, headers=header)
        response_json = result.json()
        data = response_json["sessions"]
        n=len(data)
        for num in range(0,len(data)):
            each = data[num]
            if(int(each["available_capacity_dose1"])>0):
                counter +=1
                string = string + f"Center Name: *{each['name']}*, Address: *{each['address']}*, Minimun Age: *{each['min_age_limit']}*, Vaccine: *{each['vaccine']}*, Fee: *{each['fee_type']}* Total Available Dose Capacity: *{each['available_capacity']}* \t \t  "
            # with open("abc.txt" ,'a') as file:
            #     dataf = file.writelines(f"Center Name: *{each['name']}*, Address: *{each['address']}*, Minimun Age: *{each['min_age_limit']}*, Vaccine: *{each['vaccine']}*, Fee: *{each['fee_type']}* Total Available Dose Capacity: *{each['available_capacity']}* \t \t  ")
            
        if(counter==0):
            msg.body("\n*No Available Slots right now!!! Try again tomorrow...*\n")
        if(counter):
        # with open('abc.txt','r') as file:
        #     ndata = file.read()
        #     return ndata
            msg.body(string)
        
        responded = True

    elif(len(incoming_msg)>6 or incoming_msg.isalnum()):
        msg.body("*Type the correct Pin Code*")

    else:
        msg.body("This is *COVID VACCINE TRACKER BOT*\nGreet the bot with *Hi* or *Hello* to initiate the conversation.")
    return str(resp)

if __name__=='__main__':
    app.run()


