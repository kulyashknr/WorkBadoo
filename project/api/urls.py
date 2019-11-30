from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from users.views import Register, RegisterCompany, RegisterWorker
from .views import matching

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', Register.as_view()),
    path('register/company/', RegisterCompany.as_view()),
    path('register/workers/', RegisterWorker.as_view()),
    path('like/', matching.like),
    path('dislike/', matching.dislike),
]

router = routers.DefaultRouter()
router.register('matching', matching.MatchingViewSet, base_name='api')

urlpatterns += router.urls