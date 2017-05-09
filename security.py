votingRecords = {}
infoString = ''
keysArray=[]
dataStack={}
stateVotes={}
influence={}
numVotes=0

def main():
    filename=input('Specify dataset: ')
    readInData(filename)
    countVotes()
    #dataComputations()
    influenceGame()
    checkBestResponses()
    #checkVote()
    
    
def checkBestResponses():
    correctResponses=0
    wrongResponses=0
    countries=[]
    untruncatedList=[]
    for item in votingRecords.keys():
        untruncatedList.append(item)
    for i in range(1,len(untruncatedList)):
        countries.append(untruncatedList[i])
    for country in countries:
        for i in range(0,len(votingRecords[country])):
            value = 0
            for key in influence:
                if key[0]==country:
                    secondVote=votingRecords[key[1]][i]
                    influenceVote=0
                    if secondVote == "0":
                        influenceVote = -1
                    elif secondVote == "1":
                        influenceVote = 1
                    else:
                        influenceVote = -.25
                    value+=(influenceVote*influence[(country,key[1])])
            if value>=1 and votingRecords[country][i]=='1':
                correctResponses+=1
            elif value<=1 and votingRecords[country][i]=='0':
                correctResponses+=1
            elif value<=0 and votingRecords[country][i]=='0':
                correctResponses+=1
            elif value<=0 and votingRecords[country][i]=='2':
                correctResponses+=1
            elif value>0 and votingRecords[country][i]=='1':
                correctResponses+=1
            elif value>0 and votingRecords[country][i]=='2':
                correctResponses+=1 
            else:
                print("in "+votingRecords["Meeting Record"][i]+ " " + country + " voted against best response")
                wrongResponses+=1
                print(str(value)+ " should have produced the vote of...")
    print("Number correct: "+str(correctResponses)+ " Number wrong: "+str(wrongResponses))
                
            
        
def checkVote():
    currentCountry="Go"
    while(currentCountry!="Stop"):
        currentCountry=input("Whose vote is in question?")
        global influence
        value=0
        for key in influence:
            if key[0]==currentCountry:
                countryVote=input("What is "+key[1]+"'s vote?")
                vote=int(countryVote)
                value+=(vote*influence[(currentCountry,key[1])])
        if value>=1:
            print(currentCountry+ " has best response of YES")
        elif value<=-1:
            print(currentCountry+ " has best response of NO")      
        elif value>0:
            print(currentCountry+ " has best response of ABSTAIN or YES")
        elif value<=-0:
            print(currentCountry+ " has best response of ABSTAIN or NO")        
        print(value)
    
    
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
    
def influenceGame():
    global influence, dataStack, keysArray, votingRecords
    for i in range(1,len(keysArray)):
        currentCountry=keysArray[i]
        for j in range(1,len(keysArray)):
            if i!=j:
                secondCountry=keysArray[j]
                influence[(currentCountry,secondCountry)]=0
                for v in range(0,len(votingRecords[secondCountry])):
                    if votingRecords[currentCountry][v]=='1':
                        if votingRecords[secondCountry][v]=='0':
                            influence[(currentCountry,secondCountry)]-=.5
                        elif votingRecords[secondCountry][v]=='1':
                            influence[(currentCountry,secondCountry)]+=1
                        elif votingRecords[secondCountry][v]=='2':
                            influence[(currentCountry,secondCountry)]-=.5 
                    if votingRecords[currentCountry][v]=='0':
                        if votingRecords[secondCountry][v]=='0':
                            influence[(currentCountry,secondCountry)]+=3
                        elif votingRecords[secondCountry][v]=='1':
                            influence[(currentCountry,secondCountry)]-=1
                        elif votingRecords[secondCountry][v]=='2':
                            influence[(currentCountry,secondCountry)]+=1
                influence[(currentCountry,secondCountry)]=influence[(currentCountry,secondCountry)]/100
                print(currentCountry+"'s influence on "+secondCountry+" is "+str(influence[(currentCountry,secondCountry)]))
    #for key in influence.keys():
        #print(key[1]+" influences "+key[0]+" with "+str(influence[key]))
        
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
