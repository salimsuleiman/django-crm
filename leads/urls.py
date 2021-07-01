from django.urls import path
from .views import *

app_name = 'leads'

urlpatterns = [
    path('', LeadList.as_view(), name='leads'),
    path('<int:pk>/', LeadDetail.as_view(), name='lead_detail'),
    
    path('create/', LeadCreate.as_view(), name='lead_create'),
    path('assign-agent/<int:pk>/', AssignAgentView.as_view(), name='assign_agent'),
    path('lead_category_update/<int:pk>/', LeadCategoryUpdate.as_view(), name='lead_category_update'),
    path('update/<int:pk>', LeadUpdate.as_view(), name='lead_update'),
    path('delete/<int:pk>', LeadDelete.as_view(), name='lead_delete'),

    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('categories/<pk>/', CategoryUpdate.as_view(), name='category_update'),
    path('categories/<pk>/', CategoryDelete.as_view(), name='category_delete'),
    path('categories/create/', CategoryCreate.as_view(), name='category_create')
]
