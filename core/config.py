from os import getenv
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
ADMIN_ID = getenv("ADMIN_ID")
#POSTGRES_URI = getenv("POSTGRES_URI")
DATABASE_URL = getenv("DATABASE_URL")