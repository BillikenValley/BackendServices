import datetime
import math

def relevant(booltype):
    # Determines if
    return not (booltype == 0)

def can_take_individual(person, shelter):
    # Check if a shelter could EVER concievably take this individual under any circumstances
    # (There may be additional party requirements for the whole party)
    requirements = shelter.get("constraints", None)

    """if len(requirements) == 0: #if there are no requirements
        return True

    if requirements == None:
        return True"""

    accepts_men = requirements.get("accepts_men", 1)
    accepts_single_men = requirements.get("accepts_single_men",1)
    max_male_age = requirements.get("max_male_age",1000)
    min_male_age = requirements.get("min_male_age",-1000)
    accepts_women = requirements.get("accepts_women",1)
    accepts_single_women = requirements.get("accepts_single_women",1)
    max_female_age = requirements.get("max_female_age",1000)
    min_female_age = requirements.get("min_female_age",-1000)
    trans_friendly = requirements.get("trans_friendly",1)
    must_be_pregnant = requirements.get("must_be_pregnant",0)
    max_pregnancy_weeks = requirements.get("max_pregnancy_weeks",1000)
    min_pregnancy_weeks = requirements.get("min_pregnancy_weeks",-1000)
    accepts_children = requirements.get("accepts_children",1)
    max_children = requirements.get("max_children",100)


    # Check gender and age requirements
    max_age = max(max_male_age, max_female_age)
    min_age = min(min_male_age, min_female_age)


    if person.get("sex", 1) == 1 and person.get("gender", 1) == 1:
        # Male and not trans
        if (not accepts_men) or max_male_age < person.get("age",10) or min_male_age > person.get("age", 10):
            # Person is not in the right age range for their gender; return false
            return False
        if must_be_pregnant:
            return False
    elif person.get("sex", 2) == 2 and person.get("gender", 2) == 2:
        # Female and not trans
        if (not accepts_women) or max_female_age < person.get("age",10) or min_female_age > person.get("age",10):
            # Person is not in the right age range for their gender; return false
            return False
    else:
        # Person is transgender/intersex; see if shelter deals with such people
        if not trans_friendly:
            return False
        else:
            # Use person's gender identity instead of birth sex
            if person.get("gender", 1) == 1:
                return (person.get("age", 30) >= min_male_age) and (person.get("age", 30) <= max_male_age)
            elif person.get("gender", 2) == 2:
                return (person.get("age", 20) >= min_female_age) and (person.get("age", 20) <= max_female_age)
            else:
                # gender == "other"
                return (person.get("age", 20) <= max_age) or (person.get("age", 20) >= min_age)

    if must_be_pregnant:
        if not person.get("is_pregnant", 0):
            return False
        elif person.get("weeks_pregnant", 10) > max_pregnancy_weeks or person.get("weeks_pregnant",10) < min_pregnancy_weeks:
            return False

    # True by process of elimination
    return True

def computeRank(party, shelter, current_time, location):
    # Return -1 if ineligible, else return distance to shelter

    # Check if shelter is open
    openTime = shelter["open_time"].split('.')[0]
    openTime = datetime.datetime.strptime(openTime, "%Y-%m-%dT%H:%M:%S")
    closeTime = shelter["close_time"].split('.')[0]
    closeTime = datetime.datetime.strptime(closeTime, "%Y-%m-%dT%H:%M:%S")

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    openTime = (openTime - midnight).seconds/60
    closeTime = (closeTime -midnight).seconds/60

    if openTime > 0 and closeTime > 0:
        # Shelter is not 24/7
        if current_time > closeTime or current_time < openTime:
            # Shelter is closed
            #print 'shelter is closed'
            return -1

        TimeUntilClose = closeTime - current_time


    # Check if there are the right number of beds available
    num_open_beds = 0
    for bed in shelter["beds"]:
        if bed == 0:
            num_open_beds += 1
    #print num_open_beds
    if num_open_beds < len(party):
        #print "not enough beds"
        return -1


    # Check if shelter takes a party of the specified demographics
    if len(party) == 1:
        # Match the lone individual's demographics

        if shelter.get("constraints"):
            if not can_take_individual(party[0], shelter):
                #print 'ineligible'
                return -1
            if party[0].get("sex", 1) == 1 and not shelter.get("constraints").get("accepts_single_men",1):
                #print 'no men'
                return -1
            if party[0].get("sex", 2) == 2 and not shelter.get("constraints").get("accepts_single_women",1):
                #print 'no women'
                return -1
    else:
        # Party contains more than one person; run through rules for the individuals, then for parties

        max_children = shelter.get("constraints").get("max_children",100)
        # Check individual requirements for each party member and count the number of children, adult males and adult females
        num_men = 0
        num_women = 0
        num_children = 0
        num_pregnancies = 0
        for person in party:
            # If any person in the party cannot be taken by the shelter in any concievable manner, stop here
            if not can_take_individual(person, shelter):
                #print 'ineligible'
                return -1
            if person.get("age", 20) < 18:
                num_children += 1
            else:
                if person.get("gender", 1) == 1:
                    num_men += 1
                elif person.get("gender", 2) == 2:
                    num_women += 1
                    if person.get("is_pregnant", 0):
                        num_pregnancies += 1

        # Check maternity & family requirements
        if num_children > max_children:
            # Shelter cannot take this many children at once; not a match
            #print 'no kids'
            return -1
        if must_be_pregnant and num_pregnancies == 0:
            # Party must include at least one pregnant woman; not a match
            #print 'preggo'
            return -1

        # Check for rules on mixed-sex parties
        if (not accepts_single_men and num_women == 0):
            #print 'nsm'
            return -1
        if (not accepts_single_women and num_men == 0):
            #print 'nsw'
            return -1

        # Shelter can accept this party; return the distance to it as its desirability score
        #return dist_between(location, shelter["location"])

    return dist_between(location, shelter.get("location"))

def dist_between(location1, location2): #compute longitude-latitude distance between two points
    loc1 = [location1["Lat"], location1["Lng"]]
    loc2 = [location2["Lat"], location2["Lng"]]
    userLat = math.radians(loc1[0])
    userLong = math.radians(loc1[1])

    shelterLat = math.radians(loc2[0])
    shelterLong = math.radians(loc2[1])

    dLon = shelterLong - userLong
    dLat = shelterLat - userLat

    R = 3959.0 #approx radius of earth
    a = math.sin(dLat / 2)**2 + math.cos(userLat) * math.cos(shelterLat) * math.sin(dLon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R*c
