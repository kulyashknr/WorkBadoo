from django.db import models
from users.models import MainUser, Worker, Company
from .constants import *


class ItVacancyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(industry=IT_INDUSTRY)


class BusinessVacancyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(industry=BUSINESS_INDUSTRY)


class ServiceVacancyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(industry=SERVICE_INDUSTRY)


class EducationVacancyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(industry=EDUCATION_INDUSTRY)


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='vacancy_creator')
    description = models.TextField
    salary = models.IntegerField
    is_active = models.BooleanField(blank=True, default=True)
    industry = models.SmallIntegerField(choices=INDUSTRY_TYPES)

    # itVacancies = ItVacancyManager()
    # businessVacancies = BusinessVacancyManager()
    # serviceVacancies = ServiceVacancyManager()
    # educationVacancies = EducationVacancyManager()

    def __str__(self):
        return f'{ self.name }: { self.salary }'


class MatchingForWorker(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.DO_NOTHING, null=True, related_name='matchforworker_worker')
    vacancies = models.ManyToManyField(Vacancy)

    def __str__(self):
        return f'{self.worker}'


class MatchingForCompany(models.Model):
    workers = models.ManyToManyField(Worker)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.DO_NOTHING, null=True, related_name='matchforcompany_vacancy')


class Matching(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.DO_NOTHING, null=True, related_name='vacancy')
    worker = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, null=True, related_name='worker')
    status = models.PositiveSmallIntegerField(choices=MATCHING_STATUSES)




