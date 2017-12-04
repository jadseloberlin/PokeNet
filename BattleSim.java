import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.Scanner;
import java.util.Set;

public class BattleSim {
	
	String[] types = {"fire", "water", "grass", "bug", "ghost","psychic","dragon","electric", "rock", "ice", "poison", "normal", "ground","fighting", "flying","none"};
	HashMap<String, Mon> validMon = new HashMap<String, Mon>();
	
	Mon[] team1 = new Mon[3]; 
	Mon[] team2 = new Mon[3]; 
	
	HashMap<String, HashMap<String, Double>> atkMult = new HashMap<String, HashMap<String, Double>>(); //input attacking type to get a hashmap whose key is the defending type, to get the multiplier
	//anything attacking type none is x1
	
	AI p1; //player input, simple original, nn
	AI p2;
	
	//Mon activeP1;
	//Mon activeP2;
	
	//labels: quick attack, strong attack, switch to 1st available, switch to 2nd available
	
	public HashMap<String,Double> createBasicMap(){
		HashMap<String, Double> rtn = new HashMap<String, Double>();
		for(String type : this.types) {
			rtn.put(type, 1.0);
		}
		return rtn;
	}
	public String contents(String[] par) {
		StringBuilder sb = new StringBuilder();
		sb.append("[");
		for(String str : par) {
			sb.append(str+", ");
		}
		sb.append("]");
		return sb.toString();
	}
	//varXY represents player X's Y'th pokemon
	public BattleSim(String p1AI, String p2AI, String p1Mon1, String p1Mon2, String p1Mon3, String p2Mon1, String p2Mon2, String p2Mon3) {
		//populate type matchups
		HashMap<String, Double> fireAttack = createBasicMap();
		
		fireAttack.put("fire", .5);
		fireAttack.put("water", .5);
		fireAttack.put("grass", 2.0);
		fireAttack.put("bug", 2.0);
		fireAttack.put("ice", 2.0);
		fireAttack.put("rock", .5);
		fireAttack.put("steel", 2.0);
		fireAttack.put("dragon", .5);
		this.atkMult.put("fire", fireAttack);
		
		HashMap<String, Double> waterAttack = createBasicMap();
		waterAttack.put("dragon", .5);
		waterAttack.put("grass", .5);
		waterAttack.put("fire", 2.0);
		waterAttack.put("rock",2.0);
		waterAttack.put("ground", 2.0);
		waterAttack.put("water", .5);
		this.atkMult.put("water", waterAttack);
		
		HashMap<String, Double> grassAttack = createBasicMap();
		grassAttack.put("water", 2.0);
		grassAttack.put("rock", 2.0);
		grassAttack.put("ground", 2.0);
		grassAttack.put("grass", .5);
		grassAttack.put("fire", .5);
		grassAttack.put("bug", .5);
		grassAttack.put("poison", .5);
		grassAttack.put("dragon", .5);
		grassAttack.put("flying", .5);
		grassAttack.put("steel", .5);
		this.atkMult.put("grass", grassAttack);
		
		HashMap<String, Double> electricAttack = createBasicMap();
		electricAttack.put("water", 2.0);
		electricAttack.put("ground", 0.0);
		electricAttack.put("flying", 2.0);
		electricAttack.put("dragon", .5);
		electricAttack.put("electric", .5);
		electricAttack.put("grass", .5);
		this.atkMult.put("electric", electricAttack);
		
		HashMap<String, Double> iceAttack = createBasicMap();
		iceAttack.put("ice", .5);
		iceAttack.put("steel", .5);
		iceAttack.put("water", .5);
		iceAttack.put("fire", .5);
		iceAttack.put("dragon", 2.0);
		iceAttack.put("flying", 2.0);
		iceAttack.put("grass", 2.0);
		iceAttack.put("ground", 2.0);
		this.atkMult.put("ice", iceAttack);
		
		HashMap<String, Double> ghostAttack = createBasicMap();
		ghostAttack.put("ghost", 2.0);
		ghostAttack.put("psychic", 2.0);
		ghostAttack.put("dark", .5);
		ghostAttack.put("normal", 0.0);
		this.atkMult.put("ghost", ghostAttack);
		
		HashMap<String, Double> groundAttack = createBasicMap();
		groundAttack.put("electric", 2.0);
		groundAttack.put("fire", 2.0);
		groundAttack.put("poison", 2.0);
		groundAttack.put("rock", 2.0);
		groundAttack.put("steel", 2.0);
		groundAttack.put("bug", .5);
		groundAttack.put("grass", .5);
		groundAttack.put("flying", 0.0);
		this.atkMult.put("ground", groundAttack);
		
		HashMap<String, Double> fairyAttack  = createBasicMap();
		fairyAttack.put("dark", 2.0);
		fairyAttack.put("dragon", 2.0);
		fairyAttack.put("fighting", 2.0);
		fairyAttack.put("fire", .5);
		fairyAttack.put("poison", .5);
		fairyAttack.put("steel", .5);
		this.atkMult.put("fairy", fairyAttack);
		
		HashMap<String, Double> bugAttack = createBasicMap();
		bugAttack.put("dark", 2.0);
		bugAttack.put("grass", 2.0);
		bugAttack.put("psychic", 2.0);
		bugAttack.put("fairy", .5);
		bugAttack.put("fighting", .5);
		bugAttack.put("flying", .5);
		bugAttack.put("ghost", .5);
		bugAttack.put("poison", .5);
		bugAttack.put("fire", .5);
		bugAttack.put("steel", .5);
		this.atkMult.put("bug", bugAttack);
		
		HashMap<String, Double> psychicAttack = createBasicMap();
		psychicAttack.put("fighting", 2.0);
		psychicAttack.put("poison", 2.0);
		psychicAttack.put("psychic", .5);
		psychicAttack.put("steel", .5);
		psychicAttack.put("dark", 0.0);
		this.atkMult.put("psychic", psychicAttack);
		
		HashMap<String, Double> poisonAttack = createBasicMap();
		poisonAttack.put("fairy", 2.0);
		poisonAttack.put("grass", 2.0);
		poisonAttack.put("ground", .5);
		poisonAttack.put("rock", .5);
		poisonAttack.put("ghost", .5);
		poisonAttack.put("poison", .5);
		poisonAttack.put("steel", 0.0);
		this.atkMult.put("poison", poisonAttack);
		
		HashMap<String, Double> rockAttack = createBasicMap();
		rockAttack.put("bug", 2.0);
		rockAttack.put("fire", 2.0);
		rockAttack.put("flying", 2.0);
		rockAttack.put("ice", 2.0);
		rockAttack.put("fighting", .5);
		rockAttack.put("ground",.5);
		rockAttack.put("steel", .5);
		this.atkMult.put("rock", rockAttack);
		
		HashMap<String, Double> flyingAttack = createBasicMap();
		flyingAttack.put("bug", 2.0);
		flyingAttack.put("fighting", 2.0);
		flyingAttack.put("grass", 2.0);
		flyingAttack.put("electric", .5);
		flyingAttack.put("rock", .5);
		flyingAttack.put("steel", .5);
		this.atkMult.put("flying", flyingAttack);
		
		HashMap<String, Double> normalAttack = createBasicMap();
		normalAttack.put("rock", .5);
		normalAttack.put("steel", .5);
		normalAttack.put("ghost", 0.0);
		this.atkMult.put("normal", normalAttack);
		
		HashMap<String, Double> steelAttack = createBasicMap();
		steelAttack.put("fairy",2.0);
		steelAttack.put("ice",2.0);
		steelAttack.put("rock", 2.0);
		steelAttack.put("electric",.5);
		steelAttack.put("fire", .5);
		steelAttack.put("steel",.5);
		steelAttack.put("water", .5);
		this.atkMult.put("steel", steelAttack);
		
		HashMap<String, Double> dragonAttack = createBasicMap();
		dragonAttack.put("dragon", 2.0);
		dragonAttack.put("steel", .5);
		dragonAttack.put("fairy", 0.0);
		this.atkMult.put("dragon", dragonAttack);
		
		HashMap<String, Double> fightingAttack = createBasicMap();
		fightingAttack.put("normal", 2.0);
		fightingAttack.put("dark", 2.0);
		fightingAttack.put("ice",2.0);
		fightingAttack.put("steel", 2.0);
		fightingAttack.put("rock",2.0);
		fightingAttack.put("bug", .5);
		fightingAttack.put("fairy",.5);
		fightingAttack.put("flying",.5);
		fightingAttack.put("poison", .5);
		fightingAttack.put("psychic", .5);
		fightingAttack.put("ghost",0.0);
		this.atkMult.put("fighting", fightingAttack);
		
		HashMap<String, Double> darkAttack = createBasicMap();
		darkAttack.put("ghost", 2.0);
		darkAttack.put("psychic", 2.0);
		darkAttack.put("dark", .5);
		darkAttack.put("fairy", .5);
		darkAttack.put("fighting", .5);
		this.atkMult.put("dark", darkAttack);
		
		
		
		//load AI
		if(p1AI.equals("user")) {
			p1 = new UserControl();
		}
		else if(p1AI.equals("nn")) {
		//	p1 = new PokeNet();
		}
		else if(p1AI.equals("basic")) {
			p1 = new BasicAI();
		}
		else {
			System.out.println("invalid ai for player 1");
			System.exit(1);
		}
		
		if(p2AI.equals("user")) {
			p2 = new BasicAI();
		}
		else if(p2AI.equals("nn")) {
		//	p2 = new PokeNet();
		}
		else if(p2AI.equals("basic")) {
			p2 = new BasicAI();
		}
		else {
			System.out.println("invalid ai for player 2");
			System.exit(1);
		}
		
		//load validMon
		Scanner s = null;
		try {
			s = new Scanner(new File("C:\\Users\\jadse\\eclipse-workspace\\PokeNet\\bin\\pokemon.csv"));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			System.out.println("cannot find list of valid pokemon");
			System.exit(1);
		}
		s.nextLine();
		while(s.hasNextLine()) {
			String[] lineparts = s.nextLine().split(","); 
			String name = lineparts[0];
			//System.out.println(contents(lineparts));
			validMon.put(name, new Mon(name, Integer.parseInt(lineparts[1]), Integer.parseInt(lineparts[2]),Integer.parseInt(lineparts[3]),
					Integer.parseInt(lineparts[4]), lineparts[5], Integer.parseInt(lineparts[6]), Integer.parseInt(lineparts[7]),
					lineparts[8], lineparts[9],Integer.parseInt(lineparts[10]),Integer.parseInt(lineparts[11]),lineparts[12],
					lineparts[13], lineparts[14]));
		}
		//load teams
		Mon m11 = validMon.get(p1Mon1).copy();
		m11.active=true;
		Mon m12 = validMon.get(p1Mon2).copy();
		Mon m13 = validMon.get(p1Mon3).copy();
		Mon m21 = validMon.get(p2Mon1).copy();
		m21.active=true;
		Mon m22 = validMon.get(p2Mon2).copy();
		Mon m23 = validMon.get(p2Mon3).copy();
		team1[0]=m11;
		team1[1]=m12;
		team1[2]=m13;
		team2[0]=m21;
		team2[1]=m22;
		team2[2]=m23;
	}
	public boolean isDefeated(Mon[] team) {//returns whether or not team has no usable Pokemon left
		
		return team[0].defeated&&team[1].defeated&team[2].defeated;
	}
	
