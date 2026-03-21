from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from datetime import datetime, timedelta

import time
import pandas as pd
import numpy as np

def get_info(recordID, data):
    """
    Get name, operation date, JJ sonde removal date
    """
    name = data['Name'][data['RecordID']==int(recordID)].to_list()[0]
    
    gender = data['Gender'][data['RecordID']==int(recordID)].to_list()[0]
    if gender == 'Male':
        genderVN = 'anh'
    if gender == 'Female':
        genderVN = 'chị'
        
    phoneNumber = data['PhoneNumber'][data['RecordID']==int(recordID)].to_list()[0]
    if str(phoneNumber)[0] != '0':
        phoneNumber = '0'+ str(phoneNumber)
    
    opDate = data['OperationDate'][data['RecordID']==int(recordID)].to_list()[0]
        
    opDate_object = datetime.strptime(opDate, '%d/%m/%Y')    
    
    removalTime = data['RemovalTime'][data['RecordID']==int(recordID)].to_list()[0]
    
    calculatedDate = opDate_object + timedelta(days=int(removalTime))
    
    # If the removal date is on the weekend, move it to the next Monday
    if calculatedDate.strftime("%A") == 'Saturday':
        removalDate = calculatedDate + timedelta(days=2)
    elif calculatedDate.strftime("%A") == 'Sunday':
        removalDate = calculatedDate + timedelta(days=1)
    else:
        removalDate = calculatedDate

    Dx = data['Dx'][data['RecordID']==int(recordID)].to_list()[0]

    return name, genderVN, phoneNumber, opDate, removalDate.strftime("%d/%m/%Y"), removalDate.strftime("%A"), Dx

def get_message(name, gender, removalDateStrVN, removalDate, Dx):
    if Dx == 'JJ':
        message = f"Xin chào {name}, xin mời {gender} đến phòng 121 nhà B2 vào {removalDateStrVN}, {removalDate} để được kiểm tra lại và xem xét rút sonde JJ."
    if Dx == 'TLT':
        message = f"Xin chào {name}, xin mời {gender} đến phòng khám số 10, Trung tâm Kĩ thuật cao và Tiêu hóa vào {removalDateStrVN}, {removalDate} để được kiểm tra lại tình trạng sau phẫu thuật."
    return message

def translator (englishDate: str):
    '''
    Convert English date to Vietnamese date
    '''
    if englishDate == 'Monday':
        vietnameseDate = 'Thứ hai'
    if englishDate == 'Tuesday':
        vietnameseDate = 'Thứ ba'
    if englishDate == 'Wednesday':
        vietnameseDate = 'Thứ tư'
    if englishDate == 'Thursday':
        vietnameseDate = 'Thứ năm'
    if englishDate == 'Friday':
        vietnameseDate = 'Thứ sáu'
    if englishDate == 'Saturday':
        vietnameseDate = 'Thứ bảy'
    if englishDate == 'Sunday':
        vietnameseDate = 'Chủ nhật'
    return vietnameseDate
    
def zaloHandler (zaloPath, phoneNumber:str, message:str):
    '''
    Open Zalo app, find the patient's phone number and send a message
    '''
    # Open the Zalo app window
    zaloWin = Application(backend='uia').start(zaloPath).connect(title='Zalo', active_only=True, timeout=100)
    # zaloWin.Zalo.print_control_identifiers()
    
    # Click on the search box
    searchBox = zaloWin.Zalo.child_window(auto_id="contact-search-input", control_type="Edit").wrapper_object()
    searchBox.set_focus()
    
    # Give a short delay to ensure focus
    time.sleep(0.2)
    searchBox.click_input()
    send_keys('^a')
    send_keys("{DELETE}")
    time.sleep(0.2)
    
    # Type in a phone number (e.g., patient's number)
    send_keys(str(phoneNumber), with_spaces=True)
    time.sleep(2)
    send_keys("{ENTER}")
    
    # time.sleep(0.5)
    chatBox = zaloWin.Zalo.child_window(auto_id="richInput", control_type="Group").wrapper_object()
    chatBox.set_focus()
    
    # Give a short delay to ensure focus before sending the message
    time.sleep(0.2)
    chatBox.click_input()
    send_keys('^a')
    send_keys("{DELETE}")
    send_keys(message, with_spaces=True)
    
    # time.sleep(0.2)
    # send_keys("{ENTER}")
    
if __name__ == "__main__":
    
    filePath = r"D:\BS_LeDuyBinh\automation\zaloAuto\JJsonde_reminder.xlsx"
    zaloPath = r"C:\Users\Techsi.vn\AppData\Local\Programs\Zalo\Zalo.exe"
    data = pd.read_excel(filePath, engine=None) 
    validPhoneNumber = True

    for recordID in data['RecordID']:
        name, gender, phoneNumber, opDate, removalDate, removalDateStr, Dx = get_info(recordID, data)
        validPhoneNumber = True
        if len(phoneNumber) != 10:
            validPhoneNumber = False
        if validPhoneNumber:
            removalDateStrVN = translator(removalDateStr)
            
            message = get_message(name, gender, removalDateStrVN, removalDate, Dx)
            zaloHandler(zaloPath, phoneNumber, message)
        else:
            pass
        
