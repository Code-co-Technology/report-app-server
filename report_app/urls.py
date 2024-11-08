from django.urls import path

from report_app.reports.views import BobView, TypeOfWorkView, RepostsFileDetaileView
from report_app.report_user.views import (
    UserReportReceivedView, UserReportReturnView,
    UserReportsView, UserReportView, UserReportCount
)
from report_app.report_contractor.views import (
    ContractorReportsView, ContractorReportView, ContractorReporCountView
)
from report_app.report_customer.views import (
    CusntomerReporCountView, 
    CustomerReportsView, CustomerReportView
)
from report_app.report_admin.views import AdminReportsView, AdminReportView, AdminOwnerReportView


urlpatterns = [
    # Reports
    path('report/section/', BobView.as_view()),
    path('report/type_work/', TypeOfWorkView.as_view()),
    path('report/files/<int:pk>/', RepostsFileDetaileView.as_view()),
    # User Reports
    path('report/user/count/', UserReportCount.as_view()),
    path('report/user/received/', UserReportReceivedView.as_view()),
    path('report/user/returned/', UserReportReturnView.as_view()),
    path('report/user/', UserReportsView.as_view()),
    path('report/user/<int:pk>/', UserReportView.as_view()),
    # Contractor Reports
    path('report/contractor/count/', ContractorReporCountView.as_view()),
    path('report/contractor/', ContractorReportsView.as_view()),
    path('report/contractor/<int:pk>/', ContractorReportView.as_view()),
    # Customer Reports
    path('report/customer/count/', CusntomerReporCountView.as_view()),
    path('report/customer/', CustomerReportsView.as_view()),
    path('report/customer/<int:pk>/', CustomerReportView.as_view()),
    # Admin Resports
    path('report/admin/', AdminReportsView.as_view()),
    path('report/admin/owner/report/<int:pk>/', AdminOwnerReportView.as_view()),
    path('report/admin/<int:pk>/', AdminReportView.as_view()),

]
