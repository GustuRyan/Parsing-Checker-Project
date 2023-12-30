from modules.cnf_algorithm import get_set_of_production, get_raw_set_of_production
import graphviz

TRIANGULAR_TABLE = {}
PARSE_TREE = None
PREV_NODE = None

def is_accepted(inputString):
    global TRIANGULAR_TABLE
    TRIANGULAR_TABLE = {}
    prodRules = get_raw_set_of_production()
    inputString = inputString.lower().split(" ")
    for i in range(1, len(inputString) + 1):
        for j in range(i, len(inputString) + 1):
            TRIANGULAR_TABLE[(i, j)] = []
    for i in range(len(inputString), 0, -1):
        for j in range(1, i + 1):
            if j == j + len(inputString) - i:
                tempList = []
                for key, value in prodRules.items():
                    for val in value:
                        if val == inputString[j - 1] and key not in tempList:
                            tempList.append(key)
                TRIANGULAR_TABLE[(j, j + len(inputString) - i)] = tempList
            else:
                tempList = []
                resultList = []
                for k in range(len(inputString) - i):
                    first = TRIANGULAR_TABLE[(j, j + k)]
                    second = TRIANGULAR_TABLE[(j + k + 1, j + len(inputString) - i)]
                    for fi in first:
                        for se in second:
                            if fi + " " + se not in tempList:
                                tempList.append(fi + " " + se)
                for key, value in prodRules.items():
                    for val in value:
                        if val in tempList and key not in resultList:
                            resultList.append(key)
                TRIANGULAR_TABLE[(j, j + len(inputString) - i)] = resultList
    return "K" in TRIANGULAR_TABLE[(1, len(inputString))]

def is_parent(posX, posY, limit, check, prodRules):
    global TRIANGULAR_TABLE
    x = posX
    y = posY
    while posX > 1 and posY <= limit:
        posX -= 1
        if TRIANGULAR_TABLE[(posX, posY)] != []:
            backVar = TRIANGULAR_TABLE[(posX, posY)][-1]
            for i in prodRules[backVar]:
                if check in i.split(" "):
                    return [True, posX, posY]
            return [False, None, None]
    posX = x
    posY = y
    while posX >= 1 and posY < limit:
        posY += 1
        if TRIANGULAR_TABLE[(posX, posY)] != []:
            backVar = TRIANGULAR_TABLE[(posX, posY)][-1]
            for i in prodRules[backVar]:
                if check in i.split(" "):
                    return [True, posX, posY]
            return [False, None, None]
    return [False, None, None]

