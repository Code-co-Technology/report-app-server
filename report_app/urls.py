from django.urls import path
from report_app.reports.views import BobView, TypeOfWorkView
from report_app.report_user.views import UserReportReceivedView, UserReportReturnView, UserReportsView, UserReportView

urlpatterns = [
    # Reports
    path('report/section/', BobView.as_view()),
    path('report/type_work/', TypeOfWorkView.as_view()),
    # User Reports
    path('report/user/received/', UserReportReceivedView.as_view()),
    path('report/user/returned/', UserReportReturnView.as_view()),
    path('report/user/', UserReportsView.as_view()),
    path('report/user/<int:pk>/', UserReportView.as_view()),

]