import sys
import getopt
import json
import random
import datetime #get the elapsed minutes since midnight

import match

def getUserLoc(users_dict):
    lat = users_dict["UserStatus"]["Location"]["Lat"]
    longitude = users_dict["UserStatus"]["Location"]["Lng"]
    return [latitude, longitude]


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
        opts, args = getopt.getopt(argv,"hu:s:l:",["users=","shelters="])
    except getopt.GetoptError:
        print 'mainScript.py -u <userObjects> -s <shelterObjects>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mainScript.py -u <userObjects> -s <shelterObjects>'
            sys.exit()
        elif opt in ("-u", "--users"):
            user_objects = arg
        elif opt in ("-s", "--shelters"):
            shelter_objects = arg

    #f = open('testuser2.txt', 'r')
    #user_objects = f.read()
    #print user_objects
    #print getUserLoc(json.loads(user_objects))

    if user_objects and shelter_objects:
        shelter_dictionaries = json.loads(shelter_objects)
        users_dict = json.loads(user_objects)
        for shelter in shelter_dictionaries: #for each shelter in the list

            location = getUserLoc(users_dict)
            rank = match.computeRank(users_dict,shelter, minutesSinceMidnight, location)


            if rank >= 0:
                if rank not in returnShelters.keys():
                    returnShelters[rank] = shelter
                else:
                    while rank in returnShelters.keys(): #break ties if the rank is already a hash key
                        rank+= random.randint(-1,1)
                    returnShelters[rank] = shelter

        bestShelters = [value for (key, value) in sorted(returnShelters.items(), reverse=True)]

        matches  = {"Party": users_dict, "Shelters": bestShelters}
        print json.dumps(matches) #unicode?

if __name__ == "__main__":
   main(sys.argv[1:])
