import os
import requests
import logging
from datetime import date, datetime
import pandas as pd
from countryinfo import CountryInfo
from notion_client import Client
from notion_client.helpers import get_id
from notion_client.helpers import collect_paginated_api

# initiate logging
logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s')
#       filename='./tmp/myapp.log',
    #   filemode='w'

def is_date_in_range(target_date, start_date, end_date):
    """
    Checks if a target date falls within the given range.
    target_date, start_date, end_date are of type datetime
    """
    return start_date <= target_date <= end_date

def current_country(scheduled_countries:list, today=datetime.today().date()):
    """
    Takes a Notion database itinerary in list format and a datetime object.
    Extracts information of country that is listed in itinerary for the input datetime object.
    Returns a tuple.

    Input:
        scheduled_countries (list) - Notion database information. 
        today (datetime) - date search for in list

    Returns:
        tuple (
            i (int): index of current iteration,
            country (dict): Notion page / country info for current iteration,
            country_name (str): country that corresponds to input date,
            country_page_id (str): Notion page ID for corresponding country page (country page is a child of the Notion database corresponding to the input list)
        )
    """
    for i, country in enumerate(scheduled_countries):
        try:
            start_date_str = (country['properties']['Planned Stay']['date']['start'])
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

            end_date_str = (country['properties']['Planned Stay']['date']['end'])
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except Exception as e:
            continue
        
        if is_date_in_range(today, start_date, end_date):
            country_name = country['properties']['Country']['title'][0]['text']['content']
            country_page_id = country['id']
            
            return i, country, country_name, country_page_id
        else:
            continue

def travel_info(itinerary:dict):
    country_info = {}

    for date, country in itinerary.items():
        if date not in country_info:
            country_info[date] = dict()
            country_info[date]['country'] = country
        # get info (currency and lat/long) per country        
        country_data = CountryInfo(country[0]).info()
    #     print(date, country, country_info)
        current_currency = country_data['currencies'][0]
        lat, lon = country_data['capital_latlng']
        # get currency exchange rate via API
        exchange_rate = requests.get("https://api.fxratesapi.com/latest").json()['rates'][current_currency]
        # get weather for country on date
        weather_api = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m&current=relative_humidity_2m&current=precipitation_probability&current=cloud_cover"
        time, x, temp, humidity, rain_prob, cloud_cover = requests.get(weather_api).json()['current'].values()
        
        # add exchange rate and weather data to country_info dict      
        country_info[date]['exchange'] = exchange_rate
        country_info[date]['temp'] = temp
        country_info[date]['rain_prob'] = rain_prob
        country_info[date]['cloud_cover'] = cloud_cover
    return country_info

logging.info(f"Started travel app.")

# get personal Notion token from env variables; see Notion documentation to obtain token here: https://developers.notion.com/reference/create-a-token
token = os.environ['NOTION_TOKEN']
logging.info(f"Notion Token {os.environ['NOTION_TOKEN']}")

# get id for main database containing the itinerary overview
itinerary_db_id = os.environ['DB_ID']  
logging.info(f"Pulling info from Notion db with ID: {os.environ['DB_ID']}")

# define date to use for app (for testing: use date that is contained in Notion db, otherwise use today)
# today = date.today()  #use future date that IS in Notion database for testing --> else error will be thrown as current_country() will return None
date_string = "2026-02-12"
format_string = "%Y-%m-%d"
today = datetime.strptime(date_string, format_string).date()

# initiate notion client to query databases and pages
notion = Client(auth=token)

# Construct the filter to ensure "Planned Stay" property is not empty, to ensure all returned results are scheduled in itinerary
filter = {
    "property": "Planned Stay",
    "date": {
        "is_not_empty": True
    }
}

all_results = collect_paginated_api(
    notion.databases.query, 
    database_id=itinerary_db_id, 
    filter=filter
)


current_countries = dict()
datelist = pd.date_range(today, periods=4).tolist()

logging.info(f"Extracting info for countries visited between {datelist[0].date()} and {datelist[-1].date()}.")

for i in datelist:
    entry_info = current_country(all_results, i.date())  #i.date() to convert pandas date object into datetime date for comparison of datetime dates in function used
    if entry_info:
        country_to_add = entry_info[2]
        page_id = entry_info[3]
        current_countries[i.strftime("%Y-%m-%d")]= (country_to_add.strip(), page_id)
    else:
        continue

test_info_output = travel_info(current_countries)

logging.info(test_info_output)