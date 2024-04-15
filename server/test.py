import random

r1 = ["A", 0, 0, 0, 0, 0, 0]
r2 = ["B", 0, 0, 0, 0, 0, 0]
r3 = ["C", 0, 0, 0, 0, 0, 0]
r4 = ["D", 0, 0, 0, 0, 0, 0]
r5 = ["E", 0, 0, 0, 0, 0, 0]

e1 = ["A", 1, 2, 3, 4, 5, 6]
e2 = ["B", 1, 2, 3, 4, 5, 6]
e3 = ["C", 1, 2, 3, 4, 5, 6]
e4 = ["D", 1, 2, 3, 4, 5, 6]
e5 = ["E", 1, 2, 3, 4, 5, 6]

pieces = dict({"p1_tanker": [0,0], "p1_bomber": [0,0], "p1_jammer": [0,0], "p1_comms": [0,0], "p1_fighter1": [0,0], "p1_fighter2": [0,0],
"p2_tanker": [0,0], "p2_bomber": [0,0], "p2_jammer": [0,0], "p2_comms": [0,0], "p2_fighter1": [0,0], "p2_fighter2": [0,0]})

tiles = [["A",1],["A",2],["A",3],["A",4],["A",5],["A",6],["B",1],["B",2],["B",3],["B",4],["B",5],["B",6],["C",1],["C",2],["C",3],["C",4],["C",5],["C",6],["D",1],["D",2],["D",3],["D",4],["D",5],["D",6]]
movements = 0

board = [r1, r2, r3, r4, r5]
format = [e1, e2, e3, e4, e5]
p1_jam = 0
p2_jam = 0

class aircraft:
    def __init__(self, model, pos, p_num, c_num, c_ran, range):
        self.model = type
        self.pos = [0,0]
        self.player_num = p_num
        self.combat_val = c_num
        self.combat_range = c_ran
        self.range = range

class player:
    global r1
    global r4
    def __init__(self,name,column):
        if name == "1":
            r1[column] = "A"
            self.row = "A"
        else:
            r4[column] = "B"
            self.row = "D"
        self.column = column
        self.health = 2
        self.tanker = aircraft("tanker", [0,0], int(name), 0, 0, 100)
        self.bomber = aircraft("bomber", [0,0], int(name), 1, 2, 100)
        self.jammer = aircraft("jammer", [0,0], int(name), 0, 0, 2)
        self.comms = aircraft("comms", [0,0], int(name), 0, 3, 2)
        self.fighter1 = aircraft("fighter", [0,0], int(name), 3, 1, 2)
        self.fighter2 = aircraft("fighter", [0,0], int(name), 3, 1, 2)


def genUnit(turn,pos, row, column):
    temp = [row,column]
    if pos != [0,0]:
        return False

    if turn == 1:
        if (temp != ["A",1] and temp != ["A",2] and temp != ["B",1]):
            return False
    else:
        if (temp != ["D",6] and temp != ["D",5] and temp != ["C",6]):
            return False

    # Adjusts Numbers on board
    orgCheck = ((row == "A" and column == 1) == False)
    orgCheck2 = ((row == "D" and column == 6) == False)
    if orgCheck and orgCheck2:
        increase_unit(row,column)
    # don't need to print this, website should update image
    # else:
        # print("Unit is on the same tile as the Carrier, however, the symbol will not change. \n")

    return True

def move(pos, row, column):
    if pos != [0,0]:
        return checkmove(pos,row,column)

def showFormat(rows):
    print("-----------------")
    for x in rows:
        if x[0] == "E":
            print("Row", x[0])
            print(x[1] , "         " , x[5])
        else:
            print("Row ", x[0])
            print(x[1], "   ", x[3], "   " , x[5])
            print("  ", x[2],"   " , x[4], "   ", x[6])
            print()
    print("-----------------")

