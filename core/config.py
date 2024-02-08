from os import getenv
from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
ADMIN_ID = getenv("ADMIN_ID")
#POSTGRES_URI = getenv("POSTGRES_URI")
DATABASE_URL = getenv("DATABASE_URL")
WEB_SERVER_HOST = getenv("WEB_SERVER_HOST")
WEB_SERVER_PORT = int(getenv("WEB_SERVER_PORT"))
WEBHOOK_PATH = getenv("WEBHOOK_PATH")
WEBHOOK_URL = getenv("WEBHOOK_URL")