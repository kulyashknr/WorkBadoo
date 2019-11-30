from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import MatchingForCompany, MatchingForWorker
from api.serializers import MatchingForWorkerSerializer, MatchingForCompanySerializer


class MatchingViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = MatchingForWorkerSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return MatchingForWorkerSerializer
        return MatchingForCompanySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MatchingForCompany.objects.filter(vacancy=user)
        else:
            return MatchingForWorker.objects.filter(worker=user)


@api_view(['POST'])
def like(request):
    return Response({"message": "Got some data!", "data": request.data})


@api_view(['POST'])
def dislike(request):
    pass
