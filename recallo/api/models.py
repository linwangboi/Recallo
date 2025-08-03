from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# TODO: going to implement tags model and link them into User,
# so that user can click on tags and all related items


class StudyItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_items"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):
        return f"{self.title} ({self.user.email})"


class ReviewSession(models.Model):
    study_item = models.ForeignKey(
        StudyItem,
        on_delete=models.CASCADE,
        related_name="review_sessions",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="review_sessions",
    )
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reviewed_at"]

    def __str__(self):
        return (
            f"Review for '{self.study_item.title}' "
            f"on {self.reviewed_at} by {self.user.email}"
        )
