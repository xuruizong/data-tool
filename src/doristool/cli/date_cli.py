import click
from datetime import datetime,timedelta
import chinese_calendar as calendar
from lunarcalendar import Converter,Solar,Lunar
import csv


@click.command(name="generate",help="批量生成日期")
@click.option('--start',required=True, help='起始日期')
@click.option('--end',required=True, help='结束日期')
def generate(start, end):
    start_date = datetime.strptime(start,'%Y-%m-%d')
    one_day = timedelta(days=1)
    end_date = datetime.strptime(end,'%Y-%m-%d')

    date_list=[]

    while start_date < end_date:
        lunar: Lunar = Converter().Solar2Lunar(Solar.from_date(start_date))
        on_holiday, holiday_name = calendar.get_holiday_detail(start_date)
        start_date = start_date + one_day

        date_f=start_date.strftime('%Y-%m-%d')
        lunar_f="{}{}{}".format(lunar.year,lunar.month,lunar.day)

        date_list.append([date_f,holiday_name,lunar_f,calendar.is_workday(start_date)])
    
    print(date_list)

    with open('/home/wangzhen/workspace/data-tool/data/dates.csv', 'w', newline='') as file:
        header = ['date', 'festal_day', 'lunar_day','is_workday']
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(date_list)

