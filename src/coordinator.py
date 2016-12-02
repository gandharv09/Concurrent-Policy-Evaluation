from classes import version as ver
from classes import request as req
from classes import attribute as att
import time
output=print
config(channel='fifo')

class Coordinator(process):
    def setup(numWorkers:int,coordinators:list,database:Database):
        output("Inside setup of coordinator process")
        self.versionMap = dict()
        self.cachedUpdates = dict()
        self.readQueue = list()
        self.writeQueue = list()


    def run():
        if (await(some(received(('evalRequest',sender, request, order))))):
            pass
        if (await(some(received(('updateReadAttr',sender, request, order))))):
            pass
        if (await(some(received(('updateObj',sender, request, order))))):
            pass

    def receive(msg=(str,sender, request,order)):
        if str == 'evalRequest':
            output("Received Request from Client")
            evaluate(sender, request, order)
        elif str == 'updateReadAttr':
            output("Received updateReadAttr from worker")
            updateReadAttr(sender, request, order)
        elif str == 'updateObj':
            output("Received updateObj from worker")
            updateWriteAttr(sender, request, order)
        elif str == 'restartRequest':
            output("Received restartRequest from coordinator")
            restartRequest(sender, request, order)


    def restartRequest(sender, request, order):
        pass
    def evaluate(sender, request, order):

        output("....Evaluating Request....")
        object = obj(request, order)

        output("Processing object " + order)

        if request.isWriteReq is False:
            output("Request is of type Read-Only")

            for attr in defReadAttr(object, request):
                v = latestVersionBefore(object, attr, request.reqTs)
                v.rts = request.reqTs

            for attr in mightReadAttr(object, request):
                v = latestVersionBefore(object, attr, request.reqTs)
                v.pendingMightRead.add(request.reqId)

        else:
            output("Request is of type Write")

            for attr in defReadAttr(object, request):
                v = latestVersionBefore(object, attr, request.reqTs)
                v.pendingMightRead.add(request.reqId)

            for attr in mightReadAttr(object, request):
                v = latestVersionBefore(object, attr, request.reqTs)
                v.pendingMightRead.add(request.reqId)

        output("done with latesVersionBefore update")
        request.cachedUpdates[order] = cachedUpdates(object, request)
        output("done with cache update")

        if order == 1:
            coordinatorIndex = coord(obj(request, 2))
            if coordinators[coordinatorIndex] == self.id:
                evaluate(sender, request, 2)
            else:
                send(("evalRequest", self.id, request, 2), to=coordinators[coordinatorIndex])

        else:
            workerId = (Coordinator.workerNumber) % (self.numWorkers)
            Coordinator.workerNumber += 1
            output("Coordinator sending worker request")
            send(("workerRequest", request), to=self.workers[workerId])



    def updateReadAttr(sender, request, order):

        output("....Updating Read Attributes....")
        object = obj(request, order)

        for attr in mightReadAttr(object, request):
            v = latestVersionBefore(object, attr, request.reqTs)
            v.pendingMightRead.remove(request.reqId)
            if attr in request.readAttributes:
                v.rts = request.reqTs
        output("....Done Updating Read Attributes....")


    def updateWriteAttr(sender, request, order):

        output("....Updating Write Attributes....")
        object = obj(request, order)

        self.writeQueue[request] = list()

        output("Checking for first conflict")
        if checkForConflict(obj, request) is not True:
            output("conflict not found")

            for K,V in request.updateAttributes.items():
                pendingList = latestVersionBefore(object, K, request.reqTs).pendingMightRead
                if len(pendingList) > 1 or (len(pendingList) == 1 and pendingList[0] != request.reqId):
                    for reqId in pendingList:
                        if reqId != request.reqId:
                            output("adding conflicting read requests to write waiting queue and going to wait")
                            self.writeQueue.get(request).add(reqId)
                            return

            output("Checking for second conflict")
            if checkForConflict(object, request) is not True:
                output("conflict not found second time")

                output("....Updating DB....")
                updateDB(request)

                output("....Updating Cache....")
                updateCachedUpdates(object, request)

                output("....Updating Latest Version Before....")
                updateLatesVersionBefore(object, request)


                for attr in defReadAttr(object, request):
                    v = latestVersionBefore(object, attr, request.reqTs)
                    v.pendingMightRead.remove(request.reqId)
                    if attr in request.readAttributes[request.updatedObj]:
                        v.rts = request.reqTs

                for attr in mightReadAttr(object, request):
                    v = latestVersionBefore(object, attr, request.reqTs)
                    v.pendingMightRead.remove(request.reqId)
                    if attr in request.readAttributes[request.updatedObj]:
                        v.rts = request.reqTs

                self.writeQueue.remove(request)

                for K,V in self.readQueue.items():
                    if request.reqId in V:
                        V.remove(request.reqId)
                        if len(V) == 0:
                            self.readQueue.remove(K)
                            coordinatorIndex = coord(obj(request, 1))
                            send(("evalRequest", self.id, request, 1), to=coordinators[coordinatorIndex])




            else:
                output("Restarting Request because of conflict")
                restart(object, request)
        else:
            output("Restarting Request because of conflict")
            restart(object, request)

    def restart(obj, request):


    def updateCachedUpdates(obj, request):

        objCache = self.cachedUpdates.get(obj)
        for K,V in request.updateAttributes.items():
            if objCache.get(K) is not None:
                #objCache.get(K).add(att.Attribute(K, V, request.reqTs))
                objCache[k].append(att.Attribute(K, V, request.reqTs))
            else:
                objCache[K] = list()
                objCache[K].append(att.Attribute(K, V, request.reqTs))

    def updateLatestVersionBefore(obj, request):


        if self.versionMap.get(obj) is None:
            self.versionMap[obj] = dict();

        for attr in request.updateAttributes:

            if self.versionMap.get(obj).get(attr) is None:
                self.versionMap[obj][attr] = list();

            self.versionMap[obj][attr].append(ver.Version(0, request.reqTs))



    def updateDB(obj, request):

    def checkForConflict(obj, request):

        for K,V in request.updateAttributes.items():
            v = latesVersionBefore(obj, K, request.reqTs)
            if v.rts > request.reqTs:
                return True

        return False

    def defReadAttr(object, request):


    def mightReadAttr(object, request):


    def coord(object):
    # get coordinator for this object from object_coord_map

    def obj(request, i):

        writeObj = None
        writeObj = mightWriteObj(request)

        if writeObj is not None:
            if i == 1:
                request.reqTs = time.time()
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

    def latestVersionBefore(obj, attr, ts):

        latestVersion = None
        if self.versionMap.get(obj) is not None:
            attrMap = self.versionMap.get(obj)
            versionList = attrMap.get(attr)
            for version in versionList:
                if version.wts <= ts and version.wts > latestVersion.wts:
                    latestVersion = version


            if latestVersion is None:
                latestVersion = ver.Version()
                versionList.append(latestVersion)
        else:
            self.versionMap[obj] = dict()
            self.versionMap[obj][attr] = []
            self.versionMap[obj][attr].append(latestVersion)

        return latestVersion

    def cachedUpdates(object, request):

        upd = list();

        objCache = self.cachedUpdates.get(object)
        for attr in defReadAttr(object, request):
            if objCache.get(attr) is not None:

                latestAttr = att.Attribute()
                for attrib in objCache.get(attr):
                    if attrib.ts <= request.reqTs and attrib.ts > latestAttr.ts:
                        latestAttr = attrib

                if latestAttr.ts != 0:
                    upd.append(latestAttr)

        for attr in mightReadAttr(object, request):
            if objCache.get(attr) is not None:

                latestAttr = att.Attribute()
                for attrib in objCache.get(attr):
                    if attrib.ts <= request.reqTs and attrib.ts > latestAttr.ts:
                        latestAttr = attrib

                if latestAttr.ts != 0:
                    upd.append(latestAttr)

        return upd