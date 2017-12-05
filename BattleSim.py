from copy import deepcopy
import os
import math
import nn
from userControl import UserControl
from basicAI import BasicAI
from mon import Mon

class BattleSim:
    types = ["fire", "water", "grass", "bug", "ghost","psychic","dragon","electric", "rock", "ice", "poison", "normal", "ground","fighting", "flying","dark","steel","fairy","none"]
    validMon = {}
    team1 = []
    team2 = []
    atkMult = {}
    p1 = None
    p2 = None

    def createBasicMap():
        rtn = {}
        for t in types:
            rtn[t] = 1.0
        return rtn

    def contents(par):
        sb = "["
        for s in par:
            sb += (s + ", ")
        sb += "]"
        return sb

    def BattleSim(p1AI, p2AI, p1Mon1, p1Mon2,  p1Mon3,  p2Mon1, p2Mon2,  p2Mon3):
        # populate type matchups
		fireAttack = createBasicMap()
		fireAttack["fire"] = .5
		fireAttack["water"] = .5;
		fireAttack.put["grass"] = 2.0
		fireAttack["bug"] = 2.0
		fireAttack["ice"] = 2.0
		fireAttack["rock"] = .5
		fireAttack["steel"] = 2.0
		fireAttack["dragon"] = .5
		atkMult["fire"] = fireAttack

		waterAttack = createBasicMap()
		waterAttack["dragon"] = .5
		waterAttack["grass"] = .5
		waterAttack["fire"] = 2.0
		waterAttack["rock"] = 2.0
		waterAttack["ground"] = 2.0
		waterAttack["water"] = .5
		atkMult["water"] = waterAttack

		grassAttack =  createBasicMap()
		grassAttack["water"] = 2.0
		grassAttack["rock"] = 2.0
		grassAttack["ground"] = 2.0
		grassAttack["grass"] = .5
		grassAttack["fire"] = .5
		grassAttack["bug"] = .5
		grassAttack["poison"] = .5
		grassAttack["dragon"] = .5
		grassAttack["flying"] = .5
		grassAttack["steel"] = .5
		atkMult["grass"] = grassAttack

		electricAttack = createBasicMap()
		electricAttack["water"] = 2.0
		electricAttack["ground"] = 0.0
		electricAttack["flying"] = 2.0
		electricAttack["dragon"] = .5
		electricAttack["electric"] = .5
		electricAttack["grass"] = .5
		atkMult["electric"] = electricAttack

		iceAttack = createBasicMap()
		iceAttack["ice"] = .5
		iceAttack["steel"] = .5
		iceAttack["water"] = .5
		iceAttack["fire"] = .5
		iceAttack["dragon"] = 2.0
		iceAttack["flying"] = 2.0
		iceAttack["grass"] = 2.0
		iceAttack["ground"] = 2.0
		atkMult["ice"] = iceAttack

		ghostAttack = createBasicMap()
		ghostAttack["ghost"] = 2.0
		ghostAttack["psychic"] = 2.0
		ghostAttack["dark"] = .5
		ghostAttack["normal"] = 0.0
	    atkMult["ghost"] = ghostAttack

		groundAttack = createBasicMap()
		groundAttack["electric"] = 2.0
		groundAttack["fire"] = 2.0
		groundAttack["poison"] = 2.0
		groundAttack["rock"] = 2.0
		groundAttack["steel"] = 2.0
		groundAttack["bug"] = .5
		groundAttack["grass"] = .5
		groundAttack["flying"] = 0.0
		atkMult["ground"] = groundAttack

		fairyAttack = createBasicMap()
		fairyAttack["dark"] = 2.0
		fairyAttack["dragon"] = 2.0
		fairyAttack["fighting"] = 2.0
		fairyAttack["fire"] = .5
		fairyAttack["poison"] = .5
		fairyAttack["steel"] = .5
		atkMult["fairy"] = fairyAttack

		bugAttack = createBasicMap()
		bugAttack["dark"] = 2.0
		bugAttack["grass"] = 2.0
		bugAttack["psychic"] = 2.0
		bugAttack["fairy"] = .5
		bugAttack["fighting"] = .5
		bugAttack["flying"] = .5
		bugAttack["ghost"] = .5
		bugAttack["poison"] = .5
		bugAttack["fire"] = .5
		bugAttack["steel"] = .5
		atkMult["bug"] bugAttack

		psychicAttack = createBasicMap()
		psychicAttack["fighting"] = 2.0
		psychicAttack["poison"] = 2.0
		psychicAttack["psychic"] = .5
		psychicAttack["steel"] = .5
		psychicAttack["dark"] = 0.0
		atkMult["psychic"] = psychicAttack

		poisonAttack = createBasicMap()
		poisonAttack["fairy"] = 2.0
		poisonAttack["grass"] = 2.0
		poisonAttack["ground"] = .5
		poisonAttack["rock"] = .5
		poisonAttack["ghost"] = .5
		poisonAttack["poison"] = .5
		poisonAttack["steel"] = 0.0
		atkMult["poison"] = poisonAttack

		rockAttack = createBasicMap()
		rockAttack["bug"] = 2.0
		rockAttack["fire"] = 2.0
		rockAttack["flying"] = 2.0
		rockAttack["ice"] = 2.0
		rockAttack["fighting"] = .5
		rockAttack["ground"] = .5
		rockAttack["steel"] = .5
		atkMult["rock"] = rockAttack

		flyingAttack = createBasicMap()
		flyingAttack["bug"] = 2.0
		flyingAttack["fighting"] = 2.0
		flyingAttack["grass"] = 2.0
		flyingAttack["electric"] = .5
		flyingAttack["rock"] = .5
		flyingAttack["steel"] = .5
		atkMult["flying"] = flyingAttack

		normalAttack = createBasicMap()
		normalAttack["rock"] = .5
		normalAttack["steel"] = .5
		normalAttack["ghost"] = 0.0
		atkMult["normal"] = normalAttack

		steelAttack = createBasicMap()
		steelAttack["fairy"] = 2.0
		steelAttack["ice"] = 2.0
		steelAttack["rock"] = 2.0
		steelAttack["electric"] = .5
		steelAttack["fire"] = .5
		steelAttack["steel"] = .5
		steelAttack["water"] = .5
		atkMult["steel"] = steelAttack

		dragonAttack = createBasicMap()
		dragonAttack["dragon"] = 2.0
		dragonAttack["steel"] = .5
		dragonAttack["fairy"] = 0.0
		atkMult["dragon"] = dragonAttack

		fightingAttack = createBasicMap()
		fightingAttack["normal"] = 2.0
		fightingAttack["dark"] = 2.0
		fightingAttack["ice"] = 2.0
		fightingAttack["steel"] = 2.0
		fightingAttack["rock"] = 2.0
		fightingAttack["bug"] = .5
		fightingAttack["fairy"] = .5
		fightingAttack["flying"] = .5
		fightingAttack["poison"] = .5
		fightingAttack["psychic"] = .5
		fightingAttack["ghost"] =0.0
		atkMult["fighting"] = fightingAttack

		darkAttack = createBasicMap()
		darkAttack["ghost"] = 2.0
		darkAttack["psychic"] = 2.0
		darkAttack["dark"] = .5
		darkAttack["fairy"] = .5
		darkAttack["fighting"] = .5
		atkMult["dark"] = darkAttack


		//load AI
		if(p1AI=="user") {
			p1 = UserControl
		}
		else if(p1AI=="nn") {
		# 	p1 = PokeNet
		}
		else if(p1AI.equals("basic")) {
			p1 = BasicAI
		}
		else {
			print("invalid ai for player 1")
			System.exit(1);
		}

		if(p2AI=="user") {
			p2 = BasicAI
		}
		else if(p2AI=="nn") {
			# p2 = PokeNet
		}
		else if(p2AI=="basic") {
			p2 = BasicAI
		}
		else {
			print("invalid ai for player 2")
			System.exit(1);
		}

        fileLocation = "pokemon.csv"
        dataFile = open(fileLocation, 'r')
        line = next(dataFile)
        for line in dataFile:
            lineparts = line.split(",")
            name  = lineparts[0]
            validMon[name] = Mon(name, int(lineparts[1]), int(lineparts[2]), int(lineparts[3]),
					int(lineparts[4]), lineparts[5], int(lineparts[6]), int(lineparts[7]),
					lineparts[8], lineparts[9], int(lineparts[10]), int(lineparts[11]), lineparts[12],
					lineparts[13], lineparts[14]))

        # load teams
		m11 = deepcopy(validMon[p1Mon1])
		m11.active = True
		m12 = deepcopy(validMon[p1Mon2])
		m13 = deepcopy(validMon[p1Mon3])
		m21 = deepcopy(validMon[p2Mon1])
		m21.active = True;
		m22 = deepcopy(validMon[p2Mon2])
		m23 = deepcopy(validMon[p2Mon3])
		team1[0] = m11;
		team1[1] = m12;
		team1[2] = m13;
		team2[0] = m21;
		team2[1] = m22;
		team2[2] = m23;

    def isDefeated(team):
        # returns whether or not team has no usable Pokemon left
	   return team[0].defeated and team[1].defeated & team[2].defeated

   	def active(team):
        if team[0].active :
			return team[0];
        elif team[1].active:
            return team[1];
        else:
            return team[2];

    def switch1(team)  #what if nothing to switch to
	   if (team[0].active):
           if not (team[1].defeated) :
               team[0].active = False;
               team[1].active = True;
               if not (team[0].defeated):
                   println(team[0].name+"  is switching out!")
               println("Go, "+team[1].name + "!")
               return
           elif not (team[2].defeated) :
				team[0].active = False;
				team[2].active = True;
				if not (team[0].defeated) :
                    println(team[0].name+"  is switching out!")
				println("Go, "+team[2].name+"!")
				return
            else :
				return
        elif (team[1].active):
            if not (team[2].defeated) :
                team[1].active = False
				team[2].active = True
				if not (team[1].defeated) :
                    println(team[1].name + " is switching out!")
				println("Go, "+team[2].name+"!");
				return
            elif not (team[0].defeated):
				team[1].active = False
				team[0].active = True
				if not (team[1].defeated) :
                    println(team[1].name + " is switching out!")
				println("Go, "+team[0].name+"!")
				return
            else :
				return
		elif (team[2].active) :
			if not (team[0].defeated):
				team[2].active = False
				team[0].active = True
				if not (team[2].defeated):
                    println(team[2].name+"  is switching out!")
				println("Go, "+team[0].name+"!")
				return
            elif not (team[1].defeated):
				team[2].active = False
				team[1].active = True
				if not(team[2].defeated):
                    println(team[2].name+"  is switching out!")
				println("Go, "+team[1].name+"!")
				return
            else :
				return
		else :
			return
