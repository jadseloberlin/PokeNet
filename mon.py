class Mon(object):
    def __init__(self, species, health, atk, defe, spe, qMN, qmp, qma, qmt, sMN, smp, sma, smt, typeOne, typeTwo):
        self.name = species

        self.maxhp = health
        self.hp = self.maxhp

        self.attack = atk
        self.defense = defe
        self.speed = spe

        self.quickMoveName = qMN
        self.quickMovePower = qmp
        self.quickMoveAcc = qma
        self.quickMoveType = qmt
        self.strongMoveName = sMN
        self.strongMovePower = smp
        self.strongMoveAcc = sma
        self.strongMoveType = smt

        self.type1 = typeOne
        self.type2 = typeTwo

        self.active = None
        self.defeated = False

    def copy(self):
		rtn = Mon(self.name, self.maxhp, self.attack, self.defense, self.speed, self.quickMoveName, self.quickMovePower, self.quickMoveAcc, self.quickMoveType, self.strongMoveName, self.strongMovePower, self.strongMoveAcc, self.strongMoveType, self.type1, self.type2)
		return rtn
