from django.urls import path
from customer_account.views import CustumerUserGroupView, CustumerUsersView

urlpatterns = [
    path('groups/', CustumerUserGroupView.as_view()),
    path('users/', CustumerUsersView.as_view()),

]