# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# scorer.py
# -------------------------------------------------------
# Jackson Hambridge
# CMSC 416 Spring 2020
# 3/5/2020
#
# This file will compare a predicted tagged file with the
# key, the file with the correct tags. It will then create
# a confusion matrix based on the correct/incorrect guesses.
#
# python scorer.py [tagged output] [tagged key] > [confusion matrix]
# Example run:
# python scorer.py pos-test-with-tags.txt post-test-key.txt > pos-tagging-report.txt
# 
# The output will be a confusion matrix of the correct and incorrect tags
# where the HORIZONTAL axis is the ACTUAL tag and the VERTICLE axis is the PREDICTION
#
# Tagged correctly: 47711
# Tagged incorrect: 9113
# Accuracy: 83.96%

import re
import sys


# This method calculates the number of spaces needed to make "word" spaceNumber long
# It is used for formatting purposes
def calculateSpaces(word,spaceNumber):
    index=0
    spaces=""
    while index < spaceNumber - len(word):
        spaces+=" "
        index+=1
    return spaces

# Gather command line arguments, set to default if none
if len(sys.argv) == 1:
    taggedFile="pos-test-with-tags.txt"
    keyFile="pos-test-key.txt"
elif len(sys.argv) == 2:
    taggedFile=sys.argv[1]
    keyFile="pos-test-key.txt"
else:
    taggedFile=sys.argv[1]
    keyFile=sys.argv[2]

# Read the key and gather it into realData
file=open(keyFile,'r',encoding = 'utf-8')
realData=file.read().lower()
file.close()
realData=re.sub("\[","",realData)
realData=re.sub("\]","",realData)
realData=str.split(realData)

# Read the predicted file and gather it into guessData
file=open(taggedFile,'r',encoding = 'bom')
guessData=file.read().lower()
file.close()
guessData=re.sub("\[","",guessData)
guessData=re.sub("\]","",guessData)
guessData=str.split(guessData)

correct=0
incorrect=0

confusionMatrix={}

index=0

# Loop through the entire file
while index<len(realData):

    # Gather the realTag from realData at the current index
    pairing = str.split(realData[index],"/")

    if len(pairing)>2:
        realWord = pairing[0] + pairing[1]
        realTag = pairing[2]
    else:
        realWord = pairing[0]
        realTag = pairing[1]
    
    # Gather the guessTag from guessData at the current index
    pairing = str.split(guessData[index],"/")

    if len(pairing)>2:
        guessTag = pairing[0] + pairing[1]
        guessTag = pairing[2]
    else:
        guessWord = pairing[0]
        guessTag = pairing[1]
    


    if '|' in realTag:
        realTag = str.split(realTag,'|')[0]


    # If the realTag and guessTag are the same, increment correct
    if realTag == guessTag:
        correct+=1
    # Otherwise the guess was wrong, and increment incorrect
    else:
        incorrect+=1

    # Add the tag to the confusionMatrix dictionary
    if realTag not in confusionMatrix:
        confusionMatrix[realTag]={
            guessTag: 1
        }

    elif guessTag not in confusionMatrix[realTag]:
        confusionMatrix[realTag][guessTag]=1
    else:
        confusionMatrix[realTag][guessTag]+=1

    index+=1

# Display accuracy
print("Correct: " + str(correct))
print("Incorrect: " + str(incorrect))
results=correct/(correct+incorrect)*100
print("Accuracy: " + str(results))

# Set empty spaces in the confusion matrix to 0
for key1 in confusionMatrix:
    for key2 in confusionMatrix:
        if key2 not in confusionMatrix[key1]:
            confusionMatrix[key1][key2]=0


row="      "

# Gather the x-axis header of the confusion matrix
for key1 in confusionMatrix:
    row+=key1+calculateSpaces(str(key1),6)
print(row)

# Gather the rest of the confusion matrix
for key2 in confusionMatrix:
    row=key2 + calculateSpaces(key2,6)
    for key1 in confusionMatrix:
        addition=str(confusionMatrix[key1][key2]) + calculateSpaces(str(confusionMatrix[key1][key2]),6)
        row+=addition
    print(row)

# Thank you :)