from io import BytesIO

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView, RedirectView
from django.http import HttpResponse

from braces.views import LoginRequiredMixin, AnonymousRequiredMixin

from .forms import LoginForm, AttendanceForm
from .models import Room, Attendance


class AttendanceView(LoginRequiredMixin, FormView):
    form_class = AttendanceForm
    template_name = 'add-attendance.html'
    success_url = reverse_lazy('attendance')

    def form_valid(self, form):
        student_number = form.cleaned_data['student_number']
        # If student is in library do an exit
        if Attendance.student_in_library(student_number):
            Attendance.exit(student_number)
            return redirect(self.success_url)
        # If student not already in the library do a new entry
        Attendance.entry(student_number, self.request.session['room'])
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(AttendanceView, self).get_context_data(**kwargs)
        context['students'] = Attendance.students_in_library()
        return context


class LoginView(AnonymousRequiredMixin, FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('attendance')

    def form_valid(self, form):
        room_id = Room.objects.get(name=form.cleaned_data['room_no']).id
        # Add the room id of the user to the session
        self.request.session['room'] = room_id
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.form_invalid(form)


class LogoutView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('login'))


# class ExcelView(FormView):
#     form_class = ExcelForm
#     template_name = 'excel.html'
#     success_url = '/excel'
#
#     def form_valid(self, form):
#         year = int(form.cleaned_data['year'])
#         month = int(form.cleaned_data['month'])
#
#         output = BytesIO()
#         report(year=year, month=month, output=output)
#         output.seek(0)
#         response = HttpResponse(output.read(),
#                                 content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#         response[
#             'Content-Disposition'] = "attachment; filename=Library_report.xlsx"
#         return response
