votingRecords = {}
infoString = ''
keysArray=[]
dataStack={}
stateVotes={}
numVotes=0

def main():
    filename=input('Specify dataset: ')
    readInData(filename)
    countVotes()
    dataComputations()
    
    
def dataComputations():
    global dataStack, keysArray, votingRecords
    for i in range(1,len(keysArray)):
        currentCountry=keysArray[i]
        for vote in ['0','1','2']:
            for j in range(1,len(keysArray)):
                if i!=j:
                    secondCountry=keysArray[j]
                    dataStack[(currentCountry,secondCountry,vote)]=0
                    for v in range(0,len(votingRecords[secondCountry])):
                        if votingRecords[currentCountry][v]==vote:
                            if votingRecords[secondCountry][v]==vote:
                                dataStack[(currentCountry,secondCountry,vote)]+=1
    for key in dataStack.keys():
        vote=''
        if key[2]=='0':
            vote=' votes no'
        elif key[2]=='1':
            vote=' votes yes'
        else:
            vote=' abstains'
        percentage=int(100*(int(dataStack[key])/stateVotes[key[0]][int(key[2])]))
        print(key[0]+vote+". "+key[1]+" also"+vote+ " at %" +str(percentage)+" frequency.")
    
def countVotes():
    global keysArray, votingRecords, stateVotes
    for i in range(1,len(keysArray)):
        yesCount=0
        noCount=0
        abstainCount=0
        stateVotes[keysArray[i]]=[]
        for vote in votingRecords[keysArray[i]]:
            if vote=='1':
                yesCount+=1
            if vote=='2':
                abstainCount+=1
            if vote=='0':
                noCount+=1
        stateVotes[keysArray[i]].append(noCount)
        stateVotes[keysArray[i]].append(yesCount)
        stateVotes[keysArray[i]].append(abstainCount)
        print(keysArray[i]+"---- Yes: "+str(yesCount)+ " No: "+str(noCount)+" Abstain: "+str(abstainCount))
        
def readInData(filename):

    #opens the file
    myFile = open(filename, "r")
    
    #reads and parses the rowActions and colActions integers
    trashString = myFile.readline()
    newstring = myFile.readline()
    global infoString 
    infoString = newstring
    global keysArray
    keysArray=infoString.strip().split(',')
    print("Using Data For: "+keysArray[1]+", "+keysArray[2]+", "+keysArray[3]+", "+keysArray[4]+", "+keysArray[5])
    global votingRecords
    for key in keysArray:
        votingRecords[key]=[]
    
    #reads and parses the payoff matrix
    my_text = myFile.readlines()
    for line in my_text:
        lineArray=line.strip().split(',')
        for i in range(0,len(lineArray)):
            votingRecords[keysArray[i]].append(lineArray[i])
    global numVotes
    numVotes=len(votingRecords[keysArray[0]])
main()
