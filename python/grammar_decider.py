import enum

class Grammars(enum.Enum):
   fcns = 0
   cfns = 1
   nfcs = 2
   fncs = 3
   cnfs = 4
   ncfs = 5
   ncsf = 6
   cnsf = 7
   sncf = 8
   nscf = 9
   csnf = 10
   scnf = 11 #~3 big red circle filled
   sfnc = 12
   fsnc = 13
   nsfc = 14 # ...square big filled red
   snfc = 15
   fnsc = 16 # ... filled square big red
   nfsc = 17
   cfsn = 18
   fcsn = 19
   scfn = 20 #1 big red filled circle
   csfn = 21 
   fscn = 22 #~3 filled big red circle
   sfcn = 23 #2  big filled red circle

class GrammarDecider():
    def grammar(self, moves):
        pass

"""
For each move, increment a count of those grammars that are compatable with it
return the best, possibly with some kind of confidence
"""
class MostMatched(GrammarDecider):

    prototypes = [[1,2,3,0],
                [2,1,3,0],
                [3,1,2,0],
                [1,3,2,0],
                [2,3,1,0],
                [3,2,1,0],
                [3,2,0,1],
                [2,3,0,1],
                [0,3,2,1],
                [3,0,2,1],
                [2,0,3,1],
                [0,2,3,1],
                [0,1,3,2],
                [1,0,3,2],
                [3,0,1,2],
                [0,3,1,2],
                [1,3,0,2],
                [3,1,0,2],
                [2,1,0,3],
                [1,2,0,3],
                [0,2,1,3],
                [2,0,1,3],
                [1,0,2,3],
                [0,1,2,3]]

    def __init__(self):
        self.matches = [0] * 24
        self.grammars = None

    def create(self, moves):
        self.matches = [0] * 24
        for m in moves:
            for i, p in enumerate(MostMatched.prototypes):
                if MostMatched._matches(m, p):
                    self.matches[i] += 1
        maxGrammars = []
        maxVal = -1
        for i, v in enumerate(self.matches):
            if (v == maxVal):
                maxGrammars.append(Grammars(i))
            elif v > maxVal:
                maxGrammars = [Grammars(i)]
                maxVal = v
        self.grammars = maxGrammars
        return self

    def _matches(move, prototype):
        pIndex = -1
        for w in move:
            found = False
            for j in range(pIndex+1, 4):
                if prototype[j] == w.value:
                    pIndex = j
                    found = True
                    break
            if not found:
                return False
        return True


