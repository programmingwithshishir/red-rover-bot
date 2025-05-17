from playwright.sync_api import sync_playwright, TimeoutError
from config import (
    logger,
    EMAIL_XPATH,
    NEXT_BUTTON_XPATH,
    PASSWORD_XPATH,
    LOGIN_XPATH,
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
            exit(0)
        except KeyboardInterrupt:
            logger.critical("KeyboardInterrupt: Exiting!")
            exit(0)

def main():
    # Launch Playwright browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        logger.info("Browser launched. Ready for login.")
        logger.info("Attempting to Login.")
        login(page)
        logger.info("Login successful.")

if __name__ == "__main__":
    main()