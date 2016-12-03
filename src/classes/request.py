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
        self.mightReadAttr = list()
        self.defReadAttr = list()
        self.mightWriteObj = list()
        self.mightWriteAttr = list ()
        self.updatedObj = None
        self.readOnlyObj = None
        self.decision = False
        self.workerCoordinatorId = None
        self.readDB = dict()