def checkmove(unit, row, column): #need to make this return which player needs to try again
    global r1
    global r2
    global r3
    global r4
    global r5
    global movements

    distance = calcDistance(ord(unit[0]) - 64, unit[1], (ord(row) - 64),column)
    if distance == 1:
        translate(distance, unit[0],unit[1],row, column)
       # print("success")
        return True
    else:
        print("Unit attempted to move from", unit[0], unit[1],"to", row, column, "distance was", distance, "User may attempt to move again\n")
        return False

def calcDistance(currRow, currCol,newRow, newCol):
    rowDiff = currRow - newRow
    if rowDiff < 0:
        rowDiff = rowDiff * -1
    colDiff = currCol - newCol
    if colDiff < 0:
        colDiff = colDiff * -1

    distance = 0
    offset = 0

    if rowDiff == 2:
        offset = 1
    elif rowDiff == 3:
        offset = 2

    if colDiff == 0:
        distance = rowDiff
    if colDiff == 1:
        if currCol % 2 ==0:
            if newRow < currRow:
                distance = 1 + rowDiff
            elif newRow > currRow:
                distance = rowDiff
        else:
            if newRow < currRow:
                distance = rowDiff
            elif newRow > currRow:
                distance = 1 + rowDiff
    if colDiff == 2:
        distance = offset+colDiff
    if colDiff == 3:
        if offset > 1:
            distance = 1 + colDiff
        else:
            distance = colDiff
        distance = offset + colDiff
    if colDiff == 4 or colDiff == 5:
        if offset > 1:
            distance = 1 + colDiff
        else:
            distance = colDiff
    if rowDiff == 0:
        distance = colDiff

    return distance

def printBoard(rows):
    first = 0
    print("-----------------")
    for x in rows:
        if x[0] == "E":
            print("         \\       /         \\       /         \\       / ")
            print("          \\     /           \\     /           \\     / ")
            print("           -----             -----             -----")
            print(x[1] , "         " , x[5])

        else:
            if first == 0:
                first+=1
                print("  -----             -----             -----")
                print(" /     \\           /     \\           /     \\")
                print("/       \\         /       \\         /       \\")
                print("   ",x[1], "     -----     ", x[3], "     -----     " , x[5], "     -----")
                print("\\       / /     \\ \\       / /     \\ \\       / /     \\")
                print(" \\     / /       \\ \\     / /       \\ \\     / /       \\")
                print("  -----     ",x[2],"     -----     ",x[4],"     -----     ",x[6])
            else:
                # print("  -----             -----             -----")
                print(" /     \\ \\       / /     \\ \\       / /     \\ \\       /")
                print("/       \\ \\     / /       \\ \\     / /       \\ \\     /")
                print("   ",x[1], "     -----     ", x[3], "     -----     " , x[5], "     -----")
                print("\\       / /     \\ \\       / /     \\ \\       / /     \\")
                print(" \\     / /       \\ \\     / /       \\ \\     / /       \\")
                print("  -----     ",x[2],"     -----     ",x[4],"     -----     ",x[6])

            # print("    ", x[2],"   " , x[4], "   ", x[6])

            # print(x[1], "   ", x[3], "   " , x[5])
            # print("  ", x[2],"   " , x[4], "   ", x[6])
    print("-----------------")

def reveal(row,column):
    enemies = ""
    for x in pieces:
        if pieces[x] == [row,column]:
            enemies+= (x + ", ")
    return enemies

def increase_unit(row,column):
    if row == "A":
        r1[column] +=1
    elif row == "B":
        r2[column] +=1
    elif row == "C":
        r3[column] +=1
    elif row == "D":
        r4[column] +=1
    elif row == "E":
        r5[column] +=1

def decrease_unit(row,column):
    if row == "A":
        r1[column] -=1
    elif row == "B":
        r2[column] -=1
    elif row == "C":
        r3[column] -=1
    elif row == "D":
        r4[column] -=1
    elif row == "E":
        r5[column] -=1

