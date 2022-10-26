# Written in Python 3.8.5

from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
from time import sleep
import winsound

win = Tk()
win.geometry("500x250")
win.title("Reminder Console")

def display_time(popup):
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=int(reminder_length.get()))
    
    current_time = "00:"+reminder_length.get().zfill(2)+":00"
    
    popup.timer_label.config(text = current_time)
    popup.flavor_label.grid(row=0, column=0, padx=40, pady=40)
    popup.timer_label.grid(row=1, column=0, padx=40, pady=40)

    popup.update_idletasks()
    popup.update()
    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    while(datetime.now() < end_time):
        time_left = end_time - datetime.now()
        current_time = str(int(time_left.seconds/3600)).zfill(2)+":"+str(int((time_left.seconds%3600)/60)).zfill(2)+":"+str(time_left.seconds%60).zfill(2)
        try:
            popup.timer_label.config(text = current_time)
            popup.flavor_label.grid(row=0, column=0, padx=40, pady=40)
            popup.timer_label.grid(row=1, column=0, padx=40, pady=40)

            popup.update_idletasks()
            popup.update()
        except:
            print("Popup closed after only "+str(datetime.now()-start_time)+", with "+str(end_time-datetime.now())+" left to go.")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            return
    print("Break over.")
    popup.destroy()
    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
    return

def open_popup():
    popup=Toplevel(win)
    popup.geometry("1280x720")
    popup.title("Break Reminder")
    popup.state('zoomed')
    popup.attributes('-topmost', True)
    popup.focus_set()
    popup.columnconfigure(0,weight=1)
    popup.rowconfigure(0,weight=1)
    break_length_in_milliseconds = int(reminder_length.get()) * 60 * 1000
    curr_time = datetime.now().time()
    flavor_message = "Go take a break! Stand up, do some yoga, refill your water, and take a piss! Your work can wait."
    if(curr_time.hour >= (int(reminder_end.get())-1)):
        #This fires off at the hour you've designated as the end of your reminder period.
        #It was made with the assumption that you'd leave the timing as default, where the break goes from :55 to :00.
        flavor_message = "You're done! Stand up, do some yoga, refill your water, and take a piss! Your workday is over."
    if((curr_time.hour == 11 and curr_time.minute >= 30) or (curr_time.hour == 12 and curr_time.minute <= 30)):
        #This fires off for reminders that happen within 30 minutes of local noon, which is assumed to be when you'd eat lunch.
        flavor_message = "Go eat lunch! It's about that time! Your work can wait for you to stop being hungry."
    popup.flavor_label = Label(popup, wraplength=1200, text= flavor_message, font=('Helvetica 28 bold'))
    popup.timer_label = Label(popup, wraplength=1200, text= "00:"+reminder_length.get().zfill(2)+":00", font=('Helvetica 28 bold'))
    popup.flavor_label.grid(row=0, column=0, padx=40, pady=40)
    popup.timer_label.grid(row=1, column=0, padx=40, pady=40)
    popup.update()
    display_time(popup)

def has_focus(window):
    return window.focus_displayof()

#I took the bones of this from an online tutorial and have made it unrecognizable.
#This file used to be a lot uglier before I decided it'd be a good portfolio piece and realized I had to make it presentable.

Label(win, text="Time For Hourly Break:", font= ('Helvetica 14 bold')).grid(column=0,row=0,sticky=(W,E))
reminder_schedule = StringVar()
reminder_schedule_entry = ttk.Entry(win, width=2, textvariable=reminder_schedule)
reminder_schedule_entry.grid(column=1,row=0,sticky=(W,E))
reminder_schedule_entry.insert(END, "55")

Label(win, text="Length Of Hourly Break:", font= ('Helvetica 14 bold')).grid(column=0,row=1,sticky=(W,E))
reminder_length = StringVar()
reminder_length_entry = ttk.Entry(win, width=2, textvariable=reminder_length)
reminder_length_entry.grid(column=1,row=1,sticky=(W,E))
reminder_length_entry.insert(END, "5")

Label(win, text="Start Of Hourly Breaks:", font= ('Helvetica 14 bold')).grid(column=0,row=2,sticky=(W,E))
reminder_start = StringVar()
reminder_start_entry = ttk.Entry(win, width=2, textvariable=reminder_start)
reminder_start_entry.grid(column=1,row=2,sticky=(W,E))
reminder_start_entry.insert(END, "6")

Label(win, text="End Of Hourly Breaks:", font= ('Helvetica 14 bold')).grid(column=0,row=3,sticky=(W,E))
reminder_end = StringVar()
reminder_end_entry = ttk.Entry(win, width=2, textvariable=reminder_end)
reminder_end_entry.grid(column=1,row=3,sticky=(W,E))
reminder_end_entry.insert(END, "18")

ttk.Button(win, text= "Open", command= open_popup).grid(column=0,row=4) #pack()
reminder_spawned = False
win.update_idletasks()
win.update()

while(True):
    if(datetime.now().weekday() < 5):
        now_raw = datetime.now().time()
        minute_raw = now_raw.minute
        hour_raw = now_raw.hour
        if(minute_raw == int(reminder_schedule.get()) and reminder_spawned == False and hour_raw > int(reminder_start.get()) and hour_raw < int(reminder_end.get())):
            reminder_spawned = True
            open_popup()
        elif(minute_raw != int(reminder_schedule.get()) and reminder_spawned == True):
            reminder_spawned = False
        try:
            win.update_idletasks()
            win.update()
            sleep(1)
        except:
            print("Application closed.")
            break
    else:
        sleep(60)
