import json
import time
import requests
import webbrowser
import tkinter as tk
from tkinter import ttk
import datetime
from playsound import playsound

Pin_code=[560002] #write list of pincode for which you want to check 
Your_age=46 #Write your age in year
sleep_time=10 #in sec, If you take too small then api will block you so take it as 60 sec
How_many_days=3 #2 it will check for slot available Today or Tomorrow 

def callback():
    webbrowser.open_new(r"https://selfregistration.cowin.gov.in/")

def play():
    playsound('./output/1.mp3')

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Vaccine is Available")
    for i in msg:
        label = ttk.Label(popup, text=i)
        label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Go to Website", command = callback)
    B1.pack()
    popup.mainloop()

def check_available():
    while True:
        try:
            Date=[]
            msg=[]
            for k in range(How_many_days):
                Date.append((datetime.date.today() + datetime.timedelta(days = k)).strftime("%d-%m-%Y"))
            flag=False
            for j in Pin_code:
                for k in Date:
                    rsp = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(j)+"&date="+k)
                    strrsp = rsp.text
                    jsonrsp = json.loads(strrsp)
                    availability=jsonrsp['sessions']
                    for i in availability:
                        print("Name:",i['name']," PinCode: ",i['pincode']," Name of the Vaccine: ",i['vaccine']," Available Capacity: ",i['available_capacity'], "Date: ",k, "Age: ",i['min_age_limit'])
                        if(i['available_capacity']>0 and i['min_age_limit']<=Your_age):
                            msg.append("Name: "+i['name']+" PinCode: "+str(i['pincode'])+" Name of the Vaccine: "+i['vaccine']+" Available Dose: "+str(i['available_capacity'])+" Date: "+k+" Age_limit: "+str(i['min_age_limit']))
                            flag=True
            
            print("[INFO] Checked,Till now no center available, will check after: ",sleep_time," sec")
            if flag:
                playsound("./output/alert.mp3")
                popupmsg(msg)
                break
            
            time.sleep(sleep_time)
        except Exception as e:
            print(e)

if(__name__=="__main__"):
    print("[INFO] Script Started successfully") 
    check_available()