

from django.urls import include, path
from .views import *


from .views import class_checkout_view, class_specific_checkout_view, create_comment

urlpatterns = [
    path('', ClassListView.as_view(), name='class_list'),
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/archive', StaffArchiveView.as_view(), name='staff_archive'),
    # path('pay/summary/', CheckoutSummaryView.as_view(), name='summary'), 
    path('enrolled/', RegisteredClassesView.as_view(), name='registered_classes'),
    #path('paid/', PaidClassesView.as_view(), name='paid_classes'),
    # path('checkout/', class_checkout_view, name='checkout'),
    path('clear/old-classes/', ClearOldClassesView.as_view(), name='clear'),
    # path('payment-success/', PaymentSuccessView.as_view(), name='payment_success'),
    # path('schedule/', ClassScheduleView.as_view(), name='schedule'),


    path('<slug:slug>/', ClassDetailView.as_view(), name='class_detail'),
    path('<slug:slug>/staff/', ClassStaffUsersDetailView.as_view(), name='staff_class_user_detail'),
    path('<slug:slug>/register/', ClassRegistrationView.as_view(), name='register'),
    path('<slug:slug>/unregister/', ClassUnregisterView.as_view(), name='unregister'),
    # path('<slug:slug>/remove-from-cart', ClassUnregisterCartView.as_view(), name='cart_unregister'), 
    path('<slug:slug>/edit/', ClassUpdateView.as_view(), name='class_update'),
    # path('<slug:slug>/pay-now/', class_specific_checkout_view, name='class_pay'),
    path('<slug:slug>/archive/', ClassArchiveView.as_view(), name='archive_class'),

    path('<slug:slug>/forum/', ForumListView.as_view(), name='forum_list'),
    path('<slug:slug>/forum/posts/new/', ForumCreateView.as_view(), name='forum_new'),
    path('<slug:slug>/forum/posts/<int:pk>/', ForumDetailView.as_view(), name='forum_detail'), 
    path('<slug:slug>/forum/posts/<int:pk>/edit/', ForumUpdateView.as_view(), name='forum_edit'),
    path('<slug:slug>/forum/posts/<int:pk>/delete/', ForumDeleteView.as_view(), name='forum_delete'),
    path('<slug:slug>/forum/posts/<int:pk>/comment/', create_comment, name='comment_new'),

    path('<slug:slug>/lessons/overview/', LessonListView.as_view(), name='lesson_list'),
    path('<slug:slug>/lessons/autopopulateform/', StaffAutoPopulateField.as_view(), name='auto_populate'),
    path('<slug:slug>/lessons/welcome/', ClassIntroView.as_view(), name='lesson_intro'),
    path('<slug:slug>/lessons/welcome/edit/', ClassIntroUpdateView.as_view(), name = 'intro_edit'),
    path('<slug:slug>/lessons/create/', LessonCreateView.as_view(), name='lesson_create'),
    path('<slug:slug>/lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson_detail'),
    path('<slug:slug>/lessons/<int:pk>/edit/', LessonUpdateView.as_view(), name='lesson_edit'),
    
    
    
    

]