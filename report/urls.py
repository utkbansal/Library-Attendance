from django.conf.urls import url


from .views import AdminTestView

urlpatterns = [
    url(r'^', AdminTestView.as_view(), name='report-admin')
]