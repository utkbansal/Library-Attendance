import xlsxwriter
from django.utils import timezone

from attendance.models import Attendance


def report(year, month, output=None):
    # for headders
    date_now = timezone.datetime(year, month, 1)
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    format = workbook.add_format()
    format.set_align('center')
    format.set_align('vcenter')

    merge_format = workbook.add_format({
        'bold': True,
        'border': 0,
        'align': 'center',
        'valign': 'vcenter',

    })

    worksheet.merge_range('A1:J6',
                          'AJAY KUMAR GARG ENGINEERING COLLEGE, GHAZIABAD \n' +
                          'CENTRAL LIBRARY \n ' +
                          'LIBRARY VISITORS REPORT: ' + date_now.strftime(
                              "%B %Y"), merge_format)

    fst_col = [['S.NO.', 'A'],
               ['DATE', 'B'],
               ["DAY'S", 'C'],
               ['8:30AM \n TO \n 4:00PM', 'D'],
               ['4:00PM \nTO \n 7:00PM', 'E'],
               ['7:00PM \n TO \n 9:00PM', 'F'],
               ['9:00PM \n TO \n 12 MIDNIGHT', 'G'],
               ['TOTAL \n 4:00PM \n TO \n 12 MIDNIGHT', 'H'],
               ['TOTAL \n 8:30AM \n TO \n 12 MIDNIGHT', 'I'],
               ['REMARKS', 'J']
               ]
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:B', 18)

    for heading, x in fst_col:
        worksheet.merge_range(x + '8' + ':' + x + '11' + '', heading,
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
    for day in days:
        time_start = timezone.datetime(year, month, day)
        time_end = timezone.datetime(year, month, day, 23, 59, 59)
        attds = Attendance.objects.filter(entry_time__gt=time_start,
                                          entry_time__lt=time_end).all()
        time_start_slot_1 = timezone.datetime(year, month, day, 8, 30, 0)
        time_end_slot_1 = timezone.datetime(year, month, day, 15, 59, 59)
        time_start_slot_2 = timezone.datetime(year, month, day, 16, 0, 0)
        time_end_slot_2 = timezone.datetime(year, month, day, 18, 59, 59)
        time_start_slot_3 = timezone.datetime(year, month, day, 19, 0, 0)
        time_end_slot_3 = timezone.datetime(year, month, day, 20, 59, 59)
        time_start_slot_4 = timezone.datetime(year, month, day, 21, 0, 0)
        time_end_slot_4 = timezone.datetime(year, month, day, 23, 59, 59)
        attds_slot_1 = Attendance.objects.filter(
            entry_time__gt=time_start_slot_1,
            entry_time__lt=time_end_slot_1).all()
        attds_slot_2 = Attendance.objects.filter(
            entry_time__gt=time_start_slot_2,
            entry_time__lt=time_end_slot_2).all()
        attds_slot_3 = Attendance.objects.filter(
            entry_time__gt=time_start_slot_3,
            entry_time__lt=time_end_slot_3).all()
        attds_slot_4 = Attendance.objects.filter(
            entry_time__gt=time_start_slot_4,
            entry_time__lt=time_end_slot_4).all()
        attds_slot_1_count = attds_slot_1.count()
        attds_slot_2_count = attds_slot_2.count()
        attds_slot_3_count = attds_slot_3.count()
        attds_slot_4_count = attds_slot_4.count()
        attds_slot_5_count = attds_slot_2_count + attds_slot_3_count + attds_slot_4_count
        attds_slot_6_count = attds_slot_5_count + attds_slot_1_count

        worksheet.write(10 + day, 0, day, format)
        worksheet.write(10 + day, 1, time_start.strftime("%d, %B %Y"), format)
        worksheet.write(10 + day, 2, time_start.strftime('%A'), format)

        # list for all the slots
        ls = [attds_slot_1_count, attds_slot_2_count, attds_slot_3_count,
              attds_slot_4_count,
              attds_slot_5_count, attds_slot_6_count
              ]
        for j in range(3, 9):
            if ls[-1] == 0:
                worksheet.write(10 + day, j, 'Holiday', format)
            elif ls[j - 3] == 0:
                worksheet.write(10 + day, j, 'Closed', format)
            else:
                worksheet.write(10 + day, j, ls[j - 3], format)

    workbook.close()
    return workbook
