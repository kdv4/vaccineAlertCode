import json
import time
import requests
import webbrowser
import tkinter as tk
from tkinter import ttk
from datetime import date



Pin_code=[395009,395006,560002] #write list of pincode for which you want to check 
Age_limit=18 #Either 18 or 45
sleep_time=10 #in sec, If you take too small then api will block you so take it as 60 sec

def callback():
        webbrowser.open_new(r"https://selfregistration.cowin.gov.in/")

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Vaccine is Available")
    for i in msg:
        label = ttk.Label(popup, text=i)
        label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Go to Website", command = callback)
    B1.pack()
    popup.mainloop()

        
while True:
    try:
        Date=date.today().strftime("%d-%m-%Y")
        flag=False
        msg=[]
        for j in Pin_code:
            rsp = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(j)+"&date="+Date)
            strrsp = rsp.text
            jsonrsp = json.loads(strrsp)
            availability=jsonrsp['sessions']
            for i in availability:
                print("Name:",i['name']," PinCode: ",i['pincode']," Name of the Vaccine: ",i['vaccine']," Available Capacity: ",i['available_capacity'])
                if(i['available_capacity']>0):
                    msg.append("Name: "+i['name']+"PinCode: "+str(i['pincode'])+" Name of the Vaccine: "+i['vaccine']+" Available Capacity: "+str(i['available_capacity']))
                    flag=True

        if flag:
            popupmsg(msg)
            break

        time.sleep(sleep_time)
    except Exception as e:
        print(e)