from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from users.models import Company, Worker
from api.models import MatchingForWorker, MatchingForCompany, MainUser
from api.models import Vacancy as Vac
from api.serializers import VacancySerializer, UserFullSerializer, UserShortSerializer

import logging

logger = logging.getLogger(__name__)


class IsCompany(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserFullSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        print(self.request.user)
        return MainUser.objects.all()


def create_connection(vacancy, company, industry):
    workers = Worker.objects.filter(industry=industry)
    match = MatchingForWorker.objects.filter(worker__in=workers)
    if len(match) == 0:
        for worker in workers:
            vv = MatchingForWorker.objects.create(worker=worker)
            vv.vacancies.add(vacancy)
        print(MatchingForWorker.objects.all())
    else:
        print("not here")
        for obj in match:
            obj.vacancies.add(vacancy)
        print("all right")
    match = MatchingForCompany.objects.filter(vacancy__creator=company)
    if len(match) == 0:
        mtching = MatchingForCompany.objects.create(vacancy=vacancy)
        for worker in workers:
            mtching.workers.add(worker)
        logger.info(f"CONNECTION CREATED!")
    else:
        for obj in match:
            for worker in workers:
                obj.workers.add(worker)
                obj.save()
            # obj.workers.add(workers)
            # obj.save()


class VacancyListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = VacancySerializer
    queryset = Vac.objects.all()
    lookup_field = 'industry'

    def get_queryset(self):
        return Vac.objects.all()


class VacancyViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    # queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsCompany, )

    @action(methods=['POST'], detail=True)
    def perform_create(self, serializer):
        try:
            logger.info(f"{self.request.user} created vacancy {self.request.data.get('name')}")
            company = Company.objects.get(user=self.request.user)
            vacancy = serializer.save(creator=company)
            create_connection(vacancy, company, serializer.data['industry'])
            return vacancy
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

