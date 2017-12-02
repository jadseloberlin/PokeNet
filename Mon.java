//import java.util.HashMap;

public class Mon {
	
	String name;
	
	int maxhp;
	int hp;
	
	int attack;
	int defense;
	int speed;
	
	String quickMoveName;
	int quickMovePower;
	int quickMoveAcc;
	String quickMoveType;
	String strongMoveName;
	int strongMovePower;
	int strongMoveAcc;
	String strongMoveType;
	
	String type1;
	String type2;
	
	boolean active;
	boolean defeated = false;
	
	public Mon(String species, int health, int atk, int def, int spe, String qMN, int qmp, int qma, String qmt, String sMN, int smp, int sma, String smt, String typeOne, String typeTwo) {
		name = species;
		maxhp = health;
		attack = atk;
		defense = def;
		speed = spe;
		quickMoveName = qMN;
		quickMovePower = qmp;
		quickMoveAcc = qma;
		quickMoveType = qmt;
		strongMoveName = sMN;
		strongMovePower = smp;
		strongMoveAcc = sma;
		strongMoveType = smt;
		type1 = typeOne;
		type2 = typeTwo;
		
		hp = maxhp;
	}
	
	public Mon copy() {
		Mon rtn = new Mon(name, maxhp, attack, defense, speed, quickMoveName, quickMovePower, quickMoveAcc, quickMoveType, strongMoveName, strongMovePower, strongMoveAcc, strongMoveType, type1, type2);
		return rtn;
	}
	
	
	/*int level;
	String[] moves = new String[4]; //String[]?
	String type1;
	String type2; //"NT" if no type available
	
	//for all stat arrays, index 0 is base, index 1 is EV, index 2 is IV
	//we simulate with perfect IVs and EVs of 15 and 63
	double[] hpArr;
	double[] attackArr;
	double[] defenseArr;
	double[] specialArr;
	double[] speedArr;
	
	double maxhp;
	double attack;
	double defense;
	double special;
	double speed;
	
	double hp;
	
	int status; //-1 = healthy, 1 = paralysis, 2 = poison, 3 = burn, 4 = sleep, 5 = frozen
	HashMap<Integer, Boolean> secondaryStatus = new HashMap<Integer, Boolean>(); //1 = confusion, 2 = partially trapped, 3= solarbeam1, 4=sky attack1, 5 = rage, 6 = rest, 7 = thrash1, 8 = thrash2
	HashMap<Integer, Integer> statChanges; //keys: 1 for attack, 2 for defense, 3 for special, 4 for speed
	
	public void processStats(int stat) { //same as stat changes, except 0 is all stats
		//use statArr to memoize stat
		if(stat==1||stat==0) {
			int statStage = this.statChanges.get(1);
			this.attack = Math.floor((2*attackArr[0]+attackArr[1]+attackArr[2])*this.level/100+5 ) * Math.max(2, 2+statStage/Math.max(2, 2-statStage));
			if(this.status==3) this.attack = Math.floor(this.attack*.5);
		}
		if(stat==2||stat==0) {
			int statStage = this.statChanges.get(2);
			this.defense = Math.floor((2*defenseArr[0]+defenseArr[1]+defenseArr[2])*this.level/100+5 ) * Math.max(2, 2+statStage/Math.max(2, 2-statStage));
		}
		if(stat==3||stat==0) {
			int statStage = this.statChanges.get(3);
			this.special = Math.floor((2*specialArr[0]+specialArr[1]+specialArr[2])*this.level/100+5 ) * Math.max(2, 2+statStage/Math.max(2, 2-statStage));
		}
		if(stat==4||stat==0) {
			int statStage = this.statChanges.get(4);
			this.speed = Math.floor((2*speedArr[0]+speedArr[1]+speedArr[2])*this.level/100+5 ) * Math.max(2, 2+statStage/Math.max(2, 2-statStage));
			if(this.status==1) this.speed = Math.floor(this.speed*.25);
		}
		if(stat==0) {
			this.maxhp = Math.floor((2*this.hpArr[0]+hpArr[1]+hpArr[2])*this.level/100+this.level+10);
	
			hp = maxhp;
		}
	}
	
	public Mon(int lev, double hpBase, double atkBase, double defBase, double specBase, double speBase) {
		clearStatChanges();
		level = lev;
		double[] hpArr1 = {hpBase, 63, 15};
		hpArr=hpArr1;
		double[] attackArr1 = {atkBase, 63, 15};
		attackArr = attackArr1;
		double[] defArr = {defBase, 63, 15};
		defenseArr = defArr;
		double[] specArr = {specBase, 63, 15};
		specialArr = specArr;
		double[] speArr = {speBase, 63, 15};
		speedArr = speArr;
		
		processStats(0);
	}
	
	public void changeStatus(int st) {
		status = st;
	}
	
	public int status() {
		return this.status;
	}
	
	public boolean secStatus(int key) {
		return this.secondaryStatus.get(key);
	}
	
	public void activateSecStatus(int key) {
		this.secondaryStatus.put(key, true);
	}
	
	public void deactivateSecStatus(int key) {
		this.secondaryStatus.put(key, false);
	}
	
	public void statChange(int stat, int change) {
		int oldStat = this.statChanges.get(stat);
		this.statChanges.put(stat, oldStat+change);
		processStats(stat);
	}
	
	public void clearStatChanges() {
		for(int i = 1; i <=4; i++) {
			this.statChanges.put(i, 0);
		}
	}
	
	public boolean knockedOut() {
		return hp == 0;
	}
	
	public double getHP() {
		return hp;
	}
	
	public double getAtk() {
		return attack;
	}
	
	public double getDef() {
		return defense;
	}
	
	public double getSpecial() {
		return special;
	}
	
	public double getSpeed() {
		return speed;
	}
	
	public String[] moves() {
		return this.moves;
	}
	*/
}
