import os
import logging

# initiate logging
logging.basicConfig(level=logging.DEBUG,
format='%(asctime)s %(levelname)s %(message)s')
#       filename='./tmp/myapp.log',
    #   filemode='w'

# log Notion token and DB ID used
logging.info(f"Started travel app.")
logging.info(f"Notion Token {os.environ['NOTION_TOKEN']}.")
logging.info(f"Pulling info from Notion db with ID: {os.environ['DB_ID']}.")