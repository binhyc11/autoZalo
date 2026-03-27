def get_message(name, gender, DateStrVN, Date, Dx, whichMessage=None):
    greeting = f"Xin chào {gender} {name}, tôi là Bác sĩ Lê Duy Bình, khoa Ngoại tiết niệu, Bệnh viện Đa khoa Xanh Pôn."
    goodbye = f"\n\nXin lưu ý: Đây là tin nhắn nhắc hẹn khám được tự động gửi theo số điện thoại đã đăng kí. Nếu Anh/Chị là người nhà, kính nhờ Anh/Chị chuyển lời đến {gender} {name}.\
                \nMọi câu hỏi Anh/chị có thể hỏi tại đây hoặc liên hệ đến Hotline của khoa ???\
                \n\nXin cảm ơn!"
    if whichMessage == 'first':
        if Dx == 'JJ':
            message = f"{greeting}\
                        \nXin mời {gender} đến phòng 121 nhà B2 vào {DateStrVN}, {Date} để được kiểm tra lại và xem xét rút sonde JJ.\
                        {goodbye}"
        elif Dx == 'TLT':
            message = f"{greeting}\
                        \nXin mời {gender} đến phòng khám số 10, Trung tâm Kĩ thuật cao và Tiêu hóa vào {DateStrVN}, {Date} để được đánh giá sau quá trình điều trị.\
                        {goodbye}"
        elif  Dx == 'Other':
            message = f"{greeting}\
                        \nXin  mời {gender} đến phòng 121 nhà B2 vào {DateStrVN}, {Date} để được khám lại và đánh giá sau quá trình điều trị.\
                        {goodbye}"
    return message