# HW1  comp 135
# Xu Liu

import sys
import numpy as np
import math
import random
import argparse

#knn alogrithm with weight or not
# data is instances set, k is neighbours need to explore, 
#w is weight with 1 as default value        
#return tpos, fpos, tneg, fneg, accuracy               
def knn(data, k, w):
    candidate = [[float("inf"), 0]]
    instances = len(data)
    
    pos_in = 0
    tpos = 0
    fpos = 0
    tneg = 0
    fneg = 0
    #check how many instances are 1.
    for ins in data:
        pos_in = pos_in + ins[-1]        
    #classify every instance
    for target in data :
        #find k nearest neighours for the target
        for others in data:
            if target == others:
                continue
            dist = Ed(target, others, w)
            c_len = k if len(candidate) > k else len(candidate)
            for i in range(0, c_len):
                if candidate[i][0] > dist:
                    candidate.insert(i, [dist, others[-1]])
                    break;
        #check how many neighours are 1
        cl = 0
        for i in range(0, k):
            cl = cl + candidate[i][1]
        #classify target as 1 if # of 1's are major otherwise as 0
        if (cl > k/2) :
            if (target[-1] == 1):
                tpos = tpos + 1
            else:
                fpos = fpos + 1
        else :
            if (target[-1] == 0):
                tneg = tneg + 1
            else:
                fneg = fneg + 1    
        candidate = [[float("inf"), 0]]
    return tpos, fpos, tneg, fneg, float(tpos + tneg)/instances

#take data set and the times of relief as parameter
#return two weight:
# one weight is 1's at top 14 features positions 0's at other positions
# the other weight is 0's for negtive features and keeping positive features 
def relief(train, m):
    oneset = []
    zeroset = []
    #seperate the data set according to eye_detection
    for inst in train:
        if(inst[-1] == 1):
            oneset.append(inst)
        else:
            zeroset.append(inst)
    weight = np.zeros(len(train[0]))
    posN = [float("inf"), 0]
    negN = [float("inf"), 0]
    #repeat m times to calculate weight
    for i in range(0, m):
        pick = train[random.randint(0, len(train) - 1)]
        for inst in oneset:
            if (pick == inst):
                continue
            dist = Ed(pick, inst)
            if dist < posN[0]:
                    posN = [dist, inst]

        for inst in zeroset:
            if (pick == inst):
                continue
            dist = Ed(pick, inst)
            if dist < negN[0]:
                negN = [dist, inst] 
            
            
        weight = weight - [abs(pick[i] - posN[1][i]) for i in range(0, len(posN[1]))] + \
                 [abs(pick[i] - negN[1][i]) for i in range(0, len(negN[1]))]
    #rslt_w is the weight keeping only positive features and changing negative features
    #to 0's
    rslt_w = [weight[i] if (weight[i] > 0) else 0 for i in range(0, len(weight))]
    #rslt_14 keep top 14 features
    rslt_14 = [1 for i in range(0, len(weight))]
    if (len(weight) > 15):
        w_index = [[float("-inf"), len(weight) - 1]]     
        for i in range(0, len(weight) - 1):
            for j in range(0, len(w_index)):
                if (weight[i] > w_index[j][0]):
                    w_index.insert(j, [weight[i], i])
                    break;
        for i in range(0, 14):
                rslt_14[w_index[i][1]]= 1
        for i in range(14, len(w_index) - 1):
                rslt_14[w_index[i][1]] = 0
         
    return (rslt_w, rslt_14)

#calculate distance of two instances, default weight is 1    
def Ed(p1, p2, *w):
    if len(w) == 0 :
        weight = np.ones_like(p1)
    else :
        weight = np.array(w[0])
    sqr = np.array([(p1[i] - p2[i])*(p1[i] - p2[i]) \
                       for i in range(0, len(p1))])
    
    return math.sqrt(np.dot(sqr[0: -1], weight[0:-1].T))
    
    

def readData(file) :
    attr = []
    src = open(file)
    line = src.readline()
    while line[: 5] != "@DATA":
        if line[:9] == "@Relation" :
            relation = line.split(' ')[1][:-2]
        if line[:10] == "@ATTRIBUTE" :
            attr.append(line.split(' ')[1])
        line = src.readline()
    data = []
    line = src.readline()
    while line != '':
        tmp = line.split(',')
        data.append([float(tmp[i]) for i in range(0, len(tmp))])
        line = src.readline()
    src.close()
    return data    
    
 
                
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-T", "--test", action="store", dest="testfile", help="test file is required", required=True)
    parser.add_argument("-t", "--train", action="store", dest="trainfile", help="train file ", required=True)
    parser.add_argument("-o", "--output", action="store", dest="outfile", help="out file is required", required=True)
    parser.add_argument("-k", "--neighbours", action="store", dest="nb", type=int, help="number of neighbours to explore, required", required=True)
    parser.add_argument("-rt", "--relieftimes", action="store", dest="relt", type=int, help="relief times, required", required=True)
    parser.add_argument("-rk", "--reliefkinds", action="store", dest="relk", choices= ['o', 'w', 'a'], help="relief kinds info")
    args = parser.parse_args()
    train = readData(args.trainfile)
    #result of original knn alogrithm
    r_o = [0, 0, 0, 0, 0]
    #result according to top 14 features
    r_14 = [0, 0, 0, 0, 0]
    #result according to weight
    r_w = [0, 0, 0, 0, 0]
    test = readData(args.testfile)
    
    if(args.relk == 'a' or args.relk == 'o'):
        uniform = np.ones_like(test[0])
        r_o = knn(test, args.nb, uniform)
    if(args.relk == 'a' or args.relk == 'w'):
        w, w_14 = relief(train, args.relt)
        r_14 = knn(test, args.nb, w_14)
        r_w = knn(test, args.nb, w)
    out = open(args.outfile, 'a')
    #only keep accuracy for plotting
    print >> out, "Accuracy   %f  %f  %f" % (r_o[4], r_14[4], r_w[4])
    out.close()

 
        
    
