from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import FormView, RedirectView
from braces.views import LoginRequiredMixin, AnonymousRequiredMixin

from .forms import LoginForm, AttendanceForm
from .models import Room, Attendance


class AttendanceView(FormView):
    form_class = AttendanceForm
    template_name = 'add-attendance.html'
    success_url = '/add-attendance'

    def form_valid(self, form):
        student_number = form.cleaned_data['student_number']
        if Attendance.student_in_library(student_number):
            Attendance.exit(student_number)
            return redirect(self.success_url)
        Attendance.entry(student_number, self.request.session['room'])
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super(AttendanceView, self).get_context_data(**kwargs)
        context['students'] = Attendance.students_in_library()
        return context


class LoginView(AnonymousRequiredMixin, FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '/add-attendance'

    def form_valid(self, form):
        room_id = Room.objects.get(name=form.cleaned_data['room_no']).id
        self.request.session['room'] = room_id
        print room_id
        return HttpResponseRedirect(self.success_url)


class LogoutView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
