import java.util.ArrayList;
import java.util.HashMap;

public class BasicAI implements AI {


	public String chooseMove(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
			HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups) {
		
		//find the move with the highest type multiplier
		double maxMult = -1;
		String multString = "";
		for(String moveStr : active.moves()) {
			Move move = validMoves.get(moveStr);
			String moveType = move.type;
			String defType1 = activeOpp.type1;
			double mult = typeMatchups.get(moveType).get(defType1);
			String defType2 = activeOpp.type2;
			if(!defType2.equals("NT")) {
				mult = mult * typeMatchups.get(moveType).get(defType2);
			}
			
			if(mult > maxMult) {
				maxMult = mult;
				multString = moveStr;
			}
		}
		
		if(maxMult > 1) { //if a super effective move is found, use it
			return multString;
		}
		
		//otherwise find the highest damage
		int maxDmg = 0;
		String dmgStr = "";
		for(String moveStr: active.moves()) {
			Move move = validMoves.get(moveStr);
			int moveDmg = move.damage;
			if(moveDmg > maxDmg) {
				maxDmg = moveDmg;
				dmgStr = moveStr;
			}
		}
		
		return dmgStr;
		
	}


	public Mon chooseSwitch(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp,
			HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups) {
		String activeName = active.name;
		Mon rtn = team.get(0);
		for(Mon pkmn : team) {
			if(pkmn.name.equals(activeName)) {
				continue;
			}
			rtn = pkmn;
			break;
		}
		return rtn;
	}

}
