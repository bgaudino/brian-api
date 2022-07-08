from datetime import timedelta, datetime

from django.utils.timezone import make_aware


def check_tokens(func):
    def wrapper(*args, **kwargs):
        account = args[0]
        now = make_aware(datetime.now()) + timedelta(minutes=30)
        if account.expires_at < now:
            print("Refreshing tokens")
            account.refresh_tokens()
        return func(*args, **kwargs)

    return wrapper
