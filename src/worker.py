
import da
PatternExpr_204 = da.pat.TuplePattern([da.pat.ConstantPattern('workerRequest'), da.pat.FreePattern('request')])
PatternExpr_229 = da.pat.TuplePattern([da.pat.ConstantPattern('dbResponse'), da.pat.FreePattern('response'), da.pat.FreePattern('retVal')])
PatternExpr_258 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'channel': 'fifo'}
from xml.etree import ElementTree as ET
import os

class Worker(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._WorkerReceivedEvent_0 = []
        self._WorkerReceivedEvent_1 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_0', PatternExpr_204, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_1', PatternExpr_229, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_WorkerReceivedEvent_2', PatternExpr_258, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Worker_handler_257])])

    def setup(self, coordinatorList, dbProcess, policyFile):
        self.coordinatorList = coordinatorList
        self.dbProcess = dbProcess
        self.policyFile = policyFile
        self.dbProcess = self.dbProcess
        self.coordinatorList = self.coordinatorList
        if (not os.path.exists(self.policyFile)):
            self.output('ERROR:Policy File does not exist')
        else:
            self.policyFile = self.policyFile

    def _da_run_internal(self):
        super()._label('_st_label_201', block=False)
        request = None

        def ExistentialOpExpr_202():
            nonlocal request
            for (_, _, (_ConstantPattern219_, request)) in self._WorkerReceivedEvent_0:
                if (_ConstantPattern219_ == 'workerRequest'):
                    if True:
                        return True
            return False
        _st_label_201 = 0
        while (_st_label_201 == 0):
            _st_label_201 += 1
            if ExistentialOpExpr_202():
                pass
                _st_label_201 += 1
            else:
                super()._label('_st_label_201', block=True)
                _st_label_201 -= 1
        super()._label('_st_label_226', block=False)
        retVal = response = None

        def ExistentialOpExpr_227():
            nonlocal retVal, response
            for (_, _, (_ConstantPattern246_, response, retVal)) in self._WorkerReceivedEvent_1:
                if (_ConstantPattern246_ == 'dbResponse'):
                    if True:
                        return True
            return False
        _st_label_226 = 0
        while (_st_label_226 == 0):
            _st_label_226 += 1
            if ExistentialOpExpr_227():
                pass
                _st_label_226 += 1
            else:
                super()._label('_st_label_226', block=True)
                _st_label_226 -= 1

    def sendResponseToCoordinator(self, request):
        self.output('Worker Sending Response to coordinator')
        self._send(('workerResponse', request), request.workerCoordinatorId)

    def processCoordinatorRequest(self, request):
        '\n        send entire request to the database.\n        database will determine mightRead and defRead and return values\n        '
        self.output('Worker sending read request to db')
        self._send(('read_request', request, self.id), self.dbProcess)

    def findRule(self, request):
        try:
            tree = ET.parse(self.policyFile)
            root = tree.getroot()
            for rule in root.iter('rule'):
                if (rule.find('action').attrib.get('name') == request.action):
                    if (not (request.objects[0].find(rule.find('subjectCondition').attrib.get('position')) == (- 1))):
                        if (request.objects[1] == rule.find('resourceCondition').attrib.get('type')):
                            self.output('Found a matching rule for this policy')
                            return rule
            return (- 1)
        except:
            import traceback
            print(traceback.print_exc())
            self.output('XML file not in proper syntax')
            return (- 1)

    def evaluatePolicy(self, request):
        self.output('Inside Worker Evaluate Policy')
        matchedRule = self.findRule(request)
        attrReadFromDB = request.readDB
        if (matchedRule == (- 1)):
            self.output('None of the rules matched for this request.')
            request.decision = False
            self.sendResponseToCoordinator(request)
        else:
            condition = matchedRule.find('resourceCondition').attrib.get('viewCount')
            self.output('Need to validate that viewCount ', condition)
            self.output('Checking request cached updates for value')
            if (not (request.cachedUpdates.get(request.objects[1]) is None)):
                currentViewCount = request.cachedUpdates.get(request.objects[1]).get('viewCount')
                allowedViewCount = int(condition[1:])
                if ((int(currentViewCount) + 1) <= int(allowedViewCount)):
                    request.updateAttributes['viewCount'] = (currentViewCount + 1)
                    request.updatedObj = 1
                    request.readAttributes.append('viewCount')
                    request.decision = True
                    self.sendResponseToCoordinator(request)
                else:
                    subscription = attrReadFromDB.get('subscriptionType')
                    if (subscription.upper() == 'PREMIUM'):
                        request.updateAttributes['viewCount'] = (currentViewCount + 1)
                        request.updatedObj = 1
                        request.readAttributes.append('viewCount')
                        request.decision = True
                        request.readAttributes.append('subscriptionType')
                        self.sendResponseToCoordinator(request)
                    else:
                        request.readAttributes.append('viewCount')
                        request.decision = False
                        request.readAttributes.append('subscriptionType')
                        self.sendResponseToCoordinator(request)
            else:
                currentViewCount = attrReadFromDB.get(request.objects[1]).get('viewCount')
                if (currentViewCount is None):
                    self.output('ERROR: attribue not found in the database')
                    request.decision = False
                    return self.sendResponseToCoordinator(coordinator)
                else:
                    allowedViewCount = int(condition[1:])
                    if ((int(currentViewCount) + 1) <= int(allowedViewCount)):
                        request.updateAttributes['viewCount'] = str((int(currentViewCount) + 1))
                        request.updatedObj = 1
                        request.readAttributes.append('viewCount')
                        request.decision = True
                        self.output('Decision is True')
                        self.output('Sending decision back to coordinator')
                        return self.sendResponseToCoordinator(request)
                    else:
                        subscription = attrReadFromDB.get(request.objects[0]).get('subscriptionType')
                        if (subscription.upper() == 'PREMIUM'):
                            request.updateAttributes['viewCount'] = (currentViewCount + 1)
                            request.updatedObj = 1
                            request.readAttributes.append('viewCount')
                            request.decision = True
                            request.readAttributes.append('subscriptionType')
                        else:
                            request.readAttributes.append('viewCount')
                            request.decision = False
                            request.readAttributes.append('subscriptionType')
                            self.output('Decision is False')
                            return self.sendResponseToCoordinator(request)

    def _Worker_handler_257(self, a, b):
        if (a == 'workerRequest'):
            self.output('Worker received evalRequest from coordinator')
            self.processCoordinatorRequest(b)
        elif (a == 'dbResponse'):
            self.evaluatePolicy(b)
    _Worker_handler_257._labels = None
    _Worker_handler_257._notlabels = None
