[![uni2dbbannerraised](https://github.com/lukew3/uni2db/assets/47042841/df07ae36-b64c-4f4f-863d-4120bb485fd7)](https://uni2db.com)

The Unified University Database (uni<sup>2</sup>db).
This repo includes:
* Scrapers to get course info from college websites and populate a MongoDB database (`/scrapers`)
* A command line tool to help you manage scraping (`cli.py`)
* An API that you can host to access scraped data through http requests (`server.py`)

Join the discord community: https://discord.gg/TxeZdrnTU7

## Contributing
See [CONTRIBUTING.md](https://github.com/lukew3/uni2db/blob/main/CONTRIBUTING.md)

## API Routes
The following are API routes available. Results are returned in JSON lists of strings or objects.

### `/v0/schools`
Returns an array of distinct names from the courses collection

### `/v0/subjects`
List distinct subjects offered at a school. Requires query parameter for `school`

### `/v0/courses`
Lists all information about courses offered in a subject at a certain school. Requires query parameters for `school` and `subject`

### `/v0/transfers`
Lists all courses that can be transfered from a certain `src_school` to a `dest_school`. Requires query params for `src_school` and `dest_school`

### `/v0/sections`
Lists all information about sections offered for a certain course at a certain school. Requires query parameters for `school` and `code`.
