from datetime import datetime, timedelta, date
from gen_messages import get_message

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
        
    dischargeDate = data['DischargeDate'][data['RecordID']==int(recordID)].to_list()[0]
    
    timeToReVisit = data['TimeToReVisit'][data['RecordID']==int(recordID)].to_list()[0]

    Dx = data['Dx'][data['RecordID']==int(recordID)].to_list()[0]

    return name, genderVN, phoneNumber_1, phoneNumber_2, dischargeDate, timeToReVisit, Dx

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
    return convertedDate_object.strftime("%d/%m/%Y"), convertedDate_object.strftime("%A")


def calculate_dates(dischargeDate: str, TimeToReVisit:str):
    """
    Calculate reminder dates: 1 day after discharge day, 3 days and 1 day prior to the revisit day.
    """
    dischargeDate_object = datetime.strptime(dischargeDate, '%d/%m/%Y')
    
    firstReminderDate_object = dischargeDate_object + timedelta(days=1)
    reVisitDate_object = dischargeDate_object + timedelta(days=int(TimeToReVisit))
    secondReminderDate_object = reVisitDate_object + timedelta(days=-1)
    thirdReminderDate_object = reVisitDate_object + timedelta(days=-3)

    return firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object

def is_today(dateTimeObject):
    """
    Check if a given datetime or date object is today.
    """
    if not isinstance(dateTimeObject, (datetime, date)):
        raise TypeError("Input must be a datetime or date object.")
    
    today = date.today()
    # If dateTimeObject is datetime, compare only the date part
    return dateTimeObject.date() == today if isinstance(dateTimeObject, datetime) else dateTimeObject == today

def create_message (firstReminderDate_object, secondReminderDate_object, thirdReminderDate_object, name, gender, Dx):
    """
    Get message for each visit
    """
    if is_today(firstReminderDate_object):
        Date, DateStrVN = convert_dates(firstReminderDate_object)
        return get_message(name, gender, DateStrVN, Date, Dx, whichMessage = 'first')
    elif is_today(secondReminderDate_object):
        Date, DateStrVN = convert_dates(secondReminderDate_object)
        return get_message(name, gender, DateStrVN, Date, Dx, whichMessage = 'second')
    elif is_today(thirdReminderDate_object):
        Date, DateStrVN = convert_dates(thirdReminderDate_object)
        return get_message(name, gender, DateStrVN, Date, Dx, whichMessage = 'third')
    else:
        return None
    
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