#
#hw3 comp135
#Xu Liu
#
import math
import numpy
import random
import argparse

class cluster:
    def __init__(self, filename, k):
        self.data = {}
        self.attributes = []
        self.classes = {}
        self.type = []
        self.kmean = []
        self.readData(filename)
        self.cs = 0
        self.nmi = 0
        if k == 0:
            self.k = len(self.type)
        else:
            self.k = k
        
    
    def readData(self, filename):
        src = open(filename)
        line = src.readline()
        
        while line[: 5] != "@DATA":
            if line[:10] == "@ATTRIBUTE" :
                self.attributes.append(line.split(' ')[1])
            line = src.readline()
        line = src.readline()
        
        while line != '':
            tmp = line.strip().split(',')
            if tmp[-1] in self.data:
                self.data[tmp[-1]].append(\
                    [float(tmp[i]) for i in range( len(tmp) - 1)])
            else:
                self.data[tmp[-1]] = \
                [[float(tmp[i]) for i in range( len(tmp) - 1)]]
                self.type.append(tmp[-1])
            line = src.readline() 
        src.close()
        
    
    def distance(self, p1, p2):
        tmp1 = numpy.array(p1)
        tmp2 = numpy.array(p2)
        tmprlt = tmp1 - tmp2
        return math.sqrt(numpy.dot(tmprlt, tmprlt.T))
    
    def isstable(self, old_kmean, new_kmean):
        for i in range(len(old_kmean)):
            if self.distance(old_kmean[i], new_kmean[i])\
                > 0.0000000001:
                return False
        return True
    
    def which_class(self, kmean, point):
        min_dis = float('inf')
        t = 0
        for i in range(len(kmean)):
            dis = self.distance(kmean[i], point)
            if dis < min_dis:
                min_dis = dis
                t = i
        return t

    def mean(self, cl):
            sum = numpy.zeros(len(cl[0]))
            size = len(cl)
            for i in range(size):
                sum = sum + numpy.array(cl[i])
            tmp =(sum/size).tolist()
            return tmp
                
               

    def classify(self):
        k = self.k
        self.kmean = []
        self.classes.clear()
        
        collection = []
        for i in range(len(self.type)):
            collection = collection + self.data[self.type[i]]
        tmp_kmean = []
        for i in range(k):
            tmp_kmean.append(numpy.zeros(len(collection[0])).tolist())
        
        random.seed()
        selected = []
        while len(selected) < k:
            tmp_selected = random.randint(0, len(collection) - 1)
            if tmp_selected not in selected:
                self.kmean.append(collection[tmp_selected])
                selected.append(tmp_selected)
            
        
        while not self.isstable(self.kmean, tmp_kmean):
            for i in range(k):
                tmp_kmean[i] = self.kmean[i]
                
            self.classes.clear()
            for i in range(k):
                self.classes[str(i)] = []
            length = len(collection)
            for i in range(length):
                self.classes[str(self.which_class(tmp_kmean, collection[i]))]\
                                                        .append(collection[i])
            #in case there is empty set,
            #I am wondering if there really is 
            for i in range(k):
                if len(self.classes[str(i)]) == 0:
                    self.classify()
                    return
            for i in range(k):
                self.kmean[i] = self.mean(self.classes[str(i)])
                
        
                
                     
           
    def cal_cs(self):
        self.cs = 0        
        for i in range(self.k):
            t = str(i)
            size = len(self.classes[t])
            mean_i = numpy.array(self.kmean[i])
            class_sum = 0
            for j in range(size):
                tmp = numpy.array(self.classes[t][j])\
                      - mean_i
                tmp = numpy.dot(tmp, tmp.T)      
                class_sum = class_sum + tmp
            self.cs = self.cs + class_sum
            
        
    def cal_nmi(self):
        self.nmi = 0
        inter_matrix = []
        for i in range(len(self.classes)):    
            row = []
            for j in self.type:
                count = 0
                for h in self.data[j]:
                    if h in self.classes[str(i)]:
                        count = count + 1   
                row.append(count)
            inter_matrix.append(row)
        N = 0
        for i in self.type:
            N = N + len(self.data[i])
        
        I_uv = 0
        for i in range(len(self.classes)):
            for j in range(len(self.type)):
                if inter_matrix[i][j] == 0:
                    continue
                n_ij = inter_matrix[i][j]
                a_i = len(self.classes[str(i)])
                b_j = len(self.data[self.type[j]])
                I_uv = I_uv + (float(n_ij)/N)*\
                      math.log((float(n_ij)/N)/((a_i * b_j)/float(N*N)), 2)
                
        H_u = 0
        for i in range(len(self.classes)):
            a_i = len(self.classes[str(i)])
            H_u = H_u - (float(a_i)/N)*math.log(float(a_i)/N, 2)
            
        H_v = 0
        for j in self.type:
            b_j = len(self.data[j])
            H_v = H_v - (float(b_j)/N)*math.log(float(b_j)/N, 2)

        self.nmi = 2 * I_uv /(H_u + H_v)
        
        
            


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", action="store",\
                        dest="filename", required=True)
    parser.add_argument("-k", "--classes", action="store",\
                        dest="classes", type=int, required=True)
    parser.add_argument("-r", "--rlt", action="store",\
                        dest="rlt", type=int, required=True)
    args = parser.parse_args()
    
    mycluster = cluster(args.filename, args.classes)
    mycluster.classify()
    
    
    if args.rlt == 0:
        mycluster.cal_cs()
        print mycluster.cs
    elif args.rlt == 1:
        mycluster.cal_nmi()
        print mycluster.nmi
    elif args.rlt == 3:
        mycluster.cal_cs()
        mycluster.cal_nmi()
        print mycluster.cs,  mycluster.nmi
        
    
    
    
    
        
    
            
        
