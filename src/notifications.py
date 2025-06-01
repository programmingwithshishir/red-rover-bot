import requests
from config import logger, PUSHOVER_TOKEN, PUSHOVER_USER_KEY

class Notification:
    @staticmethod
    def format_message(job):
        notification = title = ""
        for key, value in job.items():
            if key == "note": notification += f"Note: {value}\n"
            elif key == "scheduled_dt": title = value
            else: notification += f"{value}\n"
        return title, notification

    @staticmethod
    def send_log_notification(title, message, priority):
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
            if response.status_code == 200: break
            else: logger.warning(f"Notification failed with status code {response.status_code}. Retrying!")

    @staticmethod
    def send_mobile_notification(job, reappeared):
        title, message = Notification.format_message(job)
        if(reappeared): message += "\nThis job was either dropped by someone or resent by the teacher\n"
        Notification.send_log_notification(title, message, 1)