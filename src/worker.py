from xml.etree import ElementTree as ET
import os
d = import_da("database")

class Worker(process):

    def setup(coordinatorList:list, dbProcess:Database, policyFile:str):
        self.dbProcess=dbProcess
        self.coordinatorList = coordinatorList
        if not os.path.exists(policyFile):
            output("ERROR:Policy File does not exist")
        else:
            # policy file exists and is proper.
            self.policyFile = policyFile

    def run():
        if await(some(received('evalRequest',request))):
            pass
        if await(some(received('dbResponse',response))):
            pass

    def receive(a,b):
        if a == 'evalRequest':
            output("Worker received evalRequest from coordinator")
            processCoordinatorRequest(b)
        if a == 'dbResponse':
            output("Worker received response from db")
            processDBResponse(b)

    def processCoordinatorResponse(request):
        send()
    def findRule(request):
        try:
            tree = ET.parse(policyFile)
            root = tree.getroot()
            for rule in root.iter('rule'):


                if rule.get('action').attrib('name') == request.action:
                        # possible candidate as action matches.
                    if request.objects[0].find(rule.get('subjectCondition').attrib('position'))!=-1:
                            # subject condition matched
                            # check for resource condition
                        if request.objects[1] == rule.get('resourceCondition').attrib('type'):
                            # resource condition also matched, valid rule found.
                            return rule
            ## out of for loop , none of the rules matched ##
            return -1
        except :
            output("XML file not in proper syntax")
            return -1


    def evaluatePolicy(request):
            output("Inside Worker Evaluate Policy")
            ################################################################
            #                                                              #
            # 1. Check for view Count attribute for movie                  #
            # 2. If viewCount exceeds then check for subscription type     #
            # 3. If both conditions return False, return False , else True #
            ################################################################
            matchedRule = findRule(request)
            if matchedRule == -1 :
                # none of the rules matched return False
                output("None of the rules matched for this request.")
                request.decision = False
                # send
            else:
                # rule matched.
                condition = matchedRule.get('resourceCondition').attrib('viewCount')
                output("Need to validate that viewCount ",condition)
                # first check for value in the cached updated in request.
                output("Checking request cached updates for value")
                if request.cachedUpdates.get(request.objects[1]) is not None:
                    currentViewCount = request.cachedUpdates.get(request.objects[1]).get('viewCount')
                    allowedViewCount = int(condition[1:])
                    if (currentViewCount < allowedViewCount) :
                        # valid , need to increment viewCount and return.
                        request.updateAttributes['viewCount'] = currentViewCount + 1
                        request.updatedObj = 1
                        request.readAttributes.append('viewCount')
                        request.decision = True
                    else:
                        # viewCount already exhausted , need to check subscription type



