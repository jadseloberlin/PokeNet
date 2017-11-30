
public abstract class Move {
	
	String name;
	
	int damage;
	double accuracy;
	int priority; //0 at default
	boolean special;
	String type; //String type;
	
	int numHits; //number of times a move hits
	
	//returns true if defend faints
	public abstract boolean attack(Mon attack, Mon defend) ;
	
	public int priority() {
		return priority;
	}

}
