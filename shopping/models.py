from django.db import models
from user.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)
    store = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    added_by = models.ForeignKey(User, related_name="items_added", null=True, blank=True, on_delete=models.CASCADE)
    purchased_by = models.ForeignKey(User, related_name="items_purchased", null=True, blank=True, on_delete=models.CASCADE)
    is_purchased = models.BooleanField(default=False)
    purchased_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            "name": self.name,
            "created_at": self.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
            "is_purchased": self.is_purchased,
            "purchased_at": self.purchased_at.strftime("%m/%d/%Y, %H:%M:%S") if self.purchased_at else None,
        }
