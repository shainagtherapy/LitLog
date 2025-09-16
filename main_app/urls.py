from django.urls import path
from . import views 
# Import views to connect routes to view functions

urlpatterns = [
    path('', views.home, name='home'),
    path('logs/', views.log_index, name='log-index'),
    path('logs/<int:log_id>/', views.log_detail, name='log-detail'),
    path('logs/create/', views.LogCreate.as_view(), name='log-create'),
]