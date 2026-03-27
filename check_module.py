from datetime import datetime, timedelta

import time
import pandas as pd
import numpy as np
from utils import get_info, translator, is_today, calculate_dates, convert_dates, create_message

root = r"D:\BS_LeDuyBinh\automation\zaloAuto\\"
filePath = root + "JJsonde_reminder.xlsx"
data = pd.read_excel(filePath, engine=None)
# print (data)

recordIDs = [recordID for recordID in data['RecordID']]
# for recordID in recordIDs:
#     name, gender, phoneNumber_1, phoneNumber_2, dischargeDate, timeToReVisit, Dx = get_info(recordID, data)
#     print (name, gender, phoneNumber_1, phoneNumber_2, dischargeDate, timeToReVisit, Dx)

#     firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object = calculate_dates(dischargeDate, timeToReVisit)
#     print (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object)
#     print ('about to create message')
#     message = create_message (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, name, gender, Dx)
#     print (message)

new_row = pd.DataFrame({'PatientID': ['Bob'],
                        'RecordID': [30],
                        'Name': [5],
                        'Gender': ['m'],
                        'Age': ['a'],
                        
                        
                        })

df = []
print (df)
for recordID in recordIDs:
    ptDict = data[data['RecordID'] == recordID].to_dict()
    print (ptDict)
    for k, v in ptDict.items():
        print (k,v)
        ptOrder = [key for key in v.keys()][0]
        theValue = ptDict[k][ptOrder]
        ptDict[k]= theValue
    ptDict['FirstReminderDate']= 'Đã gửi'
    # Add the new row
    df.append(ptDict)
print (pd.DataFrame(df))