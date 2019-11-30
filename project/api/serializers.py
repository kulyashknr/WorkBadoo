from rest_framework import serializers
from .models import MainUser, Vacancy, MatchingForWorker, MatchingForCompany


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'


class MatchingForWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchingForWorker
        fields = '__all__'


class MatchingForCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchingForCompany
        fields = '__all__'

