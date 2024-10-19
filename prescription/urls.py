from django.urls import path
from prescription.customer.views import CustomerProjectView, CustomerTypeOfViolationView, UstumerPrescriptionsView, UstumerPrescriptionView
from prescription.admin_acc.views import AdminPrescriptionsView, AdminPrescriptionView

urlpatterns = [
    # Customer
    path('prescription/customer/projects/', CustomerProjectView.as_view()),
    path('prescription/customer/type_violation/', CustomerTypeOfViolationView.as_view()),
    path('prescription/customer/', UstumerPrescriptionsView.as_view()),
    path('prescription/customer/<int:pk>/', UstumerPrescriptionView.as_view()),
    # Admin
    path('prescription/admin/', AdminPrescriptionsView.as_view()),
    path('prescription/admin/<int:pk>/', AdminPrescriptionView.as_view()),

]