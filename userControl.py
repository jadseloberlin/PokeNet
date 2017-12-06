import sys

class UserControl(object):
    def __init__(self):
        self.nothing = 0

    def chooseMove(self, team, activeOpp, typeMatchups):
        move = input("Please type in move from move list: switch1, switch2, strong, quick :   "  )
        while((not (move == "quick") ) and (not (move == "strong")) and (not (move == "switch1")) and (not (move =="switch2")) ):
            move = input("Plese choose a valid move: switch1, switch2, strong, quick :  ")
        return move

	# def chooseMove(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
	# 		HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups):
    #
    #
	# def chooseSwitch(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
	# 		HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups):
