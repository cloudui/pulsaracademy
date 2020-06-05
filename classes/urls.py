

from django.urls import include, path
from .views import (
    ClassListView, 
    ClassDetailView, 
    ClassRegistrationView, 
    ClassUnregisterView, 
    ClassPaymentView, 
    CheckoutSummaryView, 
    RegisteredClassesView, 
    PaidClassesView,
    StaffAutoPopulateField,
    LessonListView,
    LessonDetailView,
    LessonUpdateView,
    ForumListView,
    ForumDetailView,
    ForumUpdateView,
    ForumCreateView,
)

from .views import class_checkout_view

urlpatterns = [
    path('', ClassListView.as_view(), name='class_list'),
    path('pay/summary/', CheckoutSummaryView.as_view(), name='summary'), 
    path('registered/', RegisteredClassesView.as_view(), name='registered_classes'),
    path('paid/', PaidClassesView.as_view(), name='paid_classes'),
    path('checkout/', class_checkout_view, name='checkout'),


    path('<slug:slug>/', ClassDetailView.as_view(), name='class_detail'),
    path('<slug:slug>/register/', ClassRegistrationView.as_view(), name='register'),
    path('<slug:slug>/unregister/', ClassUnregisterView.as_view(), name='unregister'),

    path('<slug:slug>/forum/', ForumListView.as_view(), name='forum_list'),
    path('<slug:slug>/forum/posts/<int:pk>/', ForumDetailView.as_view(), name='forum_detail'), 
    path('<slug:slug>/forum/posts/<int:pk>/edit/', ForumUpdateView.as_view(), name='forum_edit'), 
    path('<slug:slug>/forum/posts/new/', ForumCreateView.as_view(), name='forum_new'),

    path('<slug:slug>/lessons/overview/', LessonListView.as_view(), name='lesson_list'),
    path('<slug:slug>/lessons/autopopulateform/', StaffAutoPopulateField.as_view(), name='auto_populate'),
    path('<slug:slug>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('<slug:slug>/lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    
    
    

]