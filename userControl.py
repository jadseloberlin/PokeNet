import sys

class UserControl(object):
    def __init__(self):

    def chooseMove(self, team, activeOpp, typeMatchups):
        move = input("Please type in move from move list: switch1, switch2, strong, quick :   "  )
        return move

	# def chooseMove(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
	# 		HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups):
    #
    #
	# def chooseSwitch(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
	# 		HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups):
