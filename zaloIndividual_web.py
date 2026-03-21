import re
from playwright.sync_api import Playwright, sync_playwright, expect

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

def run(playwright: Playwright, recordIDs:list) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()


    # First, load the Zalo chat page. Wait for the user to login by QR code. If not logged in, move to google.com
    try:
        page.goto("https://chat.zalo.me/")
        print ('QR scanning')
        # Wait for 200s until logged in and the search contact box is visible
        page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=200000)
        print ('Login successfully')

        # Loop through all the record IDs
        for recordID in recordIDs:
            name, gender, phoneNumber, opDate, removalDate, removalDateStr, Dx = get_info(recordID, data)
            # Check whether the phone number is valid
            phoneNumber= phoneNumber.replace(' ','')
            validPhoneNumber = True
            if len(phoneNumber) != 10:
                validPhoneNumber = False

            # If the phone number is valid, run the main task
            if validPhoneNumber:
                removalDateStrVN = translator(removalDateStr)
                message = get_message(name, gender, removalDateStrVN, removalDate, Dx)

                page.get_by_title("Thêm bạn").click()
                page.get_by_role("textbox", name="Vui lòng điền số điện thoại").click()
                page.get_by_role("textbox", name="Vui lòng điền số điện thoại").fill(phoneNumber)
                page.locator("#zl-modal__dialog-body").get_by_text("Tìm kiếm").click()
                
                try:
                    # page.pause()
                    page.get_by_text("Nhắn tin", exact=True).wait_for(state="visible", timeout=5000)
                    page.get_by_text("Nhắn tin", exact=True).click()
                    print ('Clicked on Chat box')
                    page.locator("#input_line_0").fill(message)
                    # Pauses for 5 seconds (5000 milliseconds)
                    page.wait_for_timeout(5000)
                except:
                    print (f'{recordID} không dùng Zalo')
                    page.get_by_text("Hủy", exact=True).click()
                    pass

                

            if not validPhoneNumber:
                print (f'{recordID} bị sai số điện thoại')

        # context.close()
        # browser.close()
    except:
        page.goto("https://google.com")
        page.wait_for_timeout(500000)



with sync_playwright() as playwright:
    filePath = r"D:\BS_LeDuyBinh\automation\zaloAuto\JJsonde_reminder.xlsx"
    data = pd.read_excel(filePath, engine=None)
    recordIDs = [recordID for recordID in data['RecordID']]
    run(playwright, recordIDs)
