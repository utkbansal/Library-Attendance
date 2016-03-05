from django.conf.urls import url

from .views import LoginView, AttendanceView, LogoutView, ExitAllView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^$', AttendanceView.as_view(), name='attendance'),
    url(r'^exit_all$', ExitAllView.as_view(), name='exit_all')
]
