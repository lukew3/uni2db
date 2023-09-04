import json
import re
from pymongo import MongoClient

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']

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
    i = 0
    while i < len(s3):
        if s3[i] == 'AND':
            cur['type'] = s3[i]
        elif s3[i] == 'OR':
            # IF "OR ABOVE" pattern found, concatenate those two groups to last. Else treat like AND
            if s3[i+1][:5] == 'ABOVE':
                cur['items'][-1] += ' ' + s3[i] + ' ' + s3[i+1]
            else:
                cur['type'] = s3[i]
        elif s3[i][-1] == ';':
            # Remove the last character ';' from the word
            s3[i] = s3[i][:-1]
            # Remove unnecessary nesting in cur
            if len(cur['items']) == 0:
                cur = s3[i]
            else:
                cur['items'].append(s3[i])
            # Add cur to m items
            m['items'].append(cur)
            # Set the type of m to the next word
            if i != len(s3)-1:
                m['type'] = s3[i+1]
                i += 1
            # Reset the cur
            cur = {'type': 'AND', 'items': []}
        else:
            # Add a requirement to cur group
            cur['items'].append(s3[i])
        i += 1

    # Remove unnecessary nesting in cur
    if len(cur['items']) == 1:
        cur = cur['items'][0]
    # Remove unnecessary nesting in m
    if len(m['items']) == 0:
        m = cur
    else:
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
                print(json.dumps(update, indent=4))
                updates[field] = update
#        db['course'].update_one(course, {'$set': updates})


if __name__ == '__main__':
    parse_reqs()
