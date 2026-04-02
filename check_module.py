from datetime import datetime, timedelta, date
from utils import calculate_dates, convert_dates
import time
import pandas as pd
import numpy as np
filePath = "./JJsonde_reminder.xlsx"
data = pd.read_excel(filePath, engine=None)
data = data.astype(str)
    
recordIDs = [recordID for recordID in data['RecordID']]

def check_date(recordID, data):
    """
    Check whether today is the day for reminder. If yes, create a date and weekday as string.
    """
    dischargeDate = data['DischargeDate'][data['RecordID']==recordID].to_list()[0]
    timeToReVisit = data['TimeToReVisit'][data['RecordID']==recordID].to_list()[0]

    firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object = calculate_dates(dischargeDate, timeToReVisit)
    if is_today(firstReminderDate_object):
        Date, DateStrVN = convert_dates(firstReminderDate_object)
        whichDate = 'first'
    elif is_today(secondReminderDate_object):
        Date, DateStrVN = convert_dates(secondReminderDate_object)
        whichDate = 'second'
    elif is_today(thirdReminderDate_object):
        Date, DateStrVN = convert_dates(thirdReminderDate_object)
        whichDate = 'third'
    else:
        whichDate, Date, DateStrVN = None, None, None
    print (whichDate)
    return whichDate, Date, DateStrVN


def is_today(dateTimeObject):
    """
    Check if a given datetime or date object is today.
    """
    if not isinstance(dateTimeObject, (datetime, date)):
        raise TypeError("Input must be a datetime or date object.")
    
    today = date.today()
    # If dateTimeObject is datetime, compare only the date part
    return dateTimeObject.date() == today if isinstance(dateTimeObject, datetime) else dateTimeObject == today
pronoun, name = 'a', 'b'
goodbye = f"\n\nLưu ý: Đây là tin nhắn nhắc hẹn khám được tự động gửi theo số điện thoại đã đăng kí. Nếu Anh/Chị là người nhà, kính nhờ Anh/Chị chuyển lời đến {pronoun} {name}.\
            \nMọi câu hỏi Anh/Chị có thể hỏi tại đây hoặc liên hệ đến Hotline của khoa 02437331502.\
            \n\nXin cảm ơn!"
message = f"Xin chào {pronoun} {name},\
            \nXin được nhắc {pronoun} có hẹn đánh giá sau quá trình điều trị vào tại phòng khám số 10, Trung tâm Kĩ thuật cao và Tiêu hóa.\
            \nNếu {pronoun} đã đến, xin bỏ qua tin nhắn này.\
            {goodbye}"
print (message)