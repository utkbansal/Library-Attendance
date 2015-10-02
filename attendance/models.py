from django.utils import timezone

from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)

    def __unicode__(self):
        return self.name


class Attendance(models.Model):
    room = models.ForeignKey('Room')
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(null=True, default=None)
    student_number = models.CharField(max_length=255)

    @staticmethod
    def students_in_library():
        return Attendance.objects.filter(exit_time=None)

    @staticmethod
    def student_in_library(student_number):
        students = Attendance.students_in_library()
        for s in students:
            if s.student_number == student_number:
                return True
        return False

    @staticmethod
    def entry(student_number, room):
        room = Room.objects.get(id=room)
        obj = Attendance(
            student_number=student_number,
            entry_time=timezone.now(),
            room=room
        )
        obj.save()

    @staticmethod
    def exit(student_number):
        Attendance.objects.filter(
            student_number=student_number,
            exit_time=None
        ).update(
            exit_time=timezone.now()
        )

    def __unicode__(self):
        return self.student_number

    class Meta:
        verbose_name_plural = 'Attendance'
        ordering = ['entry_time', 'exit_time']
