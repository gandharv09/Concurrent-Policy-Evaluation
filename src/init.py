
import da
_config_object = {}
import os, sys, traceback, json, random
try:
    database = da.import_da('database')
    coordinator = da.import_da('coordinator')
    client = da.import_da('client')
except ImportError:
    self.output('Failed to import class files')

class Init(da.DistProcess):

    def __init__(self, parent, initq, channel, props):
        super().__init__(parent, initq, channel, props)
        self._events.extend([])

    def setup(self):
        pass

    def _da_run_internal(self):
        if (not os.path.exists(sys.argv[2])):
            self.output(('Config file %s does not exist.' % sys.argv[2]))
            sys.exit((- 1))
        configData = json.loads(open(sys.argv[2]).read())
        numCoordinator = configData.get('globalConfig').get('numCoordinators')
        numWorkerPerCoordinator = configData.get('globalConfig').get('numWorkerPerCoordinator')
        if self.initProcesses(int(numCoordinator), int(numWorkerPerCoordinator)):
            self.output('Failed to setup the environment')
            sys.exit((- 1))

    def initProcesses(self, numCoordinator, numWorkerPerCoordinator):
        try:
            coordinators = da.new(coordinator.Coordinator, num=numCoordinator)
            clients = da.new(client.Client)
            db = da.new(database.Database)
            if (len(sys.argv) < 3):
                self.output('Improper Arguments')
                return (- 1)
            objectCoordMap = dict()
            objectCoordMap['movieA'] = random.randint(0, (numCoordinator - 1))
            objectCoordMap['customerA'] = random.randint(0, (numCoordinator - 1))
            dbLoad = sys.argv[1]
            args = []
            args.append(dbLoad)
            da.setup(db, args)
            self.output('DbEmulator process set up')
            da.setup(coordinators, (numWorkerPerCoordinator, list(coordinators), db, objectCoordMap))
            self.output('Coordinators have been setup')
            da.setup(clients, (list(coordinators), sys.argv[2], objectCoordMap))
            self.output('Client process has been set up')
            da.start(clients)
            da.start(coordinators)
            da.start(db)
            self.output('Started all processes')
            return 0
        except:
            self.output('STACK TRACE')
            self.output(traceback.print_exc())
            return (- 1)

def main():
    init = da.new(Init)
    da.setup(init, ())
    da.start(init)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        self.output('SYSTEM EXITING')
        sys.exit((- 1))
