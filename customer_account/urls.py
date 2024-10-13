from django.urls import path
from customer_account.views.users_views import CustumerUserGroupView, CustumerUsersView, CustomerUserView

urlpatterns = [
    path('user/roll/', CustumerUserGroupView.as_view()),
    path('users/', CustumerUsersView.as_view()),
    path('user/<int:pk>/', CustomerUserView.as_view()),

]