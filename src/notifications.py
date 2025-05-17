import requests
from config import logger, PUSHOVER_TOKEN, PUSHOVER_USER_KEY

class Notification:
    def __init__(self, job):
        self.job = job

    def format_message(self, job):
        notification = title = ""
        for key, value in job.items():
            if key == "notes":
                notification += f"{key}: {value}\n"
            elif key == "scheduled_dt":
                title = value
            else:
                notification += f"{value}\n"
        return title, notification

    def send_mobile_notification(self, title, message):
        title, message = self.format_message(self.job)
        url = "https://api.pushover.net/1/messages.json"
        params = {
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
            "priority": "1",
        }
        while True:
            response = requests.post(
                url,
                params=params,
            )
            if response.status_code == 200:
                logger.info("Notification sent successfully")
                break
            else: logger.warning(f"Notification failed with status code {response.status_code}. Retrying!")