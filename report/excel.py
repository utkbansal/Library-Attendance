import os
import calendar
import xlsxwriter

from django.utils import timezone
from datetime import time, datetime
from pytz import timezone as tz

from attendance.models import Attendance


def report(year, month, output=None):
    # for headers
    date_now = timezone.datetime(year, month, 1)
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')

    # line separator
    sep = os.linesep

    merge_format = workbook.add_format({
        'bold': True,
        'border': 0,
        'align': 'center',
        'valign': 'vcenter',

    })

    footer_format = workbook.add_format({
        'bold': True,
        'border': 0,
    })
    worksheet.merge_range('A1:J6',
                          'AJAY KUMAR GARG ENGINEERING COLLEGE, GHAZIABAD ' +
                          sep + 'CENTRAL LIBRARY ' + sep +
                          'LIBRARY VISITORS REPORT: ' + date_now.strftime(
                              "%B %Y"), merge_format)

    fst_col = [['S.NO.', 'A'],
               ['DATE', 'B'],
               ["DAY", 'C'],
               ['8:30AM' + sep + 'TO' + sep + '4:00PM', 'D'],
               ['4:00PM' + sep + 'TO' + sep + '7:00PM', 'E'],
               ['7:00PM' + sep + 'TO' + sep + '9:00PM', 'F'],
               ['9:00PM' + sep + 'TO' + sep + '12 MIDNIGHT', 'G'],
               ['TOTAL' + sep + '4:00PM' + sep + 'TO' + sep + '12 MIDNIGHT', 'H'],
               ['TOTAL' + sep + ' 8:30AM' + sep + 'TO' + sep + '12 MIDNIGHT', 'I'],
               ['REMARKS', 'J']
               ]
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 18)
    for heading, x in fst_col:
        worksheet.merge_range(x + '8:' + x + '11' + '', heading,
                              merge_format)
        if x != 'A' and x != 'B':
            worksheet.set_column(x + ':' + x, 13)

    # for real excel

    month_30 = [4, 6, 9, 11]
    if month == 2:
        if year % 4 == 0:
            days = range(1, 30)
        else:
            days = range(1, 29)
    elif month in month_30:
        days = range(1, 31)
    else:
        days = range(1, 32)

    num_working_days = 0
    attds_slots_total = [0] * 6
    day = 1
    for day in days:
        time_start = timezone.datetime(year, month, day)
        time_start_slot_1 = timezone.datetime(year, month, day, 8, 30, 0)
        time_end_slot_1 = timezone.datetime(year, month, day, 15, 59, 59)
        time_start_slot_2 = timezone.datetime(year, month, day, 16, 0, 0)
        time_end_slot_2 = timezone.datetime(year, month, day, 18, 59, 59)
        time_start_slot_3 = timezone.datetime(year, month, day, 19, 0, 0)
        time_end_slot_3 = timezone.datetime(year, month, day, 20, 59, 59)
        time_start_slot_4 = timezone.datetime(year, month, day, 21, 0, 0)
        time_end_slot_4 = timezone.datetime(year, month, day, 23, 59, 59)
        attds_slot_1 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_1,
            entry_datetime__lte=time_end_slot_1).all()
        attds_slot_2 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_2,
            entry_datetime__lte=time_end_slot_2).all()
        attds_slot_3 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_3,
            entry_datetime__lte=time_end_slot_3).all()
        attds_slot_4 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_4,
            entry_datetime__lte=time_end_slot_4).all()
        attds_slot_counts = []
        attds_slot_counts.append(attds_slot_1.count())
        attds_slot_counts.append(attds_slot_2.count())
        attds_slot_counts.append(attds_slot_2.count())
        attds_slot_counts.append(attds_slot_3.count())
        attds_slot_counts.append(attds_slot_4.count())
        attds_slot_counts.append(attds_slot_counts[1] + attds_slot_counts[2] +
                                 attds_slot_counts[3])
        attds_slot_counts.append(attds_slot_counts[4] + attds_slot_counts[0])

        # update total count for each slot
        attds_slots_total[0] += attds_slot_counts[0]
        attds_slots_total[1] += attds_slot_counts[1]
        attds_slots_total[2] += attds_slot_counts[2]
        attds_slots_total[3] += attds_slot_counts[3]
        attds_slots_total[4] += attds_slot_counts[4]
        attds_slots_total[5] += attds_slot_counts[5]

        worksheet.write(10 + day, 0, day, cell_format)
        worksheet.write(10 + day, 1, time_start.strftime("%d, %B %Y"), cell_format)
        worksheet.write(10 + day, 2, time_start.strftime('%A'), cell_format)

        if attds_slot_counts[-1] != 0:
            num_working_days += 1
        for j in range(3, 9):
            if attds_slot_counts[-1] == 0:
                worksheet.write(10 + day, j, 'Holiday', cell_format)
            elif attds_slot_counts[j - 3] == 0:
                worksheet.write(10 + day, j, 'Closed', cell_format)
            else:
                worksheet.write(10 + day, j, attds_slot_counts[j - 3], cell_format)
    # slot-wise average if num_working_days is not zero
    attds_slots_avg = [0] * 6
    if num_working_days:
        attds_slots_avg[0] = float(attds_slots_total[0]) / num_working_days
        attds_slots_avg[1] = float(attds_slots_total[1]) / num_working_days
        attds_slots_avg[2] = float(attds_slots_total[2]) / num_working_days
        attds_slots_avg[3] = float(attds_slots_total[3]) / num_working_days
        attds_slots_avg[4] = float(attds_slots_total[4]) / num_working_days
        attds_slots_avg[5] = float(attds_slots_total[5]) / num_working_days

    worksheet.merge_range(10 + day + 1, 0, 10 + day + 2, 2,
                          "Average", merge_format)
    worksheet.merge_range(
        10 + day + 1, 3, 10 + day + 2, 3,
        "%d / %d %s= %.2f" %
        (attds_slots_total[0], num_working_days, sep, attds_slots_avg[0])
        if attds_slots_total[0] else "-", merge_format
    )
    worksheet.merge_range(
        10 + day + 1, 4, 10 + day + 2, 4,
        "%d / %d %s= %.2f" %
        (attds_slots_total[1], num_working_days, sep, attds_slots_avg[1])
        if attds_slots_total[1] else "-", merge_format
    )
    worksheet.merge_range(
        10 + day + 1, 5, 10 + day + 2, 5,
        "%d / %d %s= %.2f" %
        (attds_slots_total[2], num_working_days, sep, attds_slots_avg[2])
        if attds_slots_total[2] else "-", merge_format
    )
    worksheet.merge_range(
        10 + day + 1, 6, 10 + day + 2, 6,
        "%d / %d %s= %.2f" %
        (attds_slots_total[3], num_working_days, sep, attds_slots_avg[3])
        if attds_slots_total[3] else "-", merge_format
    )
    worksheet.merge_range(
        10 + day + 1, 7, 10 + day + 2, 7,
        "%d / %d %s= %.2f" %
        (attds_slots_total[4], num_working_days, sep, attds_slots_avg[4])
        if attds_slots_total[4] else "-", merge_format
    )
    worksheet.merge_range(
        10 + day + 1, 8, 10 + day + 2, 8,
        "%d / %d %s= %.2f" %
        (attds_slots_total[5], num_working_days, sep, attds_slots_avg[5])
        if attds_slots_total[5] else "-", merge_format
    )

    # footer
    worksheet.merge_range(
        20 + day, 0, 20 + day + 1, 2,
        " Dr. Shiv Shankar Srivastava%s (Sr. Librarian)" % sep, footer_format
    )

    worksheet.merge_range(
        20 + day, 7, 20 + day + 1, 9,
        " Prof. B.M. Kalra%s (Dean Library Resources)" % sep, footer_format
    )
    workbook.close()
    return workbook


