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
        
    phoneNumber_1 = str(data['PhoneNumber_1'][data['RecordID']==int(recordID)].to_list()[0])
    phoneNumber_2 = str(data['PhoneNumber_2'][data['RecordID']==int(recordID)].to_list()[0])

    if str(phoneNumber_1)[0] != '0':
        phoneNumber_1 = '0'+ str(phoneNumber_1)
    if str(phoneNumber_2)[0] != '0':
        phoneNumber_2 = '0'+ str(phoneNumber_2)
        
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

    return name, genderVN, phoneNumber_1, phoneNumber_2, opDate, removalDate.strftime("%d/%m/%Y"), removalDate.strftime("%A"), Dx

def get_message(name, gender, removalDateStrVN, removalDate, Dx):
    if Dx == 'JJ':
        message = f"Xin chào {name}, xin mời {gender} đến phòng 121 nhà B2 vào {removalDateStrVN}, {removalDate} để được kiểm tra lại và xem xét rút sonde JJ."
    elif Dx == 'TLT':
        message = f"Xin chào {name}, xin mời {gender} đến phòng khám số 10, Trung tâm Kĩ thuật cao và Tiêu hóa vào {removalDateStrVN}, {removalDate} để được kiểm tra lại tình trạng sau phẫu thuật."
    elif  Dx == 'Other':
        message = f"Xin chào {name}, xin mời {gender} đến phòng 121 nhà B2 vào {removalDateStrVN}, {removalDate} để được khám lại và đánh giá sau quá trình điều trị."
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

def run(playwright: Playwright, filePath: str, exportPath: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    data = pd.read_excel(filePath, engine=None)
    recordIDs = [recordID for recordID in data['RecordID']]

    Notes = []
    # First, load the Zalo chat page. Wait for the user to login by QR code. If not logged in, move to google.com
    try:
        page.goto("https://chat.zalo.me/")
        print ('QR scanning')
        # Wait for 200s until logged in and the search contact box is visible
        page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=200000)
        print ('Login successfully')
        # Loop through all the record IDs
        for recordID in recordIDs:
            note = []
            name, gender, phoneNumber_1, phoneNumber_2, opDate, removalDate, removalDateStr, Dx = get_info(recordID, data)
            # Check whether the phone number is valid
            phoneNumber_1, phoneNumber_2 = phoneNumber_1.replace(' ',''), phoneNumber_2.replace(' ','')
            validPhoneNumber_1 = True
            if len(phoneNumber_1) != 10:
                validPhoneNumber_1 = False

            validPhoneNumber_2 = True
            if len(phoneNumber_2) != 10:
                validPhoneNumber_2 = False

            print (phoneNumber_1, phoneNumber_2)
            print (validPhoneNumber_1, validPhoneNumber_2)

            removalDateStrVN = translator(removalDateStr)
            message = get_message(name, gender, removalDateStrVN, removalDate, Dx)

            # If the first phone number is valid, run the main task
            if validPhoneNumber_1:
                print ('about to click Thêm bạn')
                page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=3000)     
                page.locator(".fa.fa-outline-add-new-contact-2").click()
                page.get_by_role("textbox", name="Vui lòng điền số điện thoại").click()
                page.get_by_role("textbox", name="Vui lòng điền số điện thoại").fill(phoneNumber_1)
                page.locator("#zl-modal__dialog-body").get_by_text("Tìm kiếm").click()
                
                try:
                    errorFlag_1=False
                    try:
                        page.get_by_text("Nhắn tin", exact=True).wait_for(state="visible", timeout=3000)
                        page.get_by_text("Nhắn tin", exact=True).click()
                    except:
                        try:
                            page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).first.wait_for(state="visible", timeout=3000)
                            page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).first.click()
                        except:
                            try:
                                page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).nth(1).wait_for(state="visible", timeout=3000)
                                page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).nth(1).click()
                            except:
                                print (f'{phoneNumber_1} không dùng Zalo')
                                note.append (f'{phoneNumber_1} không dùng Zalo')
                                errorFlag_1=True
                                page.get_by_text("Hủy", exact=True).click()
                                pass
                    if not errorFlag_1:
                        print (f'Clicked on Chat box of {recordID}')
                        note.append ('Đã gửi tin nhắn')
                        page.locator("#input_line_0").click()
                        page.keyboard.press("Control+A")
                        page.keyboard.press("Backspace")
                        page.locator("#input_line_0").fill(message)
                        # page.get_by_title("Gửi", exact=True).click()

                        page.wait_for_timeout(5000)
                except:
                    pass
            if not validPhoneNumber_1 and len(phoneNumber_1)>5:
                print (f'{phoneNumber_1} bị sai số điện thoại')
                note.append (f'{phoneNumber_1} bị sai số điện thoại')


        # If the second phone number is valid, run the main task
            if validPhoneNumber_2:
                print ('about to click Thêm bạn')
                page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=3000)     
                page.locator(".fa.fa-outline-add-new-contact-2").click()
                page.get_by_role("textbox", name="Vui lòng điền số điện thoại").click()
                page.get_by_role("textbox", name="Vui lòng điền số điện thoại").fill(phoneNumber_2)
                page.locator("#zl-modal__dialog-body").get_by_text("Tìm kiếm").click()
                
                try:
                    errorFlag_2=False
                    try:
                        page.get_by_text("Nhắn tin", exact=True).wait_for(state="visible", timeout=3000)
                        page.get_by_text("Nhắn tin", exact=True).click()
                    except:
                        try:
                            page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).first.wait_for(state="visible", timeout=3000)
                            page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).first.click()
                        except:
                            try:
                                page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).nth(1).wait_for(state="visible", timeout=3000)
                                page.locator("div").filter(has_text=re.compile(r"^Nhắn tin$")).nth(1).click()
                            except:
                                print (f'{phoneNumber_2} không dùng Zalo')
                                note.append (f'{phoneNumber_2} không dùng Zalo')
                                errorFlag_2=True
                                page.get_by_text("Hủy", exact=True).click()
                                pass
                    if not errorFlag_2:
                        print (f'Clicked on Chat box of {recordID}')
                        note.append ('Đã gửi tin nhắn')
                        page.locator("#input_line_0").click()
                        page.keyboard.press("Control+A")
                        page.keyboard.press("Backspace")
                        page.locator("#input_line_0").fill(message)
                        # page.get_by_title("Gửi", exact=True).click()

                        page.wait_for_timeout(5000)
                except:
                    pass
            if not validPhoneNumber_2 and len(phoneNumber_2)>5:
                print (f'{phoneNumber_2} bị sai số điện thoại')
                note.append (f'{phoneNumber_2} bị sai số điện thoại')
            Notes.append(note)

        data['Notes']=Notes
        data.to_excel(exportPath, index = False)
    except:
        page.wait_for_timeout(6000)


with sync_playwright() as playwright:
    root = r"D:\BS_LeDuyBinh\automation\zaloAuto\\"
    filePath = root + "JJsonde_reminder.xlsx"
    exportPath = root + "reminder_messages.xlsx"
    run(playwright, filePath, exportPath)
