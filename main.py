from tkinter import *
import json
import time
import requests
import webbrowser
import tkinter as tk
from tkinter import ttk
import datetime

fields = ('PinCode', 'Your Age', 'Rerun Script time in sec', 'How many future days','[INFO]')

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

def check_available(Pin_code,Age_limit,sleep_time,How_many_days):
    while True:
        try:
            Date=[]
            for k in range(How_many_days):
                Date.append((datetime.date.today() + datetime.timedelta(days = k)).strftime("%d-%m-%Y"))
            flag=False
            msg=[]
            for j in Pin_code:
                for k in Date:
                    rsp = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode="+str(j)+"&date="+k)
                    strrsp = rsp.text
                    jsonrsp = json.loads(strrsp)
                    availability=jsonrsp['sessions']
                    for i in availability:
                        print("Name:",i['name']," PinCode: ",i['pincode']," Name of the Vaccine: ",i['vaccine']," Available Capacity: ",i['available_capacity'], "Date: ",k)
                        if(i['available_capacity']>0 and i['min_age_limit']<=int(Age_limit)):
                            msg.append("Name: "+i['name']+" PinCode: "+str(i['pincode'])+" Name of the Vaccine: "+i['vaccine']+" Available Dose: "+str(i['available_capacity'])+" Date: "+k)
                            flag=True
            
            print("[INFO] Checked,Till now no center available, will check after: ",sleep_time," sec")
            if flag:
                popupmsg(msg)
                break
            
            time.sleep(sleep_time)
        except Exception as e:
            print(e)

def find_slot(entries):
    Pin_code=eval(entries[fields[0]].get()) #write list of pincode for which you want to check 
    Age_limit=eval(entries[fields[1]].get())#Either 18 or 45
    sleep_time=eval(entries[fields[2]].get()) #in sec, If you take too small then api will block you so take it as 60 sec
    How_many_days=eval(entries[fields[3]].get()) #2 it will check for slot available Today or Tomorrow 
    entries[fields[4]].setvar("Script Started Successfully")
    check_available(Pin_code,Age_limit,sleep_time,How_many_days)

def makeform(root, fields):
   entries = {}
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=22, text=field+": ", anchor='w')
      ent = Entry(row)
      ent.insert(0,"0")
      row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
      lab.pack(side = LEFT)
      ent.pack(side = RIGHT, expand = YES, fill = X)
      entries[field] = ent
   return entries

if __name__ == '__main__':
   root = Tk()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e = ents: fetch(e)))
   b1 = Button(root, text = 'Run Script',
      command=(lambda e = ents: find_slot(e),root.quit))
   b1.pack(side = LEFT, padx = 5, pady = 5)
   b3 = Button(root, text = 'Quit', command = root.quit)
   b3.pack(side = LEFT, padx = 5, pady = 5)
   root.mainloop()