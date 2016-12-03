
import da
PatternExpr_215 = da.pat.TuplePattern([da.pat.ConstantPattern('resp_from_coordinator'), da.pat.FreePattern('b')])
PatternExpr_473 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'channel': 'fifo'}
from classes import request as req
import os, json, time
import random
import lib

class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._ClientReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_0', PatternExpr_215, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_ClientReceivedEvent_1', PatternExpr_473, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Client_handler_472])])

    def setup(self, coordinators, configFile, objectCoordMap):
        self.coordinators = coordinators
        self.configFile = configFile
        self.objectCoordMap = objectCoordMap
        self.output('Client setup with config file', self.configFile)
        self.objCoordMap = self.objectCoordMap

    def _da_run_internal(self):
        i = 0
        while True:
            if (i == 0):
                self.sendRequest()
                i = (i + 1)
            super()._label('_st_label_212', block=False)
            b = None

            def ExistentialOpExpr_213():
                nonlocal b
                for (_, _, (_ConstantPattern230_, b)) in self._ClientReceivedEvent_0:
                    if (_ConstantPattern230_ == 'resp_from_coordinator'):
                        if True:
                            return True
                return False
            _st_label_212 = 0
            while (_st_label_212 == 0):
                _st_label_212 += 1
                if ExistentialOpExpr_213():
                    pass
                    _st_label_212 += 1
                else:
                    super()._label('_st_label_212', block=True)
                    _st_label_212 -= 1
            else:
                if (_st_label_212 != 2):
                    continue
            if (_st_label_212 != 2):
                break

    def sendRequest(self):
        if (not os.path.exists(self.configFile)):
            self.output('ConfigFile does not exist')
        configData = open(self.configFile).read()
        try:
            configData = json.loads(configData)
        except:
            self.output('Config File not in proper json syntax')
            return
        for i in range(len(configData.get('scenarios'))):
            scenarios = configData.get('scenarios')[i]
            request = req.Request()
            request.clientId = self.id
            request.objects.append(scenarios.get('subject'))
            request.objects.append(scenarios.get('resource'))
            request.action = scenarios.get('action')
            if (not (scenarios.get('defReadAttr') is None)):
                request.defReadAttr = [attr for attr in scenarios.get('defReadAttr').split(',')]
            if (not (scenarios.get('mightReadAttr') is None)):
                request.mightReadAttr = [attr for attr in scenarios.get('mightReadAttr').split(',')]
            if (not (scenarios.get('mightWriteObj') is None)):
                request.mightWriteObj = [attr for attr in scenarios.get('mightWriteObj').split(',')]
            if (not (scenarios.get('mightWriteAttr') is None)):
                request.mightWriteAttr = [attr for attr in scenarios.get('mightWriteAttr').split(',')]
            request.reqId = random.randint(0, 1000)
            request.reqTs = int(time.time())
        if (not (len(lib.mightWriteObj(request)) == 0)):
            request.isWriteReq = True
        coordinatorIndex = lib.coord(lib.obj(request, 1), self.objectCoordMap)
        self.output(' Application Sending message to coordinator\n')
        self._send(('evalRequest', self.id, request, 1), self.coordinators[coordinatorIndex])

    def _Client_handler_472(self, a, b):
        if (a == 'resp_from_coordinator'):
            self.output('--------- DECISION RECEIVED------------')
            self.output('Application Received Decision for request ', b.reqId)
            self.output(' Decision is ', b.decision)
            self.output('----------------------------------------')
    _Client_handler_472._labels = None
    _Client_handler_472._notlabels = None
