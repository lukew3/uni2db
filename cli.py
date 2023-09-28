import click
import os
import importlib

@click.group()
def cli():
    pass

@cli.command()
def schools():
    """ Lists all available schools"""
    list_schools()

def list_schools():
    print("Available schools:")
    schools = [filename[:-3] for filename in os.listdir('scrapers') if filename.endswith('.py')]
    for i, school in enumerate(schools):
        print(' ', i, school)
    return schools
"""
@cli.command()
def scrape():
    # Scrapes data from specified schools and stores in database
    schools = list_schools()
    try:
        to_scrape = [int(i) for i in input("Enter school ids seperated by spaces: ").split()]
        if max(to_scrape) > len(schools) - 1:
            raise Exception("School id too large")
        elif min(to_scrape) < 0:
            raise Exception("School id too small")
    except Exception as e:
        print(e)
        return
    for schoolid in to_scrape:
        print("Scraping", schools[schoolid])
"""

@cli.command()
def osu():
    """ Scrape OSU """
    ohioState = importlib.import_module('scrapers.ohioState')
    ohioState.scrape_courses()

@cli.command()
def scrapeall():
    """ Scrape all schools """
    for school in list_schools():
        print("Scraping", school)
        try:
            school_scraper = importlib.import_module('scrapers.' + school)
        except Exception as e:
            print(f"Error when importing {school}: ", e)
            continue
        # TODO: Log time to completion for each task. Save leaderboard of completion times to Github so that contributors can determine which scrapers need improvement
        try:
            school_scraper.courses()
        except Exception as e:
            print(f"Error when scraping courses for {school}: ", e)
        try:
            school_scraper.sections()
        except Exception as e:
            print(f"Error when scraping sections for {school}: ", e)
        try:
            school_scraper.transfers()
        except Exception as e:
            print(f"Error when scraping transfers for {school}: ", e)


if __name__ == '__main__':
    cli()