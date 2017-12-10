import sys

class UserControl(object):
    def __init__(self):
        self.nothing = 0

    def chooseMove(self, team, activeOpp, typeMatchups, turns):
        move = input("Please type in move from move list: switch1, switch2, strong, quick, exit:   "  )
        while((not (move == "quick") ) and (not (move == "strong")) and (not (move == "switch1")) and (not (move =="switch2")) and (not (move == "exit")) ):
            move = input("Plese choose a valid move: switch1, switch2, strong, quick, exit :  ")
        return move

	# def chooseMove(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
	# 		HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups):
    #
    #
	# def chooseSwitch(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
	# 		HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups):
