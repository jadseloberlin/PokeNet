class State(object):
    def __init__(self, turns, user1Name, user1Active, user1HP, user1Atk, user1Def, user1Spe, user1Type1, user1Type2, user1QType, user1QDmg, user1QAcc, user1SType, user1SDmg, user1SAcc,
    user2Name, user2Active, user2HP, user2Atk, user2Def, user2Spe, user2Type2, user2Type2, user2QType, user2QDmg, user2QAcc, user2SType, user2SDmg, user2SAcc,
    user3Name, user3Active, user3HP, user3Atk, user3Def, user3Spe, user3Type3, user3Type2, user3QType, user3QDmg, user3QAcc, user3SType, user3SDmg, user3SAcc,
    oppName, oppHP, oppAtk, oppDef, oppSpe, oppType1, oppType2, oppQType, oppQDmg, oppQAcc, oppSType, oppSDmg, oppSAcc):

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
        self.oppActive = oppActive
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

        #do we need the full opponent team ?
