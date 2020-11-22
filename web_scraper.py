from urllib.request import urlopen
from datetime import datetime
import time
from tkinter import *
from tkinter import messagebox
import numpy as np
from bs4 import BeautifulSoup

url = 'https://spaceflightnow.com/launch-schedule/'

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Dump html to a .txt file for inspection
file_object = open(r'html_dump.txt', 'r+')
file_object.write(html)
file_object.close()

soup = BeautifulSoup(html, 'html.parser')

a = soup.findAll("span", class_="launchdate")
b = soup.findAll('div', class_='missiondata')

current_date = datetime.today()

for date, mission in zip(a, b):
    # Combine time/date data to be parsed together
    missiontime = mission.text[13:17]
    if missiontime.find('TBD') != -1:
        missiontime = '0001'

    # Clean date (can have '/' in date so make sure to remove them)
    if date.text.find('/') != -1:
        split_month = date.text.split()[0]
        split_day = date.text.split('/')[1]
        date_cleaned = split_month + ' ' + split_day
    else:
        date_cleaned = date.text
    
    datemission = str(current_date.year) + date_cleaned + missiontime + 'GMT'
    # Parse the string to get date
    launch_date_parsed = datetime.strptime(datemission, '%Y%b. %d%H%M%Z')

    # if date of mission is before time now, go on to next
    if launch_date_parsed > current_date:
        print('good to go!')
        break
    
    # if it is after, use that data and exit loop


# # Function to find data given start and end string
# def get_launch_data(start_str, end_str, search_start_index=0):
#     start_index = html.find(start_str) + len(start_str)
#     end_index = html.find(end_str)
#     return html[start_index: end_index]

# Get launch data and strip spaces from beginning and end
# launch_name = get_launch_data('</span><span class="mission">', '</span></div>').strip()
# # launch_date = get_launch_data('<span class="launchdate">', '</span><span class="mission">').strip()
# launch_date = 'Nov. 25' # Temporary launch date until Falcon 9 launch removed from website
# launch_time = get_launch_data('Launch time:</span> ', '<span class="strong"><br />').strip()

# Clean launch data into usable format
launch_time_cleaned = launch_time[:launch_time.find('GMT')+len('GMT')]

# Get current year to pass to launch_datetime (not provided on website)
# current_date = datetime.today()
# current_year = str(current_date.year)

# Parse launch time and date into one object
launch_datetime = current_year + launch_date + launch_time_cleaned
launch_datetime_parsed = datetime.strptime(launch_datetime, '%Y%b. %d%H%M:%S %Z')


#####################################################
################## Countdown GUI ####################
#####################################################

# Define tk elements
root = Tk()
root.title('Launch Countdown Timer')
root.geometry('500x150')

# Launch timer header which includes launch info
timer_header = Label(root, text=launch_name, font=('Helvetica', 20), bg='black', fg='white')
timer_header.pack(pady=10, ipadx=10, ipady=10)

# Assign initial time until launch
length_of_countdown = launch_datetime_parsed - datetime.utcnow()
time_left_seconds = length_of_countdown.total_seconds()

# Define time string as a StringVar for Tkinter
time_string_to_display = StringVar()

timer_time_display = Label(root, text=time_string_to_display, font=('Helvetica', 15), bg='black', fg='red')
timer_time_display.pack(pady=10, ipadx=10, ipady=10)

while time_left_seconds:
    # Get timedelta object of time until launch
    length_of_countdown = launch_datetime_parsed - datetime.utcnow()
    #print(length_of_countdown)

    # Time until launch in seconds
    time_left_seconds = length_of_countdown.total_seconds()

    # Calculate hours, minutes, and seconds until next launch
    hours = int(abs(time_left_seconds / 3600))
    minutes = int(np.floor(time_left_seconds % 3600) / 60)
    seconds = int(np.floor(time_left_seconds % 60))
    
    # Format string for timer to display
    time_string_to_display = '{}:{}:{}'.format(hours, minutes, seconds)
    
    # Print label to display on timer
    timer_time_display.config(text = time_string_to_display)
    
    time.sleep(1)
    root.update()

root.mainloop()