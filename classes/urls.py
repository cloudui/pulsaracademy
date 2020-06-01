

from django.urls import include, path
from .views import ClassListView, ClassDetailView, ClassRegistrationView, ClassUnregisterView, ClassPaymentView, CheckoutSummaryView

from .views import class_checkout_view

urlpatterns = [
    path('', ClassListView.as_view(), name='class_list'),
    path('pay/summary/', CheckoutSummaryView.as_view(), name='summary'), 
    path('checkout/', class_checkout_view, name='checkout'),
    path('<slug:slug>/', ClassDetailView.as_view(), name='class_detail'),
    path('<slug:slug>/register/', ClassRegistrationView.as_view(), name='register'),
    path('<slug:slug>/unregister/', ClassUnregisterView.as_view(), name='unregister'),

]