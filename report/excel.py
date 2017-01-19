import os
import calendar
import xlsxwriter

from django.utils import timezone
from datetime import time, datetime, timedelta
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
            entry_datetime__lte=time_end_slot_1).count()
        attds_slot_2 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_2,
            entry_datetime__lte=time_end_slot_2).count()
        attds_slot_3 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_3,
            entry_datetime__lte=time_end_slot_3).count()
        attds_slot_4 = Attendance.objects.filter(
            entry_datetime__gte=time_start_slot_4,
            entry_datetime__lte=time_end_slot_4).count()
        attds_slot_5 = attds_slot_2 + attds_slot_3 + attds_slot_4
        attds_slot_6 = attds_slot_5 + attds_slot_1
        attds_slot_counts = list()
        attds_slot_counts.append(attds_slot_1)
        attds_slot_counts.append(attds_slot_2)
        attds_slot_counts.append(attds_slot_3)
        attds_slot_counts.append(attds_slot_4)
        attds_slot_counts.append(attds_slot_5)
        attds_slot_counts.append(attds_slot_6)

        # update total count for each slot
        for i in range(len(attds_slot_counts)):
            attds_slots_total[i] += attds_slot_counts[i]

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
    day += 1
    if num_working_days:
        for i in range(len(attds_slots_avg)):
            attds_slots_avg[i] = float(attds_slots_total[i]) / num_working_days
    worksheet.merge_range(10 + day, 0, 10 + day + 1, 2,
                          "Average", merge_format)

    for i in range(3, len(attds_slots_avg) + 3):

        worksheet.merge_range(
            10 + day, i, 10 + day + 1, i,
            "%d / %d %s= %.2f" %
            (attds_slots_total[i-3], num_working_days, sep, attds_slots_avg[i-3])
            if attds_slots_total[i-3] else "-", merge_format
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
    if not output:
        workbook = xlsxwriter.Workbook('true_reader.xlsx')
    else:
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
    worksheet.merge_range('A1:D6',
                          "AKGEC Library: True Reader Excel for %s" %
                          date_start.strftime("%B %Y"), merge_format)
    all_attendance = Attendance.objects.filter(
            entry_datetime__gte=date_start, entry_datetime__lte=date_end,
            exit_datetime__isnull=False)
    student_numbers = [stud_num[0] for stud_num in
                       all_attendance.order_by().values_list(
                               'student_number').distinct().all()]
    # print(student_numbers)
    student_records = list()
    in_tz = tz('Asia/Kolkata')  # Indian time for localizing datetime object
    for student_number in student_numbers:
        td = timezone.timedelta()  # for storing total time spent by the student
        student_attendances = all_attendance.filter(
                student_number=student_number,
                exit_time__gte=time(10, 30, 0),
                exit_time__lte=time(18, 30, 0)
        ).all()
        date_set = set()
        for student_attendance in student_attendances:
            if student_attendance.exit_time >= time(10, 30, 0):
                date_set.add(student_attendance.exit_datetime.date())
                if student_attendance.entry_time >= time(16, 0, 0):
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
            student_records.append((student_number, time_spent, td,
                                    len(date_set)))
    student_records.sort(key=lambda x: x[2], reverse=True)
    first_row = [["Rank", "A"], ["Student Number", "B"],
                 ["Time Spent", "C"], ["Number of Days", "D"]]
    for fr in first_row:
        worksheet.merge_range(fr[1] + '7:' + fr[1] + '9', fr[0],
                              merge_format)
    worksheet.set_column("A:A", 6)
    worksheet.set_column("B:B", 16)
    worksheet.set_column("C:C", 36)
    worksheet.set_column("D:D", 16)
    for i in range(len(student_records)):
        worksheet.write(9 + i, 0, i+1, excel_format)
        worksheet.write(9 + i, 1, student_records[i][0], excel_format)
        worksheet.write(9 + i, 2, student_records[i][1], excel_format)
        worksheet.write(9 + i, 3, student_records[i][3], excel_format)

    workbook.close()
    return student_records

def true_reader_details(month, year, output=None):
    """
    This function takes month and year as arguments and returns a workbook
    with details of first three true readers of the month.
    Requires:
    1 <= month <= 12
    2016 <= year
    :return: Workbook object with details of students coming to the library
    """
    true_readers = true_reader(month, year)[:3]

    workbook1 = xlsxwriter.Workbook(output)
    cell_format = workbook1.add_format()
    cell_format.set_align('center')
    cell_format.set_align('vcenter')
    heading_format = workbook1.add_format({
        'bold': True,
        'border': 0,
        'align': 'center',
        'valign': 'vcenter',
    })

    date_start = timezone.datetime(year, month, 1)  # first day of the month
    last_day = calendar.monthrange(year, month)[1]  # gets the last day of month
    date_end = timezone.datetime(year, month,
                                 last_day, 23, 59, 59)  # last day of the month

    worksheet = workbook1.add_worksheet()
    # setting appropriate column widths
    worksheet.set_column('A:A', 9)
    worksheet.set_column('B:B', 11)
    worksheet.set_column('C:C', 14)
    worksheet.set_column('D:D', 14)
    worksheet.set_column('E:E', 14)
    worksheet.set_column('F:F', 35)
    worksheet.merge_range(
        'A1:F6',
        'True Reader Details for ' + date_start.strftime('%B - %Y'),
        heading_format)
    row, column = 6, 0
    worksheet.write(row, column, "Serial No.", heading_format)
    worksheet.write(row, column+1, "Student No.", heading_format)
    worksheet.write(row, column+2, "Date", heading_format)
    worksheet.write(row, column+3, "Entry Time", heading_format)
    worksheet.write(row, column+4, "Exit Time", heading_format)
    worksheet.write(row, column+5, "Duration", heading_format)
    row += 1
    i = 1  # serial number for excel
    for reader in true_readers:
        student_number = reader[0]
        student_all_attendance = Attendance.objects.filter(student_number=student_number,
                                                           entry_datetime__gte=date_start,
                                                           exit_datetime__lte=date_end,
                                                           )
        # filtering the entries after 4 p.m IST
        student_all_attendance = student_all_attendance.filter(
            exit_time__gte=time(10, 30, 0),
            exit_time__lte=time(18, 30, 0)
        )

        reader_entries = len(student_all_attendance)
        if reader_entries == 1:
            worksheet.write(row, column, i, cell_format)
            worksheet.write(row, column + 1, student_number, cell_format)
        else:
            worksheet.merge_range(row, column,
                                  row + reader_entries - 1, column,
                                  i, cell_format)
            worksheet.merge_range(row, column + 1,
                                  row + reader_entries - 1, column + 1,
                                  student_number, cell_format)
        td_ist = timedelta(hours=5, minutes=30)  # time delta for UTC to IST conversion
        reader_total_td = timedelta(0)  # total time delta of reader
        in_tz = tz('Asia/Kolkata')
        for j in range(reader_entries):
            attendance = student_all_attendance[j]
            date_str = attendance.entry_datetime.strftime('%d-%m-%y(%a)')
            time_entry = (attendance.entry_datetime + td_ist).strftime("%I:%M:%S %p")
            time_exit = (attendance.exit_datetime + td_ist).strftime("%I:%M:%S %p")
            # time delta of current session
            if attendance.entry_time >= time(16, 0, 0):
                reader_td = attendance.exit_datetime - attendance.entry_datetime
            else:
                reader_td = attendance.exit_datetime - in_tz.localize(
                    datetime.combine(attendance.entry_datetime.date(), time(16, 0, 0))
                )
            reader_total_td += reader_td
            timespent = day_hour_minute_seconds(reader_td)
            worksheet.write(row+j, column + 2, date_str, cell_format)
            worksheet.write(row+j, column + 3, time_entry, cell_format)
            worksheet.write(row+j, column + 4, time_exit, cell_format)
            worksheet.write(row+j, column + 5, timespent, cell_format)
        row += (j+1)
        i += 1
        worksheet.merge_range(row, column, row, column + 4, 'Total time spent', heading_format)
        total_timespent = day_hour_minute_seconds(reader_total_td)
        worksheet.write(row, column + 5, total_timespent, cell_format)
        row += 1
    workbook1.close()




def day_hour_minute_seconds(td):
    """
    converts a timedelta object into day, hour, minutes, second string like
    `1 day 12 hours 3 minutes 23 seconds`
    :param td: timedelta object
    :return: string described above
    """
    days = td.days
    if days:
        day_str = "{} day{}, ".format(days, "" if days == 1 else "s")
    else:
        day_str = ""

    hours = td.seconds//3600
    if hours:
        hour_str = "{} hour{}, ".format(hours, "" if hours == 1 else "s")
    else:
        hour_str = ""

    minutes = (td.seconds//60) % 60
    if minutes:
        minute_str = "{} minute{}, ".format(minutes, "" if minutes == 1 else "s")
    else:
        minute_str = ""

    seconds = td.seconds % 60
    if seconds:
        seconds_str = "{} second{}".format(seconds, "" if seconds == 1 else "s")
    else:
        seconds_str = ""

    return day_str + hour_str + minute_str + seconds_str