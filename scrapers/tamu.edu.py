from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm


MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']

def courses():
    # Get set of subjects
    url = "https://catalog.tamu.edu/undergraduate/course-descriptions/"
    subject_listing = requests.get(url)
    soup = BeautifulSoup(subject_listing.content, 'html.parser')
    subjects = set()
    for link in soup.find_all('a'):
        match = re.search(r'/undergraduate/course-descriptions/([a-zA-Z]+)/', str(link.get('href')))
        if match:
            subjects.add(match.group(1))
    
    # Get courses for each subject
    print("Scraping subjects")
    for subject in tqdm(subjects):
        url = f"https://catalog.tamu.edu/undergraduate/course-descriptions/{subject}/"
        course_listing = requests.get(url)
        soup = BeautifulSoup(course_listing.content, 'html.parser')
        # For each child of the element with id sc_sccoursedescs
        for item in list(soup.find('div', {'id': 'sc_sccoursedescs'}).children)[1:]:
            title = item.find('h2').contents[0]
            desc = ''.join(item.find('p', {'class': 'courseblockdesc'}).parent.findAll(string=True))
            description = ' '.join(desc.split())
            credits = desc.split('\n')[4][7:-2].strip()
            db['courses'].insert_one({
                'school': 'Texas A&M University',
                'name': ' '.join(title.split()[2:]),
                'code': ' '.join(title.split()[:2]),
                'min_credits': int(credits[0]),
                'max_credits': int(credits[-1]),
                'subject': subject.upper(),
                'description': description
            })
