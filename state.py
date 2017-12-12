class State(object):
    def __init__(self, monList, turns, user1Name, user1Active, user1HP, user1Atk, user1Def, user1Spe, user1Type1, user1Type2, user1QType, user1QDmg, user1QAcc, user1SType, user1SDmg, user1SAcc,
    user2Name, user2Active, user2HP, user2Atk, user2Def, user2Spe, user2Type1, user2Type2, user2QType, user2QDmg, user2QAcc, user2SType, user2SDmg, user2SAcc,
    user3Name, user3Active, user3HP, user3Atk, user3Def, user3Spe, user3Type1, user3Type2, user3QType, user3QDmg, user3QAcc, user3SType, user3SDmg, user3SAcc,
    oppName, oppHP, oppAtk, oppDef, oppSpe, oppType1, oppType2, oppQType, oppQDmg, oppQAcc, oppSType, oppSDmg, oppSAcc):

        self.fullMonList = monList

        self.turns = turns

        self.user1Name = user1Name
        self.user1Active = user1Active
        self.user1HP = user1HP
        self.user1Atk = user1Atk
        self.user1Def = user1Def
        self.user1Spe = user1Spe
        self.user1Type1 = user1Type1
        self.user1Type2 = user1Type2
        self.user1QType = user1QType
        self.user1QDmg = user1QDmg
        self.user1QAcc = user1QAcc
        self.user1SType = user1SType
        self.user1SDmg = user1SDmg
        self.user1SAcc = user1SAcc

        self.user2Name = user2Name
        self.user2Active = user2Active
        self.user2HP = user2HP
        self.user2Atk = user2Atk
        self.user2Def = user2Def
        self.user2Spe = user2Spe
        self.user2Type1 = user2Type1
        self.user2Type2 = user2Type2
        self.user2QType = user2QType
        self.user2QDmg = user2QDmg
        self.user2QAcc = user2QAcc
        self.user2SType = user2SType
        self.user2SDmg = user2SDmg
        self.user2SAcc = user2SAcc

        self.user3Name = user3Name
        self.user3Active = user3Active
        self.user3HP = user3HP
        self.user3Atk = user3Atk
        self.user3Def = user3Def
        self.user3Spe = user3Spe
        self.user3Type1 = user3Type1
        self.user3Type2 = user3Type2
        self.user3QType = user3QType
        self.user3QDmg = user3QDmg
        self.user3QAcc = user3QAcc
        self.user3SType = user3SType
        self.user3SDmg = user3SDmg
        self.user3SAcc = user3SAcc

        self.oppName = oppName
        self.oppHP = oppHP
        self.oppAtk = oppAtk
        self.oppDef = oppDef
        self.oppSpe = oppSpe
        self.oppType1 = oppType1
        self.oppType2 = oppType2
        self.oppQType = oppQType
        self.oppQDmg = oppQDmg
        self.oppQAcc = oppQAcc
        self.oppSType = oppSType
        self.oppSDmg = oppSDmg
        self.oppSAcc = oppSAcc

    def toList(self):
        rtn = []
        rtn.append(self.turns)

        #rtn.append(self.user1Name)
        u1NameList = self.processName(self.user1Name)
        for var in u1NameList:
            rtn.append(var)
        if(self.user1Active):
            rtn.append(1)
        else:
            rtn.append(0)
        rtn.append(self.user1HP)
        rtn.append(self.user1Atk)
        rtn.append(self.user1Def)
        rtn.append(self.user1Spe)
        #rtn.append(self.user1Type1)
        u1T1List = self.processType(self.user1Type1, True)
        u1T2List = self.processType(self.user1Type2, False)
        for var in u1T1List:
            rtn.append(var)
        for var in u1T2List:
            rtn.append(var)
    #    rtn.append(self.user1Type2)
        #rtn.append(self.user1QType)
        u1qtlist = self.processType(self.user1QType, True)
        for var in u1qtlist:
            rtn.append(var)
        rtn.append(self.user1QDmg)
        rtn.append(self.user1QAcc)
        #rtn.append(self.user1SType)
        u1stlist = self.processType(self.user1SType, True)
        for var in u1stlist:
            rtn.append(var)
        rtn.append(self.user1SDmg)
        rtn.append(self.user1SAcc)

        u2NameList = self.processName(self.user2Name)
        for var in u2NameList:
            rtn.append(var)
        #rtn.append(self.user2Name)
        if(self.user2Active):
            rtn.append(1)
        else:
            rtn.append(0)
        rtn.append(self.user2HP)
        rtn.append(self.user2Atk)
        rtn.append(self.user2Def)
        rtn.append(self.user2Spe)
        # rtn.append(self.user2Type1)
        # rtn.append(self.user2Type2)
        u2T1List = self.processType(self.user2Type1, True)
        u2T2List = self.processType(self.user2Type2, False)
        for var in u2T1List:
            rtn.append(var)
        for var in u2T2List:
            rtn.append(var)
        #rtn.append(self.user2QType)
        u2qtlist = self.processType(self.user2QType, True)
        for var in u2qtlist:
            rtn.append(var)
        rtn.append(self.user2QDmg)
        rtn.append(self.user2QAcc)
        #rtn.append(self.user2SType)
        u2stlist = self.processType(self.user2SType, True)
        for var in u2stlist:
            rtn.append(var)
        rtn.append(self.user2SDmg)
        rtn.append(self.user2SAcc)

        #rtn.append(self.user3Name)
        u3NameList = self.processName(self.user3Name)
        for var in u3NameList:
            rtn.append(var)
        if(self.user3Active):
            rtn.append(1)
        else:
            rtn.append(0)
        rtn.append(self.user3HP)
        rtn.append(self.user3Atk)
        rtn.append(self.user3Def)
        rtn.append(self.user3Spe)
        # rtn.append(self.user3Type1)
        # rtn.append(self.user3Type2)
        u3T1List = self.processType(self.user3Type1, True)
        u3T2List = self.processType(self.user3Type2, False)
        for var in u3T1List:
            rtn.append(var)
        for var in u3T2List:
            rtn.append(var)
        #rtn.append(self.user3QType)
        u3qtlist = self.processType(self.user3QType, True)
        for var in u3qtlist:
            rtn.append(var)
        rtn.append(self.user3QDmg)
        rtn.append(self.user3QAcc)
        #rtn.append(self.user3SType)
        u3stlist = self.processType(self.user3SType, True)
        for var in u3stlist:
            rtn.append(var)
        rtn.append(self.user3SDmg)
        rtn.append(self.user3SAcc)

        oppNameList = self.processName(self.oppName)
        for var in oppNameList:
            rtn.append(var)
    #    rtn.append(self.oppName)
        rtn.append(self.oppHP)
        rtn.append(self.oppAtk)
        rtn.append(self.oppDef)
        rtn.append(self.oppSpe)
        # rtn.append(self.oppType1)
        # rtn.append(self.oppType2)
        oppT1List = self.processType(self.oppType1, True)
        oppT2List = self.processType(self.oppType2, False)
        for var in oppT1List:
            rtn.append(var)
        for var in oppT2List:
            rtn.append(var)
        #rtn.append(self.oppQType)
        oppqtlist = self.processType(self.oppQType, True)
        for var in oppqtlist:
            rtn.append(var)
        rtn.append(self.oppQDmg)
        rtn.append(self.oppQAcc)
        #rtn.append(self.oppSType)
        oppstlist = self.processType(self.oppSType, True)
        for var in oppstlist:
            rtn.append(var)
        rtn.append(self.oppSDmg)
        rtn.append(self.oppSAcc)

        rtn2 = [rtn]
        return rtn2

    def processName(self,name):
        rtn = [0] * len(self.fullMonList)
        rtn[self.fullMonList.index(name)] = 1
        return rtn

    def processType(self,type, primary):
        typeList = ["fire", "water", "grass", "bug", "ghost","psychic","dragon","electric", "rock", "ice", "poison", "normal", "ground","fighting","flying","dark","steel","fairy"]
        if (not primary):
            typeList.append("none")
        rtn = [0] * len(typeList)
        rtn[typeList.index(type)] = 1
        return rtn
