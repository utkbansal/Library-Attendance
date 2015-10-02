from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import Room


class AttendanceForm(forms.Form):
    student_number = forms.CharField()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['room_no'] = forms.ModelChoiceField(
            queryset=Room.objects.all().order_by('name'))