def true_reader(month, year, output=None):
    """
    :param month: month for which the true reader is required
    :param year: year of which the true reader award is required
    :param output: output file to which the excel would be written
    :return: returns a workbook containing list of students with
     their time spent in the library
    """
    date_start = timezone.datetime(year, month, 1)  # first day of the month
    last_day = calendar.monthrange(year, month)[1]  # gets the last day of month
    date_end = timezone.datetime(year, month,
                                 last_day, 23, 59, 59) # last day of the month
    workbook = xlsxwriter.Workbook(output)  # create a workbook
    worksheet = workbook.add_worksheet()  # add a sheet
    excel_format = workbook.add_format()
    excel_format.set_align("vcenter")
    excel_format.set_align("center")
    merge_format = workbook.add_format({
        'bold': True,
        'border': 0,
        'align': 'center',
        'valign': 'vcenter',
    })
    worksheet.merge_range('A1:C6',
                          "AKGEC Library: True Reader Excel for %s" %
                          date_start.strftime("%B %Y"), merge_format)
    all_attendance = Attendance.objects.filter(
            entry_datetime__gte=date_start, entry_datetime__lte=date_end,
            exit_datetime__isnull=False)
    student_numbers = [stud_num[0] for stud_num in
                       all_attendance.order_by().values_list(
                               'student_number').distinct().all()]
    # print(student_numbers)
    student_records = []
    in_tz = tz('Asia/Kolkata')
    for student_number in student_numbers:
        td = timezone.timedelta()  # for storing total time spent by student
        student_attendances = all_attendance.filter(
                student_number=student_number,
                exit_time__gte=time(10, 30, 0),
                exit_time__lte=time(18, 30, 0)
        ).all()
        print(student_attendances)
        for student_attendance in student_attendances:
            if student_attendance.exit_time >= time(10, 30, 0):
                if student_attendance.entry_time >= time(10, 30, 0):
                    td += (student_attendance.exit_datetime -
                           student_attendance.entry_datetime)
                else:
                    td += (student_attendance.exit_datetime -
                           in_tz.localize(datetime.combine(
                                   student_attendance.entry_datetime.date(),
                                   time(16, 0, 0)
                           )))
        if td > timezone.timedelta(0, 1):
            time_spent = day_hour_minute_seconds(td)
            student_records.append((student_number, time_spent, td))
    student_records.sort(key=lambda x: x[2], reverse=True)
    first_row = [["Rank", "A"], ["Student Number", "B"],
                 ["Time Spent", "C"]]
    for fr in first_row:
        worksheet.merge_range(fr[1] + '7:' + fr[1] + '9', fr[0],
                              merge_format)
    worksheet.set_column("A:A", 6)
    worksheet.set_column("B:B", 16)
    worksheet.set_column("C:C", 36)
    for i in range(len(student_records)):
        worksheet.write(9 + i, 0, i+1, excel_format)
        worksheet.write(9 + i, 1, student_records[i][0], excel_format)
        worksheet.write(9 + i, 2, student_records[i][1], excel_format)

    workbook.close()
    return workbook


def day_hour_minute_seconds(td):
    """
    converts a timedelta object into day, hour, minutes, second string like
    `1 day 12 hours 3 minutes 23 seconds`
    :param td: timedelta object
    :return: string described above
    """
    days = td.days
    hours = td.seconds//3600
    minutes = (td.seconds//60)%60
    seconds = td.seconds%60
    return "%d day%s %d hour%s %d minute%s %d second%s" % (
        days, "" if days==1 else "s",
        hours, "" if hours==1 else "s",
        minutes, "" if minutes==1 else "s",
        seconds, "" if seconds==1 else "s"
    )