"""
Compare each pair of word types for the order > 50% of the time and
decide which grammar this means is most likely for the overall proportions

Not fully implemented because I don't think I'll use it. But I'll
leave this here for now just in case.
"""
class RelativeOrder(GrammarDecider):

    def __init__(self):
        self.pairs_prop = None
        self.pairs = None
        self.grammars = None

    def grammar(self, moves):
        self.pairs = RelativeOrder._relative_order_proportions(moves)
        self.pairs_prop = RelativeOrder._calc_pairs_prop(self.pairs)
        self.grammars = self._grammar_from_relativeorders()
        return self.grammars

    def _calc_pairs_prop(pairs):
        pairs_prop = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0], [0, 0, 0, 0]]
        for i in range(4):
            for j in range(4):
                if (pairs[i][j] > 0):
                    pairs_prop[i][j] = pairs[i][j] / (pairs[i][j] + pairs[j][i])
                else:
                    pairs_prop[i][j] = None
        return pairs_prop

    def _relative_order_proportions(moves):
                    # after
                #a0  a1  a2   n
        pairs = [[0, 0, 0, 0], #a0
                [0, 0, 0, 0], #a1
                [0, 0, 0, 0], #a2 before
                [0, 0, 0, 0]] #n
        for m in moves:
            for i, j in [[0,1], [0,2], [1,2]]:
                w = m[i].value
                w2 = m[j].value
                pairs[w][w2] += 1

        return pairs

    #Size = 0
    #Filled = 1
    #Color = 2
    #Noun = 3
    def _grammar_from_relativeorders(self):
        #TODO: check for typos
        grammars = []
        if self._od(0,1) and self._od(0,2) and self._od(0,3):
            # size
            if self._od(1,2) and self._od(1,3):
                # size, filled
                if self._od(2,3):
                    grammars.append(Grammars.sfcn) # size, filled, colour
                if self._od(2,3):
                    grammars.append(Grammars.sfnc) # size, filled, noun
            if self._od(2,1) and self._od(2,3):
                # size, colour
                if self._od(1,3):
                    grammars.append(Grammars.scfn) # size, colour, filled
                if self._od(3,1):
                    grammars.append(Grammars.scnf) # size, colour, noun
            if self._od(3,1) and self._od(3,2):
                # size, noun
                if self._od(1,2):
                    grammars.append(Grammars.sncf) # size, noun, colour
                if self._od(2,1):
                    grammars.append(Grammars.snfc) # size, noun, filled
        if self._od(1,0) and self._od(1,2) and self._od(1,3):
            # filled
            if self._od(0,2) and self._od(0,3):
                # filled, size
                if self._od(2,3):
                    grammars.append(Grammars.fscn) # filled, size, colour
                if self._od(2,3):
                    grammars.append(Grammars.fsnc) # filled, size, noun
            if self._od(2,0) and self._od(2,3):
                # filled, colour
                if self._od(0,3):
                    grammars.append(Grammars.fcsn) # filled, colour, size
                if self._od(3,0):
                    grammars.append(Grammars.fcns) # filled, colour, noun
            if self._od(3,0) and self._od(3,2):
                # filled, noun
                if self._od(2,0):
                    grammars.append(Grammars.fncs) # filled, noun, colour
                if self._od(0,2):
                    grammars.append(Grammars.fnsc) # filled, noun, size
        if self._od(2,0) and self._od(2,1) and self._od(2,3):
            # colour
            if self._od(1,0) and self._od(1,3):
                # colour, filled
                if self._od(0,3):
                    grammars.append(Grammars.cfsn) # colour, filled, size
                if self._od(3,0):
                    grammars.append(Grammars.cfns) # colour, filled, noun
            if self._od(0,1) and self._od(0,3):
                # colour, size
                if self._od(1,3):
                    grammars.append(Grammars.csfn) # colour, size, filled
                if self._od(3,1):
                    grammars.append(Grammars.csnf) # colour, size, noun
            if self._od(3,0) and self._od(3,1):
                # colour, noun
                if self._od(1,0):
                    grammars.append(Grammars.cnfs) # colour, noun, filled
                if self._od(0,1):
                    grammars.append(Grammars.cnsf) # colour, noun, size
        if self._od(3,0) and self._od(3,1) and self._od(3,2):
            # noun
            if self._od(0,1) and self._od(0,2):
                # noun, size
                if self._od(1,2):
                    grammars.append(Grammars.nsfc) # noun, size, filled
                if self._od(2,1):
                    grammars.append(Grammars.nscf) # noun, size, colour
            if self._od(2,1) and self._od(2,0):
                # noun, colour
                if self._od(0,1):
                    grammars.append(Grammars.ncsf) # noun, colour, size
                if self._od(1,0):
                    grammars.append(Grammars.ncfs) # noun, colour, filled
            if self._od(1,0) and self._od(1,2):
                # noun, filled
                if self._od(2,0):
                    grammars.append(Grammars.nfcs) # noun, filled, colour
                if self._od(0,2):
                    grammars.append(Grammars.nfsc) # noun, filled, size
        return grammars

    def _od(self, i, j):
        if (self.pairs[i][j] > 0):
            prop = self.pairs[i][j] / (self.pairs[i][j] + self.pairs[j][i])
            return prop > 0.5
        else:
            return False