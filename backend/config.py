# USER_DATA_FILE = "user_data.txt"
MASKED_LOG_FILE = "masked.txt"

SUPPORTED_ENTITIES = [
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "PAN",
    "IFSC",
    "ACCOUNT_NUMBER",
    "UPI_ID",
]

FIELDS_TO_MASK = ["phone", "email", "pan", "ifsc", "upi", "account"]

from dotenv import load_dotenv
import os

load_dotenv() 
DB_URL = os.getenv("DB_URL")


# read_users_from_file,

