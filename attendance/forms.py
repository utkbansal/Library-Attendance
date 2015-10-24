from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import Room


class AttendanceForm(forms.Form):
    student_number = forms.CharField()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        """
        Extend the default Authentication form to add a 'room_no' field to it
        """
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['room_no'] = forms.ModelChoiceField(
            queryset=Room.objects.all().order_by('name'))


class ExcelForm(forms.Form):
    year = forms.IntegerField(label = 'Year')
    month = forms.ChoiceField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'),
                                       (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')],
                                 label='Month')