	public Mon active(Mon[] team) {
		if(team[0].active) {
			return team[0];
		}
		else if(team[1].active) {
			return team[1];
		}
		else {
			return team[2];
		}
	}
	
	public void switch1(Mon[] team) { //what if nothing to switch to
		if(team[0].active) {
			if(!team[1].defeated) {
				team[0].active=false;
				team[1].active=true;
				if(team[0].defeated) {
					System.out.println(team[0].name+ " fainted!");
					System.out.println("Go, "+team[1].name+"!");
				}
				else {
					System.out.println(team[0].name+"  is switching out!");
					System.out.println("Go, "+team[1].name+"!");
				}
				return;
			}
			else if(!team[2].defeated) {
				team[0].active=false;
				team[2].active=true;
				if(team[0].defeated) {
					System.out.println(team[0].name+ " fainted!");
					System.out.println("Go, "+team[2].name+"!");
				}
				else {
					System.out.println(team[0].name+"  is switching out!");
					System.out.println("Go, "+team[2].name+"!");
				}
				return;
			}
			else {
				return;
			}
		}
		
		else if(team[1].active) {
			if(!team[2].defeated) {
				team[1].active=false;
				team[2].active=true;
				if(team[1].defeated) {
					System.out.println(team[1].name+ " fainted!");
					System.out.println("Go, "+team[2].name+"!");
				}
				else {
					System.out.println(team[1].name+"  is switching out!");
					System.out.println("Go, "+team[2].name+"!");
				}
				return;
			}
			else if(!team[0].defeated) {
				team[1].active=false;
				team[0].active=true;
				if(team[1].defeated) {
					System.out.println(team[1].name+ " fainted!");
					System.out.println("Go, "+team[0].name+"!");
				}
				else {
					System.out.println(team[1].name+"  is switching out!");
					System.out.println("Go, "+team[0].name+"!");
				}
				return;
			}
			else {
				return;
			}
		}
		else if(team[2].active) {
			if(!team[0].defeated) {
				team[2].active=false;
				team[0].active=true;
				if(team[2].defeated) {
					System.out.println(team[2].name+ " fainted!");
					System.out.println("Go, "+team[0].name+"!");
				}
				else {
					System.out.println(team[2].name+"  is switching out!");
					System.out.println("Go, "+team[0].name+"!");
				}
				return;
			}
			else if(!team[1].defeated) {
				team[2].active=false;
				team[1].active=true;
				if(team[2].defeated) {
					System.out.println(team[2].name+ " fainted!");
					System.out.println("Go, "+team[1].name+"!");
				}
				else {
					System.out.println(team[2].name+"  is switching out!");
					System.out.println("Go, "+team[1].name+"!");
				}
				return;
			}
			else {
				return;
			}
		}
		else {
			return;
		}
	}
	
