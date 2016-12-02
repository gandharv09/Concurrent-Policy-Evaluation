class Attribute:
    def __init__(self,*args):
        if len(args) == 0:
            self.id = None
            self.val = None
            self.ts = 0
        else:
            self.id = args[0]
            self.val = args[1]
            self.ts = args[2]
