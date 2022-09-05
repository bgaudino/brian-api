from uuid import uuid4
from django.db import models
from user.models import User


def upload_to(instance, filename):
    return f"shopping/photos/{''.join([instance.name, '_', str(uuid4().hex[:6]), '_', filename])}"


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to=upload_to)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower().strip()
        super().save(*args, **kwargs)

    def get_photo_url(self):
        return self.photo.url if self.photo else ""


class ItemInstance(models.Model):
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)
    store = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(
        User,
        related_name="items_added",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    purchased_by = models.ForeignKey(
        User,
        related_name="items_purchased",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    is_purchased = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.item.name if self.item else "No name"

    def serialize(self):
        return {
            "name": self.item.name,
            "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "is_purchased": self.is_purchased,
            "purchased_at": self.purchased_at.strftime("%m/%d/%Y, %H:%M:%S")
            if self.purchased_at
            else None,
        }
