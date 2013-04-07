

class List:
    def __init__(self, owner_email=None, mongobj=None):

        if mongobj == None:
            self.name = ''
            self.type = ''
            self.items = []
            self.collab_emails = []
            self.list_url = ''
            self.item_count = 0
            self.owner_email = owner_email
            self.default_image = 'http://images.wikia.com/youtube/images/e/e8/Skull_-_LOGO_300x300.gif'
        else:
            self.name = mongobj['name']
            self.type = mongobj['type']
            self.items = mongobj['items']
            self.collab_emails = mongobj['collab_emails']
            self.list_url = mongobj['list_url']
            self.item_count = mongobj['item_count']
            self.owner_email = mongobj['owner_email']
            self.default_image = mongobj['default_image']
