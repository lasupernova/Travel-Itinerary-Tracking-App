import os
import logging
from datetime import date, datetime
import pandas as pd
from notion_client import Client
from notion_client.helpers import get_id
from notion_client.helpers import collect_paginated_api

# initiate logging
logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s')
#       filename='./tmp/myapp.log',
    #   filemode='w'


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
today = datetime.strptime(date_string, format_string)