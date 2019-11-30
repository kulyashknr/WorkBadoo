from django.db import models
from django.contrib.auth.models import AbstractUser

from api.constants import USER_TYPES


class MainUser(AbstractUser):
    status = models.SmallIntegerField(choices=USER_TYPES)
    #photo = models.FileField(upload_to=user_photo_path, validators=[validate_size, validate_extension], blank=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Worker(models.Model):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='worker_user')
    bio = models.TextField(max_length=500)
    education = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)


class Company(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='company_user')
    description = models.TextField
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{ self.name }: { self.description }'

