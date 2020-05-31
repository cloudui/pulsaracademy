

from django.urls import include, path
from .views import ClassListView, ClassDetailView, ClassRegistrationView, ClassUnregisterView, ClassPaymentView

from .views import class_payment_view

urlpatterns = [
    path('', ClassListView.as_view(), name='class_list'),
    path('pay/', class_payment_view, name='payment'),
    path('<slug:slug>/', ClassDetailView.as_view(), name='class_detail'),
    path('<slug:slug>/register/', ClassRegistrationView.as_view(), name='register'),
    path('<slug:slug>/unregister/', ClassUnregisterView.as_view(), name='unregister'),

]