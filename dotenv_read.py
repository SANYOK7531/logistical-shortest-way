import os
from dotenv import load_dotenv

load_dotenv(override=True)

API_KEY = os.getenv("GOOGLE_API_KEY")
START_LAT = os.getenv("START_LAT")
START_LON = os.getenv("START_LON")
START_COORD = f"{START_LAT},{START_LON}"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER")