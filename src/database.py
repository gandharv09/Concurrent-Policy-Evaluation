import traceback
import json
import time

class Database(process):
    def setup(configFile:str):
        output("Database started with config file ",configFile)
        self.objectStore = dict()
        if loadConfig(configFile):
            # failed to load the config file
            output("Failed to load data from the config file")
        else:
            # reading and loading config file was successful.
            output("After Initial load db is\n")

            output(self.objectStore.__dict__)

    def loadConfig(preInitConfigFile):

        if not os.path.exists(preInitConfigFile):
            output("Database preInit Config file %s not found"%preInitConfigFile)
            return -1
        try:
            preConfigData=json.loads(open(preInitConfigFile).read())
            currentTime = int(time.time())
            for objects in preConfigData.get("objects"):
                self.objectStore[objects] = dict()
                self.objectStore[objects]['name'] = objects.get('name')
                self.objectStore[objects]['attributes'] = dict()
                for k,v in objects.get('attributes'):
                    self.objectStore[objects]['attributes'][k] = list()
                    self.objectStore[objects]['attributes'][k].append((currentTime, v))


            return 0

        except:
            output("Json file not in correct syntax")
            output("STACK TRACE")
            print(traceback.print_exc())
            return -1

    def run():
        while True:
            if await(some(received('read_request', object, attribute, timestamp, sender))):
                #processReadRequest(object,attribute,timestamp,sender)
                pass
            elif await(some(received('write_request',object,attribute,timestamp,value))):
                #processWriteRequest(object,attribute,timestamp,value)
                pass

    def receive(msg=('read_request',object,attribute,timestamp,sender)):
        processReadRequest(object, attribute, timestamp, sender)

    def receive(msg=('write_request',object,attribute,timestamp,value)):
        processWriteRequest(object,attribute,timestamp,value)

    def processReadRequest(object,attribute,timestamp,sender):

        try:
            retVal = None
            timeStamps = []
            requiredTimeStamp = 0
            for values in self.objectStore[object]['attributes'][attribute]:
                timeStamps.append(values[0])
            timeStamps.sort()

            timeStamps = [ ts for ts in timeStamps if ts <=timestamp]

            requiredTimeStamp = timeStamps[-1]
            for values in self.objectStore[object]['attributes'][attribute]:
                if values[0] == requiredTimeStamp:
                    retVal = values[1]
            output("Db returning value ", retVal)
            send(('db_read_response', retVal),to = sender)
        except:
            output("Invalid arguments to processReadRequest")




    def processWriteRequest(object,attribute,timeStamp,value):
        try:
            self.objectStore[object]['attributes'][attribute].append((timeStamp, value))
        except KeyError:
            output("Invalid arguments to writeRequest")



