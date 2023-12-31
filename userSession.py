class UserSession:
    def __init__(self):
        self.logged_in_user_id = None
        self.logged_in_user_name = None

    def set_logged_in_user_name(self, user_name):
        self.logged_in_user_name = user_name

    def get_logged_in_user_name(self):
        return self.logged_in_user_name

    def set_logged_in_user_id(self, user_id):
        self.logged_in_user_id = user_id

    def get_logged_in_user_id(self):
        return self.logged_in_user_id


userSession = UserSession()
