class Lecture:
    def __init__(self, lecture_code, lectured_time):
        self.lecture_code = lecture_code
        self.lectured_time = lectured_time

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, Lecture) and \
                self.lecture_code == other.lecture_code and \
                self.lectured_time == other.lectured_time:
            return True
        return False

