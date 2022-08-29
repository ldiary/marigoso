import statistics

# Identify how many times a ball number is drawn in same order
def getFrequencyPerDrawOrder(listOfDraws):
    frequencyPerDrawOrder = {
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {}
    }
    for draw in listOfDraws:
        for drawnOrder in frequencyPerDrawOrder:
            ball = draw[drawnOrder]
            if ball not in frequencyPerDrawOrder[drawnOrder]:
                frequencyPerDrawOrder[drawnOrder][ball] = 1
            else:
                frequencyPerDrawOrder[drawnOrder][ball] += 1
    return frequencyPerDrawOrder

# Identify ball number that has appeared at least twice on same drawn order
def getQualifiedNumbers(listOfDraws, drawnOrder):
    frequencyPerDrawOrder = getFrequencyPerDrawOrder(listOfDraws)
    qualifiedNumbers = []
    for ball in frequencyPerDrawOrder[drawnOrder]:
        if frequencyPerDrawOrder[drawnOrder][ball] >= 2:
            qualifiedNumbers.append(ball)
    return qualifiedNumbers

# Identify the next time the number is due and when it is overdue
def getDueTimesOfQualifiedNumbers(listOfDraws, drawnOrder):
    qualifiedNumbers = getQualifiedNumbers(listOfDraws, drawnOrder)
    detailsOfQualifiedBalls = {}
    for ball in qualifiedNumbers:
        listOfAllOccurences = []
        # Get all occurences of the ball number in the same drawn order
        for draw in listOfDraws:
            if draw[drawnOrder] == ball:
                listOfAllOccurences.append(draw)
        detailsOfQualifiedBalls[ball] = {"intervals": []}
        qualifiedBall = detailsOfQualifiedBalls[ball]
        for index, draw in enumerate(listOfAllOccurences):
            if index == 0:
                qualifiedBall["last drawn"] = draw["index"]
            else:
                qualifiedBall["intervals"].append(listOfAllOccurences[index - 1]["index"] - draw["index"])
        qualifiedBall["next due"] = qualifiedBall["last drawn"] + min(qualifiedBall["intervals"])
        # qualifiedBall["over due"] = qualifiedBall["last drawn"] + max(qualifiedBall["intervals"])
        qualifiedBall["over due"] = qualifiedBall["last drawn"] + int(statistics.fmean(qualifiedBall["intervals"]))
    return detailsOfQualifiedBalls

# Identify the over due ball numbers per draw order
def getOverDuePerDrawnOrder(listOfDraws, drawnOrder):
    detailedQualifiedNumbers = getDueTimesOfQualifiedNumbers(listOfDraws, drawnOrder)
    overdues = {}
    for ball in detailedQualifiedNumbers:
        if detailedQualifiedNumbers[ball]["over due"] <= len(listOfDraws):
            overdues[ball] = detailedQualifiedNumbers[ball]
    return overdues

def getOverDueBallsPerDrawnOrder(listOfDraws):
    overdues = {}
    for drawnOrder in range(1, 6):
        overdues[drawnOrder] = getOverDuePerDrawnOrder(listOfDraws, drawnOrder)
    return overdues

# Identify the ball numbers that has most over due in multiple draw orders
def getShortLists(listOfDraws, noLimit=True):
    overDueBallsPerDrawnOrder = getOverDueBallsPerDrawnOrder(listOfDraws)
    shortLists = {}
    finalShortList = []
    for drawnOrder in overDueBallsPerDrawnOrder:
        for ball in overDueBallsPerDrawnOrder[drawnOrder]:
            if ball not in shortLists:
                shortLists[ball] = 1
            else:
                shortLists[ball] += 1
    for index, ball in enumerate(sorted(shortLists, key=shortLists.get, reverse=True)):
        finalShortList.append(ball)
        if (noLimit != True):
            if len(finalShortList) == noLimit:
                return finalShortList
    return finalShortList

def getOverAllChancesOfMatching(listOfDraws, noLimit=True):
    matched3 = 0
    matched4 = 0
    matched5 = 0
    lastDraw = len(listOfDraws) + 1
    for nthDraw in range(1, lastDraw):
        includedRange = []
        nextDraw = None
        for draw in listOfDraws:
            if draw["index"] <= nthDraw:
                # print("{} | {}".format(draw["index"], draw["day"]))
                includedRange.append(draw)
            if draw["index"] == nthDraw + 1:
                nextDraw = draw
        assert(nthDraw == len(includedRange))
        rangeShortList = getShortLists(includedRange, noLimit)
        # print("{} | {} | {}".format(nthDraw, len(rangeShortList), rangeShortList))
        matchedNumbers = []
        if nextDraw is not None:
            for drawnOrder in range(1, 6):
                if nextDraw[drawnOrder] in rangeShortList:
                    matchedNumbers.append(nextDraw[drawnOrder])
            noOfMatches = len(matchedNumbers)
            if noOfMatches == 3:
                matched3 += 1
            elif noOfMatches == 4:
                matched4 += 1
            elif noOfMatches == 5:
                matched5 += 1
            # print("{} | {}".format(nthDraw, matchedNumbers))
            # print("{} | ({}, {}, {})".format(nthDraw, matched3, matched4, matched5))
            print("{:05d} | {:05d} | ({:03d}, {:03d}, {:03d}) | {}".format(nthDraw, len(rangeShortList), matched3, matched4, matched5, matchedNumbers))
        else:
            print("{:05d} | {:05d} | (---, ---, ---) | {}".format(nthDraw, len(rangeShortList), rangeShortList))