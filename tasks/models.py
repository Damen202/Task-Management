from django.db import models
from django.utils import timezone
from users.models import CustomUser


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.BooleanField(default=False)  # False = Pending, True = Completed
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')

    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.status and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.status and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
