class User:
    def __init__(self, user_id, account, email=None):
        self.user_id = user_id
        self.account = account
        self.email = email
        self.token=None
