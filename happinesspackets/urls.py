from django.urls import include, path

urlpatterns = [
    path("", include("happinesspackets.messaging.urls", namespace="messaging")),
]
