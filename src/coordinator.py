
import da
PatternExpr_175 = da.pat.TuplePattern([da.pat.ConstantPattern('hello'), da.pat.FreePattern('msg')])
PatternExpr_199 = da.pat.TuplePattern([da.pat.FreePattern('a'), da.pat.FreePattern('b')])
_config_object = {'channel': 'fifo'}

class Coordinator(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._CoordinatorReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_0', PatternExpr_175, sources=None, destinations=None, timestamps=None, record_history=True, handlers=[]), da.pat.EventPattern(da.pat.ReceivedEvent, '_CoordinatorReceivedEvent_1', PatternExpr_199, sources=None, destinations=None, timestamps=None, record_history=None, handlers=[self._Coordinator_handler_198])])

    def setup(self, numWorkers, coordinators, database):
        self.numWorkers = numWorkers
        self.coordinators = coordinators
        self.database = database
        self.output('In setup of coordinator process')

    def _da_run_internal(self):
        super()._label('_st_label_172', block=False)
        msg = None

        def ExistentialOpExpr_173():
            nonlocal msg
            for (_, _, (_ConstantPattern190_, msg)) in self._CoordinatorReceivedEvent_0:
                if (_ConstantPattern190_ == 'hello'):
                    if True:
                        return True
            return False
        _st_label_172 = 0
        while (_st_label_172 == 0):
            _st_label_172 += 1
            if ExistentialOpExpr_173():
                pass
                _st_label_172 += 1
            else:
                super()._label('_st_label_172', block=True)
                _st_label_172 -= 1

    def _Coordinator_handler_198(self, a, b):
        self.output('Received message')
    _Coordinator_handler_198._labels = None
    _Coordinator_handler_198._notlabels = None
