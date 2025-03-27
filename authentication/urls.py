from django.urls import path,include
from . import views

urlpatterns = [

    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogOutView.as_view(),name='logout'),
    path('identifyusersendotp/',views.IdentifyUserSendOtp.as_view(),name='identifyusersendotp'),
    path('verifyotp/',views.VerifyOtpLoginView.as_view(),name='verifyotp'),
    path('dashboard/',views.DashBoardView.as_view(),name='dashboard'),
    path('reset_password/<username>/',views.ResetPasswordView.as_view(),name='resetpassword'),
    path('accounts/', include('allauth.urls')),
]