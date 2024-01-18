from django.db.models.signals import Signal, post_save
from django.dispatch import receiver
from .models import Task


task_completed_signal = Signal()

# Define a receiver function
@receiver(post_save, sender=Task)
def task_completion_handler(sender, instance, **kwargs):
    # Check if the task is marked as completed
    if instance.completed:
        # Send the task_completed_signal
        task_completed_signal.send(sender=Task, instance=instance)