	public void switch2(Mon[] team) {
		if(team[0].active) {
			if(!team[2].defeated) {
				team[0].active=false;
				team[2].active=true;
				if(team[0].defeated) {
					System.out.println(team[0].name+ " fainted!");
					System.out.println("Go, "+team[2].name+"!");
				}
				else {
					System.out.println(team[0].name+"  is switching out!");
					System.out.println("Go, "+team[2].name+"!");
				}
				return;
			}
			else if(!team[1].defeated) {
				team[0].active=false;
				team[1].active=true;
				if(team[0].defeated) {
					System.out.println(team[0].name+ " fainted!");
					System.out.println("Go, "+team[1].name+"!");
				}
				else {
					System.out.println(team[0].name+"  is switching out!");
					System.out.println("Go, "+team[1].name+"!");
				}
				return;
			}
			else {
				return;
			}
		}
		else if(team[1].active) {
			if(!team[0].defeated) {
				team[1].active=false;
				team[0].active=true;
				if(team[1].defeated) {
					System.out.println(team[1].name+ " fainted!");
					System.out.println("Go, "+team[0].name+"!");
				}
				else {
					System.out.println(team[1].name+"  is switching out!");
					System.out.println("Go, "+team[0].name+"!");
				}
				return;
			}
			else if(!team[2].defeated) {
				team[1].active=false;
				team[2].active=true;
				if(team[1].defeated) {
					System.out.println(team[1].name+ " fainted!");
					System.out.println("Go, "+team[2].name+"!");
				}
				else {
					System.out.println(team[1].name+"  is switching out!");
					System.out.println("Go, "+team[2].name+"!");
				}
			}
			else {
				return;
			}
		}
		else if(team[2].active){
			if(!team[1].defeated) {
				team[2].active=false;
				team[1].active=true;
				if(team[2].defeated) {
					System.out.println(team[2].name+ " fainted!");
					System.out.println("Go, "+team[1].name+"!");
				}
				else {
					System.out.println(team[2].name+"  is switching out!");
					System.out.println("Go, "+team[1].name+"!");
				}
				return;
			}
			else if(!team[0].defeated) {
				team[2].active=false;
				team[0].active=true;
				if(team[2].defeated) {
					System.out.println(team[2].name+ " fainted!");
					System.out.println("Go, "+team[0].name+"!");
				}
				else {
					System.out.println(team[2].name+"  is switching out!");
					System.out.println("Go, "+team[0].name+"!");
				}
				return;
			}
			else {
				return;
			}
		}
		else {
			return;
		}
	}
	
