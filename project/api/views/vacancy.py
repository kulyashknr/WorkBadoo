from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Vacancy
from api.serializers import VacancySerializer


import logging

logger = logging.getLogger(__name__)


class IsCompany(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class VacancyViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet,
                    mixins.ListModelMixin):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsCompany, )

    def get_queryset(self):
        print(self.request.user)
        return Vacancy.objects.all()

    @action(methods=['POST'], detail=False)
    def perform_create(self, serializer):
        logger.info(f"{self.request.user} created vacancy {self.request.data.get('name')}")
        return serializer.save(creator=self.request.user)

    @action(methods=['PUT'], detail=True)
    def perform_update(self, serializer):
        if self.request.user == self.get_object().creator:
            serializer.save()
            logger.info(f"{self.request.user} updated vacancy {self.request.data.get('name')}")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE'], detail=True)
    def perform_destroy(self, instance):
        if self.request.user == self.get_object().creator:
            logger.info(f"{self.request.user} deleted vacancy {self.request.data.get('name')}")
            instance.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)