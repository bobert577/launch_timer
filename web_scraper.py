from urllib.request import urlopen
from datetime import datetime
import time
from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup

url = 'https://spaceflightnow.com/launch-schedule/'

# Save url html data
page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Parse html data into a soup object
soup = BeautifulSoup(html, 'html.parser')

# Define data we care about into lists
a = soup.findAll("span", class_="launchdate")
b = soup.findAll('div', class_='missiondata')
c = soup.findAll("span", class_="mission")

# Assign current_date to now
current_date = datetime.today()

# Run for loop until future launch is found (website isn't updated automatically)
for date, missiondata, mission in zip(a, b, c):
    # Assign launch name
    launch_name = mission.text
        
    # Combine time/date data to be parsed together
    missiontime = missiondata.text[13:17]
    # If mission time is "TBD" assign it as 0001 so you don't miss the launch!
    if missiontime.find('TBD') != -1:
        missiontime = '0001'

    # Clean date (can have '/' in date so make sure to remove them)
    if date.text.find('/') != -1:
        # Get month of launch
        split_month = date.text.split()[0]
        # Get day of launch (GMT will always be 2nd of two dates provided)
        split_day = date.text.split('/')[1]
        date_cleaned = split_month + ' ' + split_day
    else:
        date_cleaned = date.text
    
    # Concatenate all date info into one string for parseing
    mission_date_time = str(current_date.year) + date_cleaned + missiontime + 'GMT'
    # Parse the string to get datetime object
    launch_datetime_parsed = datetime.strptime(mission_date_time, '%Y%b. %d%H%M%Z')

    # if date of mission is in future, break loop and proceed
    if launch_datetime_parsed > current_date:
        print('good to go!')
        break


#####################################################
################## Countdown GUI ####################
#####################################################

# Define tkinter elements
root = Tk()
root.title('Launch Countdown Timer')
root.geometry('550x150')
root.configure(background='black')

# Launch timer header which includes launch info
timer_header = Label(root, text=launch_name, font=('Helvetica', 20), bg='black', fg='white')
timer_header.pack(pady=10, ipadx=10, ipady=10)

# Define time string as a StringVar for Tkinter
time_string_to_display = StringVar()

timer_time_display = Label(root, text=time_string_to_display, font=('Helvetica', 20), bg='black', fg='red')
timer_time_display.pack(pady=0, ipadx=10, ipady=10)

# Assign initial time until launch (will get re-assigned every loop)
length_of_countdown = launch_datetime_parsed - datetime.utcnow()
time_left_seconds = length_of_countdown.total_seconds()

while time_left_seconds:
    # Get timedelta object of time until launch
    length_of_countdown = launch_datetime_parsed - datetime.utcnow()
    
    # Time until launch in seconds
    length_of_countdown_seconds = length_of_countdown.total_seconds()

    # Calculate hours, minutes, and seconds until next launch and convert to zero padded string
    hours = str(int(length_of_countdown_seconds / 3600)).zfill(2)
    minutes = str(int(length_of_countdown_seconds % 3600 / 60)).zfill(2)
    seconds = str(int(length_of_countdown_seconds % 60)).zfill(2)
    
    # Format string for timer to display
    time_string_to_display = '{}:{}:{}'.format(hours, minutes, seconds)
    
    # Print label to display on timer
    timer_time_display.config(text = time_string_to_display)
    
    # Sleep for 1 second then update tk
    time.sleep(1)
    root.update()

root.mainloop()