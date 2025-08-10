import os
import logging
from typing import Final
from dotenv import load_dotenv

load_dotenv()
REFRESH_SLEEP_TIME: Final = int(os.getenv("REFRESH_SLEEP_TIME"))
TIMEOUT: Final = int(os.getenv("TIMEOUT")) * 1000
HEADLESS: Final = os.getenv("HEADLESS","true") == "true"
TESTING: Final = os.getenv("TESTING","false") == "true"

# Pushover Credentials
PUSHOVER_TOKEN: Final = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_USER_KEY: Final = os.getenv("PUSHOVER_USER_KEY")

# Red Rover Credentials
BASE_URL: Final = "https://app.redroverk12.com/substitute"
CLIENT_EMAIL: Final = os.getenv("REDROVER_EMAIL")
CLIENT_PASSWORD: Final = os.getenv("REDROVER_PASSWORD")

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Login XPaths
EMAIL_XPATH: Final = 'xpath=//*[@id="loginId"]'
NEXT_BUTTON_XPATH: Final = "xpath=/html/body/main/main/div/div/div/main/form/div/button"
PASSWORD_XPATH: Final = 'xpath=//*[@id="password"]'
LOGIN_XPATH: Final = "xpath=/html/body/main/main/div/div/div/main/form/div/button"

# Job XPaths
FILTER_BUTTON_XPATH: Final = 'xpath=//*[@id="content-view"]/div/div/div[3]/div/div[2]/div/div[2]/div/div'
LOADER_XPATH: Final = 'xpath=//*[@id="edlumin-app"]/div/div/div/div/header/span'
REFRESH_BUTTON_XPATH: Final = 'xpath=//*[@id="content-view"]/div/div/div[3]/div/div[1]/button'
ALL_JOBS_XPATH: Final = 'xpath=//*[@id="content-view"]/div/div[2]/div[3]'
NOTE_XPATH: Final = "xpath=/html/body/div[5]"