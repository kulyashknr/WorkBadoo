from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from api.views.vacancy import VacancyListView
from users.views import Register, RegisterCompany, RegisterWorker
from .views import matching, vacancy

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', Register.as_view()),
    path('register/company/', RegisterCompany.as_view()),
    path('register/workers/', RegisterWorker.as_view()),
    path('vacancies/', VacancyListView.as_view()),
    path('like/', matching.like),
    path('dislike/', matching.dislike),
]

router = routers.DefaultRouter()
router.register('matching', matching.MatchingViewSet, base_name='api')
router.register('vacancy', vacancy.VacancyViewSet, base_name='api')

urlpatterns += router.urls
