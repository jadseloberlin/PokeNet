import java.util.ArrayList;
import java.util.HashMap;
import java.util.Set;

public class BattleSim {
	
	Array team1; 
	ArrayList<Mon> team2; //pass these to represent state to nn
	
	HashMap<String, HashMap<String, Double>> atkMult = new HashMap<String, HashMap<String, Double>>(); //input attacking type to get a hashmap whose key is the defending type, to get the multiplier
	
	AI p1; //player input, simple original, nn
	AI p2;
	
	Mon activeP1;
	Mon activeP2;
	
	
	HashMap<String, Move> validMoves = new HashMap<String, Move>(); //all valid moves in file
	
	
	
	public BattleSim(ArrayList<Mon> t1, String a1, ArrayList<Mon> t2, String a2) { //FIX THIS
		team1 = t1;
		activeP1 = team1.get(0);
		team2 = t2;
		activeP2 = team2.get(0);
		
		p1=pickAI(a1);
		p2=pickAI(a2);
		
	}
	
	public boolean winner() { //true for player 1, false for player 2
		return(team2.isEmpty());
	}
	
	
	public AI pickAI(String input) {
		
		
	}
	
	public String pickMove(int playerNum) { //1 for p1, 2 for p2
		
		AI player = p1;
		ArrayList<Mon> team = team1;
		Mon active = activeP1;
		ArrayList<Mon> oppTeam = team2;
		Mon activeOpp = activeP2;
		if(playerNum==2) {
			player = p2;
			team = team2;
			oppTeam = team1;
			activeOpp = activeP1;
			active = activeP2;
		}
		String moveName = player.chooseMove(team, active, oppTeam, activeOpp, this.validMoves, atkMult);
		return moveName;
		
	}
	
	private void switchMon(int playerNum) {
		AI player = p1;
		ArrayList<Mon> team = team1;
		Mon active = activeP1;
		ArrayList<Mon> oppTeam = team2;
		Mon activeOpp = activeP2;
		if(playerNum==2) {
			player = p2;
			team = team2;
			oppTeam = team1;
			activeOpp = activeP1;
			active = activeP2;
		}
		Mon newActive = player.chooseSwitch(team, active, oppTeam, activeOpp, this.validMoves, atkMult);
		if(playerNum==1) {
			this.activeP1=newActive;
		}
		else {
			this.activeP2=newActive;
		}
		
	}
	
	public void fainted(int playerNum, Mon knockedOut) {
		ArrayList<Mon> team = team1;
		if(playerNum==2) {
			team = team2;
		}		
		switchMon(playerNum);
		team.remove(0);
	}
	
	public boolean battleComplete() {
		return(team1.isEmpty()||team2.isEmpty());
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		//process mon, move data
		
		//process args

		BattleSim sim = new BattleSim();
		//run battle
		while(!sim.battleComplete()) {
			
			//handle edge cases appropriately
			
			//KEEP A LOG OF BATTLE
			
			//calculate who moves first
			String p1Move = sim.pickMove(1);
			String p2Move = sim.pickMove(2);
			if(p1Move.equals("SWTICH")) {
				if(p2Move.equals("SWITCH")) {
					//if they both switch
					if(sim.activeP1.getSpeed()>=sim.activeP2.getSpeed()) {
						//p1 is faster
						sim.switchMon(1);
						sim.switchMon(2);
					}
					else {
						//p2 is faster
						sim.switchMon(2);
						sim.switchMon(1);
					}
					
				}
				else {
					//only p1 switches
					sim.switchMon(1);
					Move move2 = sim.validMoves.get(p2Move);
					if(move2.attack(sim.activeP2, sim.activeP1)) { //if there's a bug, look here to move this to its own line
						//p2 ko's p1
						sim.fainted(1, sim.activeP1);
					}
					
				}
			}
			else if( p2Move.equals("SWITCH")) {
				//only p2 switches
				sim.switchMon(2);
				Move move1 = sim.validMoves.get(p1Move);
				if( move1.attack(sim.activeP1, sim.activeP2)) {
					//p1 ko's p2
					sim.fainted(2, sim.activeP2);
				}
			}
			else {
				
				//no one switches
				Move move1 = sim.validMoves.get(p1Move);
				Move move2 = sim.validMoves.get(p2Move);
				if(move1.priority()>move2.priority()) {
					//p1 has higher priority
					if(move1.attack(sim.activeP1, sim.activeP2)) {
						//p1 ko's p2
						sim.fainted(2, sim.activeP2);
					}
					else {
						//p1 doesn't ko p2
						if(move2.attack(sim.activeP2, sim.activeP1)) {
							//p2 ko's p1
							sim.fainted(1, sim.activeP1);
						}
						
					}
				}
				else if(move2.priority()>move1.priority()) {
					//p2 has higher priority
					if(move2.attack(sim.activeP2, sim.activeP1)) {
						//p2 ko's p1
						sim.fainted(1, sim.activeP1);
					}
					else{
						//p2 doesn't ko p1
						if(move1.attack(sim.activeP1, sim.activeP2)) {
							//p1 ko's p2
							sim.fainted(2, sim.activeP2);
						}
					}
				}
				else {
					//same priority, should be most moves
					if(sim.activeP1.getSpeed() >= sim.activeP2.getSpeed()) {
						//p1 is faster
						if(move1.attack(sim.activeP1, sim.activeP2)) {
							//p1 ko's p2
							sim.fainted(2, sim.activeP2);
						}
						else {
							//p1 doesn't ko p2
							if(move2.attack(sim.activeP2, sim.activeP1)) {
								//p2 ko's p1
								sim.fainted(1, sim.activeP1);
							}
							
						}
					}
					else {
						//p2 is faster
						if(move2.attack(sim.activeP2, sim.activeP1)) {
							//p2 ko's p1
							sim.fainted(1, sim.activeP1);
						}
						else{
							//p2 doesn't ko p1
							if(move1.attack(sim.activeP1, sim.activeP2)) {
								//p1 ko's p2
								sim.fainted(2, sim.activeP2);
							}
						}
					}
				}
				
			}
			
		}
		
		boolean winner = sim.winner();
		
		
	}

	

}
