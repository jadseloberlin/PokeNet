from copy import deepcopy
import os
import math
from nn import NN
from userControl import UserControl
from basicAI import BasicAI
from mon import Mon
import random
import sys
import numpy

def main():
    #battle = BattleSim(input("Who controls P1? Choose 'user' or 'basic' : "),input("Who controls P2? Choose 'user' or 'basic' : "),input("Pick P1's first Pokemon: "),input("Pick P1's second Pokemon: "),input("Pick P1's third Pokemon: "),input("Pick P2's first Pokemon: "),input("Pick P2's second Pokemon: "),input("Pick P2's third Pokemon: "))
    #battle = BattleSim(input("Who controls P1? Choose 'user', 'nn' or 'basic' : "),"basic",input("Pick P1's first Pokemon: "),input("Pick P1's second Pokemon: "),input("Pick P1's third Pokemon: "),"Charizard", "Blastoise", "Venusaur")
    battle = BattleSim(input("Who controls P1? Choose 'user', 'nn' or 'basic' : "),"basic","Zapdos","Moltres","Articuno","Charizard", "Blastoise", "Venusaur")


class BattleSim(object):


    def createBasicMap(self):
        rtn = {}
        for t in self.types:
            rtn[t] = 1.0
        return rtn

    def contents(self,par):
        sb = "["
        for s in par:
            sb += (s + ", ")
        sb += "]"
        return sb

    def __init__ (self, p1AI, p2AI, p1Mon1, p1Mon2,  p1Mon3,  p2Mon1, p2Mon2,  p2Mon3):
        self.types = ["fire", "water", "grass", "bug", "ghost","psychic","dragon","electric", "rock", "ice", "poison", "normal", "ground","fighting","flying","dark","steel","fairy","none"]
        self.validMon = {}
        self.team1 = [0,0,0]
        self.team2 = [0,0,0]
        self.atkMult = {}
        self.p1 = None
        self.p2 = None
        # populate type matchups
        fireAttack = self.createBasicMap()
        fireAttack["fire"] = .5
        fireAttack["water"] = .5;
        fireAttack["grass"] = 2.0
        fireAttack["bug"] = 2.0
        fireAttack["ice"] = 2.0
        fireAttack["rock"] = .5
        fireAttack["steel"] = 2.0
        fireAttack["dragon"] = .5
        self.atkMult["fire"] = fireAttack

        waterAttack = self.createBasicMap()
        waterAttack["dragon"] = .5
        waterAttack["grass"] = .5
        waterAttack["fire"] = 2.0
        waterAttack["rock"] = 2.0
        waterAttack["ground"] = 2.0
        waterAttack["water"] = .5
        self.atkMult["water"] = waterAttack

        grassAttack =  self.createBasicMap()
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
        self.atkMult["grass"] = grassAttack

        electricAttack = self.createBasicMap()
        electricAttack["water"] = 2.0
        electricAttack["ground"] = 0.0
        electricAttack["flying"] = 2.0
        electricAttack["dragon"] = .5
        electricAttack["electric"] = .5
        electricAttack["grass"] = .5
        self.atkMult["electric"] = electricAttack

        iceAttack = self.createBasicMap()
        iceAttack["ice"] = .5
        iceAttack["steel"] = .5
        iceAttack["water"] = .5
        iceAttack["fire"] = .5
        iceAttack["dragon"] = 2.0
        iceAttack["flying"] = 2.0
        iceAttack["grass"] = 2.0
        iceAttack["ground"] = 2.0
        self.atkMult["ice"] = iceAttack

        ghostAttack = self.createBasicMap()
        ghostAttack["ghost"] = 2.0
        ghostAttack["psychic"] = 2.0
        ghostAttack["dark"] = .5
        ghostAttack["normal"] = 0.0
        self.atkMult["ghost"] = ghostAttack

        groundAttack = self.createBasicMap()
        groundAttack["electric"] = 2.0
        groundAttack["fire"] = 2.0
        groundAttack["poison"] = 2.0
        groundAttack["rock"] = 2.0
        groundAttack["steel"] = 2.0
        groundAttack["bug"] = .5
        groundAttack["grass"] = .5
        groundAttack["flying"] = 0.0
        self.atkMult["ground"] = groundAttack

        fairyAttack = self.createBasicMap()
        fairyAttack["dark"] = 2.0
        fairyAttack["dragon"] = 2.0
        fairyAttack["fighting"] = 2.0
        fairyAttack["fire"] = .5
        fairyAttack["poison"] = .5
        fairyAttack["steel"] = .5
        self.atkMult["fairy"] = fairyAttack

        bugAttack = self.createBasicMap()
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
        self.atkMult["bug"] = bugAttack

        psychicAttack = self.createBasicMap()
        psychicAttack["fighting"] = 2.0
        psychicAttack["poison"] = 2.0
        psychicAttack["psychic"] = .5
        psychicAttack["steel"] = .5
        psychicAttack["dark"] = 0.0
        self.atkMult["psychic"] = psychicAttack

        poisonAttack = self.createBasicMap()
        poisonAttack["fairy"] = 2.0
        poisonAttack["grass"] = 2.0
        poisonAttack["ground"] = .5
        poisonAttack["rock"] = .5
        poisonAttack["ghost"] = .5
        poisonAttack["poison"] = .5
        poisonAttack["steel"] = 0.0
        self.atkMult["poison"] = poisonAttack

        rockAttack = self.createBasicMap()
        rockAttack["bug"] = 2.0
        rockAttack["fire"] = 2.0
        rockAttack["flying"] = 2.0
        rockAttack["ice"] = 2.0
        rockAttack["fighting"] = .5
        rockAttack["ground"] = .5
        rockAttack["steel"] = .5
        self.atkMult["rock"] = rockAttack

        flyingAttack = self.createBasicMap()
        flyingAttack["bug"] = 2.0
        flyingAttack["fighting"] = 2.0
        flyingAttack["grass"] = 2.0
        flyingAttack["electric"] = .5
        flyingAttack["rock"] = .5
        flyingAttack["steel"] = .5
        self.atkMult["flying"] = flyingAttack

        normalAttack = self.createBasicMap()
        normalAttack["rock"] = .5
        normalAttack["steel"] = .5
        normalAttack["ghost"] = 0.0
        self.atkMult["normal"] = normalAttack

        steelAttack = self.createBasicMap()
        steelAttack["fairy"] = 2.0
        steelAttack["ice"] = 2.0
        steelAttack["rock"] = 2.0
        steelAttack["electric"] = .5
        steelAttack["fire"] = .5
        steelAttack["steel"] = .5
        steelAttack["water"] = .5
        self.atkMult["steel"] = steelAttack

        dragonAttack = self.createBasicMap()
        dragonAttack["dragon"] = 2.0
        dragonAttack["steel"] = .5
        dragonAttack["fairy"] = 0.0
        self.atkMult["dragon"] = dragonAttack

        fightingAttack = self.createBasicMap()
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
        self.atkMult["fighting"] = fightingAttack

        darkAttack = self.createBasicMap()
        darkAttack["ghost"] = 2.0
        darkAttack["psychic"] = 2.0
        darkAttack["dark"] = .5
        darkAttack["fairy"] = .5
        darkAttack["fighting"] = .5
        self.atkMult["dark"] = darkAttack


		#load AI
        if(p1AI=="user") :
	           self.p1 = UserControl()
        elif(p1AI=="nn"):
            self.p1 = NN()
        elif(p1AI == "basic"):
            self.p1 = BasicAI()
        else:
            print("invalid ai for player 1")
            sys.exit(1)

        if(p2AI=="user"):
            self.p2 = UserControl()
        elif(p2AI == "nn"):
            self.p2 = NN()
        elif(p2AI == "basic"):
            self.p2 = BasicAI()
        else:
            print("invalid ai for player 2")
            sys.exit(1)

        fileLocation = "pokemon.csv"
        dataFile = open(fileLocation, 'r')
        line = next(dataFile)
        for line in dataFile:
            lineparts = line.strip().split(",")
            name  = lineparts[0]
            self.validMon[name] = Mon(name, int(lineparts[1]), int(lineparts[2]), int(lineparts[3]),
					int(lineparts[4]), lineparts[5], int(lineparts[6]), int(lineparts[7]),
					lineparts[8], lineparts[9], int(lineparts[10]), int(lineparts[11]), lineparts[12],
					lineparts[13], lineparts[14])

        # load teams
        m11 = deepcopy(self.validMon[p1Mon1])
        m11.active = True
        m12 = deepcopy(self.validMon[p1Mon2])
        m13 = deepcopy(self.validMon[p1Mon3])
        m21 = deepcopy(self.validMon[p2Mon1])
        m21.active = True;
        m22 = deepcopy(self.validMon[p2Mon2])
        m23 = deepcopy(self.validMon[p2Mon3])
        self.team1[0] = m11;
        self.team1[1] = m12;
        self.team1[2] = m13;
        self.team2[0] = m21;
        self.team2[1] = m22;
        self.team2[2] = m23;

        if(self.battle()):
            print("P1 wins!")
        else:
            print("P2 wins!")

    def isDefeated(self, team):
        # returns whether or not team has no usable Pokemon left
        return team[0].defeated and team[1].defeated & team[2].defeated

    def onlyOneLeft(self, team):
        return ((team[0].defeated and team[1].defeated) or (team[0].defeated and team[2].defeated) or (team[1].defeated and team[2].defeated))

    def active(self, team):
        if team[0].active :
            return team[0];
        elif team[1].active:
            return team[1];
        else:
            return team[2];

    def switch1(self, team):  #what if nothing to switch to
        if (team[0].active):
            if not (team[1].defeated) :
                team[0].active = False;
                team[1].active = True;
                if not (team[0].defeated):
                    print(team[0].name+"  is switching out!")
                print("Go, "+team[1].name + "!")
                return
            elif not (team[2].defeated) :
                team[0].active = False;
                team[2].active = True;
                if not (team[0].defeated) :
                    print(team[0].name+"  is switching out!")
                print("Go, "+team[2].name+"!")
                return
            else :
                return
        elif (team[1].active):
            if not (team[2].defeated) :
                team[1].active = False
                team[2].active = True
                if not (team[1].defeated) :
                    print(team[1].name + " is switching out!")
                print("Go, "+team[2].name+"!");
                return
            elif not (team[0].defeated):
                team[1].active = False
                team[0].active = True
                if not (team[1].defeated) :
                    print(team[1].name + " is switching out!")
                print("Go, "+team[0].name+"!")
                return
            else :
                return
        elif (team[2].active) :
            if not (team[0].defeated):
                team[2].active = False
                team[0].active = True
                if not (team[2].defeated):
                    print(team[2].name+"  is switching out!")
                print("Go, "+team[0].name+"!")
                return
            elif not (team[1].defeated):
                team[2].active = False
                team[1].active = True
                if not(team[2].defeated):
                    print(team[2].name+"  is switching out!")
                print("Go, "+team[1].name+"!")
                return
            else :
                return
        else :
            return

    def switch2(self, team):  #what if nothing to switch to
        if (team[0].active):
            if not (team[2].defeated) :
                team[0].active = False
                team[2].active = True
                if not (team[0].defeated):
                   print(team[0].name+"  is switching out!")
                print("Go, "+team[2].name + "!")
                return
            elif not (team[1].defeated) :
                team[0].active = False
                team[1].active = True
                if not (team[0].defeated) :
                    print(team[0].name+"  is switching out!")
                print("Go, "+team[1].name+"!")
                return
            else :
                return
        elif (team[1].active):
            if not (team[0].defeated) :
                team[1].active = False
                team[0].active = True
                if not (team[1].defeated) :
                    print(team[1].name + " is switching out!")
                print("Go, "+team[0].name+"!");
                return
            elif not (team[2].defeated):
                team[1].active = False
                team[2].active = True
                if not (team[1].defeated) :
                    print(team[1].name + " is switching out!")
                print("Go, "+team[2].name+"!")
                return
            else :
                return
        elif (team[2].active) :
            if not (team[1].defeated):
                team[2].active = False
                team[1].active = True
                if not (team[2].defeated):
                    print(team[2].name+"  is switching out!")
                print("Go, "+team[1].name+"!")
                return
            elif not (team[0].defeated):
                team[2].active = False
                team[0].active = True
                if not(team[2].defeated):
                    print(team[2].name+"  is switching out!")
                print("Go, "+team[0].name+"!")
                return
            else :
                return
        else :
            return


	#returns true if p1 wins, false if p2 wins
    def battle(self):
        turns = 0
        while not (self.isDefeated(self.team1)) and not (self.isDefeated(self.team2)):
            print()
            turns += 1
            print("This is turn number "+str(turns))
            active1 = self.active(self.team1)
            active2 = self.active(self.team2)
            print("P1's "+active1.name+" has "+str(int(active1.hp))+" HP left. ")
            print("P2's "+active2.name+" has "+str(int(active2.hp))+" HP left. ")
            print("")
            move1 = self.p1.chooseMove(self.team1, active2, self.atkMult, turns)
            move2 = self.p2.chooseMove(self.team2, active1, self.atkMult, turns)

            if(self.onlyOneLeft(self.team1) and (move1 == "switch1" or move1 == "switch2")):
                move1 = "quick"
            if(self.onlyOneLeft(self.team2) and (move2 == "switch1" or move2 == "switch2")):
                move2 = "quick"
            if(move1 == "exit" or move2 == "exit"):
                print("Thank you!")
                sys.exit(0)
            if (move1 == "switch1"):
				#if player 1 is switching to first available
                if (move2 == "switch1"):
					#if player 2 is also switching to first
                    if (active1.speed >= active2.speed):
						#if p1 is faster
                        self.switch1(self.team1)
                        self.switch1(self.team2)
                    else:
						#if p2 is faster
                        self.switch1(self.team2)
                        self.switch1(self.team1)
                elif(move2 == "switch2"):
					#if p2 is switching to second available
                    if (active1.speed >= active2.speed):
						#if p1 is faster
                        self.switch1(self.team1)
                        self.switch2(self.team2)
                    else:
						#if p2 is faster
                        self.switch2(self.team2)
                        self.switch1(self.team1)
                elif(move2=="quick"):
					#p2 is attacking quickly
                    self.switch1(self.team1)
                    self.quick(active2, self.active(self.team1), self.team1)
                else:
					#p2 is attacking strongly
                    self.switch1(self.team1)
                    self.strong(active2, self.active(self.team1), self.team1)
            elif (move1 == "switch2"):
				#p1 switches to second available
                if (move2 == "switch2"):
					#if player 2 is also switching to second
                    if (active1.speed >= active2.speed):
						#if p1 is faster
                        self.switch2(self.team1)
                        self.switch2(self.team2)
                    else :
						#if p2 is faster
                        self.switch2(self.team2)
                        self.switch2(self.team1)
                elif (move2 == "switch1"):
					#if p2 is switching to first available
                    if (active1.speed >= active2.speed):
						#if p1 is faster
                        self.switch2(self.team1)
                        self.switch1(self.team2)
                    else:
						#if p2 is faster
                        self.switch1(self.team2)
                        self.switch2(self.team1)
                elif (move2 == "quick"):
					#p2 is attacking quickly
                    self.switch2(self.team1)
                    self.quick(active2, self.active(self.team1), self.team1)
                else :
					#p2 is attacking strongly
                    self.switch2(self.team1)
                    self.strong(active2, self.active(self.team1), self.team1)
            elif(move1 == "quick"):
				#p1 chooses quick
                if (move2 == "switch1"):
					#p2 switches to first available
                    self.switch1(self.team2)
                    self.quick(active1, self.active(self.team2), self.team2)
                elif(move2 == "switch2"):
					#p2 switches to second available
                    self.switch2(self.team2)
                    self.quick(active1, self.active(self.team2), self.team2)
                else:
					#p2 attacks
                    if (active1.speed >= active2.speed):
						#p1 is faster
                        self.quick(active1, active2,self.team2)
                        if ( ( self.isDefeated(self.team2) ) or (active2.defeated) ):
                            continue
                        if (move2 == "quick"):
							#p2 uses a quick attack
                            self.quick(self.active(self.team2), active1, self.team1)
                        else:
							#p2 uses a strong attack
                            self.strong(self.active(self.team2), active1, self.team1)
                    else:
						#p2 is faster
                        if(move2 == "quick"):
							#p2 uses a quick attack
                            self.quick(active2, active1, self.team1)
                        else:
							#p2 uses a strong attack
                            self.strong(active2, active1, self.team1)
                        if (self.isDefeated(self.team1)):
                            continue
                        if(active1.defeated):
                            continue
                        self.quick(active1, active2, self.team2)
            else:
				#p1 chooses strong
                if (move2 == "switch1"):
					#p2 switches to first available
                    self.switch1(self.team2)
                    self.strong(active1, self.active(self.team2), self.team2)
                elif (move2 == "switch2"):
					#p2 switches to second available
                    self.switch2(self.team2)
                    self.strong(active1, self.active(self.team2), self.team2)
                else :
					#p2 attacks
                    if (active1.speed >= active2.speed):
						#p1 is faster
                        self.strong(active1, active2, self.team2)
                        if ((self.isDefeated(self.team2)) or (active2.defeated) ):
                            continue
                        if(move2 == "quick"):
							#p2 uses a quick attack
                            self.quick(self.active(self.team2), active1, self.team1)
                        else:
							#p2 uses a strong attack
                            self.strong(self.active(self.team2), active1, self.team1)
                    else:
						#p2 is faster
                        if (move2 == "quick"):
							#p2 uses a quick attack
                            self.quick(active2, active1, self.team1)
                        else:
							#p2 uses a strong attack
                            self.strong(active2, active1, self.team1)
                        if(self.isDefeated(self.team1)):
                            continue
                        if(active1.active):
							#if active1 wasn't knocked out
                            self.strong(active1, active2, self.team2)
        print("")
        self.p1.cleanUp()
        self.p2.cleanUp()
        return self.isDefeated(self.team2)

    def quick(self, attacker, target, targetTeam): #returns true if target faints

        print(attacker.name+" used "+attacker.quickMoveName+ " on "+target.name+"!")
        accCheck = random.randint(0,100) #accuracy needs to be higher than accCheck to land
        if (attacker.quickMoveAcc <= accCheck):
            print("But it missed!")
            return False
        damage = attacker.quickMovePower + 2/3 * (attacker.attack - target.defense)
        multiplier = 1
        multiplier = multiplier * self.atkMult.get(attacker.quickMoveType).get(target.type1)
        multiplier = multiplier * self.atkMult.get(attacker.quickMoveType).get(target.type2)

        if(multiplier > 1):
            print("It's super effective!")
        elif ( multiplier == 0 ):
            print("It didn't have any effect...")
            return False
        elif(multiplier < 1 ):
            print("It's  not very effective...")
        damage = damage * multiplier
        if(damage < 5):
            damage = 5
        target.hp = target.hp - damage
        if(target.hp < 1):
            target.defeated = True
            print(target.name + " fainted!")
            if(not self.isDefeated(targetTeam)):
                self.switch1(targetTeam)
            return True
        return False

    def strong(self, attacker, target, targetTeam): #returns true if target faints

        print(attacker.name+" used "+attacker.strongMoveName+ " on "+target.name+"!")
        accCheck = random.randint(0,100) #accuracy needs to be higher than accCheck to land
        if (attacker.strongMoveAcc <= accCheck):
            print("But it missed!")
            return False
        damage = attacker.strongMovePower + 2/3* (attacker.attack - target.defense)
        if(damage < 5):
            damage = 5
        multiplier = 1
        multiplier = multiplier * self.atkMult.get(attacker.strongMoveType).get(target.type1)
        multiplier = multiplier * self.atkMult.get(attacker.strongMoveType).get(target.type2)
        if(multiplier > 1):
            print("It's super effective!")
        elif ( multiplier == 0 ):
            print("It didn't have any effect...")
            return False
        elif(multiplier < 1 ):
            print("It's  not very effective...")
        damage = damage * multiplier
        target.hp = target.hp - damage
        if(target.hp < 1):
            target.defeated = True
            print(target.name + " fainted!")
            if(not self.isDefeated(targetTeam)):
                self.switch1(targetTeam)
            return True
        return False



if __name__ == "__main__":
    main()
