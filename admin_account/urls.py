from django.urls import path
from admin_account.project.views import AdminProjectsView, AdminProjectView, ProjectImageView, ProjectFileView
from admin_account.contractor_user.views import (
    AdminOverdueView, AdminFailedReportsView, 
    AdminContractorUsersView, AdminContractorUserView, AdminContractorFalseUsersView, 
    AdminContraCountUsersView
)
from admin_account.customer_user.views import AdminCustumerUsersView, AdminCustumerUserView, AdminCustumerFalseUsersView, AdminCustumerCountUsersView

urlpatterns = [
    path('admin_account/project/', AdminProjectsView.as_view()),
    path('admin_account/project/<int:pk>/', AdminProjectView.as_view()),
    path('admin_account/project_image/<int:pk>/', ProjectImageView.as_view()),
    path('admin_account/project_file/<int:pk>/', ProjectFileView.as_view()),
    # Contractor user
    path('admin_account/contractor/count/', AdminContraCountUsersView.as_view()),
    path('admin_account/contractor/overdue/', AdminOverdueView.as_view()),
    path('admin_account/contractor/faild_reports/', AdminFailedReportsView.as_view()),
    path('admin_account/contractor/no_user/', AdminContractorFalseUsersView.as_view()),
    path('admin_account/contractor/active_user/', AdminContractorUsersView.as_view()),
    path('admin_account/contractor/user/<int:pk>/', AdminContractorUserView.as_view()),
    # Customer
    path('admin_account/customer/count/', AdminCustumerCountUsersView.as_view()),
    path('admin_account/customer/no_user/', AdminCustumerFalseUsersView.as_view()),
    path('admin_account/customer/active_user/', AdminCustumerUsersView.as_view()),
    path('admin_account/customer/user/<int:pk>/', AdminCustumerUserView.as_view()),

]