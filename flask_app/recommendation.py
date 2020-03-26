

#Preprocessing

def labels_ratio(cnn_input: List):
    n = sum(cnn_input)
    return [1+cat/n for cat in cnn_input]

def scoring_(scores):
    food = scores['Food']*weights[0]
    outdoor = scores['Outdoor']*weights[1]
    arts = scores['Arts']*weights[2]
    sights = scores['Sights']*weights[3]
    nightlife = scores['Nightlife']*weights[4]
    return food+outdoor+arts+sights+nightlife

def scoring(SB):
    SB['Score'] = SB.apply(scoring_,axis=1)
    return SB

def pipeline(SBpath,cnn_input):
    global weights
    SB = pd.read_csv(SBpath)
    weights = labels_ratio(cnn_input)
    SB = scoring(SB)
    return SB.sort_values(by='Score',ascending=False)