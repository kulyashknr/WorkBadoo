from django.db import models
from users.models import MainUser, Worker, Company
from .constants import INDUSTRY_TYPES


class Vacancy(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='vacancy_creator')
    description = models.TextField
    salary = models.IntegerField
    is_active = models.BooleanField()
    industry = models.SmallIntegerField(choices=INDUSTRY_TYPES)

    def __str__(self):
        return f'{ self.name }: { self.salary }, { self.company }'


class MatchingForWorker(models.Model):
    worker = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, null=True, related_name='matchforworker_worker')
    vacancies = models.ManyToManyField(Vacancy)


class MatchingForCompany(models.Model):
    workers = models.ManyToManyField(Worker)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.DO_NOTHING, null=True, related_name='matchforcompany_vacancy')


class Matching(models.Model):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.DO_NOTHING, null=True, related_name='vacancy')
    worker = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, null=True, related_name='worker')