	public boolean quick(Mon attacker, Mon target, Mon[] targetTeam) { //returns true if target faints
		
		System.out.println(attacker.name+" is using "+attacker.quickMoveName+ " on "+target.name+"!");
		int accCheck = new Random().nextInt(100); //accuracy needs to be higher than accCheck to land
		if(attacker.quickMoveAcc <= accCheck) {
			System.out.println("But it missed!");
			return false;
		}
		double damage = attacker.attack+attacker.quickMovePower-target.defense;
		double multiplier = 1;
		multiplier = multiplier * this.atkMult.get(attacker.quickMoveType).get(target.type1);
		multiplier = multiplier * this.atkMult.get(attacker.quickMoveType).get(target.type2);
		if(multiplier > 1) {
			System.out.println("It's super effective!");
		}
		else if (multiplier==0) {
		//	System.out.println(attacker.quickMoveType+" attacked "+target.type1+","+target.type2);
			System.out.println("It didn't have any effect...");
			return false;
		}
		else if(multiplier < 1 ) {
			System.out.println("It's  not very effective...");
		}
		damage = damage * multiplier;
		target.hp = target.hp - (int) damage;
		
		if(target.hp < 1) {
			target.defeated=true;
			if(!isDefeated(targetTeam)) {
				switch1(targetTeam);
			}
			return true;
		}
		return false;
		
	}
	