def regen(pos,row,column):
    temp = [row,column]
    if pos != ["E",1] and pos != ["E",5]:
        # print(pos," error is in pos\n")
        return False
    if (temp != ["A",1] and temp != ["A",2] and temp != ["B",1] and temp != ["D",6] and temp != ["D",5] and temp != ["C",6]):
        # print(temp,"error is in destination\n")
        return False

    reg = random.randrange(1,7)
    if reg > 5:
        # print("Unit Failed to be regenerated\n")
        return False

    # Adjusts Numbers on board
    orgCheck = ((row == "A" and column == 1) == False)
    orgCheck2 = ((row == "D" and column == 6) == False)
    if orgCheck and orgCheck2:
        increase_unit(row,column)

    return True

def relocate(turn, movers):

    if len(movers) > 2:
        return False

    if turn == 1:
        for x in movers:
            check = False
            while check == False:
                row = input("Input desired row for the " + x + " : ")
                column = int(input("Input desired column for the " + x + " : "))
                dist = calcDistance(ord(getattr(player1,x).pos[0])-64,getattr(player1,x).pos[1],ord(row)-64,column)

                if dist > 1:
                    print("This movement exceeds the 2 tile limit, please enter a different tile\n")
                    continue


                check = True
                translate(dist,getattr(player1,x).pos[0],getattr(player1,x).pos[1],row,column)
                key = "p1_" + x
                pieces[key] = [row,column]
                getattr(player1,x).pos = [row,column]

        return True
    else:
        for x in movers:
            check = False
            while check == False:
                row = input("Input desired row for the " + x + " : ")
                column = int(input("Input desired column for the " + x + " : "))
                dist = calcDistance(ord(getattr(player2,x).pos[0])-64,getattr(player2,x).pos[1],ord(row)-64,column)

                if dist > 1:
                    print("This movement exceeds the 2 tile limit, please enter a different tile\n")

                check = True
                translate(dist,getattr(player2,x).pos[0],getattr(player2,x).pos[1],row,column)
                key = "p2_" + x
                pieces[key] = [row,column]
                getattr(player2,x).pos = [row,column]

        return True

def translate(dist,oldRow, oldCol,newRow,newCol):
  #  print("Unit moved from ", oldRow, oldCol," to ", newRow, newCol, "tiles traveled was ", dist)
    orgCheck = ((oldRow == "A" and oldCol == 1) == False)
    orgCheck2 = ((oldRow == "D" and oldCol == 6) == False)

    if (orgCheck and orgCheck2):
        decrease_unit(oldRow,oldCol)

    orgCheck = ((newRow == "A" and newCol == 1) == False)
    orgCheck2 = ((newRow == "D" and newCol == 6) == False)
    if (orgCheck and orgCheck2):
        increase_unit(newRow,newCol)

def jam(turn):
    global p1_jam
    global p2_jam
    if turn == 1:
        roll = random.randrange(0,7)
        if roll <= 4:
            p1_jam = 1
            print("feedback:The Blue Player rolled a", roll, "so the jammer is activated!:")
        else:
            print("feedback:The Blue Player rolled a", roll, "so the jammer was not activated.:")

    else:
        roll = random.randrange(0,7)
        if roll <= 4:
            p2_jam = 1
            print("feedback:The Red Player rolled a", roll, "so the jammer is activated!:")
        else:
            print("feedback:The Red Player rolled a", roll, "so the jammer was not activated.:")

