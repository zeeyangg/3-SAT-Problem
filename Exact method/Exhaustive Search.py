import random
import itertools
import copy
import time

###################################################

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

def booleanLiteral(p):
    literalDict = {}
    position = 0

    #Choose the next possible combination
    for x in V:
        literalDict[x] = p[position]
        position += 1

    return literalDict

def checkSAT(CNF):
    count = 0
    CNF_copy = copy.deepcopy(CNF)
    for x in range(0, len(CNF)):
        for y in range(0, 3):
            if CNF[x][y] < 0:
                CNF[x][y] = not literalDict[abs(CNF[x][y])]

            else:
                CNF[x][y] = literalDict[CNF[x][y]]
    
    for clause in CNF:
        if True in clause:
            count += 1
    
    if count == len(CNF):
        return True, CNF

    else:
        return False, CNF_copy


##################################################

V = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

boolean = [True, False]

while True:
    V_copy = copy.copy(V)
    
    print("V =", V)
    num = input("Number of clauses: ")

    print("")
    
    CNF = generateClause(int(num))
    print("CNF:", CNF)
    
    if type(CNF) == str:
        print("")
        continue

    start_time = time.time()
    #Exhaustive Search
    for p in itertools.product(boolean, repeat=len(V)):
        literalDict = booleanLiteral(p)
        satisfied, CNF = checkSAT(CNF)

        if satisfied:
            print(CNF, "\n")
            break

    end_time = time.time()
    print("")
    print("Boolean:", literalDict, "\n")
    print("Satisfiability:", satisfied, "\n")
    print("Time:", end_time-start_time, "\n")
