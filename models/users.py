

class User:
    def __init__(self):
# these are status attributes
        self.email = ''
        self.password = ''
        self.fullname = ''

    def __str__(self):
        string = u'\nid_str: ' + repr(self.id_str)
        return string
