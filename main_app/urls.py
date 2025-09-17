from django.urls import path
from . import views 
from .views import profile
# Import views to connect routes to view functions

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('logs/', views.log_index, name='log-index'),
    path('logs/<int:log_id>/', views.log_detail, name='log-detail'),
    path('logs/create/', views.LogCreate.as_view(), name='log-create'),
    path('logs/<int:pk>/update/', views.LogUpdate.as_view(), name='log-update'),
    path('logs/<int:pk>/delete', views.LogDelete.as_view(), name='log-delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('profile/', profile, name='users-profile')
]