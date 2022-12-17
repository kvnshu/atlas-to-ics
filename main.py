from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from ics import Calendar, Event
from .course import Course

def get_courses():
    driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()))

    driver.get("https://atlas.ai.umich.edu/")
    # insert wait strategy?
    # find and click Log in element
    # wait
    # get UMID and UM Password from user
    # find umid field
    # find password field
    # fill out login information fields
    # find and click submit
    # navigate to Schedule Builder 
    #   (can I get (https://atlas.ai.umich.edu/schedule-builder/) or will this not work, in which case I have to find and click the link?)
    # get Academic Term from user 
    # Select Academic Term form dropdown 
    # wait for elements to render?
    # get Schedule name from user
    # select button with text== schedule name
    # iterate through course cards (and course section) and get class information

    # iterate through course sections and create events, add to ics object
    driver.quit()

def build_calendar():
    pass

def export_calendar():
    pass


print("Hello, World")
