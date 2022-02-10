from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TaskStatus(models.TextChoices):
    PENDING = 'PE', 'Pending'
    COMPLETED = 'CO', 'Completed'
    DROPPED = 'DR', 'Dropped'


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        # object.toString() in the java world
        # gives a human-readable representation of the object
        return self.name


# Create your models here.
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(
        default=timezone.now()
    )
    completed_at = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=2,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    @property  # properties and descriptor protocol
    def foo(self):
        return 'hello'

    def __str__(self):
        return f'{self.content} - {self.get_status_display()}'

    def get_all_tags(self, delimiter=', '):
        return delimiter.join([tag.name for tag in self.tags.all()])
