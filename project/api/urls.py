from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

from .views import Register


urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', Register.as_view()),
]

router = routers.DefaultRouter()

urlpatterns += router.urls