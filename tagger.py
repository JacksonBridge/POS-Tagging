# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# tagger.py
# -------------------------------------------------------
# Jackson Hambridge
# CMSC 416 Spring 2020
# 3/5/2020
#
# This program runs with two files, a training tagset and
# an empty set to be tagged. The program then trains on
# the training set and predicts the tags on the empty set
# using a greedy algorithm.
#
# python tagger.py [training] [untagged] > [tagged output]
# Example run:
# python tagger.py pos-train.txt pos-test.txt > pos-test-with-tags.txt
# 
# The output will be a predicted version of the empty tagset
#
# Tagged correctly: 47711
# Tagged incorrect: 9113
# Accuracy: 83.96%

import re
import sys

# Gather command line arguments, set to default if none
if len(sys.argv) == 1:
    trainingFile="pos-train.txt"
    testFile="pos-test.txt"
elif len(sys.argv) == 2:
    trainingFile=sys.argv[1]
    testFile="pos-test.txt"
else:
    trainingFile=sys.argv[1]
    testFile=sys.argv[2]

# Read training file
file=open(trainingFile,'r',encoding = 'utf-8')
inputData=file.read().lower()
file.close()

# Remove arbitrary characters
inputData=re.sub("\[","",inputData)
inputData=re.sub("\]","",inputData)

# Split into an array by space
inputData=str.split(inputData)

wordCount={}
wordList={}
tagCount={}
tagBigram={}
previousTag=""

# For every index in the training set
for words in inputData:

    # Split index into two by / to get [word,tag]
    pairing = str.split(words,"/")

    if len(pairing)>2:
        word = pairing[0] + pairing[1]
        tag = pairing[2]
    else:
        word = pairing[0]
        tag = pairing[1]

    if "|" in tag:
        tag = str.split(tag,"|")[0]

    # Add word to wordCount, which gathers word frequency
    if word not in wordCount:
        wordCount[word]=1
    else:
        wordCount[word]+=1
    
    # Add word to wordList, which gathers the frequency of a word-tag pairing
    if word not in wordList:
        wordList[word]={
            tag: 1
        }
    elif tag not in wordList[word]:
        wordList[word][tag]=1
    else:
        wordList[word][tag]+=1

    if previousTag == "":
        previousTag = "."

    # Add tag to tagCount (tag frequency)
    if tag not in tagCount:
        tagCount[tag]=1
    else:
        tagCount[tag]+=1

    # Add tag to tagBigram (frequency of a tag given another tag)
    if previousTag not in tagBigram:
        tagBigram[previousTag]={
            tag: 1
        }
    elif tag not in tagBigram[previousTag]:
        tagBigram[previousTag][tag]=1
    else:
        tagBigram[previousTag][tag]+=1

    previousTag=tag

# Read the untagged file
file=open(testFile,'r',encoding = 'utf-8')
inputData=file.read().lower()
file.close()

# Remove arbitrary characters
inputData=re.sub("\[","",inputData)
inputData=re.sub("\]","",inputData)

# Split the data into an array
inputData=str.split(inputData)

index=0
testWords=[""] * len(inputData)
testTags=[""] * len(inputData)

# For all words in the untagged set
for word in inputData:
    testWords[index]=word
    # If we have not seen the word, tag it as unknown "?"
    if word not in wordList:
        testTags[index]="?"
    # If there is only ever one tag assosiated with that word, tag it
    elif len(wordList[word]) == 1:
        key=re.sub("dict_keys\(\[\'","",re.sub("\'\]\)","",str(wordList[word].keys())))
        key=re.sub("dict_keys\(\[\"","",re.sub("\"\]\)","",str(key)))
        testTags[index]=key
    # Otherwise, tag as unknown "?"
    else:
        testTags[index]="?"
    
    index+=1

finalTag=[]
previousWord=""
unknown=[""]
count=0
index=0

# Loop through every word and tag it if it is unknown
while index<len(inputData):
    word=testWords[index]
    tag=testTags[index]

    # If there is  no previous tag, give it one (only for first iteration of loop)
    if previousTag == "":
        previousTag = "."

    # If the tag is unknown
    if tag == "?":
        product=0
        maximum=0
        finalTag=""
        # Calculate the most likely tag
        if word in wordList:
            for thisTag in wordList[word]:
            
                if thisTag in wordList[word] and thisTag in tagBigram[previousTag]:
                    # The calculation
                    product=wordList[word][thisTag]/wordCount[word] * tagBigram[previousTag][thisTag]/tagCount[previousTag]
                else:
                    product=-1
                if product > maximum:
                    maximum=product
                    tag=thisTag
            # If the sequence of tags did not occur in our corpus
            if product==-1:
                for allTags in wordList[word]:
                    if allTags in wordList[word]:
                        product=wordList[word][allTags]/wordCount[word]
                    if product > maximum:
                        maximum=product
                        tag=allTags
        # If the word did not occur in our corpus tag as "nn"
        else:
            # Tag as most likely pairing of tags
            # for allTags in tagCount:
            #    if allTags in tagBigram[previousTag]:
            #        product=tagBigram[previousTag][allTags]/tagCount[previousTag]
            #    if product > maximum:
            #        maximum=product
            #        tag=allTags
            tag="nn"


    testTags[index]=tag
    previousTag=tag
    index+=1

i=0

# Output all word/tags
while i < len(testTags):
    print(testWords[i] + "/" + testTags[i])
    i+=1


# This calculates the most likely tag pairing given a previous tag

#max=0
#for prevTag in tagBigram:
#    for curTag in tagBigram[prevTag]:
#        prod=0
#        prod=tagBigram[prevTag][curTag]/tagCount[prevTag]
#        if prod >= max and tagBigram[prevTag][curTag] != 1:
#            max = prod
#            winner = (prevTag, curTag)
#            bestProd = prod

# Most likely tag pairing is "$" "cd" with a 99.47% chance of predicting a "cd" given a "$"