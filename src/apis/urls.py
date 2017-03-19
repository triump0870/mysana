from django.conf.urls import url, include
from apis.views import ListCreateGoals, DetailUpdateGoal

urlpatterns = [
    url(r'^goals/$', ListCreateGoals.as_view(), name='goals'),
    url(r'^goals/(?P<pk>\d+)/$', DetailUpdateGoal.as_view(), name='goal-details'),

]
