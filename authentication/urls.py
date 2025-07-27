"""
URLs for the authentication app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets
router = DefaultRouter()
router.register(r'api-keys', views.APIKeyViewSet, basename='api-keys')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh-token'),
    
    # Password management
    path('password/change/', views.ChangePasswordView.as_view(), name='change-password'),
    path('password/reset/', views.PasswordResetView.as_view(), name='password-reset'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update-profile'),
    
    # API Key management
    path('api-keys/generate/', views.GenerateAPIKeyView.as_view(), name='generate-api-key'),
    path('api-keys/<int:key_id>/regenerate/', views.RegenerateAPIKeyView.as_view(), name='regenerate-api-key'),
    path('api-keys/<int:key_id>/revoke/', views.RevokeAPIKeyView.as_view(), name='revoke-api-key'),
    
    # Account verification
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', views.ResendVerificationView.as_view(), name='resend-verification'),
    
    # Security
    path('login-attempts/', views.LoginAttemptsView.as_view(), name='login-attempts'),
    path('active-sessions/', views.ActiveSessionsView.as_view(), name='active-sessions'),
    path('revoke-all-tokens/', views.RevokeAllTokensView.as_view(), name='revoke-all-tokens'),
]
