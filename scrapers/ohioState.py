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
import sqlite3
import os.path

def read_page(conn, cursor, driver):
    WebDriverWait(driver, timeout=10).until_not(lambda x: driver.find_element(By.ID, "WAIT_win0").is_displayed())
    main_content = driver.find_element(By.ID, "ACE_SSR_CAT_SRCH1$0").get_attribute('innerHTML')
    soup = BeautifulSoup(main_content, 'html.parser')
    for i in range(50): # at most 50 items on each page
        if not soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CRSE_HEADER${i}"}): break

        course_name = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CRSE_HEADER${i}"}).get_text()
        print(course_name)
        course_credits = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_UNITS_DESCR${i}"}).get_text()
        course_campus = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CAMPUS_DESCR${i}"}).get_text()
        course_career = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CAREER_DESCR${i}"}).get_text()
        course_grading = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_GRADING_DESCR${i}"}).get_text()
        course_attributes = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_CRSE_ATTR_VALS${i}"}).get_text()
        course_description = soup.find("textarea", {"id": f"OSR_CAT_SRCH_DESCRLONG${i}"}).get_text()

        course_components1 = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_DESCR1${i}"}).get_text()
        # course_option1 = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_1_OPTION${i}"}).get_text()
        #course_components2 = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_DESCR2${i}"}).get_text()
        # course_option2 = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_2_OPTION${i}"}).get_text()
        #course_components3 = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_DESCR3${i}"}).get_text()
        # course_option3 = soup.find("span", {"id": f"OSR_CAT_SRCH_OSR_COMP_3_OPTION${i}"}).get_text()
    next_btn = driver.find_element(By.ID, "OSR_CAT_SRCH_WK_BUTTON_FORWARD")
    if not next_btn.get_attribute("disabled"):
        next_btn.click()
        read_page(conn, cursor, driver)

def scrape():
    conn = sqlite3.connect('roomMatrix.db')
    cursor = conn.cursor()

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

    read_page(conn, cursor, driver)
    pass

if __name__ == '__main__':
    scrape()
