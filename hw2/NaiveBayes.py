# Project 2  comp 135
# Xu Liu
# Navie Bayes with cross validation

import sys
import numpy as np
import math
import argparse



#read index file, return instances space
def readIndex(filename) :
    src = open(filename)
    space = []
    line = src.readline()
  
    while line != '':
        tmp = line.split('|')
        space.append([tmp[0], tmp[1]])
        line = src.readline()
         
    src.close()
    return space 
 
#seperate instances space into k folds
#return the list of k folds
def straitify(space, k):
    #class yes
    cly = []
    #class no
    cln = []
    for e in space:
        if e[1] == 'yes':
            cly.append(e)
        else:
            cln.append(e)
    cly = np.random.permutation(cly).tolist()
    clylen = len(cly)
         
    cln = np.random.permutation(cln).tolist()
    clnlen = len(cln)
    
    straitified = []
    subsizey = len(cly)/k + 1
    subsizen = len(cln)/k + 1

    for i in range(k):
        beginy = i * subsizey
        beginn = i * subsizen   
        endy = (i + 1) * subsizey \
        if (i+1)*subsizey < len(cly) else len(cly)
        endn = (i + 1) * subsizen \
        if (i + 1) * subsizen < len(cln) else len(cln)
        
        straitified.append(cly[beginy:endy] + cln[beginn:endn])
       
    return straitified

#cross validation of the k folds        
def cross_val(straitified, path, k, smooth, trainsize):
    acc = []
    #repeat k times on different choice of test set 
    for i in range(k):
        trainset = []
        for j in range(k):
            if j != i:
                trainset = trainset + straitified[j]
        #learning on train sets
        knowledge = learn_on_sub(trainset, path, trainsize)
        #add accuracy of testing 
        acc.append(test(straitified[i], path, knowledge, smooth))
  
    #average accuracy
    average = np.mean(acc)
    std = np.std(acc)
     
    return average, std

#learning on train sets        
def learn_on_sub(trainset, path, size):
    # frequence information from train set
    knowledge = {}
    # frequence of every feature in yes of train sets
    frqY = {}
    # frequence of every feature in no of train sets
    frqN = {}
    # total counts of all features in yes of all train sets
    total_f_y = 0
    # total counts of all features in no of all train sets
    total_f_n = 0
    # total number of yes in train sets
    nmb_y = 0
     # total number of no in train sets 
    nmb_n = 0

    straitified = straitify(trainset, 10)  
    #determine train set index range
    indexrange = int(math.floor(10 * size))
        
   
    #learn on train set    
    for index in range(indexrange):
        for e in straitified[index]:
            filename = path + e[0] + ".clean"
            features = readFeature(filename)
            #calculate frequency(feature|yes), frequency(yes) and freq(all features in yes)
            if e[1] == 'yes':
                nmb_y = nmb_y + 1
                total_f_y = total_f_y + len(features)
                for f in features:
                    if frqY.has_key(f):
                        frqY[f] = frqY[f] + 1
                    else:
                        frqY[f] = 1                    
            #calculate frequency(feature|no), frequency(no) and  freq(all features in no)       
            if e[1] == 'no':
                nmb_n = nmb_n + 1
                total_f_n = total_f_n + len(features)
                 
                for f in features:
                    if frqN.has_key(f):
                        frqN[f] = frqN[f] + 1
                    else:
                        frqN[f] = 1                   
    
    knowledge["frqy"] = frqY 
    knowledge["frqn"] = frqN 
    knowledge["total_f_y"] = total_f_y 
    knowledge["total_f_n"] = total_f_n 
    knowledge["nmb_y"] = nmb_y
    knowledge["nmb_n"] = nmb_n
    return knowledge    

#read in features for designated file
#return a list of features        
def readFeature(filename) :
    src = open(filename)
    f = []
    line = src.readline()
    while line != '':
        tmp = line.split()
        f = f + tmp
        line = src.readline()
    src.close()  
    return f

#testing on test set
#return accuracy of the test
def test(testset, path, knowledge, smooth):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    
    for e in testset:
        filename = path + e[0] + ".clean"
        features = np.unique(readFeature(filename)).tolist()
        class_y = yes(features, knowledge, smooth)
        if class_y == 'yes':
            if e[1] == 'yes':
                tp = tp + 1
            else:
                fp = fp + 1
        else:
            if e[1] == 'no':
                tn = tn + 1
            else:
                fn = fn + 1
    return float(tp + tn)/(fp + fn + tp + tn)
            
    
#determine if a instance is yes or no
#return true if yes otherwise no
def yes(features, knowledge, smooth):
    
    #calculate probability of yes
    p_y = math.log(np.true_divide(float(knowledge["nmb_y"]), (knowledge["nmb_y"] + knowledge["nmb_n"])))
    p_f_y = p_y
    #calculate probability of no
    p_n = math.log(np.true_divide(float(knowledge["nmb_n"]), (knowledge["nmb_y"] + knowledge["nmb_n"])))
    p_f_n = p_n
    for e in features:
        #calculate p(yes|features)
        if (not knowledge["frqy"].has_key(e)) and (not knowledge["frqn"].has_key(e)):
            continue
        tmp = (0 if (not knowledge["frqy"].has_key(e)) else knowledge["frqy"][e]) + smooth
        if tmp == 0:
            p_f_y =float('-inf')
        else:
            p_f_y = p_f_y + math.log(float(tmp)/(len(knowledge["frqy"]) * smooth + knowledge["total_f_y"]))
        
        #calculate p(no|features) 
        tmp = (0 if (not knowledge["frqn"].has_key(e)) else knowledge["frqn"][e]) + smooth
        if tmp == 0:
            p_f_n =float('-inf')
        else:
            p_f_n = p_f_n + math.log(float(tmp)/(len(knowledge["frqn"]) * smooth + knowledge["total_f_n"]))

    if (p_f_y == float('-inf') and p_f_n == float('-inf')):
        rlt = 'yes' if p_y > p_n else 'n0'     
    else:
        rlt = 'yes' if p_f_y > p_f_n else 'no' 
    return rlt
        
 
                
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action="store", dest="path", help="path of data files", required=True)
    parser.add_argument("-s", "--smooth", action="store", dest="smooth", type=float, help=" ", required=True)
    parser.add_argument("-k", "--folds", action="store", dest="folds", type=int, help="cross folds", required=True)
    parser.add_argument("-t", "--trainsize", action="store", dest="trainsize", type=float, help="size of train set", required=True)
    args = parser.parse_args()
 
    space = readIndex(args.path+'index.Full')
    straitified = straitify(space, args.folds) 
    rlt = cross_val(straitified, args.path, args.folds, args.smooth, args.trainsize)
    print("folds  %3d  smooth  %3.1f  trainsize  %2.1f  %8.3f  %8.3f"\
              %(args.folds, args.smooth, args.trainsize, rlt[0], rlt[1]))
 
   
        
    
