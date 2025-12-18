from django.urls import path

from account.views import CreateUserView, ActivateUserView, LoginUserView, LogoutUserView, UpdateUserView, \
    UpdateUserEmailView, ConfirmedUpdateUserEmailView, UpdateUserPasswordView, ConfirmUpdateUserPasswordView

urlpatterns = [
    path('create', CreateUserView.as_view()),
    path('activate', ActivateUserView.as_view()),
    path('login', LoginUserView.as_view()),
    path('logout', LogoutUserView.as_view()),
    path('update', UpdateUserView.as_view()),
    path('update/email', UpdateUserEmailView.as_view()),
    path('update/email/confirm', ConfirmedUpdateUserEmailView.as_view()),
    path('update/password', UpdateUserPasswordView.as_view()),
    path('update/password/confirm', ConfirmUpdateUserPasswordView.as_view()),
]