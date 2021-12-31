import requests

from django.core.management.base import BaseCommand
from config.settings import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, SITE_URL, STRAVA_WEBHOOK_VERIFY_TOKEN


class Command(BaseCommand):
    help = "Create a Strava webhook"

    def handle(self, *args, **options):
        print("Creating a Strava webhook")
        url = "https://www.strava.com/api/v3/push_subscriptions"
        body = {
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "callback_url": f"{SITE_URL}/api/exercise/strava/webhook/",
            "verify_token": "strava_webhook_verify_token",
        }
        res = requests.post(url, json=body)
        print(res.json())
