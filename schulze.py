

#input: preference
    # p[i,j] = number of voters that prefer candidate i to canditate j
#output: order
    # o[i,j] = bottleneck number in the strongest path

def voting_results(preference, candidates):
    #prepare results
    results = dict()
    for candidate in candidates:
        results[candidate] = dict()
    
    #calculate voting rank
    for i in candidates:
        for j in candidates:
            if i != j:
                if preference[i][j] > preference[j][i]:
                    results[i][j] = preference[i][j]
                else:
                    results[i][j] = 0

    for i in candidates:
        for j in candidates:
            if i != j:
                for k in candidates:
                    if i != k and j != k:
                        #p[j,k] := max ( p[j,k], min ( p[j,i], p[i,k] ) )
                        results[j][k] = max(results[j][k], min(results[j][i], results[i][k]))
    return results

"""
    input: votes is a list of preference ordered votes
        vote = [(1,'a'), (2, 'b'), (2, 'd'), (2, 'x'), (100, 'y')]
    input: candidates is a list of candidate voting keys:
    candidates = ['a,' 'b,' 'c,' 'd,' 'x,' 'y']

    Note that candidate 'c' is not listed in the example vote. This means no vote for 'c'.

    output: A dictionary of preference counts for each candidate.
    preference = {
                    'a': {'a': 0, 'b': 1, 'c': 1, 'd,' 1, 'x,' 1, 'y': 1}, #place ahead of everyone
                    'b': {'b': 0, 'a': 0, 'c': 1, 'd,' 1, 'x,' 1, 'y': 1}, #not placed ahead of a, equal to d and x
                    'c': {'c': 0, 'b': 0, 'a': 0, 'd,' 0, 'x,' 0, 'y': 0}, #not placed ahead of anyone
                    'd': {'d': 0, 'b': 1, 'c': 1, 'a,' 0, 'x,' 1, 'y': 1}, #equal to b and x, ahead of y
                    'x': {'x': 0, 'b': 1, 'c': 1, 'd,' 1, 'a,' 0, 'y': 1}, #equal to b and d, ahead of y
                    'y': {'y': 0, 'b': 0, 'c': 1, 'd,' 0, 'x,' 0, 'a': 0}, #c got no vote
                    #'self' is always 0
                }
"""
def rank_votes(votes, candidates):
    invalid_votes = list()
    #prepare the output - 0 set all candidates
    preference = dict()
    for candidate in candidates:
        preference[candidate] = dict()
        for opponent in candidates:
            preference[candidate][opponent] = 0

    for vote in votes:
        vote.sort() #make sure the votes are in order
        if len(set([x[1] for x in vote])) == len(vote): #check for duplicate choices
            for i, choice in enumerate(vote):
                voted_candidates = set([x[1] for x in vote])
                tied_candidates = [x[1] for x in vote if choice[0] == x[0]] #so that [(1, 'a'), (2, 'c'), (2, 'e'), (3, 'b'), (5, 'd')] 'e' also gets a 'c' increment
                not_voted_candidates = set(candidates)-set(voted_candidates)
                #increment against all other candidates
                candidate = vote[i][1]
                opponents_to_increment = list(set([x[1] for x in vote[i+1:]] + list(not_voted_candidates) + tied_candidates))
                increment_candidate(candidate, opponents_to_increment, preference)
                #print preference
        else:
            #duplicate choice, invalid!
            invalid_votes.append(vote)
    return preference

def increment_candidate(candidate, opponents, preference_dict):
    for opponent in opponents:
        if opponent in preference_dict[candidate]:
            preference_dict[candidate][opponent] += 1
        else:
            preference_dict[candidate][opponent] = 1

candidates = ['a', 'b', 'c', 'd', 'e', 'x']
votes = [
        [(1,'a'),(2,'c'),(3,'b'),(4,'e'),(5,'d')],
        [(1,'a'),(2,'c'),(3,'b'),(4,'e'),(5,'d')],
        [(1,'a'),(2,'c'),(3,'b'),(4,'e'),(5,'d')],
        [(1,'a'),(2,'c'),(3,'b'),(4,'e'),(5,'d')],
        [(1,'a'),(2,'c'),(3,'b'),(4,'e'),(5,'d')], #5
        [(1,'a'),(2,'d'),(3,'e'),(4,'c'),(5,'b')],
        [(1,'a'),(2,'d'),(3,'e'),(4,'c'),(5,'b')],
        [(1,'a'),(2,'d'),(3,'e'),(4,'c'),(5,'b')],
        [(1,'a'),(2,'d'),(3,'e'),(4,'c'),(5,'b')],
        [(1,'a'),(2,'d'),(3,'e'),(4,'c'),(5,'b')], #5
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')],
        [(1,'b'),(2,'e'),(3,'d'),(4,'a'),(5,'c')], #8
        [(1,'c'),(2,'a'),(3,'b'),(4,'e'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'b'),(4,'e'),(5,'d')], #20
        [(1,'c'),(2,'a'),(3,'b'),(4,'e'),(5,'d')], #3
        [(1,'c'),(2,'b'),(3,'a'),(4,'d'),(5,'e')],
        [(1,'c'),(2,'b'),(3,'a'),(4,'d'),(5,'e')], #2
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')],
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')],
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')],
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')],
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')],
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')],
        [(1,'d'),(2,'c'),(3,'e'),(4,'b'),(5,'a')], #30
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')],
        [(1,'c'),(2,'a'),(3,'e'),(4,'b'),(5,'d')], #7
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')],
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')],
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')], #40
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')],
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')],
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')],
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')],
        [(1,'e'),(2,'b'),(3,'a'),(4,'d'),(5,'c')] #8
    ]


#candidates = ['x','y','z']
"""
votes = [
    [(1, 'x'),(2,'y'),(3,'z')],
    [(1, 'y'),(2,'z'),(3,'x')],
    [(1, 'z'),(2,'x'),(3,'y')]
]
"""
print 'number of votes:', len(votes)

#create directed graph
preference = rank_votes(votes, candidates)

#extract rank numbers
results = voting_results(preference, candidates)

print results
"""
    {'a': 
        {'x': 45, 'c': 28, 'b': 28, 'e': 24, 'd': 30}, 
    'c': 
        {'a': 25, 'x': 45, 'b': 29, 'e': 24, 'd': 29}, 
    'b': 
        {'a': 25, 'x': 45, 'c': 28, 'e': 24, 'd': 33}, 
    'e': 
        {'a': 25, 'x': 45, 'c': 28, 'b': 28, 'd': 31}, 
    'd': 
        {'a': 25, 'x': 45, 'c': 28, 'b': 28, 'e': 24}, 
    'x': 
        {'a': 0, 'c': 0, 'b': 0, 'e': 0, 'd': 0}}
"""

#print preference
"""{'a': 
        {'c': 26, 'b': 20, 'e': 22, 'd': 30}, 
    'c': 
        {'a': 19, 'b': 29, 'e': 24, 'd': 17}, 
    'b': 
        {'a': 25, 'c': 16, 'e': 18, 'd': 33}, 
    'e': 
        {'a': 23, 'c': 21, 'b': 27, 'd': 31},
    'd': 
        {'a': 15, 'c': 28, 'b': 12, 'e': 14}}
"""
#voting_results([])
