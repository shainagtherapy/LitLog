from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
# Import views to connect routes to view functions

urlpatterns = [
    path('', views.Home.as_view(), name='home'),

    path('logs/', views.log_index, name='log-index'),
    path('logs/<int:log_id>/', views.log_detail, name='log-detail'),
    path('logs/create/', views.LogCreate.as_view(), name='log-create'),
    path('logs/<int:pk>/update/', views.LogUpdate.as_view(), name='log-update'),
    path('logs/<int:pk>/delete', views.LogDelete.as_view(), name='log-delete'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.LoginView.as_view(template_name="auth/login_form.html"), name='login'),
    path('profile/', views.profile_detail, name='profile-detail'),
    path('profile/edit/', views.profile_edit, name='profile-edit'),

    # Spotify API:
    path('audiobooks/search/', views.audiobook_search, name='audiobook-search'),
    path('audiobooks/save/', views.audiobook_save, name='audiobook-save'),
    path('podcasts/search/', views.podcast_search, name='podcast-search'),
    path('podcasts/save/', views.podcast_save, name='podcast-save'),

    # Google Books API:
    path('books/search/', views.book_search, name='book-search'),
    path('books/save', views.book_save, name='book-save'),
]