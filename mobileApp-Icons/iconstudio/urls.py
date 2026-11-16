from django.urls import path

from studio.views import home


urlpatterns = [
    path("", home, name="home"),
]
