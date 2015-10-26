from braces.views import GroupRequiredMixin
from django.shortcuts import redirect


from django.views.generic import TemplateView

class AdminTestView(TemplateView):
    group_required = 'Generate Report'
    template_name = 'report/admin.html'

    # def get(self, request, *args, **kwargs):



