import java.util.ArrayList;
import java.util.HashMap;

public interface AI {
	
	
	
	public String chooseMove(Mon[] team, Mon activeOpp, HashMap<String, HashMap<String, Double>> typeMatchups) ;
	
	//public Mon chooseSwitch(ArrayList<Mon> team, Mon active, ArrayList<Mon> oppTeam, Mon activeOpp, HashMap<String, Move> validMoves, HashMap<String, HashMap<String, Double>> typeMatchups);

}
