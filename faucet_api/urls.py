
from django.urls import path
from .views import FundApiView, StatsApiView


urlpatterns = [
    path('fund', FundApiView.as_view()),
    path('stats', StatsApiView.as_view()),
]