def check_fuel():
    p1_stuff = list(pieces.keys())[0:6]
    p2_stuff = list(pieces.keys())[6:]
    p1_des = 0
    p2_des = 0

    for x in p1_stuff:
        if getattr(player1,x[3:]).pos == [0,0]:
            continue
        temp = getattr(player1,x[3:]).pos
        fr = getattr(player1,x[3:]).range
        homeDist = calcDistance(ord(temp[0])-64,temp[1],1,1)
        tankDist = 10

        if player1.tanker.pos != [0,0] and player1.tanker.pos != ["E",1]:
            tankDist = calcDistance(ord(temp[0])-64,temp[1],ord(player1.tanker.pos[0])-64,player1.tanker.pos[1])

        if homeDist > fr and tankDist > fr:
            decrease_unit(getattr(player1,x[3:]).pos[0],getattr(player1,x[3:]).pos[1])
            increase_unit("E",1)
            pieces[x] = ["E",1]
            getattr(player1,x[3:]).pos = ["E",1]
            p1_des +=1
            print("feedback:", x, " is out of its fuel range!:")


    for x in p2_stuff:
        if getattr(player2,x[3:]).pos == [0,0]:
            continue
        temp = getattr(player2,x[3:]).pos
        fr = getattr(player2,x[3:]).range
        homeDist = calcDistance(ord(temp[0])-64,temp[1],4,6)
        tankDist = 10

        if player2.tanker.pos != [0,0] and player2.tanker.pos != ["E",5]:
            tankDist = calcDistance(ord(temp[0])-64,temp[1],ord(player2.tanker.pos[0])-64,player2.tanker.pos[1])

        if homeDist > fr and tankDist > fr:
            decrease_unit(getattr(player2,x[3:]).pos[0],getattr(player2,x[3:]).pos[1])
            increase_unit("E",5)
            pieces[x] = ["E",5]
            getattr(player2,x[3:]).pos = ["E",5]
            p2_des +=1
            print("feedback:", x, " is out of its fuel range!:")
    return (p1_des,p2_des)

def evade(turn, unitPos):
    if turn == 2:
        temp = unitPos
        avail = []
        for x in tiles:
            if x[0] != temp[0] or x[1] != temp[1]:
                dist = calcDistance(ord(temp[0])-64,temp[1],ord(x[0])-64,x[1])
                # print("Tile is ",x, " dist is ",dist)
                if dist == 1:
                    avail.append(x)
        # print(avail)
        for x in avail:
            temp = [x[0],x[1]]
            if player2.fighter1.pos == temp or player2.fighter2.pos == temp or player2.bomber.pos == temp:
                avail.remove(x)
        # print(avail)
        return avail
    else:
        temp = unitPos
        avail = []
        for x in tiles:
            if x[0] != temp[0] or x[1] != temp[1]:
                dist = calcDistance(ord(temp[0])-64,temp[1],ord(x[0])-64,x[1])
                if dist == 1:
                    avail.append(x)
        # print(avail)
        for x in avail:
            temp = [x[0],x[1]]
            if player1.fighter1.pos == temp or player1.fighter2.pos == temp or player1.bomber.pos == temp:
                avail.remove(x)
        return avail
        # print(avail)

def detect_combat(turn):
    p1_stuff = list(pieces.keys())[0:6]
    p2_stuff = list(pieces.keys())[6:]

    p1_all = [x[3:] for x in p1_stuff]
    p1_atk = [p1_all[1],p1_all[4],p1_all[5]]

    p2_all = [x[3:] for x in p2_stuff]
    p2_atk = [p2_all[1],p2_all[4],p2_all[5]]

    p1_targs = []
    p2_targs = []

    for i in p1_atk:
        pos = getattr(player1,i).pos
        if pos != [0,0] and pos != ["E",1]:
            ran = getattr(player1,i).combat_range
            targs = [i]

            for j in p2_all:
                spot = getattr(player2,j).pos

                if spot != [0,0] and spot != ["E",5]:
                    dist = calcDistance(ord(pos[0]) - 64, pos[1], ord(spot[0]) - 64, spot[1])

                    if dist <= ran:
                        targs.append(j)
            if calcDistance(4,6,ord(pos[0])-64,pos[1]) <= ran:
                targs.append("carrier")
            p1_targs.append(targs)

    for i in p2_atk:
        pos = getattr(player2,i).pos
        if pos != [0,0] and pos != ["E",5]:
            ran = getattr(player2,i).combat_range
            targs = [i]

            for j in p1_all:
                spot = getattr(player1,j).pos

                if spot != [0,0] and spot != ["E",1]:
                    dist = calcDistance(ord(pos[0]) - 64, pos[1], ord(spot[0]) - 64, spot[1])

                    if dist <= ran:
                        targs.append(j)
            if calcDistance(1,1,ord(pos[0])-64,pos[1]) <= ran:
                targs.append("carrier")

            p2_targs.append(targs)

    return resolve(turn,[p1_targs,p2_targs])
    # return[p1_targs,p2_targs]

