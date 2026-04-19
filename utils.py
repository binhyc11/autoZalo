from datetime import datetime, timedelta, date
from gen_messages import get_message

def check_date(recordID, data):
    """
    Check whether today is the day for reminder. If yes, create a date and weekday as string.
    """
    dischargeDate = data['DischargeDate'][data['RecordID']==recordID].to_list()[0].strip()
    timeToReVisit = data['TimeToReVisit'][data['RecordID']==recordID].to_list()[0].strip()
    if timeToReVisit == '0':
        whichDate, Date, DateStrVN = None, None, None
    else:
        firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, reVisitDate_object = calculate_dates(dischargeDate, timeToReVisit)

        Date, DateStrVN = convert_dates(reVisitDate_object)

        if is_today(convert_first_reminder_dates(firstReminderDate_object)):
            whichDate = 'first'
        # elif is_today(convert_first_reminder_dates(secondReminderDate_object)):
        #     whichDate = 'second'
        # If the third reminder is on Sunday (it means the revisit date is on Monday) --> Then move the third reminder to Friday
        elif is_today(convert_third_reminder_dates(thirdReminderDate_object)):
            if convert_third_reminder_dates(thirdReminderDate_object).strftime("%A") == 'Friday':
                whichDate = 'third_Friday'
            else:
                whichDate = 'third'
        else:
            whichDate, Date, DateStrVN = None, None, None
    return whichDate, Date, DateStrVN

def get_info(recordID: str, data):
    """
    Get name, operation date, JJ sonde removal date
    """
    name = data['Name'][data['RecordID']==recordID].to_list()[0].strip()
    age = data['Age'][data['RecordID']==recordID].to_list()[0].strip()
    gender = data['Gender'][data['RecordID']==recordID].to_list()[0].strip()
    site = data['SiteToReVisit'][data['RecordID']==recordID].to_list()[0].strip()
    phoneNumber_1 = str(data['PhoneNumber_1'][data['RecordID']==recordID].to_list()[0]).strip()
    phoneNumber_2 = str(data['PhoneNumber_2'][data['RecordID']==recordID].to_list()[0]).strip()

    if site == '10':
        siteToReVisit = 'phòng khám số 10, Trung tâm Kĩ thuật cao và Tiêu hóa'
    elif site == '121':
        siteToReVisit = 'phòng 121 nhà B2'
    else:
        siteToReVisit = 'Không cần khám lại'

    if str(phoneNumber_1)[0] != '0':
        phoneNumber_1 = '0'+ str(phoneNumber_1)
    if str(phoneNumber_2)[0] != '0':
        phoneNumber_2 = '0'+ str(phoneNumber_2)

    JJ = data['JJ'][data['RecordID']==recordID].to_list()[0]

    return name, gender, age, phoneNumber_1, phoneNumber_2, JJ, siteToReVisit

def convert_dates (dateObjects):
    """
    Convert datetime objects to date and string format.
    """
    if dateObjects.strftime("%A") == 'Saturday':
        convertedDate_object = dateObjects + timedelta(days=2)
    elif dateObjects.strftime("%A") == 'Sunday':
        convertedDate_object = dateObjects + timedelta(days=1)
    else:
        convertedDate_object = dateObjects
    return convertedDate_object.strftime("%d/%m/%Y"), translator(convertedDate_object.strftime("%A"))

def convert_first_reminder_dates (dateObjects):
    """
    Convert reminder dates if they are on the weekend.
    """

    if dateObjects.strftime("%A") == 'Saturday':
        convertedDate_object = dateObjects + timedelta(days=2)
    elif dateObjects.strftime("%A") == 'Sunday':
        convertedDate_object = dateObjects + timedelta(days=1)
    else:
        convertedDate_object = dateObjects
    return convertedDate_object

def convert_third_reminder_dates (dateObjects):
    """
    Convert the third reminder date if it is on Sunday.
    """

    if dateObjects.strftime("%A") == 'Sunday':
        convertedDate_object = dateObjects + timedelta(days=-2)
    else:
        convertedDate_object = dateObjects
    return convertedDate_object

def calculate_dates(dischargeDate: str, TimeToReVisit:str):
    """
    Calculate reminder dates: 1 day after discharge day, 3 days and 1 day prior to the revisit day.
    """
    
    dischargeDate_object = datetime.strptime(dischargeDate, '%d/%m/%Y')
    
    firstReminderDate_object = dischargeDate_object + timedelta(days=1)
    reVisitDate_object = dischargeDate_object + timedelta(days=int(TimeToReVisit))
    secondReminderDate_object = reVisitDate_object + timedelta(days=-3)
    thirdReminderDate_object = reVisitDate_object + timedelta(days=-1)

    return firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, reVisitDate_object

def is_today(dateTimeObject):
    """
    Check if a given datetime or date object is today.
    """
    if not isinstance(dateTimeObject, (datetime, date)):
        raise TypeError("Input must be a datetime or date object.")
    
    today = date.today()
    # If dateTimeObject is datetime, compare only the date part
    return dateTimeObject.date() == today if isinstance(dateTimeObject, datetime) else dateTimeObject == today

    
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

def add_notes (df, recordID, note: dict):
    """
    Add notes to the dataframe.
    df: Pandas dataframe
    recordID: recordID whose the note should be added
    note: Dictionary contains keys as df column names and values as the content to be added
    --> return: updated df
    """
    for key, value in note.items():
        df.loc[df['RecordID'] == recordID, key] = value
    return df