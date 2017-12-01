class Instance(object):
    def __init__(self, inputDict, inputLabel):
        self.dict = inputDict
        self.label = inputLabel
        self.labelList = []
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

    def labelListProcess(self, labelList, binaryLabel):
        if binaryLabel == False:
            self.labelList = [0] * len(labelList)
            self.labelList[labelList.index(self.label)] = 1
        else:
            if labelList.index(self.label) == 0:
                self.labelList.append(0)
            else:
                self.labelList.append(1)