	public boolean strong(Mon attacker, Mon target, Mon[] targetTeam) { //returns true if target faints
		System.out.println(attacker.name+" is using "+attacker.strongMoveName+ " on "+target.name+"!");
		int accCheck = new Random().nextInt(100); //accuracy needs to be higher than accCheck to land
		if(attacker.strongMoveAcc <= accCheck) {
			System.out.println("But it missed!");
			return false;
		}
		int damage = attacker.attack+attacker.strongMovePower-target.defense;
		double multiplier = 1;
		multiplier = multiplier * this.atkMult.get(attacker.strongMoveType).get(target.type1);
		multiplier = multiplier * this.atkMult.get(attacker.strongMoveType).get(target.type2);
		if(multiplier > 1) {
			System.out.println("It's super effective!");
		}
		else if (multiplier==0) {
		//	System.out.println(attacker.strongMoveType+" attacked "+target.type1+","+target.type2);
			System.out.println("It didn't have any effect...");
			return false;
		}
		else if(multiplier < 1 ) {
			System.out.println("It's  not very effective...");
		}
		target.hp = target.hp - damage;
		if(target.hp < 1) {
			target.defeated=true;
			if(!isDefeated(targetTeam)) {
				switch1(targetTeam);
			}
			return true;
		}
		return false;
		
	}
	
	public boolean battle() {
		return this.battle(team1, team2);
	}
	
