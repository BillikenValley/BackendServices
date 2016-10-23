import sys
import getopt
import json
import random
import datetime #get the elapsed minutes since midnight

import match

def main(argv):

    #to do: coordinate and test i/o with David's API
    #why won't JSON objects load properly?

    #initialize everything to null
    user_objects = None
    shelter_objects = None
    returnShelters = {}
    bestShelters = {}

    #compute the elapsed minutes since midnight
    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    minutesSinceMidnight = (now - midnight).seconds/60

    try:
        opts, args = getopt.getopt(argv,"hu:s:l:",["users=","shelters=", "location="])
    except getopt.GetoptError:
        print 'mainScript.py -u <requester> -s <shelter> -l <location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mainScript.py -u <requester> -s <shelter> -l <location>'
            sys.exit()
        elif opt in ("-u", "--users"):
            user_objects = arg
        elif opt in ("-s", "--shelters"):
            shelter_objects = arg
        elif opt in ("-l", "--location"):
            location_obj = arg

    #TEST CODE
    f = open('testuser2.txt', 'r') #use this if you want to read a user from a file instead
    user_objects = f.read()
    f.close()
    g = open('testshelter2.txt','r')
    shelter_objects = g.read()
    g.close()
    #END TEST CODE


    if user_objects and shelter_objects:
        shelter_dictionaries = json.loads(shelter_objects)
        users_dict = json.loads(user_objects)
        for shelter in shelter_dictionaries: #for each shelter in the list
            location = json.loads(location_obj)
            rank = match.computeRank(users_dict,shelter, minutesSinceMidnight, location)

            if rank >= 0:
                returnShelters[shelter["uuid"]] = rank

        bestShelters = sorted(returnShelters, key=returnShelters.__getitem__)

        if len(bestShelters) > 15:
            bestShelters = bestShelters[:,15] #truncate the error
        print bestShelters

if __name__ == "__main__":
   main(sys.argv[1:])
