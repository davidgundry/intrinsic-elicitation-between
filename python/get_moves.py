import json
import enum

class Categories(enum.Enum):
    Size = 0
    Filled = 1
    Color = 2
    Noun = 3

def all_moves(filename, correct_form, coded):
    """ Returns moves from file as a single array """
    rawData = _load_data(filename)
    moves = []
    for d in rawData:
        if (d["data"]["gameVersion"] == "Normal" or d["data"]["gameVersion"] == "normal"):
            for m in d["data"]["moves"]:
                if correct_form:
                    if _correct_form(m):
                        if coded:
                            for i, w in enumerate(m):
                                m[i] = _replace(w)
                        moves.append(m)
                else:
                    if coded:
                        for i, w in enumerate(m):
                            m[i] = _replace(w)
                    moves.append(m)
    return moves

def moves_by_user(filename, condition, correct_form, coded):
    """ Returns moves from file as an array of arrays of moves per user. """
    rawData = _load_data(filename)
    moves = []
    for d in rawData:
        if (d["data"]["gameVersion"] == condition):
            u = []
            for m in d["data"]["moves"]:
                if correct_form:
                    if _correct_form(m):
                        if coded:
                            for i, w in enumerate(m):
                                m[i] = _replace(w)
                        u.append(m)
                else:
                    if coded:
                        for i, w in enumerate(m):
                            m[i] = _replace(w)
                    u.append(m)
            moves.append(u)
        
    return moves

def _load_data(filename):
    rawData = []
    with open(filename) as f:
        content = f.read()
        rawData = json.loads(content)
    return rawData

def _correct_form(array):
    a1, a2, a3, n = 0,0,0,0
    adj1 = ["big", "small"]
    adj2 = ["empty", "filled"]
    adj3 = ["red", "blue", "green"]
    nouns = ["square","circle","triangle","diamond"]
    for word in array:
        if word in adj1:
            a1 += 1
        elif word in adj2:
            a2 += 1
        elif word in adj3:
            a3 += 1
        elif word in nouns:
            n += 1
    return (a1 < 2) and (a2 < 2) and (a3 < 2) and (n == 1)

def _replace(word):
    adj1 = ["big", "small"]
    adj2 = ["empty", "filled"]
    adj3 = ["red", "blue", "green"]
    nouns = ["square","circle","triangle","diamond"]
    if word in adj1:
        return Categories.Size
    if word in adj2:
        return Categories.Filled
    if word in adj3:
        return Categories.Color
    if word in nouns:
        return Categories.Noun
