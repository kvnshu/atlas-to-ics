from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from ics import Calendar, Event
from course import Course
import re

# check if Schedule Builder is offline for scheduled maintenance. It will return online at 7:30 AM.


def document_initialised(driver):
    return driver.execute_script("return initialised")


def login(driver):
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
        WebDriverWait(driver, timeout=100).until(
            lambda d: d.find_element(by=By.CLASS_NAME, value="nav-bar-links"))
    else:
        print("Log in button not found")


def get_courses(driver):
    # navigate to Schedule Builder
    # get Academic Term from user
    term_select = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_element(by=By.CSS_SELECTOR, value=".dropdown"))

    # Select Academic Term form dropdown
    term_select.click()
    # Check if dropdown item is present
    WebDriverWait(driver, timeout=3).until(
        EC.presence_of_element_located((By.XPATH, "(/html/body/div[1]/div/div/div/div[2]/div[1]/div/select/option)[2]")))
    term_select.send_keys(Keys.ARROW_DOWN, Keys.ENTER)

    # TODO: ask for schedule name

    courses = []
    course_cards_list = WebDriverWait(driver, timeout=3).until(
        lambda d: d.find_elements(by=By.CSS_SELECTOR, value=".sb-course-card-container"))
    for course in course_cards_list:
        title = course.find_element(
            by=By.CSS_SELECTOR, value=".course-code-and-filter .text-xsmall").get_attribute("innerHTML")
        print(title)
        # iterate through sections
        section_lists = WebDriverWait(course, timeout=120).until(
            lambda d: d.find_elements(by=By.CSS_SELECTOR, value=".course-section-details"))
        print("Number of sections: ", len(section_lists))
        for section in section_lists:
            # skip if date == "Days TBA" or section title contains "MID"
            section_type_raw = section.find_element(
                by=By.CSS_SELECTOR, value=".course-section-details .row .row .regular").get_attribute("innerHTML")

            section_time = section.find_element(
                by=By.CSS_SELECTOR, value=".section-time").get_attribute("innerHTML")

            # get type
            name_reg = r'\(([A-Z]+)\)'
            name_match = re.search(name_reg, section_type_raw)
            section_type = name_match.group(1)
            if section_type == "MID":
                continue

            # TODO get section number
            section_name = section.find_element(
                by=By.CSS_SELECTOR, value=".dropdown-label").get_attribute("innerHTML")
            section_reg = r'\W(\d{3})\W'
            section_match = re.search(section_reg, section_name)
            section_num = section_match.group(1)

            # get time start
            # get time end
            # get days
            time_reg = r'([\d]+:[\d]+\W[\w]+) - ([\d]+:[\d]+\W[\w]+) \| ([\w]+[ \w]*)'
            time_match = re.search(time_reg, section_time)
            start_time = time_match.group(1)
            end_time = time_match.group(2)
            days = time_match.group(3)
            if "Days TBA" in days:
                continue
            else:
                days_reg = r'[A-Z][a-z]{0,1}'
                days_list = re.findall(days_reg, days)

            # get location
            location = section.find_element(
                by=By.CSS_SELECTOR, value=".section-time+ .text-xsmall").get_attribute("innerText").strip()

            course = Course(title, section_type, section_num,
                            days_list, start_time, end_time)
            courses.append(course)
    return courses

    # wait for elements to render?
    # TODO: prevent usage inside maintenence hours
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


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option(
    'excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=chrome_options)

isProductiontMode = 0
if (isProductiontMode):
    driver.get("https://atlas.ai.umich.edu/")
    login(driver)
    driver.get("https://atlas.ai.umich.edu/schedule-builder/")
else:
    driver.get(
        r"C:\Users\k3vnx\Documents\GitHub\atlas-to-ics\testing\Atlas-schedule-builder-winter2023.html")

courses = get_courses(driver)
# uniqname = "kevx"
# term = "Winter 2023"
# schedule_name = "Winter 2023 - default"
# calendar_filename = f'Course Schedule - {uniqname}: {term}.ics'
