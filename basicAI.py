import math
import random
import sys


class BasicAI(object):
    def __init__(self):

	def chooseMove(self, team, activeOpp, typeMatchups):
		# randomly choose an action
		randNum = random.randint(0,100);
		if(randNum%27==0):
			return "switch1"
		if(randNum%29==0):
			return "switch2"
		if(randNum%2==1):
			return "strong"
		return "quick"
