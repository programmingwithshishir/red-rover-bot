from playwright.sync_api import sync_playwright, TimeoutError
import time
import datetime
import json
import hashlib
from database import Database
from notifications import Notification
from config import (
    logger,
    TESTING,
    FILTER_BUTTON_XPATH,
    REFRESH_BUTTON_XPATH,
    LOADER_XPATH,
    EMAIL_XPATH,
    NEXT_BUTTON_XPATH,
    PASSWORD_XPATH,
    LOGIN_XPATH,
    ALL_JOBS_XPATH,
    REFRESH_SLEEP_TIME,
    BASE_URL,
    CLIENT_EMAIL,
    CLIENT_PASSWORD,
    TIMEOUT,
    HEADLESS
)

def login(page):
    while True:
        try:
            page.goto(BASE_URL, timeout=TIMEOUT)

            # Finding the email input element
            email_input_el = page.locator(EMAIL_XPATH)
            email_input_el.wait_for(state="attached", timeout=TIMEOUT)
            email_input_el.click()
            email_input_el.fill(value=CLIENT_EMAIL)

            # Finding the next button element
            next_button_el = page.locator(NEXT_BUTTON_XPATH)
            next_button_el.wait_for(state="attached", timeout=TIMEOUT)
            next_button_el.click()

            # Finding the password input element
            password_input_el = page.locator(PASSWORD_XPATH)
            password_input_el.wait_for(state="attached", timeout=TIMEOUT)
            password_input_el.click()
            password_input_el.fill(value=CLIENT_PASSWORD)

            # Finding the login button element
            login_button_el = page.locator(LOGIN_XPATH)
            login_button_el.wait_for(state="attached", timeout=TIMEOUT)
            login_button_el.click()
            
            break
        except TimeoutError: logger.error("Login unsuccessful: Browser Timeout - Check your connection!")
        except Exception as e: 
            logger.critical(f"Login unsuccessful: Exception Type - {type(e).__name__}!")
            Notification.send_message("Bot crashed",f"Exception - {type(e).__name__}!",-1)
            exit(0)
        except KeyboardInterrupt:
            logger.critical("KeyboardInterrupt: Exiting!")
            exit(0)

def filter(page):
    # Find the filter button
    filter_button = page.locator(FILTER_BUTTON_XPATH)
    filter_button.wait_for(state="attached", timeout=TIMEOUT)
    filter_button.click()

    # Finding filter options
    filter_options = filter_button.get_by_role("listbox").get_by_role("option").all()
    for option in filter_options:
        if option.inner_text() == "All (ignore preferences)" if TESTING else "Default":
            option.click()
            break
    page.locator(LOADER_XPATH).wait_for(state="hidden", timeout=TIMEOUT)

def generate_unique_identifier(data_dict):
    json_string = json.dumps(data_dict, sort_keys=True)
    encoded_string = json_string.encode("utf-8")
    sha256_hash = hashlib.sha256()
    sha256_hash.update(encoded_string)
    return sha256_hash.hexdigest()

def extract_job_details(job):
    formatted_job = {}
    job_details = job.split("\n")
    formatted_job["scheduled_dt"] = ", ".join([job_details[1], job_details[0], job_details[-1], job_details[-2]])
    formatted_job["teacher"] = job_details[-3].replace("for ", "")
    formatted_job["position"] = job_details[-4]
    formatted_job["location"] = ", ".join(job_details[2:-4])
    return formatted_job

def look_for_jobs(page, db):
    # Finding the refresh button element
    time.sleep(REFRESH_SLEEP_TIME)
    refresh_button_el = page.locator(REFRESH_BUTTON_XPATH)
    refresh_button_el.wait_for(state="attached", timeout=TIMEOUT)
    refresh_button_el.click()
    # Wait for the page to load
    page.locator(LOADER_XPATH).wait_for(state="hidden", timeout=TIMEOUT)
    logger.info(f"Successfully refreshed jobs at {time.ctime()}")

    # Find all sub job divs in main div
    sub_jobs_parent = page.locator(ALL_JOBS_XPATH)
    sub_jobs_parent.wait_for(state="attached", timeout=TIMEOUT)
    sub_jobs_children = sub_jobs_parent.locator(":scope > div").all()

    # Check if it's a job div
    for sub_job_child in sub_jobs_children:
        sub_job = sub_job_child.locator('[class*="infoContainer"]')
        if sub_job.count() > 0: 
            logger.info("Found a job!")
            db.delete_old_jobs()
            data = extract_job_details(sub_job.inner_text())
            # TODO: Get Notes if any here

            # Adding a unique identifier for the job and inserting to database
            data["uid"] = generate_unique_identifier(data)
            data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if db.uid_exists(): 
                logger.info("Job already exists in the database.")
                continue
            db.insert_job(data)
            logger.info("Successfully inserted the jobs into the database.")

            # Sending the notification
            try:
                Notification.send_mobile_notification(data)
                logger.info(f"Notification sent for uid: {data['uid']}")
            except: logger.critical("Notification Error: Notification wasn't sent!")
            
def main():
    try:
        logger.info("Loading the database.")
        db = Database("jobs.db")
        db.create_table()
        logger.info("Database loaded. Launching the browser.")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            page = browser.new_page()
            logger.info("Browser launched. Ready for login.")
            login(page)
            logger.info("Login successful.")
            filter(page)
            logger.info("Desired jobs filtered.")
            while True: look_for_jobs(page, db)
    except Exception as e: 
        logger.critical(f"Running unsuccessful: Exception Type - {type(e).__name__}!")
        Notification.send_message("Bot crashed",f"Exception - {type(e).__name__}!",-1)
        exit(0)
    except KeyboardInterrupt: 
        logger.critical("KeyboardInterrupt: Exiting!")

if __name__ == "__main__":
    main()