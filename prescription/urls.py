from django.urls import path
from prescription.customer.views import CustomerProjectView, CustomerTypeOfViolationView, UstumerPrescriptionsView

urlpatterns = [
    path('prescription/customer/projects/', CustomerProjectView.as_view()),
    path('prescription/customer/type_violation/', CustomerTypeOfViolationView.as_view()),
    path('prescription/customer/', UstumerPrescriptionsView.as_view())

]