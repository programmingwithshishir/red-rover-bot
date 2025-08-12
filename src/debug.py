import traceback
import sys
from playwright.sync_api import sync_playwright, TimeoutError
import time
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
    REFRESH_SLEEP_TIME,
    BASE_URL,
    CLIENT_EMAIL,
    CLIENT_PASSWORD,
    TIMEOUT,
    HEADLESS
)

def print_error_info(exc):
    tb = traceback.extract_tb(sys.exc_info()[2])[-1]  # Get last call in traceback
    filename, lineno, func, text = tb
    print(f"Error: {type(exc).__name__}: {exc}")
    print(f"Line {lineno} in {filename}: {text}")

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
    filter_options = page.get_by_role("option").all()
    for option in filter_options:
        if option.inner_text() == ("All (ignore preferences)" if TESTING else "Default"):
            option.click()
            break
    page.locator(LOADER_XPATH).wait_for(state="hidden", timeout=TIMEOUT)

def look_for_jobs(page):
    while True:
        # Finding the refresh button element
        time.sleep(REFRESH_SLEEP_TIME)
        refresh_button = page.locator(REFRESH_BUTTON_XPATH)
        refresh_button.wait_for(state="attached", timeout=TIMEOUT)
        refresh_button.click()

        # Wait for the page to load
        page.locator(LOADER_XPATH).wait_for(state="hidden", timeout=TIMEOUT)
        logger.info(f"Successfully refreshed jobs")

        # Find all sub job divs in main div
        sub_jobs_parent = page.locator("xpath=//*[@id=\"content-view\"]/div/div/div[3]/div/div[3]")
        sub_jobs_parent.wait_for(state="attached", timeout=TIMEOUT)
        if(sub_jobs_parent.inner_text()=="No assignments available\n\nTry checking back later"): continue
        else: input("Job found, waiting...")
                
def main():
    try:
        logger.info("Launching the browser.")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS)
            page = browser.new_page()
            logger.info("Browser launched. Ready for login.")
            login(page)
            logger.info("Login successful.")
            filter(page)
            logger.info("Desired jobs filtered.")
            look_for_jobs(page)
    except Exception as e: 
        logger.critical(f"Running unsuccessful: Exception Type - {type(e).__name__}!")
        print_error_info(e)
        exit(0)
    except KeyboardInterrupt: 
        logger.critical("KeyboardInterrupt: Exiting!")

if __name__ == "__main__":
    main()