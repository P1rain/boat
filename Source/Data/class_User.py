class User:
    def __init__(self, user_code, user_id, user_pw, user_name, user_parent):
        self.user_code = user_code
        self.user_id = user_id
        self.user_pw = user_pw
        self.user_name = user_name
        self.user_parent = user_parent

    def __str__(self):
        return f"{self.__repr__()}"

    def __repr__(self):
        return f"{self.__dict__}"

    def __eq__(self, other):
        if isinstance(other, User) and \
                self.user_id == other.user_id and \
                self.user_pw == other.user_pw and \
                self.user_name == other.user_name and \
                self.user_parent == other.user_parent:
            return True
        return False

    def __lt__(self, other):
        return self.user_name < other.user_name
