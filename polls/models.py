from django.contrib.auth.models import User
from django.db import models


class RatingSubject(models.Model):
    subject = models.CharField(max_length=200)
    credits = models.FloatField()
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.subject + " " + str(self.credits)


class RatingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.ForeignKey(RatingSubject, on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True)
