class View(object):

    def __init__(self):
        self.face = None
        self.callback = None
        self.image = []

    def start(self):
        return

    def close(self):
        return

    def redraw(self, callback=None):
        self.callback = callback

    def get_image(self):
        return self.image

    def set_image(self):
        return

    def get_size(self):
        return (0, 0)
