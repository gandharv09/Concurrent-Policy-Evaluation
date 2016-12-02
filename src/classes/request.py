class Request:
    def __init__(self):
        self.objects = []
        self.action = None
        self.clientId = 0
        self.reqId = 0
        self.reqTs = 0
        self.isWriteReq = False
        self.cachedUpdates = dict()
        self.readAttributes = list()
        self.updateAttributes = dict()
        self.mightRead = list()
        self.defRead = list()
        self.mightWrite = list()
        self.updatedObj = None
        self.readOnlyObj = None
        self.decision = False

