votingRecords = {}
infoString = ''
keysArray=[]
dataStack={}
stateVotes={}
influence={}
numVotes=0

def main():
    filename="finaldata.txt"
    readInData(filename)
    countVotes()
    influenceGame()
    howToVote()
    
    
def howToVote():
    yesNo = 'n'
    while yesNo == 'n':
        country = input('What country do you represent? ')
        if country == 'uk' or country == 'UK':
            country = 'United Kingdom'
        elif country == 'us' or country == 'usa' or country == 'US' or country == 'USA':
            country = 'United States'
        else:
            country = country.title()        
        yesNo = input('You have selected ' + country + ', is this correct? (y/n) ')
    print(country)
    global influence
    value = 0
    for key in influence:
        if key[0] == country:
            countryVote = input("What is " + key[1] + "'s vote? (yes/no/abstain) ")
            if countryVote == 'yes':
                vote = 1
            elif countryVote == 'no':
                vote = -1
            elif countryVote == 'abstain':
                vote = 0
            value += (vote * influence[(country, key[1])])
    if value >= 1:
        print("Your best response is YES")
    elif value <= -1:
        print("Your best response is NO")      
    elif value > 0:
        print("Your best response is ABSTAIN or YES")
    elif value <= 0:
        print("Your best response is ABSTAIN or NO")        
    print(value)
    
    
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
