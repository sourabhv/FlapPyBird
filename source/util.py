# util.py
# -------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import sys
import inspect
import heapq, random
import cStringIO


class FixedRandom:
    def __init__(self):
        fixedState = (3, (2147483648L, 507801126L, 683453281L, 310439348L, 2597246090L, \
            2209084787L, 2267831527L, 979920060L, 3098657677L, 37650879L, 807947081L, 3974896263L, \
            881243242L, 3100634921L, 1334775171L, 3965168385L, 746264660L, 4074750168L, 500078808L, \
            776561771L, 702988163L, 1636311725L, 2559226045L, 157578202L, 2498342920L, 2794591496L, \
            4130598723L, 496985844L, 2944563015L, 3731321600L, 3514814613L, 3362575829L, 3038768745L, \
            2206497038L, 1108748846L, 1317460727L, 3134077628L, 988312410L, 1674063516L, 746456451L, \
            3958482413L, 1857117812L, 708750586L, 1583423339L, 3466495450L, 1536929345L, 1137240525L, \
            3875025632L, 2466137587L, 1235845595L, 4214575620L, 3792516855L, 657994358L, 1241843248L, \
            1695651859L, 3678946666L, 1929922113L, 2351044952L, 2317810202L, 2039319015L, 460787996L, \
            3654096216L, 4068721415L, 1814163703L, 2904112444L, 1386111013L, 574629867L, 2654529343L, \
            3833135042L, 2725328455L, 552431551L, 4006991378L, 1331562057L, 3710134542L, 303171486L, \
            1203231078L, 2670768975L, 54570816L, 2679609001L, 578983064L, 1271454725L, 3230871056L, \
            2496832891L, 2944938195L, 1608828728L, 367886575L, 2544708204L, 103775539L, 1912402393L, \
            1098482180L, 2738577070L, 3091646463L, 1505274463L, 2079416566L, 659100352L, 839995305L, \
            1696257633L, 274389836L, 3973303017L, 671127655L, 1061109122L, 517486945L, 1379749962L, \
            3421383928L, 3116950429L, 2165882425L, 2346928266L, 2892678711L, 2936066049L, 1316407868L, \
            2873411858L, 4279682888L, 2744351923L, 3290373816L, 1014377279L, 955200944L, 4220990860L, \
            2386098930L, 1772997650L, 3757346974L, 1621616438L, 2877097197L, 442116595L, 2010480266L, \
            2867861469L, 2955352695L, 605335967L, 2222936009L, 2067554933L, 4129906358L, 1519608541L, \
            1195006590L, 1942991038L, 2736562236L, 279162408L, 1415982909L, 4099901426L, 1732201505L, \
            2934657937L, 860563237L, 2479235483L, 3081651097L, 2244720867L, 3112631622L, 1636991639L, \
            3860393305L, 2312061927L, 48780114L, 1149090394L, 2643246550L, 1764050647L, 3836789087L, \
            3474859076L, 4237194338L, 1735191073L, 2150369208L, 92164394L, 756974036L, 2314453957L, \
            323969533L, 4267621035L, 283649842L, 810004843L, 727855536L, 1757827251L, 3334960421L, \
            3261035106L, 38417393L, 2660980472L, 1256633965L, 2184045390L, 811213141L, 2857482069L, \
            2237770878L, 3891003138L, 2787806886L, 2435192790L, 2249324662L, 3507764896L, 995388363L, \
            856944153L, 619213904L, 3233967826L, 3703465555L, 3286531781L, 3863193356L, 2992340714L, \
            413696855L, 3865185632L, 1704163171L, 3043634452L, 2225424707L, 2199018022L, 3506117517L, \
            3311559776L, 3374443561L, 1207829628L, 668793165L, 1822020716L, 2082656160L, 1160606415L, \
            3034757648L, 741703672L, 3094328738L, 459332691L, 2702383376L, 1610239915L, 4162939394L, \
            557861574L, 3805706338L, 3832520705L, 1248934879L, 3250424034L, 892335058L, 74323433L, \
            3209751608L, 3213220797L, 3444035873L, 3743886725L, 1783837251L, 610968664L, 580745246L, \
            4041979504L, 201684874L, 2673219253L, 1377283008L, 3497299167L, 2344209394L, 2304982920L, \
            3081403782L, 2599256854L, 3184475235L, 3373055826L, 695186388L, 2423332338L, 222864327L, \
            1258227992L, 3627871647L, 3487724980L, 4027953808L, 3053320360L, 533627073L, 3026232514L, \
            2340271949L, 867277230L, 868513116L, 2158535651L, 2487822909L, 3428235761L, 3067196046L, \
            3435119657L, 1908441839L, 788668797L, 3367703138L, 3317763187L, 908264443L, 2252100381L, \
            764223334L, 4127108988L, 384641349L, 3377374722L, 1263833251L, 1958694944L, 3847832657L, \
            1253909612L, 1096494446L, 555725445L, 2277045895L, 3340096504L, 1383318686L, 4234428127L, \
            1072582179L, 94169494L, 1064509968L, 2681151917L, 2681864920L, 734708852L, 1338914021L, \
            1270409500L, 1789469116L, 4191988204L, 1716329784L, 2213764829L, 3712538840L, 919910444L, \
            1318414447L, 3383806712L, 3054941722L, 3378649942L, 1205735655L, 1268136494L, 2214009444L, \
            2532395133L, 3232230447L, 230294038L, 342599089L, 772808141L, 4096882234L, 3146662953L, \
            2784264306L, 1860954704L, 2675279609L, 2984212876L, 2466966981L, 2627986059L, 2985545332L, \
            2578042598L, 1458940786L, 2944243755L, 3959506256L, 1509151382L, 325761900L, 942251521L, \
            4184289782L, 2756231555L, 3297811774L, 1169708099L, 3280524138L, 3805245319L, 3227360276L, \
            3199632491L, 2235795585L, 2865407118L, 36763651L, 2441503575L, 3314890374L, 1755526087L, \
            17915536L, 1196948233L, 949343045L, 3815841867L, 489007833L, 2654997597L, 2834744136L, \
            417688687L, 2843220846L, 85621843L, 747339336L, 2043645709L, 3520444394L, 1825470818L, \
            647778910L, 275904777L, 1249389189L, 3640887431L, 4200779599L, 323384601L, 3446088641L, \
            4049835786L, 1718989062L, 3563787136L, 44099190L, 3281263107L, 22910812L, 1826109246L, \
            745118154L, 3392171319L, 1571490704L, 354891067L, 815955642L, 1453450421L, 940015623L, \
            796817754L, 1260148619L, 3898237757L, 176670141L, 1870249326L, 3317738680L, 448918002L, \
            4059166594L, 2003827551L, 987091377L, 224855998L, 3520570137L, 789522610L, 2604445123L, \
            454472869L, 475688926L, 2990723466L, 523362238L, 3897608102L, 806637149L, 2642229586L, \
            2928614432L, 1564415411L, 1691381054L, 3816907227L, 4082581003L, 1895544448L, 3728217394L, \
            3214813157L, 4054301607L, 1882632454L, 2873728645L, 3694943071L, 1297991732L, 2101682438L, \
            3952579552L, 678650400L, 1391722293L, 478833748L, 2976468591L, 158586606L, 2576499787L, \
            662690848L, 3799889765L, 3328894692L, 2474578497L, 2383901391L, 1718193504L, 3003184595L, \
            3630561213L, 1929441113L, 3848238627L, 1594310094L, 3040359840L, 3051803867L, 2462788790L, \
            954409915L, 802581771L, 681703307L, 545982392L, 2738993819L, 8025358L, 2827719383L, \
            770471093L, 3484895980L, 3111306320L, 3900000891L, 2116916652L, 397746721L, 2087689510L, \
            721433935L, 1396088885L, 2751612384L, 1998988613L, 2135074843L, 2521131298L, 707009172L, \
            2398321482L, 688041159L, 2264560137L, 482388305L, 207864885L, 3735036991L, 3490348331L, \
            1963642811L, 3260224305L, 3493564223L, 1939428454L, 1128799656L, 1366012432L, 2858822447L, \
            1428147157L, 2261125391L, 1611208390L, 1134826333L, 2374102525L, 3833625209L, 2266397263L, \
            3189115077L, 770080230L, 2674657172L, 4280146640L, 3604531615L, 4235071805L, 3436987249L, \
            509704467L, 2582695198L, 4256268040L, 3391197562L, 1460642842L, 1617931012L, 457825497L, \
            1031452907L, 1330422862L, 4125947620L, 2280712485L, 431892090L, 2387410588L, 2061126784L, \
            896457479L, 3480499461L, 2488196663L, 4021103792L, 1877063114L, 2744470201L, 1046140599L, \
            2129952955L, 3583049218L, 4217723693L, 2720341743L, 820661843L, 1079873609L, 3360954200L, \
            3652304997L, 3335838575L, 2178810636L, 1908053374L, 4026721976L, 1793145418L, 476541615L, \
            973420250L, 515553040L, 919292001L, 2601786155L, 1685119450L, 3030170809L, 1590676150L, \
            1665099167L, 651151584L, 2077190587L, 957892642L, 646336572L, 2743719258L, 866169074L, \
            851118829L, 4225766285L, 963748226L, 799549420L, 1955032629L, 799460000L, 2425744063L, \
            2441291571L, 1928963772L, 528930629L, 2591962884L, 3495142819L, 1896021824L, 901320159L, \
            3181820243L, 843061941L, 3338628510L, 3782438992L, 9515330L, 1705797226L, 953535929L, \
            764833876L, 3202464965L, 2970244591L, 519154982L, 3390617541L, 566616744L, 3438031503L, \
            1853838297L, 170608755L, 1393728434L, 676900116L, 3184965776L, 1843100290L, 78995357L, \
            2227939888L, 3460264600L, 1745705055L, 1474086965L, 572796246L, 4081303004L, 882828851L, \
            1295445825L, 137639900L, 3304579600L, 2722437017L, 4093422709L, 273203373L, 2666507854L, \
            3998836510L, 493829981L, 1623949669L, 3482036755L, 3390023939L, 833233937L, 1639668730L, \
            1499455075L, 249728260L, 1210694006L, 3836497489L, 1551488720L, 3253074267L, 3388238003L, \
            2372035079L, 3945715164L, 2029501215L, 3362012634L, 2007375355L, 4074709820L, 631485888L, \
            3135015769L, 4273087084L, 3648076204L, 2739943601L, 1374020358L, 1760722448L, 3773939706L, \
            1313027823L, 1895251226L, 4224465911L, 421382535L, 1141067370L, 3660034846L, 3393185650L, \
            1850995280L, 1451917312L, 3841455409L, 3926840308L, 1397397252L, 2572864479L, 2500171350L, \
            3119920613L, 531400869L, 1626487579L, 1099320497L, 407414753L, 2438623324L, 99073255L, \
            3175491512L, 656431560L, 1153671785L, 236307875L, 2824738046L, 2320621382L, 892174056L, \
            230984053L, 719791226L, 2718891946L, 624L), None)
        self.random = random.Random()
        self.random.setstate(fixedState)