	//returns true if p1 wins, false if p2 wins
	public boolean battle(Mon[] teamNum1, Mon[] teamNum2) {
		
		int turns = 0;
		while(!isDefeated(teamNum1)&&!isDefeated(teamNum2)) {
			
			System.out.println("This is turn number "+(++turns));
			Mon active1 = active(teamNum1);
			Mon active2 = active(teamNum2);
			String move1 = p1.chooseMove(teamNum1, active2, atkMult);
			String move2 = p2.chooseMove(teamNum2, active1, atkMult);
			if(move1.equals("switch1")){
				//if player 1 is switching to first available 
				if(move2.equals("switch1")) {
					//if player 2 is also switching to first
					if(active1.speed>=active2.speed) {
						//if p1 is faster
						switch1(teamNum1);
						switch1(teamNum2);
					}
					else {
						//if p2 is faster
						switch1(teamNum2);
						switch1(teamNum1);
					}
				}
				else if(move2.equals("switch2")) {
					//if p2 is switching to second available
					if(active1.speed>=active2.speed) {
						//if p1 is faster
						switch1(teamNum1);
						switch2(teamNum2);
					}
					else {
						//if p2 is faster
						switch2(teamNum2);
						switch1(teamNum1);
					}
				}
				else if(move2.equals("quick")) {
					//p2 is attacking quickly
					switch1(teamNum1);
					quick(active2, active(teamNum1), teamNum1);
				}
				else {
					//p2 is attacking strongly
					switch1(teamNum1);
					strong(active2, active(teamNum1), teamNum1);
				}
			}
			else if(move1.equals("switch2")) {
				//p1 switches to second available
				if(move2.equals("switch2")) {
					//if player 2 is also switching to second
					if(active1.speed>=active2.speed) {
						//if p1 is faster
						switch2(teamNum1);
						switch2(teamNum2);
					}
					else {
						//if p2 is faster
						switch2(teamNum2);
						switch2(teamNum1);
					}
				}
				else if(move2.equals("switch1")) {
					//if p2 is switching to first available
					if(active1.speed>=active2.speed) {
						//if p1 is faster
						switch2(teamNum1);
						switch1(teamNum2);
					}
					else {
						//if p2 is faster
						switch1(teamNum2);
						switch2(teamNum1);
						
					}
				}
				else if(move2.equals("quick")) {
					//p2 is attacking quickly
					switch2(teamNum1);
					quick(active2, active(teamNum1), teamNum1);
				}
				else {
					//p2 is attacking strongly
					switch2(teamNum1);
					strong(active2, active(teamNum1), teamNum1);
				}
			}
			
			else if(move1.equals("quick")) {
				//p1 chooses quick
				if(move2.equals("switch1")) {
					//p2 switches to first available
					switch1(teamNum2);
					quick(active1, active(teamNum2), teamNum2);
				}
				else if(move2.equals("switch2")) {
					//p2 switches to second available
					switch2(teamNum2);
					quick(active1, active(teamNum2), teamNum2);
				}
				else {
					//p2 attacks
					if(active1.speed>=active2.speed) {
						//p1 is faster
						quick(active1, active2,teamNum2);
						if(isDefeated(teamNum2)) continue;
						if(move2.equals("quick")) {
							//p2 uses a quick attack
							quick(active(teamNum2), active1, teamNum1);
						}
						else {
							//p2 uses a strong attack
							strong(active(teamNum2), active1, teamNum1);
						}
					}
					else {
						//p2 is faster
						if(move2.equals("quick")) {
							//p2 uses a quick attack
							quick(active2, active1, teamNum1);
						}
						else {
							//p2 uses a strong attack
							strong(active2, active1, teamNum1);
						}
						if(isDefeated(teamNum1)) {
							System.out.println(active1+" fainted!");
							continue;
						}
						quick(active(teamNum1), active2, teamNum2);
					}
				}
					
			}
			else {
				//p1 chooses strong
				if(move2.equals("switch1")) {
					//p2 switches to first available
					switch1(teamNum2);
					strong(active1, active(teamNum2), teamNum2);
				}
				else if(move2.equals("switch2")) {
					//p2 switches to second available
					switch2(teamNum2);
					strong(active1, active(teamNum2), teamNum2);
				}
				else {
					//p2 attacks
					if(active1.speed>=active2.speed) {
						//p1 is faster
						strong(active1, active2, teamNum2);
						if(isDefeated(teamNum2)) continue;
						if(move2.equals("quick")) {
							//p2 uses a quick attack
							quick(active(teamNum2), active1, teamNum1);
						}
						else {
							//p2 uses a strong attack
							strong(active(teamNum2), active1, teamNum1);
						}
					}
					else {
						//p2 is faster
						if(move2.equals("quick")) {
							//p2 uses a quick attack
							quick(active2, active1, teamNum1);
						}
						else {
							//p2 uses a strong attack
							strong(active2, active1, teamNum1);
						}
						if(isDefeated(teamNum1)) {
							System.out.println(active1.name+ " fainted!");
							continue;
						}
						strong(active(teamNum1), active2, teamNum2);
					}
				}
				
			}
			
					
			
			
			
			
			
		}
		
		
		return isDefeated(teamNum2);
		
	}
	
	
	public static void main(String[] args) {
		
		BattleSim sim = new BattleSim("basic", "basic", "charizard", "blastoise", "venusaur", "gyarados", "gengar", "arcanine");
		if(sim.battle()){
			System.out.println("P1 won!");
		}
		else {
			System.out.println("P2 won!");
		}
		
	}
	
	
	/*HashMap<String, Move> validMoves = new HashMap<String, Move>(); //all valid moves in file
	
	
	
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
		
		
	}*/

	

}
