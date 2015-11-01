from io import BytesIO

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import Group
from django.views.generic import FormView
from braces.views import GroupRequiredMixin

from attendance.models import Room
from attendance.forms import LoginForm
from .forms import ReportForm
from report.excel import report


class AdminView(FormView):
    group_required = 'Generate Report'
    template_name = 'report/admin.html'
    success_url = '/admin'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        grp = Group.objects.get(name='Generate Report')

        context = super(AdminView, self).get_context_data(**kwargs)
        context['form'] = form

        if grp not in request.user.groups.all():
            context['login'] = False
        else:
            context['login'] = True
        return self.render_to_response(context)

    def form_valid(self, form):

        room_id = Room.objects.get(name=form.cleaned_data['room_no']).id
        self.request.session['room'] = room_id
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        grp = Group.objects.get(name='Generate Report')

        if user is not None and user.is_active and (grp in user.groups.all()):
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class MonthlyReportFormView(GroupRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'report/monthly-report.html'
    group_required = 'Generate Report'

    def form_valid(self, form):
        year = int(form.cleaned_data['year'])
        month = int(form.cleaned_data['month'])

        output = BytesIO()
        report(year=year, month=month, output=output)
        output.seek(0)
        response = HttpResponse(output.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response[
            'Content-Disposition'] = "attachment; filename=Library_report.xlsx"
        return response


class TrueReaderFormView(GroupRequiredMixin, FormView):
    form_class = ReportForm
    template_name = 'report/true-reader.html'
    group_required = 'Generate Report'
