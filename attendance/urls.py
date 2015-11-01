from django.conf.urls import url

from .views import LoginView, AttendanceView, LogoutView, ExcelView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^add-attendance/$', AttendanceView.as_view(), name='attendance'),
    url(r'^excel/$', ExcelView.as_view(), name='excel'),

]
