def get_VNpronouns (gender, age):
    """
    Get Vietnamese pronoun for different ages and genders
    """
    if int(age)<45:
        me = 'tôi'
        if gender == 'Nam' or 'NAM':
            pronoun = 'Anh'
        elif gender == 'Nữ' or 'NỮ':
            pronoun = 'Chị'
    elif int(age) < 75:
        me = 'cháu'
        if gender == 'Nam' or 'NAM':
            pronoun = 'Chú'
        elif gender == 'Nữ' or 'NỮ':
            pronoun = 'Cô'
    else:
        me = 'cháu'
        if gender == 'Nam' or 'NAM':
            pronoun = 'Ông'
        elif gender == 'Nữ' or 'NỮ':
            pronoun = 'Bà'
    return me, pronoun

def get_message(name, gender, age, DateStrVN, Date, JJ, siteToReVisit, whichMessage=None):
    me, pronoun = get_VNpronouns (gender, age)

    greeting = f"Xin chào {pronoun} {name}, {me} là Bác sĩ Lê Duy Bình - Khoa Ngoại tiết niệu, Bệnh viện Đa khoa Xanh Pôn."
    goodbye = f"\n\nLưu ý: Đây là tin nhắn nhắc hẹn khám được tự động gửi theo số điện thoại đã đăng kí. Nếu Anh/Chị là người nhà, kính nhờ Anh/Chị chuyển lời đến {pronoun} {name}.\
                \nMọi câu hỏi Anh/Chị có thể hỏi tại đây hoặc liên hệ đến Hotline của khoa 02437331502.\
                \n\nXin cảm ơn!"
    if whichMessage == 'first':
        note = {'FirstReminderDate': ''}
        if JJ == 'Yes':
            message = f"{greeting}\
                        \n\nMời {pronoun} đến {siteToReVisit} vào {DateStrVN}, {Date} để được kiểm tra lại và xem xét rút sonde JJ.\
                        {goodbye}"
        else:
            message = f"{greeting}\
                        \n\nMời {pronoun} đến {siteToReVisit} vào {DateStrVN}, {Date} để được đánh giá sau quá trình điều trị.\
                        {goodbye}"
            
    if whichMessage == 'second':
        note = {'SecondReminderDate': ''}
        if JJ == 'Yes':
            message = f"Xin chào {pronoun} {name},\
                        \nXin được nhắc {pronoun} có hẹn kiểm tra lại và xem xét rút sonde JJ vào {DateStrVN}, {Date} tại {siteToReVisit}.\
                        \nNếu {pronoun} đã đến, xin bỏ qua tin nhắn này.\
                        {goodbye}"        
        else:
            message = f"Xin chào {pronoun} {name},\
                        \nXin được nhắc {pronoun} có hẹn đánh giá sau quá trình điều trị vào {DateStrVN}, {Date} tại {siteToReVisit}.\
                        \nNếu {pronoun} đã đến, xin bỏ qua tin nhắn này.\
                        {goodbye}"

    if whichMessage == 'third':
        note = {'ThirdReminderDate': ''}
        if JJ == 'Yes':
            message = f"Xin chào {pronoun} {name},\
                        \nXin được nhắc {pronoun} có hẹn kiểm tra lại và xem xét rút sonde JJ vào ngày mai tại {siteToReVisit}.\
                        \nNếu {pronoun} đã đến, xin bỏ qua tin nhắn này.\
                        {goodbye}"        
        else:
            message = f"Xin chào {pronoun} {name},\
                        \nXin được nhắc {pronoun} có hẹn đánh giá sau quá trình điều trị vào ngày mai tại {siteToReVisit}.\
                        \nNếu {pronoun} đã đến, xin bỏ qua tin nhắn này.\
                        {goodbye}"
    return note, message