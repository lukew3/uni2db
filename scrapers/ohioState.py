from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import re
import os
import requests
from pymongo import MongoClient
import pandas as pd
from tqdm import tqdm

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']

# Parses a requirement string into a nested requirement map
def req_parser(req_string, current_subject):
    return req_string

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
            'school': 'The Ohio State University',
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
        if match: new_course['prerequisites'] = req_parser(match.group(1), new_course['subject'])
        # Handle corequisites
        coreq_pattern = r"(?:(?:Coreq)|(?:Concur)|(?:Prereq or concur)): (.*?)(?:\.\s|\.$)"
        match = re.search(coreq_pattern, new_course['description'])
        if match: new_course['corequisites'] = req_parser(match.group(1), new_course['subject'])
        # Handle disqualifiers
        coreq_pattern = r"Not open to students with credit for (.*?)(?:\.\s|\.$)"
        match = re.search(coreq_pattern, new_course['description'])
        if match: new_course['disqualifiers'] = req_parser(match.group(1), new_course['subject'])

        db['course'].insert_one(new_course)
        
    next_btn = driver.find_element(By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD")
    if not next_btn.get_attribute("disabled"):
        next_btn.click()
        read_page(driver)

def courses():
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


def transfers():
    file_name = 'equivalencies.xlsx'
    if not os.path.isfile(file_name):
        print('Downloading', file_name)
        r = requests.get('https://registrar.osu.edu/transfer_credit/semester_equivalencies.xlsx')
        open(file_name, 'wb').write(r.content)
    print('Loading', file_name)
    df = pd.read_excel(file_name)
    print('Adding data to db')
    for row in tqdm(df.itertuples(), total=len(df)):
        db['equivalent'].insert_one({
            "src_school": row[1],
            "src_course": ' '.join(str(row[2]).split()),
            "dest_course": ' '.join(str(row[4]).split()),
            "dest_school": "The Ohio State University"
        })

