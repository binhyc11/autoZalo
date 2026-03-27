from datetime import datetime, timedelta

import time
import pandas as pd
import numpy as np
from utils import get_info, translator, is_today, calculate_dates, convert_dates, create_message

root = r"D:\BS_LeDuyBinh\automation\zaloAuto\\"
filePath = root + "JJsonde_reminder.xlsx"
data = pd.read_excel(filePath, engine=None)
recordIDs = [recordID for recordID in data['RecordID']]
for recordID in recordIDs:
    name, gender, phoneNumber_1, phoneNumber_2, dischargeDate, timeToReVisit, Dx = get_info(recordID, data)
    print (name, gender, phoneNumber_1, phoneNumber_2, dischargeDate, timeToReVisit, Dx)

    firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object = calculate_dates(dischargeDate, timeToReVisit)
    print (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object)
    print ('about to create message')
    message = create_message (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, name, gender, Dx)
    print (message)