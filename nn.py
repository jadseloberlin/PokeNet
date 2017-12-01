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
    iterNum = 10;
    # trainingSetPercent = float(sys.argv[5])
    seed = 1334
    completeList = []


    attributeList = []
    continuous = {}
    attributeValuesDict = {}
    attributeValuesDictList = {}
    labelList = []
    labelSet = set()

    binaryLabel = False

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

    for label in labelSet:
        labelList.append(label)
    if len(labelList) == 2:
        binaryLabel = True

    tempList = attributeValuesDict.items()
    for tup in tempList:
        attribute = tup[0]
        s = tup[1]
        tempList2 = []
        for value in s:
            tempList2.append(value)
        attributeValuesDictList[attribute] = tempList2

    for instance in completeList:
        processInstance(instance, attributeValuesDictList, labelList, binaryLabel, continuous, attributeList)

    #shuffle list
    random.seed(seed)
    shuffledCompleteList = list(completeList)
    random.shuffle(shuffledCompleteList)


    labelNum = len(labelList)
    if binaryLabel:
        labelNum = 1

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
    x = tf.placeholder(tf.float32, shape = [None, numAttributes])

    #create hidden layer
    W_hidden = tf.Variable(tf.truncated_normal([numAttributes, numNeurons], stddev = 0.1))
    b_hidden = tf.Variable(tf.constant(0.1, shape = [numNeurons]))
    net_hidden = tf.matmul(x, W_hidden) + b_hidden
    out_hidden = tf.sigmoid(net_hidden)

    #create output layer
    W_output = tf.Variable(tf.truncated_normal([numNeurons, numLabels], stddev = 0.1))
    b_output = tf.Variable(tf.constant(0.1, shape = [numLabels]))
    net_output = tf.matmul(out_hidden, W_output) + b_output
    if numLabels == 1:
        predict = tf.sigmoid(net_output)
    else:
        predict = tf.nn.softmax(net_output)

    #create the true labels
    y = tf.placeholder(tf.float32, shape = [None, numLabels])

    #create training
    if numLabels == 1:
        cost = tf.reduce_sum(0.5 * (y-predict) * (y - predict))
    else:
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=net_output))

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


def trainTensorFlow(complete, maxSteps):
    saver = tf.train.Saver()

    sess = tf.Session()
    loadTensorFlow(sess)

    #train

    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    y = graph.get_tensor_by_name("y:0")
    net_output = graph.get_tensor_by_name("net_output:0")

    #create training
    if numLabels == 1:
        cost = tf.reduce_sum(0.5 * (y-predict) * (y - predict))
    else:
        cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=net_output))

    trainer = tf.train.AdamOptimizer(learningRate).minimize(cost)

    steps = 0
    maxSteps = iterNum
    while steps < maxSteps:
        steps +=1
    #    confusionMatrix = [[0 for x in range(len(labelList))] for y in range(len(labelList))]
        p = sess.run(trainier, feed_dict = {x: complete[0], y:complete[1]})

        accuracyNum = 0.0
        accuracyDenom = 0.0

        for i in range(len(p)):
            instance = p[i]
            trueLabel = train[1][i]
            trueIndex= -1
            guessIndex = -1
            if len(instance) == 1:
                trueIndex= trueLabel[0]
                guessVal = instance[0]
                if guessVal >= .5:
                  guessIndex = 1
                else:
                  guessIndex = 0
            else:
                trueIndex = trueLabel.index(max(trueLabel))
                guessVal = instance[0]
                guessIndex = 0
                for i in range(1,len(instance)):
                    val = instance[i]
                    if val > guessVal:
                      guessVal = val
                      guessIndex = i
            if(trueIndex==guessIndex):
                accuracyNum+=1
            accuracyDenom+=1
        if steps % 10 == 0:
            print(accuracyNum/accuracyDenom)
            saver.save(sess, 'pokemon_model', global_step=steps)

    #Create a saver object which will save all the variables

    #Now, save the graph


def testTensorFlow(complete):

    sess = tf.Session()
    loadTensorFlow(sess)
    graph = tf.get_default_graph()
    x = graph.get_tensor_by_name("x:0")
    predict = graph.get_tensor_by_name("predict:0")

    #test
    # confusionMatrix = [[0 for x in range(len(labelList))] for y in range(len(labelList))]
    p = sess.run(predict, feed_dict = {x: complete[0]})

    accuracyNum1 = 0.0
    accuracyDenom1 = 0.0

    for i in range(len(p)):
        instance = p[i]
        trueLabel = test[1][i]
        trueIndex= -1
        guessIndex = -1
        if len(instance) == 1:
          trueIndex= trueLabel[0]
          guessVal = instance[0]
          if guessVal >= .5:
            guessIndex = 1
          else:
            guessIndex = 0
        else:
          trueIndex = trueLabel.index(max(trueLabel))
          guessVal = instance[0]
          guessIndex = 0
          for i in range(1,len(instance)):
            val = instance[i]
            if val > guessVal:
              guessVal = val
              guessIndex = i
        if(trueIndex==guessIndex):
            accuracyNum1+=1
        accuracyDenom1+=1

    accuracy = accuracyNum1/accuracyDenom1
    print("test accuracy " + str(accuracy))



def processInstance(instance, attributeValuesDictList, labelList, binaryLabel, continuous, attList):
    instance.labelListProcess(labelList, binaryLabel)
    instance.attributeListProcess(attributeValuesDictList, continuous, attList)

if __name__ == '__main__':
    main()
