![uni2dbbannerraised](https://github.com/lukew3/uni2db/assets/47042841/df07ae36-b64c-4f4f-863d-4120bb485fd7)

The Unified University Database (uni<sup>2</sup>db). Tools to get information about courses offered at various colleges. Includes scrapers to scrape course info from college websites and populate a database. Also an API to get information about courses from database.

## Routes
The following are API routes available. Results are returned in JSON lists of strings or objects.

### `/` List schools in db
### `/<school>/` List subjects at school
### `/<school>/<subject>/` List courses in subject at school
