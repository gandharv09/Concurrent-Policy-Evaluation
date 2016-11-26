
import da
_config_object = {}

class Database(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([])

    def setup(self, configFile):
        self.configFile = configFile
        self.output('Database started with config file ', self.configFile)

    def _da_run_internal(self):
        pass
