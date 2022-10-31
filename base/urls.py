from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="login/login.html"), name="login"),
    path("login/", auth_views.LoginView.as_view(template_name="login/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="login/login.html"), name='logout'),
    path('register/', views.register, name="register"),
    path('index/', views.index, name="index"),
    path('delete/', views.delete_user, name="delete_user"),
    path('deactivate/', views.deactivate_user, name="deactivate_user"),
    path('activate/', views.activate_user, name="activate_user"),
    path('GetBotValues/', views.GetBotValues, name="GetBotValues"),
    path('GetResources/', views.GetResources, name="GetResources"),
    path('SaveBotValues/', views.SaveBotValues, name="SaveBotValues"),
    path('GetUrls/', views.GetUrls, name="GetUrls"),
    path('bot_conf/', views.bot_conf, name="bot_conf"),
    path('alertconf/', views.alertconf, name="alertconf"),
    path('fetch/<str:user_id>/', views.fetch, name="fetch"),
    path('GetTrustedConfig/', views.GetTrustedConfig, name="GetTrustedConfig"),
    path('logsResults/', views.logsResults, name="logsResults"),
    path('revert/', views.revertChanges, name="logsResults"),
    path('revertBackChanges/', views.revertBackendChanges, name="logsResults"),
    path('revertFrontChanges/', views.revertFrontendChanges, name="logsResults"),
    path('download_report/', views.download_report, name="download_report"),
    path('GetLogs/', views.GetLogs, name="GetLogs"),
    path('GetLogsTry/', views.GetLogsTry, name="GetLogsTry"),
    path('GetImageLogs/', views.GetImageLogs, name="GetImageLogs"),
    path('StartBot/', views.StartBot, name="StartBot"),
    path('StopBot/', views.StopBot, name="StopBot"),
    path('Images/<filename>', views.open_def_img, name="open_def_img"),
    path('subdomains/', views.subdomains, name="subdomains"),
    path('admin/', views.admin, name="admin"),
    path('change_password/', views.change_password, name="change_password"),
    path('location/', TemplateView.as_view(template_name="location.html"), name='location'),
    path('location/', TemplateView.as_view(template_name="location.html"), name='location'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

]
