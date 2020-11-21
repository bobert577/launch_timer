from urllib.request import urlopen
from datetime import datetime

# url = 'http://olympus.realpython.org/profiles/aphrodite'
url = 'https://spaceflightnow.com/launch-schedule/'

page = urlopen(url)
html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Function to find data given start and end string
def get_launch_data(start_str, end_str):
    start_index = html.find(start_str) + len(start_str)
    end_index = html.find(end_str)
    return html[start_index: end_index]

# Get launch data and strip spaces from beginning and end
launch_name = get_launch_data('</span><span class="mission">', '</span></div>').strip()
launch_date = get_launch_data('<span class="launchdate">', '</span><span class="mission">').strip()
launch_time = get_launch_data('Launch time:</span> ', '<span class="strong"><br />').strip()

# print(launch_name)
# print(launch_date)
# print(launch_time)

# Dump html to a .txt file for inspection
# file_object = open(r'html_dump.txt', 'w')
# file_object.write(html)
# file_object.close()

# Clean launch data into usable format
launch_time_cleaned = launch_time[:launch_time.find('GMT')+len('GMT')]

# Get current year to pass to launch_datetime (not provided on website)
current_date = datetime.today()
current_year = str(current_date.year)

# Parse launch time and date into one object
launch_datetime = current_year + launch_date + launch_time_cleaned
launch_datetime_parsed = datetime.strptime(launch_datetime, '%Y%b. %d%H%M:%S %Z')

print(launch_datetime_parsed)