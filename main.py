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
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://atlas.ai.umich.edu/")

    login_button = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(by=By.LINK_TEXT, value="Log in"))
    if (login_button):
        print("Log in button found")
        login_button.click()
        uniqname = input("What is your uniqname?: ")
        password = input("What is your password?: ")

        uniqname_field = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element(by=By.ID, value="login"))
        password_field = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element(by=By.ID, value="password"))
        weblogin_button = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element(by=By.ID, value="loginSubmit"))

        uniqname_field.send_keys(uniqname)
        password_field.send_keys(password)
        weblogin_button.click()

        driver.switch_to.frame('duo_iframe')
        duo_button = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element(by=By.CLASS_NAME, value="auth-button"))
        duo_button.click()
        # driver.implicitly_wait(10)
        WebDriverWait(driver, timeout=100).until(
            lambda d: d.find_element(by=By.CLASS_NAME, value="nav-bar-links"))
    else:
        print("Log in button not found")

    # navigate to Schedule Builder
    driver.switch_to.default_content()
    driver.get("https://atlas.ai.umich.edu/schedule-builder/")
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
