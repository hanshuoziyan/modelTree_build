from numpy import *
import sys
def loadDataSet(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return dataMat
def binSplitDataSet(dataSet,feature,value):
    mat0 = dataSet[nonzero(dataSet[:,feature] > value)[0],:][0]
    mat1 = dataSet[nonzero(dataSet[:,feature] <= value)[0],:][0]
    return mat0,mat1

def linearSolve(dataSet):
    m,n = shape(dataSet)
    X = mat(ones((m,n))); Y = mat(ones((m,1)))
    X[:,1:n] = dataSet[:,0:n-1]; Y = dataSet[:,-1]
    xTx = X.T*X
    if linalg.det(xTx) == 0.0:
        raise NameError('this matrix is singular,cannot do inverse,\n try increasing the second value of ops')
    ws = xTx.I * (X.T * Y)
    return ws,X,Y

def regLeaf(dataSet):
    ws,X,Y = linearSolve(dataSet)
    return ws

def regErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y-yHat,2))

def chooseBestSplit(dataSet,leafType=regLeaf,errType=regErr,ops=(1,150)):
    tolS = ops[0]; tolN = ops[1]
    if len(set(dataSet[:,-1].T.tolist()[0])) == 1:
        return None,leafType(dataSet)
    m,n = shape(dataSet)
    S = errType(dataSet)
    bestS = inf; bestIndex = 0; bestValue = 0
    for featIndex in range(n-1):
        for splitVal in set(dataSet[:,featIndex]):
            mat0,mat1 = binSplitDataSet(dataSet,featIndex,splitVal)
            if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if(S-bestS) < tolS:
        return None,leafType(dataSet)
    mat0,mat1 = binSplitDataSet(dataSet,bestIndex,bestValue)
    if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
        return None,leafType(dataSet)
    return bestIndex,bestValue

def createTree(dataSet,leafType=regLeaf,errType=regErr,ops=(1,100)):
    feat,val = chooseBestSplit(dataSet,leafType,errType,ops)
    if feat == None: return val
    retTree={}
    retTree['spInd'] = feat
    retTree['spVal'] = val
    lSet,rSet = binSplitDataSet(dataSet,feat,val)
    retTree['left'] = createTree(lSet,leafType,errType,ops)
    retTree['right'] = createTree(rSet,leafType,errType,ops)
    return retTree


def printTree(treeDic):
    if type(treeDic) != dict: 
    #if 'spInd' not in treeDic.keys():
        print 1
        print 'leaf node: '+str(treeDic)
        return
    print 'spInd: '+str(treeDic['spInd'])
    print '  spVal: '+str(treeDic['spVal'])
    print '\n left child: \n'
    printTree(treeDic['left'])
    print 'right child: \n'
    printTree(treeDic['right'])

def isTree(obj):
    return (type(obj).__name__=='dict')

def modelTreeEval(model,inDat):
    n = shape(inDat)[1]
    X = mat(ones((1,n+1)))
    X[:,1:n+1] = inDat
    return float(X*model)

def treeForeCast(tree,inData, modelEval=modelTreeEval):
    if not isTree(tree):return modelEval(tree,inData)
    if inData[0,tree['spInd']] > tree['spVal']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inData,modelEval)
        else:
            return modelEval(tree['left'],inData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inData,modelEval)
        else:
            return modelEval(tree['right'],inData)

def createForeCast(tree,testData,modelEval=modelTreeEval):
    m = len(testData)
    yHat = mat(zeros((m,1)))
    for i in range(m):
        yHat[i,0] = treeForeCast(tree,mat(testData[i]),modelEval)
    return yHat

def testCorr(file):
    #myTestData = loadDataSet('corr/testDatafile')
    
    #myDat = loadDataSet('corr/datafile')
    myDat = loadDataSet(file)
    n_sample = len(myDat)
    sdix = random.permutation(n_sample)
    n_train = int(round(n_sample*0.9))
    '''
    myTestMat = []
    for s in sdix[n_train:]:
        myTestMat.append(myDat[s])
    '''
    myTestMat = mat([myDat[s] for s in sdix[n_train:]])
    myMat = mat([myDat[s] for s in sdix[:n_train]])
    
    #myTestMat =  mat(myTestData)
    #myMat = mat(myDat)
    myTree = createTree(myMat)
    yHat = createForeCast(myTree,myTestMat[:,0:2])
    import matplotlib.pyplot as plt
    ax = plt.subplot()
    ax.set_xlabel("true value")
    ax.set_ylabel("predicted value")
    ax.scatter(myTestMat[:,2],yHat)
    ax.plot(myTestMat[:,2],myTestMat[:,2],'r')
    plt.show()
    return corrcoef(yHat,myTestMat[:,2],rowvar=0)[0,1]



if __name__ == '__main__':
    myDat = loadDataSet(sys.argv[1])
    myMat = mat(myDat)
    myTree = createTree(myMat)
    #print myTree
    printTree(myTree)
    

