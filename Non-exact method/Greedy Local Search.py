import random
import itertools
import copy
import math

def generateClause(clauseNum):
    #Add NOT operator to the list (negative symbol = NOT operator)
    for x in range(0, len(V)):
        V_copy.append(V[x]*-1)
    
    #Generate all possible combinations from sample V
    clauses = list(itertools.combinations(V_copy, 3))

    if clauseNum < 5:
        return "The value must be at least 5 or more"

    elif clauseNum <= len(clauses):
        #Randomly select the number of clauses inputted
        chosenClause = random.sample(clauses, clauseNum)
        newList = [list(x) for x in chosenClause]
        
        for i in newList:
            #Randomize the literals' order of a clause
            random.shuffle(i)
            
        return newList

    else:
        return "Invalid value. The maximum number of clauses you can generate is " + str(len(clauses))

def GreedySearch(CNF):
    literalDict = {}
    for x in V:
        literalDict[x] = 0

    sumTrue = 0
    for i in range(len(V)):
        sumList = []
        count = 0

        #Count each literal and append in sumList
        for literal in V_copy:
            count = sum(x.count(literal) for x in CNF)
            sumList.append(count)

        index = sumList.index(max(sumList)) #Get the index of the max literal 
        literalMax = V_copy[index] #Get the value using the index

        if literalMax < 0:
            literalDict[abs(literalMax)] = False

        else:
            literalDict[literalMax] = True
            
        V_copy.remove(literalMax)
        V_copy.remove(-literalMax)

        #Change the current max occurance of the literal to "True" in every clause
        for j in range(len(CNF)):
            if literalMax in CNF[j]:
                CNF[j] = ["True"]
                sumTrue += 1

        if not V_copy or sumTrue == int(num):
            print(CNF, "\n")
            break

    numTrue = 0
    for clause in CNF:
        if "True" in clause:
            numTrue += 1

    print("Boolean: ", literalDict)
    print("Number of True: ", numTrue)
    print("Number of False: ", int(num) - numTrue, "\n")

    if numTrue == int(num):
        return 0, literalDict, numTrue

    else:
        return 10, literalDict, numTrue

def randomLiteral(literalList):
    #Choose the number of literals by 20% of the variable list
    numLiteral = math.ceil(0.2 * len(literalList))
    
    return random.sample(literalList, numLiteral)

def assignBoolean(chosenList, myDict):
    #Assign the new boolean for the chosen literal to be flipped
    for l in chosenList:
        if myDict[l] == True:
            myDict[l] = False
        else:
            myDict[l] = True
    
    return myDict

def checkSAT(CNF):
    for x in range(0, len(CNF)):
        for y in range(0, 3):
            if CNF[x][y] < 0:
                CNF[x][y] = not literalDict[abs(CNF[x][y])]

            else:
                CNF[x][y] = literalDict[CNF[x][y]]

    numTrue = 0
    for clause in CNF:
        if True in clause:
            numTrue += 1

    return numTrue


while True:
    V = []
    numV = int(input("Number of variables: "))

    for x in range(1, numV+1):
        V.append(x)
        
    V_copy = copy.copy(V)

    print ("V =", V)
    num = input("Number of clauses: ")

    print("")
    CNF = generateClause(int(num))

    CNF_copy = copy.deepcopy(CNF)

    print("CNF: ", CNF, "\n")

    #Start greedy search here
    count, literalDict, s1_numTrue = GreedySearch(CNF)

    literalDict_copy = copy.deepcopy(literalDict)
    s1 = copy.deepcopy(CNF_copy)
    test = False

    #Iterative Improvement
    #Start local search here
    while count > 0:
        chosenLiteral = randomLiteral(V)
        literalDict = assignBoolean(chosenLiteral, literalDict_copy)

        s2_numTrue = checkSAT(CNF_copy)
        
        if s2_numTrue > s1_numTrue:
            test = True
            literalDict_copy = literalDict
            success = copy.deepcopy(literalDict_copy)
            success2 = copy.deepcopy(CNF_copy)
            s1_numTrue = s2_numTrue
            count = 10

        CNF_copy = copy.deepcopy(s1)
        count -= 1

    if test:
        print(success2, "\n")
        print("New Boolean:", success)
        print("New Number of True:", success3)
        print("New Number of False:", int(num) - success3)

    print("")
