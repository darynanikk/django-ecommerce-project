from django.urls.conf import path, include
from . import views


urlpatterns = [
    path("login", views.login_user, name='login'),
    path("register", views.register_user, name='register'),
    path("logout", views.logout_user, name='logout'),
]