def resolve(turn,battles):
    battles[0]
    battles[1]
    p1_bats = []
    p2_bats = []

    done = 0
    round = 0
    while done == 0:
        if turn == 1:
            round +=1
            if len(battles[0]) > 0:
                for i,x in enumerate(battles[0]):
                    #print("Targets for p1's ", x[0] , "are ", end="")
                    for j,z in enumerate(x):
                        if j != 0 and j != len(x)-1:
                           # print(z,end=", ")
                            ui = 1
                        elif j!= 0 and j == len(x)-1:
                           # print(z,end="")
                            if len(x) > 1:
                                check = 0
                                while check == 0:
                                    tar = input("combat:P," + str(turn) + "|" + x[0] + "\n")
                                    if tar in x:
                                        bat = [x[0],tar]
                                        p1_bats.append(bat)
                                        check = 1
                                    else:
                                        print(tar,"invalid unit, try again\n")
        else:
            round +=1
            if len(battles[1]) > 0:
                for i,x in enumerate(battles[1]):
                  #  print("Targets for p2's ", x[0] , "are ", end=" ")
                    for j,z in enumerate(x):
                        if j != 0 and j != len(x)-1:
                           # print(z,end=", ")
                            ui = 1
                        elif j!= 0 and j == len(x)-1:
                            # print(z,end="")
                            # print('\n')
                            ui = 1

                            if len(x) > 1:
                                check = 0
                                while check == 0:
                                    tar = input("combat:P," + str(turn) + "|" + x[0] + "\n")
                                    if tar in x:
                                        bat = [x[0],tar]
                                        p2_bats.append(bat)
                                        check = 1
                                    else:
                                        print("invalid unit, try again\n")

        if turn == 1:
            turn = 2
        else:
            turn = 1

        if round == 2:
            done = 1


    bats = [p1_bats,p2_bats]
    # print(bats)
    return fight(turn,bats)

