from django.urls import path
from prescription.customer.views import (
    CustomerProjectView, CustomerTypeOfViolationView,
    UstumerPrescriptionsView, UstumerPrescriptionView, CustumerContraCountUsersView, UstumerPrescriptionCommentView
)
from prescription.admin_acc.views import AdminPrescriptionsView, AdminPrescriptionView
from prescription.constractor_app.views import (
    ContractorsPrescriptionsView, ContractorsPrescriptionNewView, 
    ContractorsPrescriptioneliminatedView, ContractorsPrescriptioneExpiredView, 
    ContractorsPrescriptionView, ContractorsPrescriptionCountView, ContractorsPrescriptionUserView
)
from prescription.user_app.views import (
    UserPrescriptionNewView, UserPrescriptioneliminatedView,
    UserPrescriptioneExpiredView, UserPrescriptionsView, UserPrescriptionView
)


urlpatterns = [
    # Customer
    path('prescription/customer/projects/', CustomerProjectView.as_view()),
    path('prescription/customer/type_violation/', CustomerTypeOfViolationView.as_view()),
    path('prescription/customer/contractors/', CustumerContraCountUsersView.as_view()),
    path('prescription/customer/', UstumerPrescriptionsView.as_view()),
    path('prescription/customer/<int:pk>/', UstumerPrescriptionView.as_view()),
    path('prescription/customer/comment/<int:pk>/', UstumerPrescriptionCommentView.as_view()),
    # Admin
    path('prescription/admin/', AdminPrescriptionsView.as_view()),
    path('prescription/admin/<int:pk>/', AdminPrescriptionView.as_view()),
    # Constractor
    path('prescription/contractor/count/', ContractorsPrescriptionCountView.as_view()),
    path('prescription/contractor/', ContractorsPrescriptionsView.as_view()),
    path('prescription/contractor/<int:pk>/', ContractorsPrescriptionView.as_view()),
    path('prescription/new/contractor/', ContractorsPrescriptionNewView.as_view()),
    path('prescription/liminate/contractor/', ContractorsPrescriptioneliminatedView.as_view()),
    path('prescription/expired/contractor/', ContractorsPrescriptioneExpiredView.as_view()),
    path('prescription/contractor/user/add/<int:pk>/', ContractorsPrescriptionUserView.as_view()),
    # User
    path('prescription/user/', UserPrescriptionsView.as_view()),
    path('prescription/user/<int:pk>/', UserPrescriptionView.as_view()),
    path('prescription/new/user/', UserPrescriptionNewView.as_view()),
    path('prescription/liminate/user/', UserPrescriptioneliminatedView.as_view()),
    path('prescription/expired/user/', UserPrescriptioneExpiredView.as_view()),

]