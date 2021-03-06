from .views import CreatePollViewSet, PollView, GetResult
from django.urls import path

urlpatterns = [
    path('createPoll/', CreatePollViewSet.as_view({'post': 'create'}), name='createPoll'),
    path('poll/', PollView.as_view(), name='poll'),
    path('getResult/', GetResult.as_view(), name='getResult'),
]
