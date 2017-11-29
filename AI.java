import java.util.HashMap;
import java.util.Set;

public interface AI {
	
	
	
	public String chooseMove(Set<Mon> team, Mon active, Set<Mon> oppTeam, Mon activeOpp, HashMap<String, Move >validMoves) ;
	
	public Mon chooseSwitch(Set<Mon> team, Mon activeOpp);

}