def search_left(listVar, checkPos, curPost, posX, posY, limit, prodRules):
    global PARSE_TREE
    global PREV_NODE

    structureTier = ["S", "P", "O", "Pel", "Ket"]

    if len(listVar) == 1:
        if (listVar[0] == "K"):
            PARSE_TREE.edge("K", PREV_NODE)
            return
        else:
            res, x, y = is_parent(posX, posY, limit, listVar[curPost], prodRules)
            if res == True:
                temp = TRIANGULAR_TABLE[(x, y)][-1]
                parentNode = str(temp + " (" + str(x) + "," + str(y) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                search_left(TRIANGULAR_TABLE[(x, y)], len(TRIANGULAR_TABLE[(x, y)])-2, len(TRIANGULAR_TABLE[(x, y)])-1, x, y, limit, prodRules)
            else:
                return
    else:
        if listVar[checkPos] in structureTier and checkPos == 0:
            res, x, y = is_parent(posX, posY, limit, listVar[checkPos], prodRules)
            if res == True:
                parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                PARSE_TREE.edge("K", parentNode)
                return
            else:
                res2, x2, y2 = is_parent(posX, posY, limit, listVar[curPost], prodRules)
                if res2 == True:
                    temp = TRIANGULAR_TABLE[(x2, y2)][-1]
                    parentNode = str(temp + " (" + str(x2) + "," + str(y2) + ")")
                    PARSE_TREE.edge(parentNode, PREV_NODE)
                    PREV_NODE = parentNode
                    search_left(TRIANGULAR_TABLE[(x2, y2)], len(TRIANGULAR_TABLE[(x2, y2)])-2, len(TRIANGULAR_TABLE[(x2, y2)])-1, x2, y2, limit, prodRules)
                else:
                    return
        elif listVar[checkPos] in structureTier and checkPos > 0:
            res, x, y = is_parent(posX, posY, limit, listVar[checkPos], prodRules)
            if res == True:
                parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                search_left(TRIANGULAR_TABLE[(x, y)], len(TRIANGULAR_TABLE[(x, y)])-2, len(TRIANGULAR_TABLE[(x, y)])-1, x, y, limit, prodRules)
            else:
                search_left(listVar, checkPos-1, curPost, posX, posY, limit, prodRules)
        elif listVar[checkPos] not in structureTier and checkPos == 0:
            parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
            PARSE_TREE.edge(parentNode, PREV_NODE)
            PREV_NODE = parentNode
            res, x, y = is_parent(posX, posY, limit, listVar[checkPos], prodRules)
            if res:
                temp = TRIANGULAR_TABLE[(x, y)][-1]
                parentNode = str(temp + " (" + str(x) + "," + str(y) + ")")
                PARSE_TREE.edge(parentNode, PREV_NODE)
                PREV_NODE = parentNode
                search_left(TRIANGULAR_TABLE[(x, y)], len(TRIANGULAR_TABLE[(x, y)])-2, len(TRIANGULAR_TABLE[(x, y)])-1, x, y, limit, prodRules)
        elif listVar[checkPos] not in structureTier and checkPos > 0:
            isFound = False
            for i in prodRules[listVar[checkPos]]:
                if listVar[curPost] in i.split(" "):
                    parentNode = str(listVar[checkPos] + " (" + str(posX) + "," + str(posY) + ")")
                    PARSE_TREE.edge(parentNode, PREV_NODE)
                    PREV_NODE = parentNode
                    isFound = True
                    break
            if isFound:
                search_left(listVar, checkPos-1, checkPos, posX, posY, limit, prodRules)

def get_parse_tree(inputString):
    if is_accepted(inputString):
        global TRIANGULAR_TABLE
        global PARSE_TREE
        global PREV_NODE

        PARSE_TREE = graphviz.Graph("G", strict=True)
        PARSE_TREE.attr("node", shape="circle")
        PARSE_TREE.node("K")

        prodRules = get_raw_set_of_production()
        inputString = inputString.lower().split(" ")

        for i in range(1, len(inputString)+1):
            baseList = TRIANGULAR_TABLE[(i, i)]
            childNode = str(inputString[i-1] + " (" + str(i) + "," + str(i) + ")")
            parentNode = str(baseList[-1] + " (" + str(i) + "," + str(i) + ")")
            PARSE_TREE.edge(parentNode, childNode)
            PREV_NODE = parentNode
            if (len(baseList) == 1):
                search_left(baseList, len(baseList)-1, len(baseList)-1, i, i, len(inputString), prodRules)
            else:
                search_left(baseList, len(baseList)-2, len(baseList)-1, i, i, len(inputString), prodRules)
                
        return PARSE_TREE
    else:
        return None


def get_table_element(inputString):
    global TRIANGULAR_TABLE
    result = []
    n = len(inputString.split(" "))
    
    # Inisialisasi TRIANGULAR_TABLE jika belum
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            if (i, j) not in TRIANGULAR_TABLE:
                TRIANGULAR_TABLE[(i, j)] = []

    for i in range(1, n + 1):
        temp = []
        for j in range(i):
            # Memeriksa apakah elemen sudah ada sebelum mengaksesnya
            if (j + 1, n - i + j + 1) in TRIANGULAR_TABLE:
                res = TRIANGULAR_TABLE[(j + 1, n - i + j + 1)]
                if len(res) == 0:
                    temp.append("\u2205")
                else:
                    temp.append("{" + ", ".join(res) + "}")
            else:
                temp.append("\u2205")
        result.append(temp)

    result.append(inputString.split(" "))
    return result

