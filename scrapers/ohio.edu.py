from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup


MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']


def get_course_page(url):
    _, ids = url.split('?')
    url2 = f'https://www.catalogs.ohio.edu/ajax/preview_course.php?{ids}&display_options=a:2:{{s:8:~location~;s:8:~template~;s:28:~course_program_display_field~;s:0:~~;}}&show'
    page = requests.get(url2)
    soup = BeautifulSoup(page.content, 'html.parser')
    title_full = soup.find('a').text.strip()
    title_split = title_full.split(' - ', 1)
    desc = soup.find_all('div')[-1].text.split(title_full)[-1].strip()
    db['courses'].insert_one({
        'school': 'Ohio University',
        'code': title_split[0],
        'subject': title_split[0].split()[0],
        'title': title_split[1],
        'description': desc
    })


def get_courses_page(pageNum):
        url = f'https://www.catalogs.ohio.edu/content.php?catoid=82&navoid=7623&filter%5Bcpage%5D={pageNum}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.find_all('a', {'target': '_blank'})
        if len(tags) == 11:
            print('No more courses')
            return
        else:
            for tag in tags:
                if tag['href'].startswith('preview_course_nopop.php'):
                    print("GETTING", tag.text)
                    get_course_page(tag['href'])
            get_courses_page(pageNum + 1)


def courses():
    get_courses_page(1)
