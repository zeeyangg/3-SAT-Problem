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
            
        return [[14, -15, -14], [-18, -1, -3], [-6, 9, -15], [7, 4, -2], [-6, 8, 3], [-19, -15, -12], [13, 7, -7], [17, 4, 6], [-12, -18, 18], [8, 3, 12], [-15, 20, -16], [-8, -11, -16], [-14, 7, 1], [-16, 7, 8], [15, -8, -19], [-18, 2, -6], [3, -16, -4], [6, -12, 5], [-18, -9, -14], [-4, 17, -7], [-13, -2, -1], [-7, 6, -4], [-10, 15, 11], [18, 13, 16], [-11, -18, -16], [13, 2, -16], [6, -2, 11], [14, -1, -2], [-8, -13, -14], [-15, -16, 13], [-18, -4, -6], [13, 20, 7], [5, 19, 4], [7, 8, -7], [11, -13, -10], [2, -17, -3], [1, -9, -5], [-9, 9, 20], [19, -11, 13], [13, -7, -6], [4, -16, -3], [1, -9, 13], [-10, -19, 2], [-5, -1, 11], [17, -9, 12], [-11, 16, 19], [-5, -13, 19], [12, 2, -2], [4, -20, 15], [-14, 5, -11], [-6, 17, 4], [-18, 13, 12], [-15, 15, 19], [-12, -6, -20], [-13, -9, 5], [12, 20, -12], [-6, 18, -10], [-11, -4, -20], [-8, -13, 13], [-12, 6, 12], [-5, 19, 3], [-5, -2, -10], [-14, 12, -13], [3, 15, -12], [2, -8, 8], [-9, 15, 18], [-16, -18, -6], [19, 16, -2], [14, -13, 1], [-11, -5, -20], [9, -5, 20], [-7, 14, 2], [-7, 2, -9], [2, 4, 9], [1, -20, -15], [-2, 2, -4], [10, 2, 17], [9, -11, -1], [-6, -18, 4], [1, -5, -15]]

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
