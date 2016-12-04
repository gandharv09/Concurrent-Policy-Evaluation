## Library file to have common methods to be used be client, coordinator. 

import json
def mightWriteObj(request):
    return request.mightWriteObj

def mightReadAttr(object, request):
    retAttr = []
    configFile = "../config/initDB.json"
    data = open(configFile).read()
    data = json.loads(data)
    #print("Request mightReadAttr is ",request.mightReadAttr)
    for attr in request.mightReadAttr:
        #print("------",attr,"-----")
        for objects in data.get('objects'):
            if objects.get('name') == object  :
                for k,v in objects.get('attributes').items():
                    #print("$$$$$$",k,"$$$$$$$")
                    if attr == v:
                        retAttr.append(v)
    print("mightReadAttr returning ",retAttr)
    return retAttr

def defReadAttr(object, request):
    #print("defReadAttr called with object ", object)
    retAttr = []
    configFile = "../config/initDB.json"
    data = open(configFile).read()
    data = json.loads(data)
    for attr in request.defReadAttr:
        
        for objects in data.get('objects'):
            if objects.get('name') == object  :
                for k,v in objects.get('attributes').items():
                    if attr == v:
                        retAttr.append(v)
    print("defReadAttr returning ",retAttr)
    return retAttr
def mightWriteAttr(request):
    return request.mightWriteAttr
def obj(request, i):
     print("In lib.obj i=",str(i))
     writeObj = mightWriteObj(request)


     if  len(writeObj) !=0:
            #  a write request.
            if i == 0:
                print("------------")
                print(request.objects[0])
                print(request.objects[1])
                print(writeObj)
                print("--------------")
                if request.objects[0] == writeObj[0]:
                    return request.objects[1]
                else:
                    print("About to return from lib")
                    return request.objects[0]

            else:
                print("Returning writeObject for i=2")
                return writeObj[0]
     else:
            if i == 0:
                return request.objects[0]
            else:
                return request.objects[1]

def coord(object, objectCoordinatorMap):
    if objectCoordinatorMap.get(object) is None:
        print("Invalid Object passed")
    else:
        return objectCoordinatorMap.get(object)
