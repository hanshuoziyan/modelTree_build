from numpy import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import sys

def loadDataSet(fr):
    #fr = open(filename)
    x1 = []
    x2 = []
    y = []
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        x1.append(float(curLine[0]))
        x2.append(float(curLine[1]))
        y.append(float(curLine[2]))
    return x1,x2,y
def loadDataSet_total(fileName,index,value):
    x1 = []
    y = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        if int(curLine[index]) == value:
            x1.append(float(curLine[1-index]))#treat as two features
            y.append(float(curLine[-1]))

    return x1,y

def getSingleVar(fileName,index):
    fr = open(fileName)
    x1,x2,y = loadDataSet(fr)
    x_c = []
    y_c = []
    fig = plt.figure()
    if index == '0':
        new_x1 = list(set(x1))
        canva_nums = int(len(new_x1)/9)+1
        for index_j in xrange(canva_nums):
            for i in xrange(9):
                index_ij = 9*index_j+i
                if index_ij < len(new_x1):
                    x_c,y_c = loadDataSet_total(fileName,0,int(new_x1[index_ij]))
                    ax = plt.subplot(331+i)
                    ax.scatter(x_c,y_c)
                    ax.set_xlabel('x')
                    ax.set_ylabel('y')
            plt.show()
    if index == '1':
        new_x1 = list(set(x2))
        canva_nums = int(len(new_x1)/9)+1
        for index_j in xrange(canva_nums):
            for i in xrange(9):
                index_ij = 9*index_j+i
                if index_ij < len(new_x1):
                    x_c,y_c = loadDataSet_total(fileName,1,int(new_x1[index_ij]))
                    ax = plt.subplot(331+i)
                    ax.scatter(x_c,y_c)
                    ax.set_xlabel('x')
                    ax.set_ylabel('y')
            plt.show()



def get3DGraph(x1,x2,y):
    #fr = open(filename)
    #x1,x2,y = loadDataSet(fr)
    #print x1,x2,y
    fig = plt.figure()
    ax = plt.subplot(311,projection='3d')
    #ax = Axes3D(fig)
    ax.scatter3D(x1,x2,y)
    ax_2d_x1  = plt.subplot(312)
    ax_2d_x1.scatter(x1,y)
    ax_2d_x2 = plt.subplot(313)
    ax_2d_x2.scatter(x2,y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

def getSmaller(a,b):
    return (a<=b)
def getBigger(a,b):
    return (a>b)

def getRangeData(fileName,index,value,Fun):
    fr = open(fileName)
    x1 = []
    x2 = []
    y = []
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        #if int(curLine[index]) < int(value):
        if Fun(int(curLine[index]), int(value)):
            x1.append(float(curLine[1-index]))#treat as two features
            x2.append(float(curLine[index]))
            y.append(float(curLine[-1]))

    return x1,x2,y


if __name__=='__main__':
    if sys.argv[2] == 'total':
        fr = open(sys.argv[1])
        x1,x2,y = loadDataSet(fr)
        if len(sys.argv) > 3:
            if sys.argv[3] == 'small':
                x1,x2,y = getRangeData(sys.argv[1],1,int(sys.argv[4]),getSmaller)
            if sys.argv[3] == 'big':
                x1,x2,y = getRangeData(sys.argv[1],1,int(sys.argv[4]),getBigger)
            if len(sys.argv) > 4:
                file = open(sys.argv[5],'w')
                for i in range(len(x1)):
                    file.write(str(x1[i])+'\t'+str(x2[i])+'\t'+str(y[i]))
                    file.write('\n')

        get3DGraph(x1,x2,y)


    if sys.argv[2] == 'singleVar':
        getSingleVar(sys.argv[1],sys.argv[3])
        #x1_m = range(4,64,2)
    #x2_m = range(96000,1000000,10)
    #[x1_r,x2_r] = meshgrid(x1_m,x2_m)
    #y_r = -611+308*x1_r+1.22e-3*x2_r
    #ax.plot_surface(x1_r,x2_r,y_r)#,rstride=2,cstride=2,cmap=plt.cm.coolwarm,alpha=0.8)
    '''result_x1 = []
    result_x2 = []
    result_y = []
    true_y = []
    for i in range(len(x1)):
        if x2[i] > 96000 and x2[i] < 1000000:
            y_new = -611+308*x1[i]+1.22e-3*x2[i]
            result_x1.append(x1[i])
            result_x2.append(x2[i])
            true_y.append(y[i])
            result_y.append(y_new)
   # ax.scatter3D(result_x1,result_x2,true_y)
    #ax.scatter3D(result_x1,result_x2,result_y,c = 'r',marker = '^')
'''


