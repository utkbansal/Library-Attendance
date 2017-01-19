from django.conf.urls import url


from .views import AdminView, MonthlyReportFormView, TrueReaderFormView, TrueReadeDetailView

urlpatterns = [
    url(r'^$', AdminView.as_view(), name='report-admin'),
    url(r'^monthly-report/$', MonthlyReportFormView.as_view(),
        name='monthly-report'),
    url(r'^true-reader-report/$', TrueReaderFormView.as_view(),
        name='true-reader-report'),
    url(r'^true-reader-detail/$', TrueReadeDetailView.as_view(),
        name='true-reader-detail'),
]