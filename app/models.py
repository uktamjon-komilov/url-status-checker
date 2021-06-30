from account.models import User
from django.db import models

class Url(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    custom_name = models.CharField(max_length=255, blank=True)
    url = models.TextField()
    request_interval = models.IntegerField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.user.fullname, self.url)