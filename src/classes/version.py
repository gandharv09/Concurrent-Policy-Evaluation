class Version:
    def __init__(self):
        self.rts = 0
        self.wts = 0
        self.pendingMightRead = set()


    def __init__(self, r, w):
        self.rts = r
        self.wts = w
        self.pendingMightRead = set()
