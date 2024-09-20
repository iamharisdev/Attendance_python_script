from skpy import Skype, SkypeEventLoop, SkypeChats
import subprocess
import webbrowser
import os
from dotenv import load_dotenv

import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Load the .env file
load_dotenv()


# # Define your Skype credentials
username = os.getenv('username')
password = os.getenv('password')
chatId =os.getenv('chatId')
file_path =os.getenv('file_path')
example=os.getenv('example')
token_file =os.getenv('token_file') # File to store the Skype token
chrome_drive = os.getenv('chrome_drive')

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for no GUI
service = Service(chrome_drive)  # Path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)




# btn btn-success btn-sm mb-3


# sk = Skype(username, password)  # Authenticate using username and password

# Initialize Skype object with token file to avoid re-authenticating on every run
try:
    sk = Skype(tokenFile=token_file)  # Load token from file
    print("Token loaded successfully.")
except Exception as e:
    print(f"Token expired or invalid. Re-authenticating... {str(e)}")
    sk = Skype(username, password, tokenFile=token_file)  # Authenticate using username and password, and save token to file
    print("Token saved successfully.")




# # # Loop through the recent chats to get detailed information
# for chat_id, chat_summary in recent_chats.items():
#     # Fetch the chat object using the chat ID
#     chat = skc[chat_id]
    
#     print (f"chat details:=>  ",{chat})
#     #  print(f"Chat Name: {chat.topic if chat.topic else 'No Topic'}")
#     # print(f"Chat ID: {chat.id}")
#     # print(f"Participants: {[user.name for user in chat.userIds]}")
#     print("-" * 30)


# Get chat by chat ID
chat = sk.chats[example]
# Fetch only the last message in the chat



# Function to ring the bell in macOS
def ring_bell():
    subprocess.run(["afplay", file_path])

# Function to extract URL from HTML anchor tag
def extract_href(html):
    # Regex pattern to find the href value within an <a> tag
    href_pattern = re.compile(r'href="([^"]+)"')
    match = href_pattern.search(html)
    return match.group(1) if match else None

# Function to open a URL in the web browser
def open_url(url):
     print(f"URL:=>  {url}")
     webbrowser.open(url)
     driver.get(url)
     click_attendance_button()
                             
                             

# Function to click the attendance button
def click_attendance_button():
    try:
        # Locate the button by its class name
        button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-success.btn-sm.mb-3")
        button.click()
        print("Button clicked successfully.")
    except Exception as e:
        print(f"Error clicking button: {str(e)}")



# Event handler for incoming messages
class MySkypeEventLoop(SkypeEventLoop):
    def __init__(self, username, password):

        super(MySkypeEventLoop, self).__init__(username, password)

    def onEvent(self, event):
       
         if event.type == "ConversationUpdate" and event.chatId == chatId:
             try:
                  recent_msgs = chat.getMsgs()
                  if recent_msgs:
                       last_msg = recent_msgs[0]
                       print(f"Sender: {last_msg.userId}")
                       print(f"Message: {last_msg.content}")
                       print(f"Time: {last_msg.time}")
                       # Check if the message contains a URL and open it
                       href_url = extract_href(last_msg.content)
                       if href_url:
                           open_url(href_url)
                            # Close the browser
                            #  driver.quit()
                            #  ring_bell()
                  else:
                    print("No recent messages found.")
             except Exception as e:
                 print(f"Error fetching messages in onEvent: {str(e)}")



# Create an instance of your event loop
skype_event_loop = MySkypeEventLoop(username, password)


# Get all chatId's
# sk = Skype(username, password)
# skc = SkypeChats(sk)
# print("name:=>  ",skc.recent())

# Start listening for events
print("Starting event loop...")
skype_event_loop.loop()
print("Event loop started.")


# import os

# # Directory to search for sound files
# directory = '/System/Library/Sounds/'

# # List all files in the directory
# files = os.listdir(directory)

# # Print all files in the directory
# print("Files in directory:")
# for file in files:
#     print(file)


