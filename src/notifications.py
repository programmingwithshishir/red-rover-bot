import requests
from config import logger, PUSHOVER_TOKEN, PUSHOVER_USER_KEY

class Notification:
    @staticmethod
    def format_message(job):
        notification = title = ""
        for key, value in job.items():
            if key == "notes": notification += f"{key}: {value}\n"
            elif key == "scheduled_dt": title = value
            else: notification += f"{value}\n"
        return title, notification

    @staticmethod
    def send_message(title, message, priority):
        url = "https://api.pushover.net/1/messages.json"
        params = {
            "token": PUSHOVER_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": title,
            "message": message,
            "priority": str(priority),
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

    @staticmethod
    def send_mobile_notification(job):
        title, message = Notification.format_message(job)
        Notification.send_message(title, message, 1)