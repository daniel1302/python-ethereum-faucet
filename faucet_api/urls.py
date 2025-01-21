
from django.urls import path
from .views import FundApiView, StatsApiView, EnvironmentApiView


urlpatterns = [
    path('fund', FundApiView.as_view()),
    path('stats', StatsApiView.as_view()),
    path('environment', EnvironmentApiView.as_view()),
]