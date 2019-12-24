from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.constants import MATCHED_BY_BOTH, MATCHED_BY_USER, MATCHED_BY_COMPANY, DECLINED_BY_COMPANY, DECLINED_BY_USER
from api.models import MatchingForCompany, MatchingForWorker, Matching
from api.serializers import MatchingForWorkerSerializer, MatchingForCompanySerializer
from users.models import Company, Worker

import logging

logger = logging.getLogger(__name__)


class MatchingViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = MatchingForWorkerSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return MatchingForCompanySerializer
        return MatchingForWorkerSerializer

    def get_queryset(self):
        user = self.request.user
        print(MatchingForWorker.objects.all())
        if user.is_staff:
            company = Company.objects.get(user=user)
            return MatchingForCompany.objects.filter(vacancy__creator=company)
        else:
            return MatchingForWorker.objects.filter(worker__user=user)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like(request):
    try:
        company_id = request.data['company_id']
        worker_id = request.data['worker_id']
        company = Company.objects.get(id=company_id)
        worker = Worker.objects.get(id=worker_id)
        try:
            obj = Matching.objects.get(company=company, worker=worker)
            if (request.user.is_staff and obj.status == MATCHED_BY_USER) or \
                    ((not request.user.is_staff) and obj.status == MATCHED_BY_COMPANY):
                obj.status = MATCHED_BY_BOTH
                MatchingForWorker.objects.filter(worker=worker, company=company).delete()
                MatchingForCompany.objects.filter(worker=worker, company=company).delete()
                obj.save()
                logger.info(f"Liked")
            else:
                return Response({"message": "In some case decided by user or company"})
        except Matching.DoesNotExist:
            Matching.objects.create(company=company, worker=worker, status=
                                    MATCHED_BY_COMPANY if request.user.is_staff else MATCHED_BY_USER)
        return Response({"message": "Liked"})
    except Exception as e:
        return Response({"error": e})


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def dislike(request):
    try:
        company_id = request.data['company_id']
        worker_id = request.data['worker_id']
        company = Company.objects.get(id=company_id)
        worker = Worker.objects.get(id=worker_id)
        try:
            obj = Matching.objects.get(company=company, worker=worker)
            obj.status = DECLINED_BY_COMPANY if request.user.is_staff else DECLINED_BY_USER
            obj.save()
            logger.info(f"Disliked")
            MatchingForWorker.objects.filter(worker=worker, company=company).delete()
            MatchingForCompany.objects.filter(worker=worker, company=company).delete()
        except Matching.DoesNotExist:
            Matching.objects.create(company=company, worker=worker, status=
                                    DECLINED_BY_COMPANY if request.user.is_staff else DECLINED_BY_USER)
        return Response({"message": "SUCCESSFUL DECLINED"})
    except Exception as e:
        return Response({"error": e})