"""
 Data structures useful for implementing SearchAgents
"""

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "Pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the stack is empty"
        return len(self.list) == 0

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0,item)

    def pop(self):
        """
          Dequeue the earliest enqueued item still in the queue. This
          operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        # FIXME: restored old behaviour to check against old results better
        # FIXED: restored to stable behaviour
        entry = (priority, self.count, item)
        # entry = (priority, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        #  (_, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))


def manhattanDistance( xy1, xy2 ):
    "Returns the Manhattan distance between points xy1 and xy2"
    return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

"""
  Data structures and functions useful for various course projects

  The search project should not need anything below this line.
"""

class Counter(dict):
    """
    A counter keeps track of counts for a set of keys.

    The counter class is an extension of the standard python
    dictionary type.  It is specialized to have number values
    (integers or floats), and includes a handful of additional
    functions to ease the task of counting data.  In particular,
    all keys are defaulted to have value 0.  Using a dictionary:

    a = {}
    print a['test']

    would give an error, while the Counter class analogue:

    >>> a = Counter()
    >>> print a['test']
    0

    returns the default 0 value. Note that to reference a key
    that you know is contained in the counter,
    you can still use the dictionary syntax:

    >>> a = Counter()
    >>> a['test'] = 2
    >>> print a['test']
    2

    This is very useful for counting things without initializing their counts,
    see for example:

    >>> a['blah'] += 1
    >>> print a['blah']
    1

    The counter also includes additional functionality useful in implementing
    the classifiers for this assignment.  Two counters can be added,
    subtracted or multiplied together.  See below for details.  They can
    also be normalized and their total count and arg max can be extracted.
    """
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.

        >>> a = Counter()
        >>> a.incrementAll(['one','two', 'three'], 1)
        >>> a['one']
        1
        >>> a['two']
        1
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.

        >>> a = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> a['third'] = 1
        >>> a.sortedKeys()
        ['second', 'third', 'first']
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['second'] = 5
        >>> a['third'] = 1.5
        >>> a['fourth'] = 2.5
        >>> a * b
        14
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> a += b
        >>> a['first']
        1
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a + b)['first']
        1
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.

        >>> a = Counter()
        >>> b = Counter()
        >>> a['first'] = -2
        >>> a['second'] = 4
        >>> b['first'] = 3
        >>> b['third'] = 1
        >>> (a - b)['first']
        -5
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

def raiseNotDefined():
    fileName = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print "*** Method not implemented: %s at line %s of %s" % (method, line, fileName)
    sys.exit(1)

def normalize(vectorOrCounter):
    """
    normalize a vector or counter by dividing each value by the sum of all values
    """
    normalizedCounter = Counter()
    if type(vectorOrCounter) == type(normalizedCounter):
        counter = vectorOrCounter
        total = float(counter.totalCount())
        if total == 0: return counter
        for key in counter.keys():
            value = counter[key]
            normalizedCounter[key] = value / total
        return normalizedCounter
    else:
        vector = vectorOrCounter
        s = float(sum(vector))
        if s == 0: return vector
        return [el / s for el in vector]

def nSample(distribution, values, n):
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    rand = [random.random() for i in range(n)]
    rand.sort()
    samples = []
    samplePos, distPos, cdf = 0,0, distribution[0]
    while samplePos < n:
        if rand[samplePos] < cdf:
            samplePos += 1
            samples.append(values[distPos])
        else:
            distPos += 1
            cdf += distribution[distPos]
    return samples

def sample(distribution, values = None):
    if type(distribution) == Counter:
        items = sorted(distribution.items())
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    choice = random.random()
    i, total= 0, distribution[0]
    while choice > total:
        i += 1
        total += distribution[i]
    return values[i]

def sampleFromCounter(ctr):
    items = sorted(ctr.items())
    return sample([v for k,v in items], [k for k,v in items])

def getProbability(value, distribution, values):
    """
      Gives the probability of a value under a discrete distribution
      defined by (distributions, values).
    """
    total = 0.0
    for prob, val in zip(distribution, values):
        if val == value:
            total += prob
    return total

def flipCoin( p ):
    r = random.random()
    return r < p

def chooseFromDistribution( distribution ):
    "Takes either a counter or a list of (prob, key) pairs and samples"
    if type(distribution) == dict or type(distribution) == Counter:
        return sample(distribution)
    r = random.random()
    base = 0.0
    for prob, element in distribution:
        base += prob
        if r <= base: return element

def nearestPoint( pos ):
    """
    Finds the nearest grid point to a position (discretizes).
    """
    ( current_row, current_col ) = pos

    grid_row = int( current_row + 0.5 )
    grid_col = int( current_col + 0.5 )
    return ( grid_row, grid_col )

def sign( x ):
    """
    Returns 1 or -1 depending on the sign of x
    """
    if( x >= 0 ):
        return 1
    else:
        return -1

def arrayInvert(array):
    """
    Inverts a matrix stored as a list of lists.
    """
    result = [[] for i in array]
    for outer in array:
        for inner in range(len(outer)):
            result[inner].append(outer[inner])
    return result

def matrixAsList( matrix, value = True ):
    """
    Turns a matrix into a list of coordinates matching the specified value
    """
    rows, cols = len( matrix ), len( matrix[0] )
    cells = []
    for row in range( rows ):
        for col in range( cols ):
            if matrix[row][col] == value:
                cells.append( ( row, col ) )
    return cells

def lookup(name, namespace):
    """
    Get a method or class from any imported module from its name.
    Usage: lookup(functionName, globals())
    """
    dots = name.count('.')
    if dots > 0:
        moduleName, objName = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
        module = __import__(moduleName)
        return getattr(module, objName)
    else:
        modules = [obj for obj in namespace.values() if str(type(obj)) == "<type 'module'>"]
        options = [getattr(module, name) for module in modules if name in dir(module)]
        options += [obj[1] for obj in namespace.items() if obj[0] == name ]
        if len(options) == 1: return options[0]
        if len(options) > 1: raise Exception, 'Name conflict for %s'
        raise Exception, '%s not found as a method or class' % name

def pause():
    """
    Pauses the output stream awaiting user feedback.
    """
    print "<Press enter/return to continue>"
    raw_input()


# code to handle timeouts
#
# FIXME
# NOTE: TimeoutFuncton is NOT reentrant.  Later timeouts will silently
# disable earlier timeouts.  Could be solved by maintaining a global list
# of active time outs.  Currently, questions which have test cases calling
# this have all student code so wrapped.
#
import signal
import time
class TimeoutFunctionException(Exception):
    """Exception to raise on a timeout"""
    pass


class TimeoutFunction:
    def __init__(self, function, timeout):
        self.timeout = timeout
        self.function = function

    def handle_timeout(self, signum, frame):
        raise TimeoutFunctionException()

    def __call__(self, *args, **keyArgs):
        # If we have SIGALRM signal, use it to cause an exception if and
        # when this function runs too long.  Otherwise check the time taken
        # after the method has returned, and throw an exception then.
        if hasattr(signal, 'SIGALRM'):
            old = signal.signal(signal.SIGALRM, self.handle_timeout)
            signal.alarm(self.timeout)
            try:
                result = self.function(*args, **keyArgs)
            finally:
                signal.signal(signal.SIGALRM, old)
            signal.alarm(0)
        else:
            startTime = time.time()
            result = self.function(*args, **keyArgs)
            timeElapsed = time.time() - startTime
            if timeElapsed >= self.timeout:
                self.handle_timeout(None, None)
        return result



_ORIGINAL_STDOUT = None
_ORIGINAL_STDERR = None
_MUTED = False

class WritableNull:
    def write(self, string):
        pass

def mutePrint():
    global _ORIGINAL_STDOUT, _ORIGINAL_STDERR, _MUTED
    if _MUTED:
        return
    _MUTED = True

    _ORIGINAL_STDOUT = sys.stdout
    #_ORIGINAL_STDERR = sys.stderr
    sys.stdout = WritableNull()
    #sys.stderr = WritableNull()

def unmutePrint():
    global _ORIGINAL_STDOUT, _ORIGINAL_STDERR, _MUTED
    if not _MUTED:
        return
    _MUTED = False

    sys.stdout = _ORIGINAL_STDOUT
    #sys.stderr = _ORIGINAL_STDERR

