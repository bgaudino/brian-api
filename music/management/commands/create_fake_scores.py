from django.core.management.base import BaseCommand

from music.helpers import create_fake_scores

class Command(BaseCommand):
    help = "Creates fake music scores"

    def handle(self, *args, **options):
        num_scores = input("How many scores would you like to create? ")
        create_fake_scores(num_scores)
        print("Created fake scores")
