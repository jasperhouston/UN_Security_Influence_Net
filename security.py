#global variable definitions
votingRecords = {}
infoString = ''
keysArray=[]
dataStack={}
stateVotes={}
influence={}
numVotes=0

#main function is called to read in a file, compute influences, and run a basic applet in the console
def main():
    #import the file into the program
    filename=input('Specify dataset: ')
    readInData(filename)
    #calculate some basic statistics about voting patterns
    countVotes()
    #data computations produces some extra stats for those that want to know more (currently commented out)
    #dataComputations()
    
    #builds the influence network
    influenceGame()
    
    #checks best response accuracy for historical examples
    checkBestResponses()
    #runs the applet
    checkVote()
    
#checkBestResponses takes in no parameters, goes through all historical examples and 
#calculates how frequently countries played their BRs    
def checkBestResponses():
    correctResponses=0
    wrongResponses=0
    countries=[]
    untruncatedList=[]
    #iterates through items to get rid of "Meeting Record" as a key
    for item in votingRecords.keys():
        untruncatedList.append(item)
    for i in range(1,len(untruncatedList)):
        countries.append(untruncatedList[i])
        
    #iterates through the list of countries
    for country in countries:
        for i in range(0,len(votingRecords[country])):
            value = 0
            #calculates influenced value
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
                    value+=(influenceVote*influence[(key[1],country)])
                    
            #checks the response against the best responses
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
                #prints incorrect responses and their meeting date
                print("in "+votingRecords["Meeting Record"][i]+ " " + country + " voted against best response")
                wrongResponses+=1
                print(str(value)+ " should have produced a different response")
    #prints the accuracy statement
    print("Number correct: "+str(correctResponses)+ " Number wrong: "+str(wrongResponses))
                
#the basic applet, when run, allows the user to specify countries and predict their votes     
def checkVote():
    currentCountry="Go"
    #loop continues until the user breaks it
    while(currentCountry!="Stop"):
        
        #asks for the vote of the country in question
        currentCountry=input("Whose vote is in question? ")
        global influence
        value=0
        for key in influence:
            if key[0]==currentCountry:
                
                #asks for the votes of the other countries
                countryVote=input("What is "+key[1]+"'s vote? ")
                vote=int(countryVote)
                influenceVote=0
                if countryVote == "0":
                    influenceVote = -1
                elif countryVote == "1":
                    influenceVote = 1
                else:
                    influenceVote = -.25
                value+=(influenceVote*influence[(key[1],currentCountry)])
                
        #compares influence total to threshold values
        if value>=1:
            print(currentCountry+ " has best response of YES")
        elif value<=-1:
            print(currentCountry+ " has best response of NO")      
        elif value>0:
            print(currentCountry+ " has best response of ABSTAIN or YES")
        elif value<=-0:
            print(currentCountry+ " has best response of ABSTAIN or NO")        
        print(value)
    
#shows voting tendencies for extra inquisitive folk! (experimental stages)    
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
        
        #shows voting similarities
        print(key[0]+vote+". "+key[1]+" also"+vote+ " at %" +str(percentage)+" frequency.")

#builds the influence network    
def influenceGame():
    #takes in global variables
    global influence, dataStack, keysArray, votingRecords
    for i in range(1,len(keysArray)):
        #looping through the first countries
        currentCountry=keysArray[i]
        for j in range(1,len(keysArray)):
            #inner for loop loops through the second countries
            if i!=j:
                secondCountry=keysArray[j]
                #starts influence off at zero
                influence[(currentCountry,secondCountry)]=0
                for v in range(0,len(votingRecords[secondCountry])):
                    #for each vote, depending on how the second country voted, the influence is altered slightly
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
                #turns influence into a smaller factor
                influence[(currentCountry,secondCountry)]=influence[(currentCountry,secondCountry)]/100
                #prints influences
                print(currentCountry+"'s influence on "+secondCountry+" is "+str(influence[(currentCountry,secondCountry)]))

#counts up the votes of each country in each way (yes, no, abstain)        
def countVotes():
    global keysArray, votingRecords, stateVotes
    #goes through countries
    for i in range(1,len(keysArray)):
        #initializes vote counts at zero
        yesCount=0
        noCount=0
        abstainCount=0
        stateVotes[keysArray[i]]=[]
        #adds to the vote counters
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
        #prints the vote count statistic
        print(keysArray[i]+"---- Yes: "+str(yesCount)+ " No: "+str(noCount)+" Abstain: "+str(abstainCount))

#reads in a file, transfers the data into the necessary data structures        
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
    
#run the main program    
main()
