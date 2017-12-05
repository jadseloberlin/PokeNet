import os
import math
import nn

class BattleSim:
    types = ["fire", "water", "grass", "bug", "ghost","psychic","dragon","electric", "rock", "ice", "poison", "normal", "ground","fighting", "flying","none"]
    validMon = {}
    team1 = []
    team2 = []
    atkMult = {}
    p1 = None
    p2 = None

    def createBasicMap():
        rtn = {}
        for t in types:
            trn[t] = 1.0
        return rtn

    def contents(par):
        sb = "["
        for s in par:
            sb += (s + ", ")
        sb += "]"
        return sb

    def BattleSim(p1AI, p2AI, p1Mon1, p1Mon2,  p1Mon3,  p2Mon1, p2Mon2,  p2Mon3):
        # populate type matchups
		fireAttack = {}
		fireAttack["fire"] = .5
		fireAttack["water"] = .5;
		fireAttack.put["grass"] = 2.0
		fireAttack["bug"] = 2.0
		fireAttack["ice"] = 2.0
		fireAttack["rock"] = .5
		fireAttack["steel"] = 2.0
		fireAttack["dragon"] = .5
		atkMult["fire"] = fireAttack

		waterAttack = {}
		waterAttack["dragon"] = .5
		waterAttack["grass"] = .5
		waterAttack["fire"] = 2.0
		waterAttack["rock"] = 2.0
		waterAttack["ground"] = 2.0
		waterAttack["water"] = .5
		atkMult["water"] = waterAttack

		grassAttack =  {}
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

		electricAttack = {}
		electricAttack["water"] = 2.0
		electricAttack["ground"] = 0.0
		electricAttack["flying"] = 2.0
		electricAttack["dragon"] = .5
		electricAttack["electric"] = .5
		electricAttack["grass"] = .5
		atkMult["electric"] = electricAttack

		iceAttack = {}
		iceAttack["ice"] = .5
		iceAttack["steel"] = .5
		iceAttack["water"] = .5
		iceAttack["fire"] = .5
		iceAttack["dragon"] = 2.0
		iceAttack["flying"] = 2.0
		iceAttack["grass"] = 2.0
		iceAttack["ground"] = 2.0
		atkMult["ice"] = iceAttack

		ghostAttack = {}
		ghostAttack["ghost"] = 2.0
		ghostAttack["psychic"] = 2.0
		ghostAttack["dark"] = .5
		ghostAttack["normal"] = 0.0
	    atkMult["ghost"] = ghostAttack

		groundAttack = {}
		groundAttack["electric"] = 2.0
		groundAttack["fire"] = 2.0
		groundAttack["poison"] = 2.0
		groundAttack["rock"] = 2.0
		groundAttack["steel"] = 2.0
		groundAttack["bug"] = .5
		groundAttack["grass"] = .5
		groundAttack["flying"] = 0.0
		atkMult["ground"] = groundAttack

		fairyAttack = {}
		fairyAttack["dark"] = 2.0
		fairyAttack["dragon"] = 2.0
		fairyAttack["fighting"] = 2.0
		fairyAttack["fire"] = .5
		fairyAttack["poison"] = .5
		fairyAttack["steel"] = .5
		atkMult["fairy"] = fairyAttack

		bugAttack = {}
		bugAttack["dark"] 2.0
		bugAttack["grass"] 2.0
		bugAttack["psychic"] 2.0
		bugAttack["fairy"].5
		bugAttack["fighting"] .5
		bugAttack["flying"] .5
		bugAttack["ghost"] .5
		bugAttack["poison"] .5
		bugAttack["fire"] .5
		bugAttack["steel"] .5
		atkMult["bug"] bugAttack

		psychicAttack = {}
		psychicAttack["fighting"] = 2.0
		psychicAttack["poison"] = 2.0
		psychicAttack["psychic"] = .5
		psychicAttack["steel"] = .5
		psychicAttack["dark"] = 0.0
		atkMult["psychic"] = psychicAttack

		poisonAttack = {}
		poisonAttack["fairy"] = 2.0
		poisonAttack["grass"] = 2.0
		poisonAttack["ground"] = .5
		poisonAttack["rock"] = .5
		poisonAttack["ghost"] = .5
		poisonAttack["poison"] = .5
		poisonAttack["steel"] = 0.0
		atkMult["poison"] = poisonAttack

		rockAttack = {}
		rockAttack["bug"] = 2.0
		rockAttack["fire"] = 2.0
		rockAttack["flying"] = 2.0
		rockAttack["ice"] = 2.0
		rockAttack["fighting"] = .5
		rockAttack["ground"] = .5
		rockAttack["steel"] = .5
		atkMult["rock"] = rockAttack

		flyingAttack = {}
		flyingAttack["bug"] = 2.0
		flyingAttack["fighting"] = 2.0
		flyingAttack["grass"] = 2.0
		flyingAttack["electric"] = .5
		flyingAttack["rock"] = .5
		flyingAttack["steel"] = .5
		atkMult["flying"] = flyingAttack

		normalAttack = {}
		normalAttack["rock"] = .5
		normalAttack["steel"] = .5
		normalAttack["ghost"] = 0.0
		atkMult["normal"] = normalAttack

		steelAttack = {}
		steelAttack["fairy"] = 2.0
		steelAttack["ice"] = 2.0
		steelAttack["rock"] = 2.0
		steelAttack["electric"] = .5
		steelAttack["fire"] = .5
		steelAttack["steel"] = .5
		steelAttack["water"] = .5
		atkMult["steel"] = steelAttack

		dragonAttack = {}
		dragonAttack["dragon"] = 2.0
		dragonAttack["steel"] = .5
		dragonAttack["fairy"] = 0.0
		atkMult["dragon"] = dragonAttack

		fightingAttack = {}
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

		darkAttack = {}
		darkAttack["ghost"] = 2.0
		darkAttack["psychic"] = 2.0
		darkAttack["dark"] = .5
		darkAttack["fairy"] = .5
		darkAttack["fighting"] = .5
		atkMult["dark"] = darkAttack
