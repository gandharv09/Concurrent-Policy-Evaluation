from classes import version as ver
from classes import request as req
from classes import attribute as att
import time

config(channel='fifo')

class Coordinator(process):
    def setup(numWorkers:int,coordinators:list,database:Database):

        self.versionMap = dict()
        self.cachedUpdates = dict()
        self.readQueue = list()
        self.writeQueue = list()

        output("In setup of coordinator process")

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
            output("Received readAttr from worker")
            updateReadAttr(sender, request, order)
        elif str == 'updateObj':
            output("Received readAttr from worker")
            updateWriteAttr(sender, request, order)



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


    def updateWriteAttr(sender, request, order):

        output("....Updating Write Attributes....")
        object = obj(request, order)

        if checkForConflict(obj, request) is not True:

            for K,V in request.updateAttributes.items():
                pendingList = latestVersionBefore(object, K, request.reqTs).pendingMightRead
                if len(pendingList) > 1 or (len(pendingList) == 1 and pendingList[0] != request.reqId):
                    for reqId in pendingList:
                        if reqId != request.reqId:
                            self.writeQueue.get(request).add(reqId)
                            return

            if checkForConflict(object, request) is not True:
                updateDB(request)
                updateCachedUpdates(object, request)
                updateLatesVersionBefore(object, request)

                for attr in defReadAttr(object, request):
                    v = latestVersionBefore(object, attr, request.reqTs)
                    v.pendingMightRead.remove(request.reqId)
                    if attr in request.readAttributes:
                        v.rts = request.reqTs

                for attr in mightReadAttr(object, request):
                    v = latestVersionBefore(object, attr, request.reqTs)
                    v.pendingMightRead.remove(request.reqId)
                    if attr in request.readAttributes:
                        v.rts = request.reqTs

    def updateCachedUpdates(obj, request):

        objCache = self.cachedUpdates.get(obj)
        for K,V in request.updateAttributes.items():
            if objCache.get(K) is not None:
                objCache.get(K).add(att(K, V, request.reqTs))
            else:
                objCache[K] = list()
                objCache[K].append(att(K, V, request.reqTs))

    def updateLatestVersionBefore(obj, request):


        if self.versionMap.get(obj) is None:
            self.versionMap[obj] = dict();

        for attr in request.updateAttributes:

            if self.versionMap.get(obj).get(attr) is None:
                self.versionMap[obj][attr] = list();

            self.versionMap[obj][attr].append(ver(0, request.reqTs))



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
                latestVersion = ver()
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

                latestAttr = att()
                for attrib in objCache.get(attr):
                    if attrib.ts <= request.reqTs and attrib.ts > latestAttr.ts:
                        latestAttr = attrib

                if latestAttr.ts != 0:
                    upd.append(latestAttr)

        for attr in mightReadAttr(object, request):
            if objCache.get(attr) is not None:

                latestAttr = att()
                for attrib in objCache.get(attr):
                    if attrib.ts <= request.reqTs and attrib.ts > latestAttr.ts:
                        latestAttr = attrib

                if latestAttr.ts != 0:
                    upd.append(latestAttr)

        return upd