def fight(turn,battles):
    p1_dead = []
    p2_dead = []

    done = 0
    round = 0
    while done == 0:
        if turn == 1:
            round+=1
            for x in battles[0]:
                escape = 0
                avail = evade(turn,getattr(player2,x[1]).pos)
                if len(avail) != 0:
                    dod = True
                    ans = input("dodge:"+str(2))
                    if ans == "no":
                        dod = False
                    if dod:
                        check = 0
                        while check == 0:
                            weave = input("evade:"+str(2))
                            weave = weave.split(",")
                            dodgeRow = weave[0]
                            dodgeCol = int(weave[1])
                            if [dodgeRow,dodgeCol] in avail:
                                check = 1
                                roll = random.randrange(1,7)
                                if roll == 1:
                                    print("feedback:Player 2 rolled a", roll, "so they can attempt to evade!:")
                                    key = "p2_" + x[1]
                                    pieces[key] = [dodgeRow,dodgeCol]

                                    decrease_unit(getattr(player2,x[1]).pos[0],getattr(player2,x[1]).pos[1])
                                    getattr(player2,x[1]).pos = [dodgeRow,dodgeCol]
                                    increase_unit(getattr(player2,x[1]).pos[0],getattr(player2,x[1]).pos[1])

                                    escape = 1
                                else:
                                    print("feedback:Player 2 rolled a", roll, " and needed a 1 so they cannot evade.:")

                if escape != 1:
                    roll = random.randrange(1,7)
                    nerf = 0
                    buff = 0
                    if getattr(player1,x[0]).pos == player2.jammer.pos and p2_jam == 1:
                        nerf = 2
                        # successful atk
                    if x[1] == "carrier" and x[0] == "bomber":
                        buff = 4
                    print("feedback:player1's",x[0]," rolled a ",roll, " and needed below or equal to a", getattr(player1,x[0]).combat_val - nerf+buff, ':')
                    if roll <= getattr(player1,x[0]).combat_val - nerf + buff:
                        if x[1] != "carrier":
                            decrease_unit(getattr(player2,x[1]).pos[0],getattr(player2,x[1]).pos[1])
                            increase_unit("E",5)

                            key = "p2_" + x[1]
                            pieces[key] = ["E",5]
                        else:
                            player2.health -= 1

        else:
            round+=1
            for x in battles[1]:
                escape = 0
                avail = evade(turn,getattr(player1,x[1]).pos)
                if len(avail) != 0:
                    dod = True
                    ans = input("dodge:"+str(1))
                    if ans == "no":
                        dod = False
                    if dod:
                        check = 0
                        while check == 0:
                            weave = input("evade:"+str(1))
                            weave = weave.split(",")
                            dodgeRow = weave[0]
                            dodgeCol = int(weave[1])
                            if [dodgeRow,dodgeCol] in avail:
                                check = 1
                                roll = random.randrange(1,7)
                                if roll == 1:
                                    print("feedback:Player 1 rolled a", roll, "so they can attempt to evade!:")
                                    key = "p1_" + x[1]
                                    pieces[key] = [dodgeRow,dodgeCol]

                                    decrease_unit(getattr(player1,x[1]).pos[0],getattr(player1,x[1]).pos[1])
                                    getattr(player1,x[1]).pos = [dodgeRow,dodgeCol]
                                    increase_unit(getattr(player1,x[1]).pos[0],getattr(player1,x[1]).pos[1])

                                    escape = 1
                                else:
                                    print("feedback:Player 1 rolled a", roll, "and needed a 1 so they cannot evade.:")
                            else:
                                print("feedback:Player 1 attempted to move to an invalid tile for evasion.:")

                if escape != 1:
                    roll = random.randrange(1,7)
                    nerf = 0
                    buff = 0
                    if getattr(player2,x[0]).pos == player1.jammer.pos and p1_jam == 1:
                        nerf = 2
                        # successful atk roll
                    if x[1] == "carrier" and x[0] == "bomber":
                        buff = 4
                    print("feedback:player2's",x[0]," rolled a ",roll, " and needed below or equal to a", getattr(player1,x[0]).combat_val - nerf+buff,':')
                    if roll <= getattr(player1,x[0]).combat_val - nerf + buff:
                        if x[1] != "carrier":
                            decrease_unit(getattr(player1,x[1]).pos[0],getattr(player1,x[1]).pos[1])
                            increase_unit("E",1)

                            key = "p1_" + x[1]
                            pieces[key] = ["E",1]
                        else:
                            player1.health -= 1

        if turn == 1:
            turn = 2
        else:
            turn = 1

        if round == 2:
            done = 1

    for x in p1_dead:
        key = "p1_" + x
        pieces[key] = ["E",1]
        decrease_unit(getattr(player1,x).pos[0],getattr(player1,x).pos[1])
        getattr(player1,x).pos = ["E",1]
        increase_unit(getattr(player1,x).pos[0],getattr(player1,x).pos[1])

    for x in p2_dead:
        key = "p2_" + x
        pieces[key] = ["E",5]
        decrease_unit(getattr(player2,x).pos[0],getattr(player2,x).pos[1])
        getattr(player2,x).pos = ["E",5]
        increase_unit(getattr(player2,x).pos[0],getattr(player2,x).pos[1])

    return [len(p1_dead),len(p2_dead)]


board = [r1, r2, r3, r4, r5]
format = [e1, e2, e3, e4, e5]

player1 = player("1",1)
player2 = player("2",6)

# print("Showing Board Format\nNOTE: Row E houses the two special tiles")
# showFormat(format)

