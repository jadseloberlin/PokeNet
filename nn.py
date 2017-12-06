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
        st = None
        et = (s, at, rt, st1)
        D.append(et)

        while len(D) > 0:
            #if running slow change while loop
            et = D.pop()
            nQ = sess.run(predict, feed_dict = {state:st1})
            i = labelList.index(et.at)
            m = [0] *numActions
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




if __name__ == '__main__':
    main()
