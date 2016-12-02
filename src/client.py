from classes import request as req
import os,json
output = print
import time

id = 0;
class Client(process):
    id = 0
    def setup(coordinators:list,configFile:str):
        output("Client setup with config file",configFile)

    def run():
        output("In run of client")
        while True:
            #send(('hello','hi'),to=coordinators[0])
            if(i == 0):
                sendRequest()
                i = i+1
            if (await(some(received(('resp_from_coordinator',b))))):
                    pass

    def sendRequest(self):
        # This function sends requests to the subject coordinators by reading from the config file .

        if not os.path.exists(self.configFile):
            output("ConfigFile does not exist")
        configData = open(self.configFile).read()
        try:
            configData = json.loads(configData)
        except :
            output("Config File not in proper json syntax")
            return
        for i in range(len(configData.get('scenarios'))):
            scenarios = configData.get('scenarios')[i]

            request = req.Request()
            request.clientId = self.id
            request.objects.append(scenarios.get('subject'))
            request.objects.append(scenarios.get('resource'))
            request.action = scenarios.get('action')
            if scenarios.get('defRead') is not None:
                request.defRead = [ attr for attr in scenarios.get('defRead').split(",")]
            if scenarios.get('mightRead') is not None:
                request.mightRead = [attr for attr in scenarios.get('mightRead').split(",")]
            if scenarios.get('mightWrite') is not None:
                request.mightWrite = [attr for attr in scenarios.get('mightWrite').split(",")]

            request.reqId = Client.id
            Client.id += 1
            request.reqTs = int(time.time())

        if len(mightWriteObj(request)) ==0:
            request.isWriteReq = True

        coordinatorIndex = coord(obj(request, 1))
        output(" Application Sending message to coordinator\n")
        send(("evalRequest",self.id, request, 1),to=coordinators[coordinatorIndex])



    def coord(object):
        #get coordinator for this object from object_coord_map

    def obj(request, i):

        writeObj = None
        writeObj = mightWriteObj(request)

        if  writeObj  is not None:
            if i == 1:

                if request.objects[0] == writeObj:
                    return request.objects[1]
                else:
                    return request.objects[0]

            else:
                return writeObj
        else:
            if i == 0:
                return request.objects[0]
            else:
                return request.objects[1]


    def receive(msg=(a,b)):
        #output("Application received a message ", a)
        if a == 'resp_from_coordinator':
            output("--------- DECISION RECEIVED------------")
            output("Application Received Decision for resource ",b.reqId)
            output(" Decision is ",b.decision)
            output("----------------------------------------")

    def mightWriteObj(request):
        return request.mightWrite
        