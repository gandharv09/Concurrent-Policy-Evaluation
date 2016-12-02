class Version:
    def __init__(self,*args):
        if len(args) == 0:
            # default case
            self.rts = 0
            self.wts = 0
            self.pendingMightRead = set()
        else:
            self.rts = args[0]
            self.wts = args[1]
            self.pendingMightRead = set()

