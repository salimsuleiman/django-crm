from django.urls import path
from .views import *

app_name = 'agents'
urlpatterns = [
    path('', AgentList.as_view(), name='agents'),
    path('create/', AgentCreate.as_view(), name='agent_create'),
    path('detail/<pk>/', AgentDetail.as_view(), name='agent_detail'),
    path('delete/<pk>/', AgentDelete.as_view(), name='agent_delete'),
    path('update/<pk>/', AgentUpdate.as_view(), name='agent_update')
]