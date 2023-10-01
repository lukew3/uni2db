# Contributing

## Setup
* [Install python](https://wiki.python.org/moin/BeginnersGuide/Download)
* [Install MongoDB Community Edition](https://www.mongodb.com/docs/manual/administration/install-community/)
* Install dependencies
  ```
  pip install -r requirements.txt
  ```

## How to contribute
Most contributions will be in the form of new scrapers.
You may want to create a scraper for a school that is important to you or find one that other people want from the [wishlist issues](https://github.com/lukew3/uni2db/issues?q=is%3Aopen+is%3Aissue+label%3AWishlist).

### Scrapers
Each university gets its own file in the `/scrapers` directory.
The name of the file is the name of the domain that that university uses followed by `.py`.
For example The Ohio State University has its website at [`osu.edu`](https://www.osu.edu/) so the file where its scrapers are located is [`osu.edu.py`](https://github.com/lukew3/uni2db/blob/main/scrapers/osu.edu.py).

Data will be stored in a MongoDB database called `uni2db`. Your file must contain the folliwing lines in order to interact with the database:
```
from pymongo import MongoClient

MONGO_CONNECTION_STRING = "mongodb://localhost:27017/"
mclient = MongoClient(MONGO_CONNECTION_STRING)
db = mclient['uni2db']
```
Now, functions can call the method `db[COLLECTION_NAME].insert_one(OBJECT_TO_INSERT)` to insert a certain python dictionary into a collection like courses, sections, or transfers.

Each type of data that we want to scrape has its own function. Each university file must have at least one of these functions defined. 
* `courses()`
  * Courses offered by the university. Each course should at least have a title, code, subject, and description. You can add other fields that your university provides like credits, offeredTerms, prerequisites or restrictions.
* `sessions()`
  * Course sections that students are enrolled in. Sessions have properties like a professor, daysOffered, startTime, endTime, startDate, endDate. There is currently a lot of flexibility over fields as the typical schema is being determined.
* `transfers()`
  * Transfers are courses that students can take at a source school and get credit for at a destination school. It has fields src_school, src_course, dest_course, dest_school

#### Validation
To ensure that your data is being saved properly, you may want to [download MongoDB Compass](https://www.mongodb.com/products/tools/compass) to view the database.

If you are confused about anything or need help, ask on our discord server: https://discord.gg/qQEDzQMmB8
