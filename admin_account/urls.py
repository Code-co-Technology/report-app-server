from django.urls import path
from admin_account.project.views import AdminProjectsView, AdminProjectView
from admin_account.contractor_user.views import AdminOverdueView, AdminFailedReportsView, AdminContractorUsersView, AdminContractorUserView

urlpatterns = [
    path('admin_account/project/', AdminProjectsView.as_view()),
    path('admin_account/project/<int:pk>/', AdminProjectView.as_view()),
    # Contractor user
    path('admin_account/contractor/overdue/', AdminOverdueView.as_view()),
    path('admin_account/contractor/faild_reports/', AdminFailedReportsView.as_view()),
    path('admin_account/contractor/user/', AdminContractorUsersView.as_view()),
    path('admin_account/contractor/user/<int:pk>/', AdminContractorUserView.as_view()),

]