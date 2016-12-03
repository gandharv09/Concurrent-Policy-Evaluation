
import da
PatternExpr_273 = da.pat.TuplePattern([da.pat.ConstantPattern('evalRequest'), da.pat.FreePattern('sender'), da.pat.FreePattern('request'), da.pat.FreePattern('order')])
PatternExpr_304 = da.pat.TuplePattern([da.pat.ConstantPattern('updateReadAttr'), da.pat.FreePattern('sender'), da.pat.FreePattern('request'), da.pat.FreePattern('order')])
PatternExpr_332 = da.pat.TuplePattern([da.pat.ConstantPattern('updateObj'), da.pat.FreePattern('sender'), da.pat.FreePattern('request'), da.pat.FreePattern('order')])
PatternExpr_359 = da.pat.TuplePattern([da.pat.FreePattern('str'), da.pat.FreePattern('sender'), da.pat.FreePattern('request'), da.pat.FreePattern('order')])
_config_object = {'channel': 'fifo'}
from classes import version as ver
from classes import request as req
from classes import attribute as att
import time, os, lib
try:
    worker = da.import_da('worker')
except ImportError:
    self.output('Failed to import worker class')

class Coordinator(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._CoordinatorReceivedEvent_0 = []
        self._CoordinatorReceivedEvent_1 = []
        self._CoordinatorReceivedEvent_2 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_0', PatternExpr_273, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_1', PatternExpr_304, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_2', PatternExpr_332, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_3', PatternExpr_359, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Coordinator_handler_358])])

    def setup(self, numWorkers, coordinators, database, objectCoordMap):
        self.numWorkers = numWorkers
        self.coordinators = coordinators
        self.database = database
        self.objectCoordMap = objectCoordMap
        workers = da.new(worker.Worker, num=self.numWorkers)
        da.setup(workers, (self.coordinators, self.database, '../config/policy.xml'))
        da.start(workers)
        self.versionMap = dict()
        self.cachedUpdates = dict()
        self.readQueue = list()
        self.writeQueue = list()
        self.objectCoordMap = self.objectCoordMap
        self.workers = list(workers)
        self.workerNumber = 0
        self.numWorkers = self.numWorkers

    def _da_run_internal(self):
        super()._label('_st_label_270', block=False)
        order = request = sender = None

        def ExistentialOpExpr_271():
            nonlocal order, request, sender
            for (_, _, (_ConstantPattern292_, sender, request, order)) in self._CoordinatorReceivedEvent_0:
                if (_ConstantPattern292_ == 'evalRequest'):
                    if True:
                        return True
            return False
        _st_label_270 = 0
        while (_st_label_270 == 0):
            _st_label_270 += 1
            if ExistentialOpExpr_271():
                pass
                _st_label_270 += 1
            else:
                super()._label('_st_label_270', block=True)
                _st_label_270 -= 1
        super()._label('_st_label_301', block=False)
        order = request = sender = None

        def ExistentialOpExpr_302():
            nonlocal order, request, sender
            for (_, _, (_ConstantPattern320_, sender, request, order)) in self._CoordinatorReceivedEvent_1:
                if (_ConstantPattern320_ == 'updateReadAttr'):
                    if True:
                        return True
            return False
        _st_label_301 = 0
        while (_st_label_301 == 0):
            _st_label_301 += 1
            if ExistentialOpExpr_302():
                pass
                _st_label_301 += 1
            else:
                super()._label('_st_label_301', block=True)
                _st_label_301 -= 1
        super()._label('_st_label_329', block=False)
        order = request = sender = None

        def ExistentialOpExpr_330():
            nonlocal order, request, sender
            for (_, _, (_ConstantPattern348_, sender, request, order)) in self._CoordinatorReceivedEvent_2:
                if (_ConstantPattern348_ == 'updateObj'):
                    if True:
                        return True
            return False
        _st_label_329 = 0
        while (_st_label_329 == 0):
            _st_label_329 += 1
            if ExistentialOpExpr_330():
                pass
                _st_label_329 += 1
            else:
                super()._label('_st_label_329', block=True)
                _st_label_329 -= 1

    def restartRequest(self, sender, request, order):
        pass

    def evaluate(self, sender, request, order):
        self.output('....Evaluating Request....')
        object = lib.obj(request, order)
        self.output(('Processing object ' + str(order)))
        if (request.isWriteReq is False):
            self.output('Request is of type Read-Only')
            for attr in defReadAttr(object, request):
                v = self.latestVersionBefore(object, attr, request.reqTs)
                v.rts = request.reqTs
            for attr in mightReadAttr(object, request):
                v = self.latestVersionBefore(object, attr, request.reqTs)
                v.pendingMightRead.add(request.reqId)
        else:
            self.output('Request is of type Write')
            for attr in lib.defReadAttr(object, request):
                v = self.latestVersionBefore(object, attr, request.reqTs)
                v.pendingMightRead.add(request.reqId)
            for attr in lib.mightReadAttr(object, request):
                v = self.latestVersionBefore(object, attr, request.reqTs)
                v.pendingMightRead.add(request.reqId)
        self.output('done with latesVersionBefore update')
        request.cachedUpdates[order] = self.getCachedUpdates(object, request)
        self.output('done with cache update')
        if (order == 1):
            coordinatorIndex = lib.coord(lib.obj(request, 2), self.objectCoordMap)
            if (self.coordinators[coordinatorIndex] == self.id):
                self.evaluate(sender, request, 2)
            else:
                self._send(('evalRequest', self.id, request, 2), self.coordinators[coordinatorIndex])
        else:
            workerId = (self.workerNumber % self.numWorkers)
            self.workerNumber += 1
            self.output('Coordinator sending worker request')
            request.workerCoordinatorId = self.id
            self._send(('workerRequest', request), self.workers[workerId])
            self.output('Coordinator sent worker request')

    def getCachedUpdates(self, object, request):
        if (self.cachedUpdates.get(object) is None):
            return dict()
        return self.cachedUpdates.get(object)

    def updateReadAttr(self, sender, request, order):
        self.output('....Updating Read Attributes....')
        object = obj(request, order)
        for attr in mightReadAttr(object, request):
            v = self.latestVersionBefore(object, attr, request.reqTs)
            v.pendingMightRead.remove(request.reqId)
            if (attr in request.readAttributes):
                v.rts = request.reqTs
        self.output('....Done Updating Read Attributes....')

    def updateWriteAttr(self, sender, request, order):
        self.output('....Updating Write Attributes....')
        object = obj(request, order)
        self.writeQueue[request] = list()
        self.output('Checking for first conflict')
        if (not (self.checkForConflict(obj, request) is True)):
            self.output('conflict not found')
            for (K, V) in request.updateAttributes.items():
                pendingList = self.latestVersionBefore(object, K, request.reqTs).pendingMightRead
                if ((len(pendingList) > 1) or ((len(pendingList) == 1) and (not (pendingList[0] == request.reqId)))):
                    for reqId in pendingList:
                        if (not (reqId == request.reqId)):
                            self.output('adding conflicting read requests to write waiting queue and going to wait')
                            self.writeQueue.get(request).add(reqId)
                            return
            self.output('Checking for second conflict')
            if (not (self.checkForConflict(object, request) is True)):
                self.output('conflict not found second time')
                self.output('....Updating DB....')
                self.updateDB(request)
                self.output('....Updating Cache....')
                self.updateCachedUpdates(object, request)
                self.output('....Updating Latest Version Before....')
                updateLatesVersionBefore(object, request)
                for attr in defReadAttr(object, request):
                    v = self.latestVersionBefore(object, attr, request.reqTs)
                    v.pendingMightRead.remove(request.reqId)
                    if (attr in request.readAttributes[request.updatedObj]):
                        v.rts = request.reqTs
                for attr in mightReadAttr(object, request):
                    v = self.latestVersionBefore(object, attr, request.reqTs)
                    v.pendingMightRead.remove(request.reqId)
                    if (attr in request.readAttributes[request.updatedObj]):
                        v.rts = request.reqTs
                self.writeQueue.remove(request)
                for (K, V) in self.readQueue.items():
                    if (request.reqId in V):
                        V.remove(request.reqId)
                        if (len(V) == 0):
                            self.readQueue.remove(K)
                            coordinatorIndex = coord(obj(request, 1))
                            self._send(('evalRequest', self.id, request, 1), self.coordinators[coordinatorIndex])
            else:
                self.output('Restarting Request because of conflict')
                self.restart(object, request)
        else:
            self.output('Restarting Request because of conflict')
            self.restart(object, request)

    def restart(self, obj, request):
        pass

    def updateCachedUpdates(self, obj, request):
        objCache = self.cachedUpdates.get(obj)
        for (K, V) in request.updateAttributes.items():
            if (not (objCache.get(K) is None)):
                objCache[k].append(att.Attribute(K, V, request.reqTs))
            else:
                objCache[K] = list()
                objCache[K].append(att.Attribute(K, V, request.reqTs))

    def updateLatestVersionBefore(self, obj, request):
        if (self.versionMap.get(obj) is None):
            self.versionMap[obj] = dict()
        for attr in request.updateAttributes:
            if (self.versionMap.get(obj).get(attr) is None):
                self.versionMap[obj][attr] = list()
            self.versionMap[obj][attr].append(ver.Version(0, request.reqTs))

    def updateDB(self, obj, request):
        pass

    def checkForConflict(self, obj, request):
        for (K, V) in request.updateAttributes.items():
            v = latesVersionBefore(obj, K, request.reqTs)
            if (v.rts > request.reqTs):
                return True
        return False

    def latestVersionBefore(self, obj, attr, ts):
        latestVersion = ver.Version()
        if (not (self.versionMap.get(obj) is None)):
            attrMap = self.versionMap.get(obj)
            versionList = attrMap.get(attr)
            for version in versionList:
                if ((version.wts <= ts) and (version.wts > latestVersion.wts)):
                    latestVersion = version
            if (latestVersion is None):
                latestVersion = ver.Version()
                versionList.append(latestVersion)
        else:
            self.versionMap[obj] = dict()
            self.versionMap[obj][attr] = []
            self.versionMap[obj][attr].append(latestVersion)
        return latestVersion

    def cachedUpdates(self, object, request):
        upd = list()
        objCache = self.cachedUpdates.get(object)
        for attr in defReadAttr(object, request):
            if (not (objCache.get(attr) is None)):
                latestAttr = att.Attribute()
                for attrib in objCache.get(attr):
                    if ((attrib.ts <= request.reqTs) and (attrib.ts > latestAttr.ts)):
                        latestAttr = attrib
                if (not (latestAttr.ts == 0)):
                    upd.append(latestAttr)
        for attr in mightReadAttr(object, request):
            if (not (objCache.get(attr) is None)):
                latestAttr = att.Attribute()
                for attrib in objCache.get(attr):
                    if ((attrib.ts <= request.reqTs) and (attrib.ts > latestAttr.ts)):
                        latestAttr = attrib
                if (not (latestAttr.ts == 0)):
                    upd.append(latestAttr)
        return upd

    def _Coordinator_handler_358(self, str, sender, request, order):
        if (str == 'evalRequest'):
            self.output('Received Request from Client')
            self.evaluate(sender, request, order)
        elif (str == 'updateReadAttr'):
            self.output('Received updateReadAttr from worker')
            self.updateReadAttr(sender, request, order)
        elif (str == 'updateObj'):
            self.output('Received updateObj from worker')
            self.updateWriteAttr(sender, request, order)
        elif (str == 'restartRequest'):
            self.output('Received restartRequest from coordinator')
            self.restartRequest(sender, request, order)
    _Coordinator_handler_358._labels = None
    _Coordinator_handler_358._notlabels = None
