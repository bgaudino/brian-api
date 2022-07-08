import requests
from .models import Score
from random import randint


def create_fake_scores(num_scores):
    try:
        num_scores = int(num_scores)
    except ValueError:
        print("Please enter a valid number of scores to create.")
        return

    for _ in range(num_scores):
        url = "https://random-data-api.com/api/users/random_user"
        res = requests.get(url).json()
        name = res["first_name"]
        num_attempted = randint(1, 50)
        game_type = ["note_id", "interval_ear_training"][randint(0, 1)]
        num_correct = randint(0, num_attempted)
        score = Score(
            name=name,
            num_attempted=num_attempted,
            num_correct=num_correct,
            game_type=game_type,
        )
        score.save()
    print(f"Created {num_scores} fake scores")
