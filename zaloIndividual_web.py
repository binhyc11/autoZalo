import re
from playwright.sync_api import Playwright, sync_playwright, expect

from datetime import datetime, timedelta
from utils import get_info, add_notes, check_date
import pandas as pd
from gen_messages import get_message


def run(playwright: Playwright, filePath: str, exportPath: str) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Load the patient data into a pandas Dataframe and format its cells all as string
    data = pd.read_excel(filePath, engine=None).astype(str)
    recordIDs = [recordID for recordID in data['RecordID']]

    # First, load the Zalo chat page. Wait for the user to login by QR code. If not logged in, move to google.com
    try:
        page.goto("https://chat.zalo.me/")
        print ('QR scanning')
        # Wait for 200s until logged in and the search contact box is visible
        page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=200000)
        print ('Login successfully')
        # Loop through all the record IDs
        for recordID in recordIDs:
            whichDate, Date, DateStrVN = check_date(recordID, data)
            name, gender, age, phoneNumber_1, phoneNumber_2, Dx = get_info(recordID, data)

            if whichDate != None:
                Notes = {'Notes':''}

                # Check whether the phone number is valid
                phoneNumber_1, phoneNumber_2 = phoneNumber_1.replace(' ',''), phoneNumber_2.replace(' ','')
                
                validPhoneNumber_1 = True
                if len(phoneNumber_1) != 10:
                    validPhoneNumber_1 = False
                    if phoneNumber_1!='0':
                        print (f'Số điện thoại {phoneNumber_1} bị sai')
                        Notes['Notes'] += f'Số điện thoại {phoneNumber_1} bị sai; '
                    else:
                        Notes['Notes'] += ''
                        
                validPhoneNumber_2 = True
                if len(phoneNumber_2) != 10:
                    validPhoneNumber_2 = False
                    if phoneNumber_2!='0':
                        print (f'Số điện thoại {phoneNumber_2} bị sai')
                        Notes['Notes'] += f'Số điện thoại {phoneNumber_2} bị sai; '
                    else:
                        Notes['Notes'] += ''

                whichReminderNote, message = get_message(name, gender, age, DateStrVN, Date, Dx, whichMessage=whichDate)

                # If the first phone number is valid, run the main task
                if validPhoneNumber_1:
                    print ('about to click Thêm bạn')
                    page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=3000)     
                    page.locator(".fa.fa-outline-add-new-contact-2").click()
                    page.get_by_role("textbox", name="Vui lòng điền số điện thoại").wait_for(state="visible", timeout=3000)                      
                    page.get_by_role("textbox", name="Vui lòng điền số điện thoại").click()
                    page.get_by_role("textbox", name="Vui lòng điền số điện thoại").fill(phoneNumber_1)
                    page.locator("#zl-modal__dialog-body").get_by_text("Tìm kiếm").wait_for(state="visible", timeout=3000)
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
                                    Notes['Notes'] += f'{phoneNumber_1} không dùng Zalo; '
                                    errorFlag_1=True
                                    page.get_by_text("Hủy", exact=True).wait_for(state="visible", timeout=3000)  
                                    page.get_by_text("Hủy", exact=True).click()
                                    whichReminderNote = {}
                                    pass
                        if not errorFlag_1:
                            print (f'Clicked on Chat box of {recordID}')
                            Notes['Notes'] += f'Đã gửi tin nhắn cho {phoneNumber_1}; '
                            page.locator("#input_line_0").wait_for(state="visible", timeout=3000)
                            page.locator("#input_line_0").click()
                            page.keyboard.press("Control+A")
                            page.keyboard.press("Backspace")
                            page.locator("#input_line_0").fill(message)
                            # page.get_by_title("Gửi", exact=True).click()

                            page.wait_for_timeout(5000)
                    except:
                        pass

                # If the second phone number is valid, run the main task
                if validPhoneNumber_2:
                    print ('about to click Thêm bạn')
                    page.locator(".fa.fa-outline-add-new-contact-2").wait_for(state="visible", timeout=3000)     
                    page.locator(".fa.fa-outline-add-new-contact-2").click()
                    page.get_by_role("textbox", name="Vui lòng điền số điện thoại").wait_for(state="visible", timeout=3000)  
                    page.get_by_role("textbox", name="Vui lòng điền số điện thoại").click()
                    page.get_by_role("textbox", name="Vui lòng điền số điện thoại").fill(phoneNumber_2)
                    page.locator("#zl-modal__dialog-body").get_by_text("Tìm kiếm").wait_for(state="visible", timeout=3000)  
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
                                    Notes['Notes'] += f'{phoneNumber_2} không dùng Zalo; '
                                    errorFlag_2=True
                                    page.get_by_text("Hủy", exact=True).wait_for(state="visible", timeout=3000)  
                                    page.get_by_text("Hủy", exact=True).click()
                                    whichReminderNote = {}
                                    pass

                        if not errorFlag_2:
                            print (f'Clicked on Chat box of {recordID}')
                            Notes['Notes'] += f'Đã gửi tin nhắn cho {phoneNumber_2}; '
                            page.locator("#input_line_0").wait_for(state="visible", timeout=3000)
                            page.locator("#input_line_0").click()
                            page.keyboard.press("Control+A")
                            page.keyboard.press("Backspace")
                            page.locator("#input_line_0").fill(message)
                            # page.get_by_title("Gửi", exact=True).click()

                            page.wait_for_timeout(60000)
                    except:
                        pass

                data = add_notes(data, recordID, Notes)
                data = add_notes(data, recordID, whichReminderNote)
        data.to_excel(filePath, index = False)
    except:
        page.wait_for_timeout(6000)


with sync_playwright() as playwright:
    filePath =  "./JJsonde_reminder.xlsx"
    exportPath =  "./reminder_messages.xlsx"
    run(playwright, filePath, exportPath)
