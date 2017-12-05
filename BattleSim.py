import os
import math
import nn

class BattleSim:
    types = ["fire", "water", "grass", "bug", "ghost","psychic","dragon","electric", "rock", "ice", "poison", "normal", "ground","fighting", "flying","none"]
    validMon = {}
    team1 = []
    team2 = []
    atkMult = {}
    p1 = None
    p2 = None

    def createBasicMap():
        rtn = {}
        for t in types:
            trn[t] = 1.0
        return rtn

    def contents(par):
