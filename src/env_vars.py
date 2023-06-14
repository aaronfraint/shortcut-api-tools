import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())


SHORTCUT_TOKEN = os.getenv("SHORTCUT_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
