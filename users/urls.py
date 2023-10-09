from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserRegisterView, UserProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
]
