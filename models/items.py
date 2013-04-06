

class Item:
    def __init__(self):
# these are status attributes
        self.id = 0
        self.name = ''
        self.image_url = ''
        self.link = ''
        self.note = ''

    def __str__(self):
        string = u'\nid_str: ' + repr(self.id_str)
        return string
