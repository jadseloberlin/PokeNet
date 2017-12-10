from instance import Instance
import math
import random
import sys
import tensorflow as tf

def main():
    # fileLocation = sys.argv[1]
    # numNeurons = int(sys.argv[2])
    # learningRate = float(sys.argv[3])
    # iterNum = int(sys.argv[4])
    # trainingSetPercent = float(sys.argv[5])
    numNeurons = 50
    learningRate = .07
    iterNum = 750;
    # trainingSetPercent = float(sys.argv[5])
    seed = 1334
    completeList = []


    attributeList = []
    continuous = {}
    attributeValuesDict = {}
    attributeValuesDictList = {}
    labelList = [] #hardcode!
    labelSet = set()  #hardcode!

    #open file and process data
    path = '*.csv' #note C:
    files = glob.glob(path)
    # dataFile = open(fileLocation, 'r')
    line = next(dataFile)
    attributeList = line.split(",")
    for i in range(1,len(attributeList)):
        attribute = attributeList[i]
        continuous[attribute] = False
        attributeValuesDict[attribute] = set()
    for line in dataFile:
        dic = {}
        arr = line.split(",")
        if arr[0] not in labelSet:
            labelSet.add(arr[0])
        for i in range(1,len(attributeList)):
            att = attributeList[i]
            dic[att] = arr[i]
            try:
                f = float(arr[i])
                continuous[att] = True
            except:
                #find all posssible types of certain attribute
                atSet = attributeValuesDict[att]
                if arr[i] not in atSet:
                    atSet.add(arr[i])
                    attributeValuesDict[att] = atSet
        newInst = Instance(dic, arr[0])
        completeList.append(newInst)

    del attributeList[0]



    tempList = attributeValuesDict.items()
    for tup in tempList:
        attribute = tup[0]
        s = tup[1]
        tempList2 = []
        for value in s:
            tempList2.append(value)
        attributeValuesDictList[attribute] = tempList2

    for instance in completeList:
        processInstance(instance, attributeValuesDictList, labelList, continuous, attributeList)

    #shuffle list
    random.seed(seed)
    shuffledCompleteList = list(completeList)
    random.shuffle(shuffledCompleteList)


    labelNum = len(labelList)

    listAtt = []
    listLab = []
    for instance in completeList:
        listAtt.append(instance.attributeList)
        listLab.append(instance.labelList)

    tupleComplete = (listAtt, listLab)

    instance = completeList[0]
    numAtt = len(instance.attributeList)

    buildTensorFlow(numAtt, labelNum, 50, .07, iterNum, labelList, 1334)
    trainTensorFlow(tupleComplete, 10)

def buildTensorFlow(numAttributes, numLabels, numNeurons, learningRate, iterNum, labelList, seed):
    # state = tf.placeholder(tf.float32, shape = [numLabels])
    # r = tf.placeholder(tf.float32, shape = [bumActions])
    # predict = tf.placeholder(tf.float32, shape = [numLabels])
    # oldPredict  = tf.placeholder(tf.float32, shape = [numLabels])
    # mask = tf.placeholder(tf.float32, shape = [1])

    state = tf.placeholder(tf.float32, shape = [numLabels])
    nextQ = tf.placeholder(tf.float32, shape = [numActions])
    r = tf.placeholder(tf.float32, shape = [numActions])
    mask = tf.placeholder(tf.float32, shape = [1])

    #create hidden layer
    W_hidden = tf.Variable(tf.truncated_normal([numAttributes, numNeurons], stddev = 0.1))
    b_hidden = tf.Variable(tf.constant(0.1, shape = [numNeurons]))
    net_hidden = tf.matmul(state, W_hidden) + b_hidden
    out_hidden = tf.sigmoid(net_hidden)

    #create output layer
    W_output = tf.Variable(tf.truncated_normal([numNeurons, numLabels], stddev = 0.1))
    b_output = tf.Variable(tf.constant(0.1, shape = [numLabels]))
    net_output = tf.matmul(out_hidden, W_output) + b_output
    predict = net_output
    action = tf.argmax(net_input,1)

    #create the true labels
    y = tf.placeholder(tf.float32, shape = [None, numLabels])

    cost = (r * mask + tf.max(nextQ) * mask - mask*predict)**2

    trainer = tf.train.AdamOptimizer(learningRate).minimize(cost)

    #start a TF session
    sess = tf.Session()
    init = tf.initialize_all_variables().run(session = sess)
    saver.save(sess, 'pokemon_model', global_step=0)


def loadTensorFlow(sess):
    save_dir = "."
    ckpt = tf.train.get_checkpoint_steate(save_dir)
    load_path = ckpt.model_checkpoint_path
    saver.restore(sess, load_path)