# print("Converting to Game Demo Mode....")
# print("NOTE: Player 1 will be respesented with an A\n Player 2 will be represented with a B")
#printBoard(board)

gameState = 1
turn = 0
round = 1
oneUnits = 0
twoUnits = 0
orders = ""
command = ""
# print("You can now generate moveable units! Their names are tanker, comms, fighter1, fighter2,jammer, and bomber!\nThe Players themselves can not move\n")

check = 0
while check == 0:
    roll1 = random.randrange(1,7)
    roll2 = random.randrange(1,7)
    if roll1 != roll2:
        check = 1
        if roll1 < roll2:
            turn = 2
        else:
            turn = 1

while gameState == 1:
    # added to tell server start of turn
    # print("start of turn")

    temp = 0
    if turn == 1:
        temp = oneUnits
    else:
        temp = twoUnits

    possible = ["A", "B", "C", "D"]


    # print("Player",turn,"currently has",temp, "units in the field","\nCommands are as follows.\ngen - make a unit\nmove - move unit\nquit - end demo\nshow - display board format\nhelp - display commands\n")
    if round == 1:
        orders = input()
        orders = orders.split("?")
        directive = orders[0].split(",")
        if int(directive[0]) != turn:
            temp = orders[0]
            orders[0] = orders[1]
            orders[1] = temp
            command = orders[0].split(",")
            command.pop(0)
          #  print(command[0])
        else:
            directive.pop(0)
            command = directive
    else:
        command = orders[1].split(",")
        command.pop(0)
      #  print(command[0])


    if command == "help":
      #  print("gen - make a unit\nmove - move unit\nquit - end demo\nshow - display board format\nhelp - display commands\n")
        continue

    elif command == "quit":
        gameState = 0
        continue

    elif command == "show":
        showFormat(format)
        continue

    elif command[0] == "gen":
        name = command[1]
        row = command[2]
        column = int(command[3])
     #   print(name,row,column)
      #  print(getattr(player1,name).pos)
        if turn == 1:
            confirm = genUnit(turn,getattr(player1,name).pos,row,column)
            if confirm:
                key = "p1_" + name
                pieces[key] = [row,column]
                getattr(player1,name).pos = [row,column]
                oneUnits +=1
              #  print("made a unit")
            else:
                print("failed to gen player1\n")
               # printBoard(board)
                continue
        else:
            confirm = genUnit(turn,getattr(player2,name).pos,row,column)
            if confirm:
                key = "p2_" + name
                pieces[key] = [row,column]
                getattr(player2,name).pos = [row,column]
                twoUnits +=1
            else:
                print("failed to gen player2\n")
              #  printBoard(board)
                continue

    elif command[0] == "move":
        name = command[1]
        row = command[2]
        column = int(command[3])

        if turn == 1:
            confirm = move(getattr(player1,name).pos,row,column)
            if confirm:
                key = "p1_" + name
                pieces[key] = [row,column]
                getattr(player1,name).pos = [row,column]
            else:
              #  printBoard(board)
                continue
        else:
            confirm = move(getattr(player2,name).pos,row,column)
            if confirm:
                key = "p2_" + name
                pieces[key] = [row,column]
                getattr(player2,name).pos = [row,column]
            else:
              #  printBoard(board)
                continue

    elif command[0] == "regen":
        name = command[1]
        row = command[2]
        column = int(command[3])

        if turn == 1:
            confirm = regen(getattr(player1,name).pos,row,int(column))
            if confirm:
                key = "p1_" + name
                pieces[key] = [row,column]
                getattr(player1,name).pos = [row,int(column)]
                oneUnits +=1
                decrease_unit("E",1)
            else:
             #   printBoard(board)
                continue
        else:
            confirm = regen(getattr(player2,name).pos,row,int(column))
            if confirm:
                key = "p2_" + name
                pieces[key] = [row,column]
                getattr(player2,name).pos = [row,int(column)]
                oneUnits +=1
                decrease_unit("E",5)
            else:
              #  printBoard(board)
                continue

    elif command[0] == "relocate":
        if turn == 1:
            if player1.comms.pos == [0,0] or player1.comms.pos == ["E",1]:
                print("Unable to relocate any units because the comms aircraft has not been deployed or is destroyed\n")
                continue
        else:
            if player2.comms.pos == [0,0] or player2.comms.pos == ["E",5]:
                print("Unable to relocate any units because the comms aircraft has not been deployed or is destroyed\n")
                continue

        names = command[1].split("|")
        units = []

        if len(names) < 6:
            units.append(names[0] + ","+names[1]+","+names[2])
        else:
            units.append(names[0] + ","+names[1]+","+names[2])
            units.append(names[3] + ","+names[4]+","+names[5])


        if turn == 1:
            for x in units:
                x = x.split(",")
                pos = getattr(player1,x[0]).pos
                row = x[1]
                column = int(x[2])
                mover = player1.comms.pos
                if pos != [0,0]:
                    if calcDistance(ord(pos[0])-64,pos[1], ord(mover[0])-64,mover[1]) <= 1:
                        confirm = move(pos,row,column)
                        if confirm:
                            key = "p1_" + x[0]
                            pieces[key] = [row,column]
                            getattr(player1,name).pos = [row,column]
                        else:
                            # printBoard(board)
                            continue
        else:
            for x in units:
                x = x.split(",")
                pos = getattr(player2,x[0]).pos
                row = x[1]
                column = int(x[2])
                mover = player2.comms.pos
                if pos != [0,0]:
                    if calcDistance(ord(pos[0])-64,pos[1], ord(mover[0])-64,mover[1]) <= 1:
                        confirm = move(pos,row,column)
                        if confirm:
                            key = "p2_" + x[0]
                            pieces[key] = [row,column]
                            getattr(player2,name).pos = [row,column]
                        else:
                            # printBoard(board)
                            continue

    elif command[0] == "jam":
        jam(turn)
    elif command[0] == "stall":
        pass
    elif command[0] == "p":
       # print(pieces)
        continue
    else:
        print("Invalid Command...Returning to start of turn\n")
        # printBoard(board)
        continue


    # printBoard(board)

    if turn == 1:
        turn = 2
    else:
        turn = 1

    if round == 1:
        round = 2
    else:
        round = 1
        des = check_fuel()
        oneUnits -= des[0]
        twoUnits -= des[1]

        x = pieces.keys()

        k = "end:"
        for n,i in enumerate(x):
            temp = pieces.get(i)
            if type(temp[0]) == "str":
                row = temp[0]
            else:
                row = str(temp[0])
            col = str(temp[1])
            p = i[:2]
            u = i[3:]
            if n!= len(x)-1:
                k+=p+","+u+","+row+","+col+"|"
            else:
                k+=p+","+u+","+row+","+col
        print(k+'\n')


        dead = detect_combat(turn)
        oneUnits -= dead[0]
        twoUnits -= dead[1]
        # print()
        # printBoard(board)
        check = 0
        while check == 0:
            roll1 = random.randrange(1,7)
            roll2 = random.randrange(1,7)
            if roll1 != roll2:
                check = 1
                if roll1 < roll2:
                    turn = 2
                else:
                    turn = 1

        x = pieces.keys()

        k = "end:"
        for n,i in enumerate(x):
            temp = pieces.get(i)
            if type(temp[0]) == "str":
                row = temp[0]
            else:
                row = str(temp[0])
            col = str(temp[1])
            p = i[:2]
            u = i[3:]
            if n!= len(x)-1:
                k+=p+","+u+","+row+","+col+"|"
            else:
                k+=p+","+u+","+row+","+col
        print(k+'\n')

        if player1.health == 0 and player2.health != 0:
            gameState = 0
            print("victor:2\n")
        elif player1.health != 0 and player2.health == 0:
            gameState = 0
            print("victor:1\n")
        elif player1.health == 0 and player2.health == 0:
            gameState = 0
            print("victor:3\n")
