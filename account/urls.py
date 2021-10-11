from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('change/', views.change_password, name='change'),
    path('active<uidb64>/<token>/', views.RegisterEmail.as_view(), name='active'),
    path('reset/', views.ForgetPassword.as_view(), name='forget_password'),
    path('reset/done', views.MessageSendEmail.as_view(), name='message_send_email'),
    path('confirm/<uidb64>/<token>/', views.ConfirmNewPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete_new_password.as_view(), name='complete_new_password'),
    path('edit_profile/<int:pk>/', views.EditProfileView.as_view(), name='edit_profile'),
    path('create_address/', views.CreateAddressView.as_view(), name='create_address'),
    path('available_addresses/<int:id>/', views.AvailableAddressesView, name='available_addresses'),
    path('remove_address<int:id>/', views.remove_address_view, name='remove_address'),
    path('edit_address/<int:pk>/', views.EditAddressView.as_view(), name='edit_address'),
    path('history/', views.history_orders, name='history'),
    path('report/', views.Report.as_view(), name='report'),
    path('create_staff/', views.create_staff, name='create_staff'),
]