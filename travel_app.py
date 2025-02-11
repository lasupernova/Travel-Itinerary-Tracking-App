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

# log Notion token and DB ID used
logging.info(f"Started travel app.")
logging.info(f"Notion Token {os.environ['NOTION_TOKEN']}")
logging.info(f"Pulling info from Notion db with ID: {os.environ['DB_ID']}")