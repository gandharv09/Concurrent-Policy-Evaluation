from classes import request as req
import time

id = 0;
class Client(process):
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

    def sendRequest():
        # This function sends requests to the subject coordinators by reading from the config file .

        if not os.path.exists(configFile):
            output("Config file %s not found"%configFile)
            sys.exit(-1)

        pseudoRandom=False
        configData=open(configFile).read()
        configData=json.loads(configData)

        if configData.get('globalConfig').get('pseudoRandom') is not None:
            output("Psuedo Random Requests Specified by user")
            # user wants pseudo random requests.
            numRequests=int(configData.get('globalConfig').get('numRequests'))
            output("User wants to generate ",numRequests,"requests")
            pseudoRandom=True
        requestSent=0


        for i in range(len(configData.get('scenarios'))):
            output("Pseudo Random is ",pseudoRandom)
            if  pseudoRandom == False:

                scenarios = configData.get('scenarios')[i]
            else:
                # generate a random request.
                idx=(random.randint(0,len(configData.get('scenarios'))-1))
                scenarios=configData.get('scenarios')[idx]
                output("Randomly picked request no ",idx)


            request = req.Request()
            request.clientId = self.id
            request.objects.append(scenarios.get('subject'))
            request.objects.append(scenarios.get('resource'))
            request.action = scenarios.get('action')
            request.reqId = Client.id
            Client.id += 1
            request.reqTs = int(time.time())

            if mightWriteObj(request) is not None:
                request.isWriteReq = True

            coordinatorIndex = coord(obj(request, 1))
            send(("evalRequest",self.id, request, 1),to=coordinators[coordinatorIndex])
            requestSent+=1
            output(" Application Sending message to coordinator\n")
            if pseudoRandom and requestSent == numRequests:
                output(" we are done with sending all the requests that the user wants.")
                break


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
        output("Application received a message ", a)
        if a == 'resp_from_coordinator':
            output("Application Received Decision for resource ",b.reqId)


    def mightWriteObj(request):
        