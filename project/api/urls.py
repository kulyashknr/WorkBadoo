from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from users.views import Register, RegisterCompany, RegisterWorker


urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', Register.as_view()),
    path('register/company/', RegisterCompany.as_view()),
    path('register/workers/', RegisterWorker.as_view()),
]

router = routers.DefaultRouter()

urlpatterns += router.urls