from rest_framework import serializers
from .models import MainUser, Vacancy, MatchingForWorker, MatchingForCompany, Company, Worker


class UserShortSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username')

    def create(self, validated_data):
        user = MainUser.objects.create_user(**validated_data)
        return user


class UserFullSerializer(UserShortSerializer):
    class Meta:
        model = MainUser
        fields = '__all__'


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError('Salary > 0')
        return value

    def validate_description(self, value):
        if len(value) < 100:
            raise serializers.ValidationError('Description should be longer')
        return value


class CompanySerializer(serializers.ModelSerializer):
    # name = serializers.CharField()
    # user = UserShortSerializer(read_only=True)
    # description = serializers.CharField(max_length=1000)
    # address = serializers.CharField()

    class Meta:
        model = Company
        fields = '__all__'

    def validate_address(self, value):
        if value.isalnum():
            raise serializers.ValidationError('Address should contain both street name and number')
        return value

    def validate_description(self, value):
        if len(value) < 100:
            raise serializers.ValidationError('Description should be longer')
        return value


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = '__all__'

    def validate_bio(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Bio should be longer')
        return value

    def validate_education(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Education description should be longer')
        return value


class MatchingForWorkerSerializer(serializers.ModelSerializer):
    vacancies = VacancySerializer(write_only=True)

    class Meta:
        model = MatchingForWorker
        fields = '__all__'


class MatchingForCompanySerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(write_only=True)

    class Meta:
        model = MatchingForCompany
        fields = '__all__'

