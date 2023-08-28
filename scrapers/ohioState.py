from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests
import time
import re
import os.path
from pymongo import MongoClient

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['collegedb']


def read_page(driver):
    WebDriverWait(driver, timeout=30).until_not(lambda x: driver.find_element(By.ID, "WAIT_win0").is_displayed())
    main_content = driver.find_element(By.ID, "ACE_SSR_CAT_SRCH1$0").get_attribute('innerHTML')
    soup = BeautifulSoup(main_content, 'html.parser')
    for i in range(50): # at most 50 items on each page
        if not soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CRSE_HEADER${i}"}): break


        name = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CRSE_HEADER${i}"}).get_text()
        print(name)
        code, full_name = name.split(' - ', 1)
        credits = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_UNITS_DESCR${i}"}).get_text().split(' units')[0]
        new_course = {
            'name': full_name,
            'code': code,
            'subject': code.split()[0],
            'credits': credits,
            'campus': soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CAMPUS_DESCR${i}"}).get_text(),
            'career': soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CAREER_DESCR${i}"}).get_text(),
            'grading': soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_GRADING_DESCR${i}"}).get_text(),
            'attributes': soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CRSE_ATTR_VALS${i}"}).get_text().strip(),
            'description': soup.find("textarea", {"id": f"OSR_CAT_SRCH_DESCRLONG${i}"}).get_text()
        }

        # Read components into properties
        for j in range(1,4):
            comp_desc = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_DESCR{j}${i}"}).get_text()
            if comp_desc.strip() != '':
                comp_opt = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_{j}_OPTION${i}"}).get_text()
                new_course[f'{comp_desc.lower()}Required'] = (comp_opt == 'Required')

        # Handle CCP Eligible Attribute
        if 'Not eligible for College Credit Plus program' in new_course['attributes']:
            new_course['attributes'] = ''.join(new_course['attributes'].split('Not eligible for College Credit Plus program')).strip()
            new_course['ccpEligible'] = True
        # Handle honors course attribute
        if 'Honors Course' in new_course['attributes']:
            new_course['attributes'] = ''.join(new_course['attributes'].split('Honors Course')).strip()
            new_course['honorsCourse'] = True

        # Handle prerequisites
        prereq_pattern = r"Prereq: (.*?)(?:\.\s|\.$)"
        match = re.search(prereq_pattern, new_course['description'])
        if match:
            new_course['prerequisites'] = match.group(1)
        # Handle corequisites
        coreq_pattern = r"Coreq: (.*?)(?:\.\s|\.$)"
        match = re.search(coreq_pattern, new_course['description'])
        if match:
            new_course['corequisites'] = match.group(1)


        db['course'].insert_one(new_course)
        
    next_btn = driver.find_element(By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD")
    if not next_btn.get_attribute("disabled"):
        next_btn.click()
        read_page(driver)

def scrape():
    # Initialize service and driver
    service = FirefoxService(executable_path=GeckoDriverManager().install())
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument('--headless') # Comment this line to see the browser gui
    driver = webdriver.Firefox(service=service, options=fireFoxOptions)

    # Load frame
    BASE_URL = "https://courses.osu.edu/psp/csosuct/EMPLOYEE/PUB/c/COMMUNITY_ACCESS.OSR_CAT_SRCH.GBL"
    print("Scraping course catalog for the Ohio State University")
    driver.get(BASE_URL)
    driver.switch_to.frame( driver.find_element(By.ID, "ptifrmtgtframe") )

    # Load initial page
    # select_career = driver.find_element(By.ID, "OSR_CAT_SRCH_WK_ACAD_CAREER")
    driver.find_element(By.ID, "OSR_CAT_SRCH_WK_BUTTON1").click()

    read_page(driver)


if __name__ == '__main__':
    scrape()
