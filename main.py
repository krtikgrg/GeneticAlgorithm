import sys
import numpy as np
import client as cl
import copy
import random
import json
tempProb = [1,1,1,1,1,1,1,1,1 ,1 ,1 ,1 ,1 ,1, 1]
with open("overfit.txt","r") as read_file:
    overfit = json.load(read_file)

trainErrorWeight =3
validationErrorWeight = 4
NUMBER_OF_GENERATIONS = 50

with open('generation.txt','r') as read_file:
    generation = json.load(read_file)
with open('trainError.txt','r') as read_file:
    trainError = json.load(read_file)
trainError = np.array(trainError)
with open('validationError.txt','r') as read_file:
    validationError = json.load(read_file)
validationError = np.array(validationError)
with open('output.txt','r') as read_file:
    coefficientValue = json.load(read_file)
coefficientValue = np.array(coefficientValue)
Error = np.add(trainErrorWeight*trainError,validationErrorWeight*validationError)
for i in range(NUMBER_OF_GENERATIONS):
    #checking redundancy so avoid premature contancy
    tempProb = [1,1,1,1,1,1,1,1,1 ,1 ,1 ,1 ,1 ,1, 1]
    a = trainError[0]
    for s in range(1,15):
        if abs(trainError[s] - a) <= 1000000:
            tempProb[s] = 0
        else:
            a = trainError[s]

    
    to_be_appended = []
    to_be_appended.append(coefficientValue.tolist())
    vis = np.zeros((15,15))
    tempgen = []
    temperror = []
    tempTrain = []
    tempValidation = []
    selection = []
    childrenmade = []

    for j in range(15): #creating 15 mutated children
        ayuKar = []
        indX = random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],weights = tempProb)
        indY = random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],weights = tempProb)
        indX = indX[0]
        indY = indY[0]


        #avoiding same indices to be picked
        while indX == indY:
            indY = random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],weights = tempProb)
            indY = indY[0]
        ctr=0


        #checking if same parents were previously picked
        while vis[indX][indY] == 1:
            ctr+=1
            if ctr == 40:
                for ayushX in range(15):
                    for ayushY in range(15):
                        if vis[ayushX][ayushY] == 0:
                            indX = ayushX
                            indY = ayushY
            else:
                indX = random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],weights = tempProb)
                indY = random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],weights = tempProb)
                indX = indX[0]
                indY = indY[0]
                while indX == indY:
                    indY = random.choices([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],weights = tempProb)
                    indY = indY[0]
        vis[indX][indY]=1
        child = []

        #crossover
        cross = random.randint(0,2)
        firstNum = random.randint(3,8)
        for k in range(11):     
            if cross == 0:  # 3,5 => 0.4 => 0.4*3 + 0.6*5
                constant = random.uniform(0,1)
                newVal = (constant*coefficientValue[indX][k]) + ((1-constant)*coefficientValue[indY][k])
                child.append(newVal)
            elif cross = 1:
                options = random.randint(0,1)
                if options == 0:
                    child.append(coefficientValue[indX][k])
                elif options ==1:
                    child.append(coefficientValue[indY][k])
            else:
                if k < firstNum:
                    child.append(coefficientValue[indX][k])
                else:
                    child.append(coefficientValue[indY][k])
        ayuKar.append(coefficientValue[indX].tolist())
        ayuKar.append(coefficientValue[indY].tolist())
        childrenmade.append(child)

        #mutation
        options = random.choices([0,1,2,3,4],weights = [1,2,1,4,3])  # 3 => No Mutation
        options = options[0]
        if options == 0:                                            #SWAP
            prob = random.randint(0,9)
            if prob>=2:
                index = random.randint(0,10)
                index2 = random.randint(0,10)
                while index2 == index:
                    index2 = random.randint(0,10)
                tempval = child[index]
                child[index] = child[index2]*random.choices([-1,1])[0]
                child[index2] = tempval*random.choices([-1,1])[0]
            else:
                for tri in range(5):
                    tempval = child[tri+6]
                    child[tri+6] = child[tri]
                    child[tri] = tempval

        elif options == 2:                                          #INVERSION MUTATION
            index = random.randint(0,10)
            index2 = random.randint(0,10)
            while index2 == index:
                index2 = random.randint(0,10)
            if index2 < index:
                index = index + index2    
                index2 = index - index2
                index = index - index2
            for k in range(index,int((index2+index)/2)+1):
                tempind = k-index
                tempind = index2 - tempind
                tempval = child[k]
                child[k] = child[tempind]
                child[tempind] = tempval 

        elif options == 1:#MULTIPLICATION MUTATION
            index = random.randint(0,10)
            factor = random.uniform(0.85,1.15)
            value = child[index]
            value = value * factor
            if value > 10:
                value = 10
            elif value < -10:
                value = -10
            child[index] = value
            # for index in range(11):
            #     factor = random.uniform(0.05,2.5)
            #     value = child[index]
            #     value = value * factor
            #     if value > 10:
            #         value = 10
            #     elif value < -10:
            #         value = -10
            #     child[index] = value

        elif options == 4:                                          #ADDITION FACTOR
            for index in range(11):
                inde = random.randint(0,14)
                factor = random.uniform(0.01,0.05) * coefficientValue[inde][index] * random.choices([-1,1])[0]
                value = child[index]
                value = value + factor
                if value > 10:
                    value = 10
                elif value < -10:
                    value = -10
                child[index] = value


            # index = random.randint(0,10)
            # factor = random.uniform(0.005,0.20) * overfit[index] * random.choices([-1,1])[0]
            # value = child[index]
            # value = value + factor
            # if value > 10:
            #     value = 10
            # elif value < -10:
            #     value = -10
            # child[index] = value

        wohoo = cl.get_errors("KEcVoPGXqH6Gwxuzx7cici4Z5HT7VilhXsPTT65mWO4eE7KJKN",list(child))
        tempgen.append(child)
        selection.append(ayuKar)
        tempTrain.append(wohoo[0])
        tempValidation.append(wohoo[1])

        #fitness evaluation (linear combination) ===========|| 
        #                                                   \/
        temperror.append(trainErrorWeight*int(wohoo[0])+validationErrorWeight*int(wohoo[1]))
    
    #Finding Best among the pool of parents and children made
    temperror = np.concatenate((Error,temperror))
    #sorting on the basis of fitness
    indices = np.argsort(temperror)
    newgen = []
    newError = []
    newTrain = []
    newValidation = []
    #top 15 picked
    for j in range(15):
        if indices[j]<15:
            newgen.append(list(coefficientValue[indices[j]]))
            newTrain.append(trainError[indices[j]])
            newValidation.append(validationError[indices[j]])
        else:
            newgen.append(tempgen[indices[j]-15])
            newTrain.append(tempTrain[indices[j]-15])
            newValidation.append(tempValidation[indices[j]-15])
        newError.append(temperror[indices[j]])
    to_be_appended.append(selection)
    to_be_appended.append(childrenmade)
    to_be_appended.append(tempgen)
    coefficientValue = np.array(newgen)
    to_be_appended.append(coefficientValue.tolist())
    generation.append(to_be_appended)
    Error = np.array(newError)
    trainError = np.array(newTrain)
    validationError = np.array(newValidation)
print("***************")
print("")
print(trainError)
print("")
print("")
print(validationError)
print("")
print("")
print("***************")
with open( 'output.txt','w') as write_file:
    json.dump(coefficientValue.tolist(),write_file)
with open('generation.txt','w') as write_file:
    json.dump(generation,write_file)
with open('trainError.txt','w') as write_file:
    json.dump(trainError.tolist(),write_file)
with open('validationError.txt','w') as write_file:
    json.dump(validationError.tolist(),write_file)