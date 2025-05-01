from django.urls import path
from .views import signup_view, login_view, dashboard_view, verify_payment_view, admin_dashboard_view, index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='landing'),  # 👈 Landing page shown first
    path('dashboard/', dashboard_view, name='dashboard'), # ✅ Fixed line
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('verify-payment/', verify_payment_view, name='verify-payment'),
    path('admin-dashboard/', admin_dashboard_view, name='admin-dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
