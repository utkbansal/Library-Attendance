from django.contrib import admin

from .models import Room, Attendance

admin.site.register(Room)


class AttendanceAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(AttendanceAdmin, self).get_form(request, obj=None,
                                                     **kwargs)
        form.base_fields['exit_time'].required = False
        return form


admin.site.register(Attendance, AttendanceAdmin)

# Register your models here.
