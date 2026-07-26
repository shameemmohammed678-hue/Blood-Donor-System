import os

from dotenv import load_dotenv

load_dotenv()



ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")




