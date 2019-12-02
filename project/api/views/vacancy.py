from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Vacancy, MatchingForWorker, MatchingForCompany
from api.serializers import VacancySerializer


import logging

from users.models import Company, Worker

logger = logging.getLogger(__name__)


class IsCompany(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


def create_connection(company, industry):
    workers = Worker.objects.filter(industry=industry)
    match = MatchingForWorker.objects.filter(worker__in=workers)
    if len(match) == 0:
        for worker in workers:
            MatchingForWorker.objects.create(worker=worker, company=company)
    else:
        for obj in match:
            obj.add(company)
            obj.save()

    match = MatchingForCompany.objects.filter(company=company)
    if len(match) == 0:
        MatchingForCompany.objects.create(company=company, workers=workers)
    else:
        match.add(workers)
        match.save()


class VacancyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet,
                     mixins.ListModelMixin):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    #permission_classes = (IsCompany, )

    def get_queryset(self):
        #industry = Vacancy.objects.filter(industry=1)
        return Vacancy.objects.filter(industry=1)

    @action(methods=['POST'], detail=True)
    def perform_create(self, serializer):
        try:
            logger.info(f"{self.request.user} created vacancy {self.request.data.get('name')}")
            company = Company.objects.get(user=self.request.user)
            create_connection(company, serializer.data['industry'])
            return serializer.save(creator=company)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['PUT'], detail=True)
    def perform_update(self, serializer):
        company = Company.objects.get(user=self.request.user)
        if company == self.get_object().creator:
            serializer.save()
            create_connection(company, serializer.data['industry'])
            logger.info(f"{self.request.user} updated vacancy {self.request.data.get('name')}")
        else:
            logger.error(f"{self.request.user} in method perform update was error")
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True)
    def perform_destroy(self, instance):
        if self.request.user == self.get_object().creator:
            logger.info(f"{self.request.user} deleted vacancy {self.request.data.get('name')}")
            instance.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

