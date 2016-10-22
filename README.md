# BackendServices
Backend Services for home.me

ALGORITHM SPECIFICATIONS:
	Input:
		Questionaire Answers (JSON)
		Time
		Location
		Current State of Database (JSON)
	Output:
		Prioiritized list of available shelters based-on, 
		rank determined by some metric we decide (Array of JSONs)
	
THE ALGORITHM:
0. Convert JSON objects to dictionaries
1. Filter locations from database using questionaire answers
2. Use time, location and questionaire answers to prioritize which locations are better, 
creating a sorted list of CoC locations
3. Return sorted list OR inform user of no matches
