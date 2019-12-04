from django.db.models.signals import post_delete
from django.dispatch import receiver

from users.models import WorkerCompanyBase
from utils.upload import photo_delete_path


@receiver(post_delete, sender=WorkerCompanyBase)
def photo_deleted(sender, instance, **kwargs):
    # instance.documents.count() > 0:
    if instance.document:
        photo_delete_path(document=instance.document)