import numpy as np
import client as cl
import copy
import random
import json

vec = np.loadtxt("./overfit.txt",dtype=str,delimiter="[")
vec = vec[1].split("]")
vec = vec[0].split(", ")
coefficients = np.array(vec).astype(np.float)
trainError = []
validationError = []
coefficientValue = []
generation = []
wohoo = cl.get_errors("KEcVoPGXqH6Gwxuzx7cici4Z5HT7VilhXsPTT65mWO4eE7KJKN",list(coefficients))
trainError.append(wohoo[0])
validationError.append(wohoo[1])
coefficientValue.append(coefficients)

for i in range(14):
    tempCoeffi = copy.deepcopy(coefficientValue[i])
    index = random.randint(0,10)
    index2 = random.randint(0,10)
    while index2 == index:
        index2 = random.randint(0,10)
    tempval = tempCoeffi[index]
    tempCoeffi[index] = tempCoeffi[index2]
    tempCoeffi[index2] = tempval
    index = random.randint(0,10)
    factor = random.uniform(0.8,1.2)
    value = tempCoeffi[index]
    value = value * random.choices([-1,1])[0] * factor
    if value > 10:
        value = 10
    elif value < -10:
        value = -10
    tempCoeffi[index] = value
    # if index2 < index:
    #     index = index + index2    # index < index2    index ---- index2    index -> (index+index2/2)+1
    #     index2 = index - index2
    #     index = index - index2
    # for k in range(index,int((index2+index)/2)+1):
    #     tempind = k-index
    #     tempind = index2 - tempind
    #     tempval = tempCoeffi[k]
    #     tempCoeffi[k] = tempCoeffi[tempind]
    #     tempCoeffi[tempind] = tempval
    coefficientValue.append(np.array(tempCoeffi))
    wohoo = cl.get_errors("KEcVoPGXqH6Gwxuzx7cici4Z5HT7VilhXsPTT65mWO4eE7KJKN",list(tempCoeffi))
    trainError.append(wohoo[0])
    validationError.append(wohoo[1])
coefficientValue = np.array(coefficientValue)
trainError = np.array(trainError)
validationError = np.array(validationError)
print("***************")
print("")
print(coefficientValue)
print("")
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
