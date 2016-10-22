import math
import time
import calendar

def computeRank(users_dict,shelter_dict):

####
    requirements = shelter_dict["Requirements"]
    #return 0 if we don't meet requirements



#######


    shelter_loc = shelter_dict["Location"]
    #distance = computeDistance(avgLoc(users_dict), shelter_loc)
    distance = computeDistance(users_dict[0]["Location"], shelter_loc)

    #apply a weight to this

######
    hour = time.gmtime().tm_hour
    minute = time.gmtime().tm_min
    dayOfWeek = time.gmtime().tm_wday #day of the week as an integer

    shelterSched = shelter_dict["ShelterSchedule"]
    #todaySched = shelterSched[calendar.day_name[dayOfWeek]]
    todaySched = shelterSched[dayOfWeek]

    openTime = todaySched["From"]
    closeTime = todaySched["To"]

    #compute the time until close, and return 0 if it is already closed

####
    status = shelter_dict["CurrentStatus"]
    bedStatus = status["Beds"]
    bedsLeft = 0
    for bed in bedStatus:
        if bed == 0:
            bedsLeft+=1

#####


def computeDistance(loc1, loc2): #compute longitude-latitude distance between two points
    userLat = math.radians(loc1[0])
    userLong = math.radians(loc1[1])

    shelterLat = math.radians(loc2[0])
    shelterLong = math.radians(loc2[1])

    dLon = shelterLong - userLong
    dLat = shelterLat - userLat

    R = 6373.0 #approx radius of earth
    a = sin(dLat / 2)**2 + cos(userLat) * cos(shelterLat) * sin(dLon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R*c

def avgLoc(users): #average the locations of the users
    avDist = [0,0]
    for user in users_dict:
        avDist += user["Location"]
    return avDist/len(users_dict)
