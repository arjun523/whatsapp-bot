import requests

def find_avail(pin_code,date):
    URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(pin_code,date)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

    counter=0
    result = requests.get(URL, headers=header)
    response_json = result.json()
    data = response_json["sessions"]
    n=len(data)
    for num in range(0,len(data)):
        each = data[num]
        if(int(each["available_capacity_dose1"])>0):
            counter +=1
            with open("abc.txt" ,'a') as file:
                dataf = file.writelines(f"Center Name: *{each['name']}*, Address: *{each['address']}*, Minimun Age: *{each['min_age_limit']}*, Vaccine: *{each['vaccine']}*, Fee: *{each['fee_type']}* Total Available Dose Capacity: *{each['available_capacity']}* \t \t  ")
            
    if(counter==0):
        return("\n*No Available Slots right now!!! Try again tomorrow...*\n")
    if(counter):
        with open('abc.txt','r') as file:
            ndata = file.read()
            return ndata
