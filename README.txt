WELCOME TO OUR UN SECURITY COUNCIL PROJECT!
-Will and Jasper


Files included in this folder:

HowToVote.py
	-Applet that allows user to predict voting for individual countries
security.py
	-the main computational file for statistics
finaldata.txt
	-the data that we used (use this as input)

README.txt (this file)
UN Security Council.pdf (the final paper)

To run the applet in the terminal:
1. Navigate to the UN_Security_Influence_Net directory
2. python HowToVote.py
3. follow the given instructions

OUTPUT:
Best Response: <- the best response for your chosen country after the vote
Influence: <- the overall influence value for your chosen country after the vote

To run the computational file in the terminal:
1. Navigate to the UN_Security_Influence_Net directory
2. python security.py
3. input filename (finaldata.txt)
4. use the applet if so desired

OUTPUT:
the computational file produces many outputs including:
-Vote counts for all countries (# yes, # no, # abstain)
-Influence network values
-Number right and wrong regarding best responses in historical examples
-Instances where countries did not play their best response (with meeting dates)
-optional similarity frequency calculator (commented out currently)


