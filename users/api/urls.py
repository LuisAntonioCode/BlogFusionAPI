from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, UserDataView

urlpatterns = [
    path('auth/register/', UserRegisterView.as_view(), name='register_user'),
    path('auth/me/', UserDataView.as_view(), name='data_user'),

    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]