# Ideation

## Schema

Document database with mongodb or other

Useful because different schools may have different properties for their classes. Implementers should aim to use commonly used attribute names but may add their own when their colleges have features that other colleges don't.

Requirements are objects, possibly nested in each other. 
```json
{
  "type": "TYPE",
  "items": [
    ObjectId,
    "COURSE CODE",
    {
      "type": "TYPE",
      "items": [
        "COURSE CODE",
	ObjectId
      ]
    }
  ]
}
```

Requirement types:
* AND (ALL) - All requirements must be completed
* OR (ONE) - One of the requirements must be completed
* CREDITS - A provided number of credits must be completed from the group
* COUNT (n) - A provided number of courses in the group must be completed

### Course Collection
```json
{
        "code": "CSE 2421",
        "name": "Systems I: Introduction to Low-Level Programming and Computer Organization",
        "units": 4,
        "campus": "Columbus",
        "subject": "CSE",
        "university": "The Ohio State University",
        "career": "Undergraduate",
        "attributes": "asdfasddf",
        "description": "Introduction to computer architecture at machine and assembly language level; pointers and addressing; C programming at machine level; computer organization. Prereq: 2122, 2123, or 2231; and 2321 or Math 2566; and enrollment in CSE, CIS, Data Analytics, Music (BS), Eng Physics, or Math major.",
        "prereqs": {
                "type": "AND",
                "requirements": [
                        {
                                "type": "OR",
                                "requirements": [
                                        "CSE 2122",
                                        "CSE 2123",
                                        "CSE 2231"
                                ]
                        },
                        {
                                "type": "OR",
                                "requirements": [
                                        "CSE 2321",
                                        "MATH 2566"
                                ]
                        },
                        "Enrollment in CSE, CIS, Data Analytics, Music(BS), Eng Physics, or Math major."
                ]
        },
        "coreqs": {
        },
        "disqualifiers": [
                "Credit for CSE 3115"
        ],
        "grading": "S/U"
}
```

### University Collection
```json
{
        "name": "The Ohio State University"
}
```

### Subject Collection
```json
{
        "school": "The Ohio State University",
        "code": "CSE",
        "name": "Computer Science & Engineering"
}
```
