class Instance(object):
    def __init__(self, inputDict, inputLabel):
        self.dict = inputDict
        self.label = inputLabel
        #self.labelList = []
        self.attributeList = []

    def attributeListProcess(self, attributeValuesDictList, continuous, attList):
        for attribute in attList:
            if continuous[attribute] == True:
                self.attributeList.append(self.dict[attribute])
            else:
                value = self.dict[attribute]
                attValues = attributeValuesDictList[attribute]
                index = attValues.index(value)
                for i in range(1,len(attValues)):
                    if i == index:
                        #print("EQUAL TO INDEX!!")
                        self.attributeList.append(1)
                    else:
                        #print("NOT EQUAL TO INDEX!!")
                        self.attributeList.append(0)
    def attributeProcess(self, attribute):
        return 1

    def actionProcess(self, action):
        actionList = ["quick", "strong", "switch1", "switch2"]
        rtn = [0] * 4
        rtn[actionList.index(action)] = 1
        return rtn
