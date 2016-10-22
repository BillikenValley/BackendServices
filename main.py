import sys
import getopt
import json

def main(argv):
    user_objects = None
    shelter_objects = None
    returnObj = {} #initialize everything to null
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
    if user_objects and shelter_objects:
        for shelter in shelter_objects: #for each shelter in the list
            users_dict = json.loads(user_objects)
            shelter_dict = json.loads(shelter)
            rank = computeRank(users_dict,shelter_dict)
            if rank >= 0:
                returnObj['shelter by id'] = rank #amend this line later when data model is finalized
        print sorted(returnObj, key=returnObj.__getitem__, reverse=True) #unicode?

if __name__ == "__main__":
   main(sys.argv[1:])
