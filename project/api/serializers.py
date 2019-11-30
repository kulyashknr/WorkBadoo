from rest_framework import serializers

from api.models import MatchingForWorker, MatchingForCompany


class MatchingForWorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchingForWorker
        fields = '__all__'


class MatchingForCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchingForCompany
        fields = '__all__'

