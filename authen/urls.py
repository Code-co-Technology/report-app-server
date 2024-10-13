from django.urls import path
from authen.views import (
    UserGroupView,
    UserSignUp,
    UserSignIn,
    UserProfile,

)


urlpatterns = [
    path('user/rolle/', UserGroupView.as_view()),
    path('user/register/', UserSignUp.as_view()),
    path('user/login/', UserSignIn.as_view()),
    path('user/profile/', UserProfile.as_view()),

]