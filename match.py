def relevant(booltype):
    # Determines if
    return not (booltype == 0)

def can_take_individual(person, shelter):
    # Check if a shelter could EVER concievably take this individual under any circumstances
    # (There may be additional party requirements for the whole party)
    requirements = shelter["constraints"]

    if len(requirements) == 0: #if there are no requirements
        return True

    accepts_men = requirements["accepts_men"]
    accepts_single_men = requirements["accepts_single_men"]
    max_male_age = requirements["max_male_age"]
    min_male_age = requirements["min_male_age"]
    accepts_women = requirements["accepts_women"]
    accepts_single_women = requirements["accepts_single_women"]
    max_female_age = requirements["max_female_age"]
    min_female_age = requirements["min_female_age"]
    trans_friendly = requirements["trans_friendly"]
    must_be_pregnant = requirements["must_be_pregnant"]
    max_pregnancy_weeks = requirements["max_pregnancy_weeks"]
    min_pregnancy_weeks = requirements["min_pregnancy_weeks"]
    accepts_children = requirements["accepts_children"]
    max_children = requirements["max_children"]


    # Check gender and age requirements
    max_age = max(max_male_age, max_female_age)
    min_age = min(min_male_age, min_female_age)

    if person["sex"] == "Male" and person["gender"] == "Male":
        # Male and not trans
        if (not accepts_men) or max_male_age < person["age"] or min_male_age > person["age"]:
            # Person is not in the right age range for their gender; return false
            return False
        if must_be_pregnant:
            return False
    elif person["sex"] == "Female" and person["gender"] == "Female":
        # Female and not trans
        if (not accepts_women) or max_female_age < person["age"] or min_female_age > person["age"]:
            # Person is not in the right age range for their gender; return false
            return False
    else:
        # Person is transgender/intersex; see if shelter deals with such people
        if not trans_friendy:
            return False
        else:
            # Use person's gender identity instead of birth sex
            if person["gender"] == "Male":
                return (person["age"] >= min_male_age) and (person["age"] <= max_male_age)
            elif person["gender"] == "Female":
                return (person["age"] >= min_female_age) and (person["age"] <= max_female_age)
            else:
                # gender == "other"
                return (person["age"] <= max_age) or (person["age"] >= min_age)

    if must_be_pregnant:
        if not person["is_pregnant"]:
            return False
        elif person["weeks_pregnant"] > max_pregnancy_weeks or person["weeks_pregnant"] < min_pregnancy_weeks:
            return False

    # True by process of elimination
    return True

def computeRank(party, shelter, current_time, location):
    # Return -1 if ineligible, else return distance to shelter

    # Check if shelter is open
    openTime = shelter["open_time"]
    closeTime = shelter["close_time"]

    if openTime > 0 and closeTime > 0:
        # Shelter is not 24/7
        if current_time > closeTime or current_time < openTime:
            # Shelter is closed
            return -1
        TimeUntilClose = closeTime - current_time


    # Check if there are the right number of beds available
    num_open_beds = 0
    for bed in shelter["Beds"]:
        if bed == 0:
            num_open_beds += 1

    if num_open_beds < len(party):
        return -1

    # Check if shelter takes a party of the specified demographics
    if len(party) == 1:
        # Match the lone individual's demographics

        if not can_take_individual(party[0], shelter):
            return -1
        if party[0]["sex"] == "Male" and not shelter["accepts_single_men"]:
            return -1
        if party[0]["sex"] == "Female" and not shelter["accepts_single_women"]:
            return -1
    else:
        # Party contains more than one person; run through rules for the individuals, then for parties

        # Check individual requirements for each party member and count the number of children, adult males and adult females
        num_men = 0
        num_women = 0
        num_children = 0
        num_pregnancies = 0
        for person in party:
            # If any person in the party cannot be taken by the shelter in any concievable manner, stop here
            if not can_take_individual(person, shelter):
                return -1
            if person["age"] < 18:
                num_children += 1
            else:
                if person["gender"] == "Male":
                    num_men += 1
                elif person["gender"] == "Female":
                    num_women += 1
                    if person["is_pregnant"]:
                        num_pregnancies += 1

        # Check maternity & family requirements
        if num_children > max_children:
            # Shelter cannot take this many children at once; not a match
            return -1
        if must_be_pregnant and num_pregnancies == 0:
            # Party must include at least one pregnant woman; not a match
            return -1

        # Check for rules on mixed-sex parties
        if (not accepts_single_men and num_women == 0):
            return -1
        if (not accepts_single_women and num_men == 0):
            return -1

        # Shelter can accept this party; return the distance to it as its desirability score
        #return dist_between(location, shelter["location"])
    return dist_between(location, shelter["location"])

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
    a = sin(dLat / 2)**2 + cos(userLat) * cos(shelterLat) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))

    return R*c
