from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.core.exceptions import ValidationError


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

    def clean(self):
        if self.due_date and self.due_date < timezone.now().date():
            raise ValidationError("Due date cannot be in the past.")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
