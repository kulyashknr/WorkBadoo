from django.db import models
from django.contrib.auth.models import AbstractUser

from api.constants import USER_TYPES, INDUSTRY_TYPES
from utils.upload import user_photo_path
from utils.validators import validate_size, validate_extension


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class WorkerCompanyBase(models.Model):
    photo = models.FileField(upload_to=user_photo_path, validators=[validate_size, validate_extension], blank=True, null=True)


    class Meta:
        abstract = True


class Worker(WorkerCompanyBase):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='worker_user')
    bio = models.TextField(max_length=500)
    education = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    industry = models.SmallIntegerField(choices=INDUSTRY_TYPES)

    def __str__(self):
        return f'{ self.user }'


class Company(WorkerCompanyBase):
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, null=True, related_name='company_user')
    name = models.CharField(max_length=255)
    description = models.TextField
    address = models.CharField(max_length=255)

    def __str__(self):
        return f'{ self.name }: { self.description }'

