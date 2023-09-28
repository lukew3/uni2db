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

### `/` List schools in db
### `/<school>/` List subjects at school
### `/<school>/<subject>/` List courses in subject at school
