class Attend_Lecture:
    def __init__(self, user_code, lecture_code, attend_time, complete_status):
        self.user_code = user_code
        self.lecture_code = lecture_code
        self.attend_time = attend_time
        self.complete_status = complete_status

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, Attend_Lecture) and \
                self.user_code == other.user_code and \
                self.lecture_code == other.lecture_code and \
                self.attend_time == other.attend_time and \
                self.complete_status == other.complete_status:
            return True
        return False