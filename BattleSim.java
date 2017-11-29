import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class BattleSim {
	
	Set<Mon> team1; 
	Set<Mon> team2; //pass these to represent state to nn
	
	HashMap<String, HashMap<String, Double>> atkMult = new HashMap<String, HashMap<String, Double>>(); //input attacking type to get a hashmap whose key is the defending type, to get the multiplier
	
	AI p1; //player input, simple original, nn
	AI p2;
	
	Mon activeP1;
	Mon activeP2;
	
	boolean battleComplete = false;
	
	HashMap<String, Move> validMoves = new HashMap<String, Move>(); //all valid moves in file
	
	
	
	public BattleSim(ArrayList<Mon> t1, String a1, ArrayList<Mon> t2, String a2) {
		team1 = new Team(t1);
		activeP1 = team1.lead();
		team2 = new Team(t2);
		activeP2 = team2.lead();
		
		p1=pickAI(a1);
		p2=pickAI(a2);
		
	}
	
	public boolean winner() { //true for player 1, false for player 2
		
	}
	
	
	public AI pickAI(String input) {
		
		
	}
	
	public String pickMove(int playerNum) { //1 for p1, 2 for p2
		
		AI player = p1;
		Set<Mon> team = team1;
		Mon active = activeP1;
		Set<Mon> oppTeam = team2;
		Mon activeOpp = activeP2;
		if(playerNum==2) {
			player = p2;
			team = team2;
			oppTeam = team1;
			activeOpp = activeP1;
		}
		String moveName = player.chooseMove(team, active, oppTeam, activeOpp, this.validMoves);
		return moveName;
		
	}
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		//process mon, move data
		
		//process args

		BattleSim sim = new BattleSim();
		//run battle
		while(!battleComplete) {
			
			//calculate who moves first
			String p1Move = sim.pickMove(1); //priority and someone fainting need to be accounted for
			String p2Move = sim.pickMove(2);
			if(p1Move.equals("SWTICH")) {
				if(p2Move.equals("SWITCH")) {
					if(sim.activeP1.getSpeed()>=sim.activeP2.getSpeed()) {
						sim.switchMon(1);
						sim.switchMon(2);
					}
					else {
						sim.switchMon(2);
						sim.switchMon(1);
					}
					
				}
				else {
					sim.activeP1 = sim.switchMon(1);
					Move move2 = sim.validMoves.get(p2Move);
					move2.attack(sim.activeP2, sim.activeP1);
				}
			}
			else if( p2Move.equals("SWITCH")) {
				sim.switchMon(2);
				Move move1 = sim.validMoves.get(p1Move);
				move1.attack(sim.activeP1, sim.activeP2);
			}
			else {
				Move move1 = sim.validMoves.get(p1Move);
				Move move2 = sim.validMoves.get(p2Move);
				if(sim.activeP1.getSpeed() >= sim.activeP2.getSpeed()) {
					move1.attack(sim.activeP1, sim.activeP2);
					move2.attack(sim.activeP2, sim.activeP1);
				}
			}
			
		}
		
		boolean winner = sim.winner();
		
		
	}

}
