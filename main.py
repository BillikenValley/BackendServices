import sys
import getopt
import json

def main(argv):
    user_objects = None
    shelter_objects = None
    location = None
    try:
        opts, args = getopt.getopt(argv,"hu:s:l:",["users=","shelters=", "location="])
    except getopt.GetoptError:
        print 'mainScript.py -u <userObjects> -s <shelterObjects> -l <location>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mainScript.py -u <userObjects> -s <shelterObjects> -l <location>'
            sys.exit()
        elif opt in ("-u", "--users"):
            user_objects = arg
        elif opt in ("-s", "--shelters"):
            shelter_objects = arg
        elif opt in ("-l", "--location"):
            location = arg
    if user_objects and shelter_objects:
        for user in user_objects:
            for shelter in shelter_objects:
                user_dict = json.loads(user)
                shelter_dict = json.loads(shelter)
                rank = computeRating(user_dict,shelter_dict)
                returnObj = json.dumps({"user": user_dict, "shelter": shelter_dict, "rank": rank})
                print returnObj #unicode?

if __name__ == "__main__":
   main(sys.argv[1:])
