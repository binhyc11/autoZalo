from datetime import datetime, timedelta

import time
import pandas as pd
import numpy as np
from utils import get_info, translator, is_today, calculate_dates, convert_dates, create_message
from gen_messages import get_message

filePath = "./JJsonde_reminder.xlsx"
data = pd.read_excel(filePath, engine=None)
data = data.astype(str)

def add_notes (df, recordID, note: dict):
    """
    Add notes to the dataframe.
    df: Pandas dataframe
    recordID: recordID whose the note should be added
    note: Dictionary contains keys as df column names and values as the content to be added
    --> return: updated df
    """
    for key, value in note.items():
        df.loc[df['RecordID'] == str(recordID), key] = value
    return df

# print (add_notes(data, 2511041725, {'Notes': 'Đã gửi tin nhắn; '}))

def calculate_dates(dischargeDate: str, TimeToReVisit:str):
    """
    Calculate reminder dates: 1 day after discharge day, 3 days and 1 day prior to the revisit day.
    """
    dischargeDate_object = datetime.strptime(dischargeDate, '%d/%m/%Y')
    
    firstReminderDate_object = dischargeDate_object + timedelta(days=1)
    reVisitDate_object = dischargeDate_object + timedelta(days=int(TimeToReVisit))
    secondReminderDate_object = reVisitDate_object + timedelta(days=-3)
    thirdReminderDate_object = reVisitDate_object + timedelta(days=-1)

    return firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object

print (calculate_dates('22/03/2026', '7'))
firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object = calculate_dates('22/03/2026', '7')
name, gender, Dx = 'a', 'anh', 'TLT'

def create_message (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, name, gender, Dx):
    """
    Get message for each visit
    """
    if is_today(firstReminderDate_object):
        Date, DateStrVN = convert_dates(firstReminderDate_object)
        note = {'FirstReminderDate': 'Đã gửi'}
        return note, get_message(name, gender, DateStrVN, Date, Dx, whichMessage = 'first')
    elif is_today(secondReminderDate_object):
        Date, DateStrVN = convert_dates(secondReminderDate_object)
        note = {'SecondReminderDate': 'Đã gửi'}
        return note, get_message(name, gender, DateStrVN, Date, Dx, whichMessage = 'second')
    elif is_today(thirdReminderDate_object):
        Date, DateStrVN = convert_dates(thirdReminderDate_object)
        note = {'ThirdReminderDate': 'Đã gửi'}
        return note, get_message(name, gender, DateStrVN, Date, Dx, whichMessage = 'third')
    else:
        note={}
        return note, None

print (create_message(firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, name, gender, Dx))