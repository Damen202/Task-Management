from django.urls import path
from .views import login, ProfileView, register, logout
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
