class Attitude:
    def __init__(self, user_code, attitude_code, attitude_time):
        self.user_code = user_code
        self.attitude_code = attitude_code
        self.attitude_time = attitude_time

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, Attitude) and \
                self.user_code == other.user_code and \
                self.attitude_code == other.attitude_code and \
                self.attitude_time == other.attitude_time:
            return True
        return False

