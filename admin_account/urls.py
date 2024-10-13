from django.urls import path
from admin_account.views.users_views import UsersView, ActivateUsersView, UserNoActiveView, UserGroupView

urlpatterns = [
    path('admin_account/users/', UsersView.as_view()),
    path('admin_account/inactive/users/', UserNoActiveView.as_view()),
    path('admin_account/user/<int:pk>/', ActivateUsersView.as_view()),
    path('admin_account/user/roll/', UserGroupView.as_view()),


]