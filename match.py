def relevant(booltype):
    # Determines if 
    return not (booltype == 0)

def can_take_individual(person, shelter):
    # Check if a shelter could EVER concievably take this individual under any circumstances
    # (There may be additional party requirements for the whole party)

    # Check gender and age requirements
    if person["sex"] == "male" and person["gender"] == "male":
        # Single male and not trans
        if (not shelter["accepts_men"]) or shelter["max_male_age"] < person["age"] or shelter["min_male_age"] > person["age"]:
            # Person is not in the right age range for their gender; return false
            return False
    elif person["sex"] == "female" and person["gender"] == "female":
        # Single female and not trans
        if (not shelter["accepts_women"]) or shelter["max_female_age"] < person["age"] or shelter["min_female_age"] > person["age"]:
            # Person is not in the right age range for their gender; return false
            return False
    else:
        # Person is transgender/intersex; see if shelter deals with those people
        if not shelter["trans_friendy"]:
            return False
    # True by process of elimination
    return True
    
def computeRank(party, shelter, current_time, location):
    # Return -1 if ineligible, else return distance to shelter in miles

    # Check if shelter is open
    if current_time < shelter["closing_time"] or current_time < shelter["opening"]:
        # Shelter is closed
        return -1
    
    # Check if shelter takes a party of the specified demographics
    if len(party) == 1:
        # Match the lone individual's demographics
        if not can_take_individual(party[0], shelter):
            return -1
        if person["sex"] == "male" and not shelter["accepts_single_men"]:
            return -1
        if person["sex"] == "female" and not shelter["accepts_single_women"]:
            return -1
    else:
        # Party contains more than one person
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
                if person["gender"] == "male":
                    num_men += 1
                elif person["gender"] == "female":
                    num_women += 1
                    if person["is_pregnant"]
                        num_pregnancies += 1
        # Check maternity & family requirements
        if num_children > shelter["max_children"]:
            return -1
        if shelter["accepts_pregnant_women"] and num_pregnancies == 0:
            return -1
                                     
        # Shelter can accept this party; return the distance to it as its desirability score
        return dist_between(location, shelter["location"])
