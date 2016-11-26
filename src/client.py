
import da
_config_object = {}

class Client(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([])

    def setup(self, coordinators, configFile):
        self.coordinators = coordinators
        self.configFile = configFile
        self.output('Client setup with config file', self.configFile)

    def _da_run_internal(self):
        self.output('In run of client')
        while True:
            self._send(('hello', 'hi'), self.coordinators[0])
