from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.models import Vacancy
from api.serializers import VacancySerializer


class IsCompany(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class VacancyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = VacancySerializer
    permission_classes = (IsCompany, )

    def get_queryset(self):
        print(self.request.user)
        return Vacancy.objects.all()