
import da
PatternExpr_317 = da.pat.TuplePattern([da.pat.ConstantPattern('read_request'), da.pat.FreePattern('object'), da.pat.FreePattern('attribute'), da.pat.FreePattern('timestamp'), da.pat.FreePattern('sender')])
PatternExpr_350 = da.pat.TuplePattern([da.pat.ConstantPattern('write_request'), da.pat.FreePattern('object'), da.pat.FreePattern('attribute'), da.pat.FreePattern('timestamp'), da.pat.FreePattern('value')])
PatternExpr_380 = da.pat.TuplePattern([da.pat.ConstantPattern('read_request'), da.pat.FreePattern('request'), da.pat.FreePattern('sender')])
PatternExpr_396 = da.pat.TuplePattern([da.pat.ConstantPattern('write_request'), da.pat.FreePattern('object'), da.pat.FreePattern('attribute'), da.pat.FreePattern('timestamp'), da.pat.FreePattern('value')])
_config_object = {'channel': 'fifo'}
import traceback
import json
import time
import os

class Database(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._DatabaseReceivedEvent_0 = []
        self._DatabaseReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_0', PatternExpr_317, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_1', PatternExpr_350, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_2', PatternExpr_380, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Database_handler_379]), da.pat.EventPattern(da.pat.ReceivedEvent, '_DatabaseReceivedEvent_3', PatternExpr_396, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Database_handler_395])])

    def setup(self, configFile):
        self.configFile = configFile
        self.output('Database started with config file ', self.configFile)
        self.objectStore = dict()
        if self.loadConfig(self.configFile):
            self.output('Failed to load data from the config file')
        else:
            self.output('After Initial load db is\n')
            self.output(self.objectStore)

    def _da_run_internal(self):
        while True:
            super()._label('_st_label_314', block=False)
            object = sender = timestamp = attribute = None

            def ExistentialOpExpr_315():
                nonlocal object, sender, timestamp, attribute
                for (_, _, (_ConstantPattern337_, object, attribute, timestamp, sender)) in self._DatabaseReceivedEvent_0:
                    if (_ConstantPattern337_ == 'read_request'):
                        if True:
                            return True
                return False
            _st_label_314 = 0
            while (_st_label_314 == 0):
                _st_label_314 += 1
                if ExistentialOpExpr_315():
                    pass
                    _st_label_314 += 1
                else:
                    super()._label('_st_label_314', block=True)
                    _st_label_314 -= 1
            else:
                if (_st_label_314 != 2):
                    continue
            if (_st_label_314 != 2):
                break
            super()._label('_st_label_347', block=False)
            object = value = timestamp = attribute = None

            def ExistentialOpExpr_348():
                nonlocal object, value, timestamp, attribute
                for (_, _, (_ConstantPattern368_, object, attribute, timestamp, value)) in self._DatabaseReceivedEvent_1:
                    if (_ConstantPattern368_ == 'write_request'):
                        if True:
                            return True
                return False
            _st_label_347 = 0
            while (_st_label_347 == 0):
                _st_label_347 += 1
                if ExistentialOpExpr_348():
                    pass
                    _st_label_347 += 1
                else:
                    super()._label('_st_label_347', block=True)
                    _st_label_347 -= 1
            else:
                if (_st_label_347 != 2):
                    continue
            if (_st_label_347 != 2):
                break

    def loadConfig(self, preInitConfigFile):
        if (not os.path.exists(preInitConfigFile)):
            self.output(('Database preInit Config file %s not found' % preInitConfigFile))
            return (- 1)
        try:
            preConfigData = json.loads(open(preInitConfigFile).read())
            currentTime = int(time.time())
            for objects in preConfigData.get('objects'):
                objName = objects.get('name')
                self.objectStore[objName] = dict()
                attrMap = objects.get('attributes')
                self.objectStore[objName][attrMap.get('name')] = list()
                self.objectStore[objName][attrMap.get('name')].append((currentTime, attrMap.get('value')))
            return 0
        except:
            self.output('Json file not in correct syntax')
            self.output('STACK TRACE')
            print(traceback.print_exc())
            return (- 1)

    def processReadRequest(self, request, sender):
        self.output('DB Received read request from worker')
        try:
            retVal = dict()
            reqTS = request.reqTs
            retVal[request.objects[0]] = dict()
            for attr in self.objectStore[request.objects[0]].keys():
                timestamps = []
                for value in self.objectStore[request.objects[0]][attr]:
                    if (value[0] <= reqTS):
                        timestamps.append(value[0])
                timestamps.sort()
                requiredTS = timestamps[(- 1)]
                for value in self.objectStore[request.objects[0]][attr]:
                    if (value[0] == requiredTS):
                        retVal[request.objects[0]][attr] = value[1]
            retVal[request.objects[1]] = dict()
            for attr in self.objectStore[request.objects[1]].keys():
                timestamps = []
                for value in self.objectStore[request.objects[1]][attr]:
                    if (value[0] <= reqTS):
                        timestamps.append(value[0])
                timestamps.sort()
                requiredTS = timestamps[(- 1)]
                for value in self.objectStore[request.objects[1]][attr]:
                    if (value[0] == requiredTS):
                        retVal[request.objects[1]][attr] = value[1]
            '\n            attributes = []\n            for attr in request.mightReadAttr:\n                attributes.append(attr)\n            for attr in request.defReadAttr:\n                attributes.append(attr)\n            timeStamps = []\n            requiredTimeStamp = 0\n            for values in self.objectStore[object]:\n                timeStamps.append(values[0])\n            timeStamps.sort()\n\n            timeStamps = [ ts for ts in timeStamps if ts <=timestamp]\n\n            requiredTimeStamp = timeStamps[-1]\n            for attribute in attributes:\n                for values in self.objectStore[object][\'attributes\'][attribute]:\n                    if values[0] == requiredTimeStamp:\n                        retVal[attr] = values[1]\n            output("Db returning value ", retVal)\n            send((\'db_read_response\', retVal),to = sender)\n            '
            self.output('DB Returning ', retVal)
            request.readDB = retVal
            self._send(('dbResponse', request), sender)
        except:
            import traceback
            print(traceback.print_exc())
            self.output('Invalid arguments to processReadRequest')

    def processWriteRequest(self, object, attribute, timeStamp, value):
        try:
            self.objectStore[object]['attributes'][attribute].append((timeStamp, value))
        except KeyError:
            self.output('Invalid arguments to writeRequest')

    def _Database_handler_379(self, request, sender):
        self.processReadRequest(request, sender)
    _Database_handler_379._labels = None
    _Database_handler_379._notlabels = None

    def _Database_handler_395(self, object, attribute, timestamp, value):
        self.processWriteRequest(object, attribute, timestamp, value)
    _Database_handler_395._labels = None
    _Database_handler_395._notlabels = None
