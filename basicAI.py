import math
import random
import sys


class BasicAI(object):
    def __init__(self):
        self.nothing = 0
    def chooseMove(self, team, activeOpp, typeMatchups, turns):
        randNum = random.randint(0,100) # randomly choose an action
        if(randNum%27==0):
            return "switch1"
        if(randNum%29==0):
            return "switch2"
        if(randNum%2==1):
            return "strong"
        return "quick"
    def cleanUp(self):
        return True