def trainTensorFlow(complete, maxSteps, numActions):
    saver = tf.train.Saver()
    sess = tf.Session()
    loadTensorFlow(sess)
    graph = tf.get_default_graph()

    state = graph.get_tensor_by_name("state:0")
    y = graph.get_tensor_by_name("y:0")
    predict = graph.get_tensor_by_name("predict:0")
    nextQ = graph.get_tensor_by_name("nextQ:0")
    action = graph.get_tensor_by_name("action:0")
    trainer = graph.get_tensor_by_name("trainer:0")
    r = graph.get_tensor_by_name("r:0")
    mask = graph.get_tensor_by_name("mask:0")


    D = []
    steps = 0
    maxSteps = iterNum
    while steps < maxSteps:
        steps +=1
        # st,at,rt,st1 = call method
        et = (st, at, rt, st1)
        D.append(et)

        shuffleD = random.shuffle(D)
        T = []

        for i in range(0, math.ceil(len(D)/2)):
            T.append(D[i])

        while len(T) > 0:
            #if running slow change while loop
            et = T.pop()
            nQ = sess.run(predict, feed_dict = {state:et.st1})
            i = labelList.index(et.at)
            m = [0] * numActions
            m[i] = 1
            sess.run(trainer, feed_dict = {mask: m, reward:r, state:st, nextQ: nQ})
            if steps % 10 == 0:
                saver.save(sess, 'pokemon_model', global_step=steps)

def testTensorFlow(complete):
    saver = tf.train.Saver()
    sess = tf.Session()
    loadTensorFlow(sess)
    graph = tf.get_default_graph()

    state = graph.get_tensor_by_name("state:0")
    y = graph.get_tensor_by_name("y:0")
    predict = graph.get_tensor_by_name("predict:0")
    oldPredict = graph.get_tensor_by_name("oldPredict:0")
    action = graph.get_tensor_by_name("action:0")
    trainer = graph.get_tensor_by_name("trainer:0")
    r = graph.get_tensor_by_name("r:0")
    mask = graph.get_tensor_by_name("mask:0")

    #test
    p = sess.run(predict, feed_dict = {state: complete[0]})


def processInstance(instance, attributeValuesDictList, labelList, continuous, attList):
    instance.labelListProcess(labelList)
    instance.attributeListProcess(attributeValuesDictList, continuous, attList)

def update():
    p = sess.run(predict, feed_dict = {x: et.st})
    qsa= [0] * len(p) #create matrix
    qsa[et.at] = p[et.at] #Q(st, at)

    qsa2 = [0] * len(p) #create matrix
    mask[et.at] = 1

    p = sess.run(predict, feed_dict = {x: et.st+1})
    maxP = max(p)



# code for interacting w simulator

def reward(self, action, state):
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
    rtn += math.log10(damage)
    acc = acc / 100
    rtn = rtn * acc

    if(state.oppHP - (damage * acc) < 1): #fainting bonus
        rtn += 2.5

    quickMap = self.atkMulk[state.oppQType]
    strongMap = self.atkMult[state.oppSType]
    quick = 1 #defending muliplier
    strong = 1 #defending multiplier
    quickAtk = 1 # attacking multiplier
    strongAtk = 1 # attacking multiplier

    if(active == 1 ):
        quick = 1 / (quickMap[state.user1Type1] * quickMap[state.user1Type2])
        strong = 1 / ( strongMap[state.user1Type1] * strongMap[state.user1Type2] )
        quickAtkMap = self.atkMulk[state.user1QType]
        strongAtkMap = self.atkMult[state.user1SType]
        quickAtk = quickAtkMap[state.oppType1] * quickAtkMap[stte.oppType2]
        strongAtk = strongAtkMap[state.oppType1] * strongAtkMap[state.oppType2]
    elif (active == 2):
        quick = 1 / (quickMap[state.user2Type1] * quickMap[state.user2Type2])
        strong = 1 / (strongMap[state.user2Type1] * strongMap[state.user2Type2])
        quickAtkMap = self.atkMulk[state.user2QType]
        strongAtkMap = self.atkMult[state.user2SType]
        quickAtk = quickAtkMap[state.oppType1] * quickAtkMap[stte.oppType2]
        strongAtk = strongAtkMap[state.oppType1] * strongAtkMap[state.oppType2]
    elif (active == 3):
        quick = 1 / (quickMap[state.user3Type1] * quickMap[state.user3Type2] )
        strong = 1 / (strongMap[state.user3Type1] * strongMap[state.user3Type2] )
        quickAtkMap = self.atkMulk[state.user3QType]
        strongAtkMap = self.atkMult[state.user3SType]
        quickAtk = quickAtkMap[state.oppType1] * quickAtkMap[stte.oppType2]
        strongAtk = strongAtkMap[state.oppType1] * strongAtkMap[state.oppType2]

    a = [math.log(quick,2), math.log(strong,2), math.log(quickAtk,2), math.log(strongAtk,2)]
    avgMult = numpy.mean(a)
    rtn += avgMult

    rtn = rtn - math.log10(state.turns)
    return rtn

def stateAction(self, state, action): # returns state, action, reward, next state
    newState = deepcopy(state)
    newState.turns = state.turns + 1
    if(action == "quick"):
        print()
    elif(action == "strong"):
        print()
    elif(action == "switch1"):
        print()
    elif(action == "switch2"):
        print()

    reward = reward(action, state)
    return state, action, reward, newState





if __name__ == '__main__':
    main()
