import re
from pymongo import MongoClient

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['collegedb']

school = 'The Ohio State University'
subjects = set(db['course'].distinct("subject", {'school': school}))

# Parses a requirement string into a nested requirement map
def req_parser(req_string, current_subject):
    # Add subjects to course codes
    last_is_subject = False
    req_string = req_string.upper()
    s = req_string.split()
    s2 = []
    for word in s:
        if not last_is_subject and word[0].isdigit():
            s2.append(current_subject)
            last_is_subject = False
        elif word in subjects:
            current_subject = word
            last_is_subject = True
        else:
            last_is_subject = False
        s2.append(word)
    s2 = ' '.join(s2)
    s3 = re.compile(r'( AND | OR |,)').split(s2)
    for i in range(len(s3)):
        s3[i] = s3[i].strip().replace(',', '')
    s3 = [item for item in s3 if item != '']
    m = {'type': 'AND', 'items': []}
    cur = {'type': 'AND', 'items': []}
    for item in s3:
        if item in ['AND', 'OR']:
            cur['type'] = item
        elif item[-1] == ';':
            item = item[:-1]
            cur['items'].append(item)
            m['items'].append(cur)
            cur = {'type': 'AND', 'items': []}
        else:
            cur['items'].append(item)
    m['items'].append(cur)
    return m


def parse_reqs():
    for course in db['course'].find():
        updates = {}
        for field in ['prerequisites', 'corequisites', 'disqualifiers']:
            if field in course:
                print('===')
                print(course[field])
                update = req_parser(course[field], course['subject'])
                print(update)
                updates[field] = update
#        db['course'].update_one(course, {'$set': updates})


parse_reqs()
