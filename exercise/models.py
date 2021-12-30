from datetime import datetime, timedelta

import requests
from config.settings import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET
from django.db import models
from django.utils.timezone import make_aware
from user.models import User


class Workout(models.Model):
    user = models.ForeignKey(
        User,
        related_name="users",
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(auto_now_add=True)
    finish_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.start_date.strftime('%m%d%y')}: {self.user.email}"


class Exercise(models.Model):
    workout = models.ForeignKey(
        Workout,
        related_name="exercises",
        on_delete=models.CASCADE,
    )
    exercise_name = models.CharField(max_length=100)

    def __str__(self):
        return self.exercise_name


class Set(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    exercise = models.ForeignKey(
        Exercise,
        related_name="sets",
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField()
    reps = models.IntegerField()


class StravaAccount(models.Model):
    strava_id = models.IntegerField()
    user = models.ForeignKey(
        User, related_name="strava_accounts",
        on_delete=models.CASCADE
    )
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.CharField(max_length=100)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    premium = models.BooleanField(default=False)
    avatar = models.URLField()
    avatar_medium = models.URLField()

    def __str__(self):
        return f"{self.username}'s Strava Account"

    def get_activities(self):
        now = make_aware(datetime.now()) + timedelta(minutes=30)
        if self.expires_at < now:
            print("Refreshing tokens")
            self.refresh_tokens()
        
        activityURL = "https://www.strava.com/api/v3/athlete/activities"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        res = requests.get(activityURL, headers=headers)
        activities = res.json()

        for activity in activities:
            try:
                cardio_session = CardioSession.objects.get(
                    strava_id=activity["id"])
            except:
                cardio_session = CardioSession(
                    user=self.user,
                    strava_id=activity["id"]
                )
            for key, value in activity.items():
                setattr(cardio_session, key, value)
            cardio_session.save()
            map = Map(
                cardio_session=cardio_session,
                map_id=activity["map"]["id"],
                summary_polyline=activity["map"]["summary_polyline"],
                resource_state=activity["map"]["resource_state"],
            )
            map.save()

    def refresh_tokens(self):
        body = {
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token",
        }
        res = requests.post("https://www.strava.com/oauth/token", json=body)
        data = res.json()
        self.token_type = data["token_type"]
        self.expires_at = make_aware(
            datetime.utcfromtimestamp(data["expires_at"]))
        self.access_token = data["access_token"]
        self.save()


class CardioSession(models.Model):
    user = models.ForeignKey(
        User, related_name="cardio_seesions",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    moving_time = models.IntegerField()
    elapsed_time = models.IntegerField()
    total_elevation_gain = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=100)
    workout_type = models.IntegerField(null=True)
    strava_id = models.IntegerField()
    external_id = models.TextField()
    upload_id = models.IntegerField()
    start_date = models.DateTimeField()
    start_date_local = models.DateTimeField()
    timezone = models.CharField(max_length=100)
    utc_offset = models.DecimalField(max_digits=10, decimal_places=2)
    average_speed = models.DecimalField(max_digits=10, decimal_places=2)
    max_speed = models.DecimalField(max_digits=10, decimal_places=2)
    has_heartrate = models.BooleanField(default=False)
    average_heartrate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    max_heartrate = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    elev_high = models.DecimalField(max_digits=10, decimal_places=2)
    elev_low = models.DecimalField(max_digits=10, decimal_places=2)
    suffer_score = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)


class Map(models.Model):
    cardio_session = models.ForeignKey(
        CardioSession, related_name="maps",
        on_delete=models.CASCADE
    )
    map_id = models.TextField()
    summary_polyline = models.TextField()
    resource_state = models.IntegerField()
