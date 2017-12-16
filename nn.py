from instance import Instance
import math
import random
import sys
import tensorflow as tf
from state import State
import numpy

class NN(object):

    def __init__(self):
        self.numNeurons = 50
        self.learningRate = .0001
        self.seed = 1334
        self.numAttributes = 460
        self.numLabels = 4
        self.labelList = ["quick", "strong", "switch1", "switch2"]
        self.prevState = None
        self.prevReward = None
        self.prevAction = None
        self.D = [] #should we store this between games?


        self.sess = None
        self.state = None
        self.y = None
        self.predict = None
        self.nextQ = None
        self.action = None
        self.trainer = None
        self.r = None
        self.mask = None
        self.steps = 0

        self.loadTensorFlow()



    def buildTensorFlow(self):

        self.state = tf.placeholder(tf.float32, shape = [None, self.numAttributes])
        self.nextQ = tf.placeholder(tf.float32, shape = [self.numLabels]) #self.numAttributes
        self.r = tf.placeholder(tf.float32, shape = [1])
        self.mask = tf.placeholder(tf.float32, shape = [self.numLabels])

        #create hidden layer
        W_hidden = tf.Variable(tf.truncated_normal([self.numAttributes, self.numNeurons], stddev = 0.1))
        b_hidden = tf.Variable(tf.constant(0.1, shape = [self.numNeurons]))
        net_hidden = tf.matmul(self.state, W_hidden) + b_hidden
        out_hidden = tf.sigmoid(net_hidden)

        #create output layer
        W_output = tf.Variable(tf.truncated_normal([self.numNeurons, self.numLabels], stddev = 0.1))
        b_output = tf.Variable(tf.constant(0.1, shape = [self.numLabels]))
        net_output = tf.matmul(out_hidden, W_output) + b_output
        self.predict = net_output
        self.action = tf.argmax(net_output,1)

        #create the true labels
        self.y = tf.placeholder(tf.float32, shape = [None, self.numLabels])

        cost = (self.r * self.mask + tf.reduce_max(self.nextQ) * self.mask - self.mask*self.predict)**2
        self.trainer = tf.train.AdamOptimizer(self.learningRate).minimize(cost)

        #start a TF session
        self.sess = tf.Session()
        init = tf.initialize_all_variables().run(session =self.sess)
        self.saver = tf.train.Saver(tf.all_variables())
        print("Built!")


    def loadTensorFlow(self):
        self.buildTensorFlow()

        try:
            save_dir = "."
            ckpt = tf.train.get_checkpoint_state(save_dir)
            load_path = ckpt.model_checkpoint_path

            self.saver.restore(self.sess, load_path)
            self.steps = int(load_path.split("-")[-1])
            print("Loaded!")

        except:
            pass

    def trainTensorFlow(self, st, at, rt, st1):
        et = (st, at, rt, st1)
        self.D.append(et)
        random.shuffle(self.D)
        T = []

        for i in range(0, min(16, len(self.D))):
            T.append(self.D[i])

        while len(T) > 0:
            #if running slow change while loop
            et = T.pop()
            stList = et[0].toList()
            st1List = et[3].toList()
            rtList = [rt]
            nQ = self.sess.run(self.predict, feed_dict = {self.state:st1List})
            i = self.labelList.index(et[1])
            m = [0] * self.numLabels
            m[i] = 1
            self.sess.run(self.trainer, feed_dict = {self.mask: m, self.r: rtList, self.state:stList, self.nextQ: nQ[0]*.99})

    def testTensorFlow(self,curState, games):
        #convert curState to list
        curStateList = curState.toList()

        #test
        p = self.sess.run(self.predict, feed_dict = {self.state: curStateList})
        a = numpy.argmax(p)
        randomCheck = random.randint(0,10000)
        if games > 0:
            if(randomCheck < 10000/games):
                a = random.randint(0,3) #choose a random action
        action= self.labelList[a]
        return action

    # code for interacting w simulator

    def reward(self, action, state, atkMult):
        damage = 0
        active = 0
        rtn = 0
        acc = 100 #if the action is a switch, accuracy is irrelevant

        if(state.user1Active):
            active = 1
        elif(state.user2Active):
            active = 2
        elif(state.user3Active):
            active = 3
        else:
            if( (not(state.user1HP == 0)) or (not (state.user2HP == 0)) or (not (state.user3HP==0))):
                print("we don't know who's active")
                sys.exit(1)
            return None
        if(action == "quick"):
            if(active == 1):
                damage += state.user1QDmg + 2/3 * (state.user1Atk - state.oppDef)
                acc = state.user1QAcc
            elif (active == 2):
                damage += state.user2QDmg + 2/3 * (state.user2Atk - state.oppDef)
                acc = state.user2QAcc
            elif (active ==3):
                damage += state.user3QDmg + 2/3 * (state.user3Atk - state.oppDef)
                acc = state.user3QAcc
        elif(action == "strong"):
            if(active == 1):
                damage += state.user1SDmg + 2/3 * (state.user1Atk - state.oppDef)
                acc = state.user1SAcc
            elif (active == 2):
                damage += state.user2SDmg + 2/3 * (state.user2Atk - state.oppDef)
                acc = state.user2SAcc
            elif (active ==3):
                damage += state.user3SDmg + 2/3 * (state.user3Atk - state.oppDef)
                acc = state.user3SAcc
        if(damage < 1):
            damage = 1
        rtn += math.log10(damage)
        acc = acc / 100
        rtn = rtn * acc

        if(state.oppHP - (damage * acc) < 1): #fainting bonus
            rtn += 2.5

        quickMap = atkMult[state.oppQType]
        strongMap = atkMult[state.oppSType]
        quick = 1 #defending muliplier
        strong = 1 #defending multiplier
        quickAtk = 1 # attacking multiplier
        strongAtk = 1 # attacking multiplier

        if(active == 1 ):
            quickDen = (quickMap[state.user1Type1] * quickMap[state.user1Type2])
            strongDen = ( strongMap[state.user1Type1] * strongMap[state.user1Type2] )
            if(quickDen == 0):
                quick = 0.0001
            else:
                quick = 1/quickDen
            if(strongDen == 0):
                strong = 0.0001
            else:
                strong = 1/strongDen
            quickAtkMap = atkMult[state.user1QType]
            strongAtkMap = atkMult[state.user1SType]
            quickAtk = quickAtkMap[state.oppType1] * quickAtkMap[state.oppType2]
            strongAtk = strongAtkMap[state.oppType1] * strongAtkMap[state.oppType2]
        elif (active == 2):
            quickDen =  (quickMap[state.user2Type1] * quickMap[state.user2Type2])
            strongDen =  (strongMap[state.user2Type1] * strongMap[state.user2Type2])
            if(quickDen == 0):
                quick = 0.0001
            else:
                quick = 1/quickDen
            if(strongDen == 0):
                strong = 0.0001
            else:
                strong = 1/strongDen
            quickAtkMap = atkMult[state.user2QType]
            strongAtkMap = atkMult[state.user2SType]
            quickAtk = quickAtkMap[state.oppType1] * quickAtkMap[state.oppType2]
            strongAtk = strongAtkMap[state.oppType1] * strongAtkMap[state.oppType2]
        elif (active == 3):
            quickDen =  (quickMap[state.user3Type1] * quickMap[state.user3Type2] )
            strongDen =  (strongMap[state.user3Type1] * strongMap[state.user3Type2] )
            if(quickDen == 0):
                quick = 0.0001
            else:
                quick = 1/quickDen
            if(strongDen == 0):
                strong = 0.0001
            else:
                strong = 1/strongDen
            quickAtkMap = atkMult[state.user3QType]
            strongAtkMap = atkMult[state.user3SType]
            quickAtk = quickAtkMap[state.oppType1] * quickAtkMap[state.oppType2]
            strongAtk = strongAtkMap[state.oppType1] * strongAtkMap[state.oppType2]

        if(quickAtk == 0):
            quickAtk += 0.0001
        if(strongAtk == 0):
            strongAtk += 0.0001
        a = [math.log(quick,2), math.log(strong,2), math.log(quickAtk,2), math.log(strongAtk,2)]
        avgMult = numpy.mean(a)
        rtn += avgMult

        rtn = rtn - math.log10(state.turns)
        return rtn

    # def stateAction(self, state, action, atkMult): # returns state, action, reward, next state
    #     newState = deepcopy(state)
    #     newState.turns = state.turns + 1
    #     active = 0
    #     if(state.user1Active):
    #         active = 1
    #     elif(state.user2Active):
    #         active = 2
    #     elif(state.user3Active):
    #         active = 3
    #     else:
    #         if( (not(state.user1HP == 0)) or (not (state.user2HP == 0)) or (not (state.user3HP==0))):
    #             print("we don't know who's active")
    #             sys.exit(1)
    #         return None
    #     if(action == "quick"):
    #         if(active == 1):
    #             damage = state.user1QDmg + 2/3 (state.user1Atk - state.oppDef)
    #             multiplierMap = atkMult[state.user1QType]
    #             multiplier = multiplierMap[oppType1] * multiplierMap[oppType2]
    #             totalDmg = multiplier * damage
    #             if(totalDmg < 5):
    #                 totalDmg = 5
    #             newState.oppHP = state.oppHP - totalDmg
    #         elif(active == 2):
    #             damage = state.user2QDmg + 2/3 (state.user2Atk - state.oppDef)
    #             multiplierMap = atkMult[state.user2QType]
    #             multiplier = multiplierMap[oppType1] * multiplierMap[oppType2]
    #             totalDmg = multiplier * damage
    #             if(totalDmg < 5):
    #                 totalDmg = 5
    #             newState.oppHP = state.oppHP - totalDmg
    #         else:
    #             damage = state.user3QDmg + 2/3 (state.user3Atk - state.oppDef)
    #             multiplierMap = atkMult[state.user3QType]
    #             multiplier = multiplierMap[oppType1] * multiplierMap[oppType2]
    #             totalDmg = multiplier * damage
    #             if(totalDmg < 5):
    #                 totalDmg = 5
    #             newState.oppHP = state.oppHP - totalDmg
    #     elif(action == "strong"):
    #         if(active == 1):
    #             damage = state.user1SDmg + 2/3 (state.user1Atk - state.oppDef)
    #             multiplierMap = atkMult[state.user1SType]
    #             multiplier = multiplierMap[oppType1] * multiplierMap[oppType2]
    #             totalDmg = multiplier * damage
    #             if(totalDmg < 5):
    #                 totalDmg = 5
    #             newState.oppHP = state.oppHP - totalDmg
    #         elif(active == 2):
    #             damage = state.user2SDmg + 2/3 (state.user2Atk - state.oppDef)
    #             multiplierMap = atkMult[state.user2SType]
    #             multiplier = multiplierMap[oppType1] * multiplierMap[oppType2]
    #             totalDmg = multiplier * damage
    #             if(totalDmg < 5):
    #                 totalDmg = 5
    #             newState.oppHP = state.oppHP - totalDmg
    #         else:
    #             damage = state.user3SDmg + 2/3 (state.user3Atk - state.oppDef)
    #             multiplierMap = atkMult[state.user3SType]
    #             multiplier = multiplierMap[oppType1] * multiplierMap[oppType2]
    #             totalDmg = multiplier * damage
    #             if(totalDmg < 5):
    #                 totalDmg = 5
    #             newState.oppHP = state.oppHP - totalDmg
    #     elif(action == "switch1"):
    #         if(active == 1):
    #             if(state.user2HP > 0):
    #                 newState.user1Active = False
    #                 newState.user2Active = True
    #             elif(state.user3HP > 0):
    #                 newState.user1Active = False
    #                 newState.user3Active = True
    #         elif ( active ==2 ):
    #             if (state.user3HP>0):
    #                 newState.user2Active = False
    #                 newState.user3Active = True
    #             elif (state.user1HP > 0):
    #                 newState.user2Active = False
    #                 newState.user1Active = True
    #         else:
    #             if(state.user1HP > 0):
    #                 newState.user3Active = False
    #                 newState.user1Active = True
    #             elif (state.user2HP > 0):
    #                 newState.user3Active = False
    #                 newState.user1Active = True
    #     elif(action == "switch2"):
    #         if(active == 1):
    #             if(state.user3HP > 0):
    #                 newState.user1Active = False
    #                 newState.user3Active = True
    #             elif(state.user2HP > 0):
    #                 newState.user1Active = False
    #                 newState.user2Active = True
    #         elif ( active ==2 ):
    #             if (state.user1HP>0):
    #                 newState.user2Active = False
    #                 newState.user1Active = True
    #             elif (state.user3HP > 0):
    #                 newState.user2Active = False
    #                 newState.user3Active = True
    #         else:
    #             if(state.user2HP > 0):
    #                 newState.user3Active = False
    #                 newState.user2Active = True
    #             elif (state.user1HP > 0):
    #                 newState.user3Active = False
    #                 newState.user1Active = True
    #     reward = reward(action, state, atkMult)
    #     return state, action, reward, newState


    def chooseMove(self, team, activeOpp, typeMatchups, turns, monList, games):
        newState = State(monList, turns, team[0].name, team[0].active, team[0].hp, team[0].attack, team[0].defense, team[0].speed, team[0].type1, team[0].type2, team[0].quickMoveType, team[0].quickMovePower, team[0].quickMoveAcc, team[0].strongMoveType, team[0].strongMovePower, team[0].strongMoveAcc, team[1].name, team[1].active, team[1].hp, team[1].attack, team[1].defense, team[1].speed, team[1].type1, team[1].type2, team[1].quickMoveType, team[1].quickMovePower, team[1].quickMoveAcc, team[1].strongMoveType, team[1].strongMovePower, team[1].strongMoveAcc, team[2].name, team[2].active, team[2].hp, team[2].attack, team[2].defense, team[2].speed, team[2].type1, team[2].type2, team[2].quickMoveType, team[2].quickMovePower, team[2].quickMoveAcc, team[2].strongMoveType, team[2].strongMovePower, team[2].strongMoveAcc, activeOpp.name, activeOpp.hp, activeOpp.attack, activeOpp.defense, activeOpp.speed, activeOpp.type1, activeOpp.type2, activeOpp.quickMoveType, activeOpp.quickMovePower, activeOpp.quickMoveAcc, activeOpp.strongMoveType, activeOpp.strongMovePower, activeOpp.strongMoveAcc)
        if( (not (self.prevState == None))):
            self.trainTensorFlow(self.prevState, self.prevAction, self.prevReward, newState) #training the network

        action = self.testTensorFlow(newState, games) #get action from nn
        reward = self.reward(action, newState, typeMatchups)
        self.prevState = newState
        self.prevReward = reward
        self.prevAction = action

        # return action
        return action

    def cleanUp(self, games):
        #save stuff
        saver = tf.train.Saver()
        self.steps += games
        if(games == 0):
            self.steps += 1
        saver.save(self.sess, "./pokemon_model", global_step=self.steps)

        return True
