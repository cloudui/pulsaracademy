from django.urls import path

from .views import ProfilePageView, StaffListView, PasswordChangeSuccessfulView, MyCustomPasswordChangeView

urlpatterns = [
    # path('signup/', SignupPageView.as_view(), name='signup'),
    path('profile/', ProfilePageView.as_view(), name='profile'),
    path('user-list/', StaffListView.as_view(), name='student_list'),
    path('password/change/', MyCustomPasswordChangeView.as_view(), name='account_change_password'),
    path('password/change/success', PasswordChangeSuccessfulView.as_view(), name='password_success'), 
]