import numpy as np
def give_solution(user, shelters):
    avail_shelter = shelters
    for shelter in shelters:
        for req in shelter.reqs:
            if isinstance(req, int):
                if user.req != 0 and user.req != shelter.req:
                    avail_shelter.pop(shelter)
                    break
            else if isinstance(req, float):
                if user.req != 0 and (user.req <= shelter.req[0] or user.req >= shelter.req[1])
                    avail_shelter.pop(shelter)
                    break

                
