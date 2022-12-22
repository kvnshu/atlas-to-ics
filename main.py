from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from ics import Calendar, Event

# check if Schedule Builder is offline for scheduled maintenance. It will return online at 7:30 AM.


def document_initialised(driver):
    return driver.execute_script("return initialised")


def get_courses():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://atlas.ai.umich.edu/")

    # insert wait strategy?
    # find and click Log in element
    login_button = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(by=By.LINK_TEXT, value="Log in"))
    if (login_button):
        print("Log in button found")
        
        login_button.click()
        # wait
        # get UMID and UM Password from user
        # find umid field
        # find password field
        # fill out login information fields
        # find and click submit
    else:
        print("Log in button not found")
    # navigate to Schedule Builder
    #   (can I get (https://atlas.ai.umich.edu/schedule-builder/) or will this not work, in which case I have to find and click the link?)
    # get Academic Term from user
    # Select Academic Term form dropdown
    # wait for elements to render?
    # get Schedule name from user
    # select button with text== schedule name
    events = []
    # iterate through course cards (and course section) and get class information
    # iterate through course sections and create events, add to ics object
    # driver.quit()


def build_calendar(courses):
    c = Calendar()
    for course in courses:
        e = Event(course.name)
        c.add(e)
    return c


def export_calendar(calendar_filename, calendar):
    with open(calendar_filename, 'w') as f:
        f.writelines(calendar.serialize_iter())

    # reopen file and add RRULE for each event


get_courses()

uniqname = "kevx"
term = "Winter 2023"
schedule_name = "Winter 2023 - default"
calendar_filename = f'Course Schedule - {uniqname}: {term}.ics'
