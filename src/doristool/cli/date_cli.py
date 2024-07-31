import click
from datetime import datetime,timedelta
import chinese_calendar as calendar
from lunarcalendar import Converter,Solar,Lunar
import csv

def transform_holiday(name):
    if name=="New Year's Day":
        return 0
    elif name == "Spring Festival":
        return 1
    elif name == "Tomb-sweeping Day":
        return 2
    elif name == "Labour Day":
        return 3
    elif name == "Dragon Boat Festival":
        return 4
    elif name == "Mid-autumn Festival":
        return 5
    elif name == "National Day":
        return 7
    elif name == "Anti-Fascist 70th Day":
        return 8
    else:
        raise ValueError("未知的节日:"+ str(name))

#生成日期列表
def generate_date_list(start_date: datetime, end_date: datetime):
    calendar_support_max_date = datetime.strptime('2024-12-31','%Y-%m-%d')
    one_day = timedelta(days=1)

    date_list=[]

    while start_date < end_date:
        # 日期
        date_f=start_date.strftime('%Y-%m-%d')
        # 农历
        lunar: Lunar = Converter().Solar2Lunar(Solar.from_date(start_date))
        lunar_f="{}{}{}".format(lunar.year,str(lunar.month).zfill(2),str(lunar.day).zfill(2))
        # 节日
        holiday = None
        is_work_day = None
        if start_date <=calendar_support_max_date:
            on_holiday, holiday_name = calendar.get_holiday_detail(start_date)
            if holiday_name is not None:
                holiday = transform_holiday(holiday_name)
            if calendar.is_workday(start_date):
                is_work_day = 1
            else:
                is_work_day = 0

        date_list.append([date_f,holiday,lunar_f,is_work_day])

        start_date = start_date + one_day
    
    return date_list

def to_file(date_list,file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(date_list)
    

@click.command(name="generate",help="批量生成日期")
@click.option('--start',required=True, help='起始日期')
@click.option('--end',required=True, help='结束日期')
def generate(start, end):
    start_date = datetime.strptime(start,'%Y-%m-%d')
    end_date = datetime.strptime(end,'%Y-%m-%d')

    date_list=generate_date_list(start_date,end_date)

    to_file(date_list,'/home/wangzhen/workspace/data-tool/data/dates.csv')

