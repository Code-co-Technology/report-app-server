from django.urls import path
from contractors_app.views.user_views import ContractorUserGroupView, ContractorUsersView, ContractorUserView

urlpatterns = [
    path('user/roll/', ContractorUserGroupView.as_view()),
    path('users/', ContractorUsersView.as_view()),
    path('user/<int:pk>/', ContractorUserView.as_view()),


]