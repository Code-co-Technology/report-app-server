from django.urls import path
from authen.views import (
    UserSignUp,
    UserContractorRegister,
    UserSignIn,
    UserProfile,
    UserInformationView,
    change_password,
    RequestPasswordRestEmail,
    SetNewPasswordView,

)


urlpatterns = [
    path('user/contractor/register/', UserSignUp.as_view()),
    path('user/customer/register', UserContractorRegister.as_view()),
    path('user/login/', UserSignIn.as_view()),
    path('user/profile/', UserProfile.as_view()),
    path('user/information/<int:pk>/', UserInformationView.as_view()),
    path('user/change/password/', change_password),
    path('forget/password/', RequestPasswordRestEmail.as_view()),
    path('forget/change/password/', SetNewPasswordView.as_view()),

]