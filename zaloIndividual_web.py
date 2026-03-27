import re
from playwright.sync_api import Playwright, sync_playwright, expect

from datetime import datetime, timedelta
from utils import get_info, translator, is_today, calculate_dates, convert_dates, create_message
import time
import pandas as pd
import numpy as np


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
            name, gender, phoneNumber_1, phoneNumber_2, dischargeDate, timeToReVisit, Dx = get_info(recordID, data)
            firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object = calculate_dates(dischargeDate, timeToReVisit)
            message = create_message (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, name, gender, Dx)
            ptDict = data[data['RecordID'] == int(recordID)].to_dict()
            note = []
            if message != None:
                # Check whether the phone number is valid
                phoneNumber_1, phoneNumber_2 = phoneNumber_1.replace(' ',''), phoneNumber_2.replace(' ','')
                validPhoneNumber_1 = True
                if len(phoneNumber_1) != 10:
                    validPhoneNumber_1 = False

                validPhoneNumber_2 = True
                if len(phoneNumber_2) != 10:
                    validPhoneNumber_2 = False

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
