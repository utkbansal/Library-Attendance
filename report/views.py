from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group

from django.views.generic import FormView

from attendance.models import Room

from attendance.forms import LoginForm


class AdminTestView(FormView):
    group_required = 'Generate Report'
    template_name = 'report/admin.html'
    success_url = '/admin'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        grp = Group.objects.get(name='Generate Report')

        context = super(AdminTestView, self).get_context_data(**kwargs)
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
