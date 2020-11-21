from urllib.request import urlopen
from datetime import datetime
import time
from tkinter import *
from tkinter import messagebox
import numpy as np

url = 'https://spaceflightnow.com/launch-schedule/'

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Dump html to a .txt file for inspection
file_object = open(r'html_dump.txt', 'w')
file_object.write(html)
file_object.close()

# Function to find data given start and end string
def get_launch_data(start_str, end_str):
    start_index = html.find(start_str) + len(start_str)
    end_index = html.find(end_str)
    return html[start_index: end_index]

# Get launch data and strip spaces from beginning and end
launch_name = get_launch_data('</span><span class="mission">', '</span></div>').strip()
# launch_date = get_launch_data('<span class="launchdate">', '</span><span class="mission">').strip()
launch_date = 'Nov. 25' # Temporary launch date until Falcon 9 launch removed from website
launch_time = get_launch_data('Launch time:</span> ', '<span class="strong"><br />').strip()

# print(launch_name)
# print(launch_date)
# print(launch_time)

# Clean launch data into usable format
launch_time_cleaned = launch_time[:launch_time.find('GMT')+len('GMT')]

# Get current year to pass to launch_datetime (not provided on website)
current_date = datetime.today()
current_year = str(current_date.year)

# Parse launch time and date into one object
launch_datetime = current_year + launch_date + launch_time_cleaned
launch_datetime_parsed = datetime.strptime(launch_datetime, '%Y%b. %d%H%M:%S %Z')

# Get timedelta object of time until launch
length_of_countdown = launch_datetime_parsed - datetime.utcnow()
#print(length_of_countdown)

hours = str(abs(np.floor(length_of_countdown.total_seconds() / 3600)))
minutes = str(np.floor((length_of_countdown.total_seconds() % 3600) / 60))
seconds = str(np.floor(length_of_countdown.total_seconds() % 60))



#####################################################
################## Countdown GUI ####################
#####################################################
# define the countdown func. 
def countdown(t): 
    
    while t: 
        mins, secs = divmod(t, 60) 
        timer = '{:02d}:{:02d}'.format(mins, secs) 
        print(timer, end="\r") 
        time.sleep(1) 
        t -= 1
      
    print('Fire in the hole!!') 
  
  
# input time in seconds 
t = length_of_countdown.total_seconds()
  
# function call 
countdown(int(t)) 