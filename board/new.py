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

tiles = [("A",1),("A",2),("A",3),("A",4),("A",5),("A",6),("B",1),("B",2),("B",3),("B",4),("B",5),("B",6),("C",1),("C",2),("C",3),("C",4),("C",5),("C",6),("D",1),("D",2),("D",3),("D",4),("D",5),("D",6)]
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

        self.tanker = aircraft("tanker", [0,0], int(name), 0, 0, 100)
        self.bomber = aircraft("bomber", [0,0], int(name), 1, 2, 100)
        self.jammer = aircraft("jammer", [0,0], int(name), 0, 0, 2)
        self.comms = aircraft("comms", [0,0], int(name), 0, 3, 100)
        self.fighter1 = aircraft("fighter", [0,0], int(name), 3, 1, 2)
        self.fighter2 = aircraft("fighter", [0,0], int(name), 3, 1, 2)


def genUnit(pos, row, column):
    temp = [row,column]
    if pos != [0,0]:
        return False
    if (temp != ["A",1] and temp != ["A",2] and temp != ["B",1] and temp != ["D",6] and temp != ["D",5] and temp != ["C",6]):
        return False

    # Adjusts Numbers on board
    orgCheck = ((row == "A" and column == 1) == False)
    orgCheck2 = ((row == "D" and column == 6) == False)
    if orgCheck and orgCheck2:
        increase_unit(row,column)
    else:
        print("Unit is on the same tile as the Carrier, however, the symbol will not change. \n")

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

def checkmove(unit, row, column):
    global r1
    global r2
    global r3
    global r4
    global r5
    global movements

    distance = calcDistance(ord(unit[0]) - 64, unit[1], (ord(row) - 64),column)
    if distance == 1:
        translate(distance, unit[0],unit[1],row, column)
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
        print(pos," error is in pos")
        return False
    if (temp != ["A",1] and temp != ["A",2] and temp != ["B",1] and temp != ["D",6] and temp != ["D",5] and temp != ["C",6]):
        print(temp,"error is in destination")
        return False

    reg = random.randrange(1,7)
    if reg > 5:
        print("Unit Failed to be regenerated")
        return False

    # Adjusts Numbers on board
    orgCheck = ((row == "A" and column == 1) == False)
    orgCheck2 = ((row == "D" and column == 6) == False)
    if orgCheck and orgCheck2:
        increase_unit(row,column)
    else:
        print("Unit is on the same tile as the Carrier, however, the symbol will not change. \n")

    print("here")
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

                if dist > 2:
                    print("This movement exceeds the 2 tile limit, please enter a different tile")
                    continue

                print("here")
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

                if dist > 2:
                    print("This movement exceeds the 2 tile limit, please enter a different tile")

                check = True
                translate(dist,getattr(player2,x).pos[0],getattr(player2,x).pos[1],row,column)
                key = "p2_" + x
                pieces[key] = [row,column]
                getattr(player2,x).pos = [row,column]

        return True

def translate(dist,oldRow, oldCol,newRow,newCol):
    print("Unit moved from ", oldRow, oldCol," to ", newRow, newCol, "tiles traveled was ", dist)
    orgCheck = ((oldRow == "A" and oldCol == 1) == False)
    orgCheck2 = ((oldRow == "D" and oldCol == 6) == False)

    if (orgCheck and orgCheck2):
        decrease_unit(oldRow,oldCol)

    orgCheck = ((newRow == "A" and newCol == 1) == False)
    orgCheck2 = ((newRow == "D" and newCol == 6) == False)
    if (orgCheck and orgCheck2):
        increase_unit(newRow,newCol)

def jam(turn):
    if turn == 1:
        roll = random.randrange(0,7)
        if roll <= 4:
            p1_jam = 1

    else:
        roll = random.randrange(0,7)
        if roll <= 4:
            p2_jam = 1

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
            pieces[x] = [5,1]
            getattr(player1,x[3:]).pos = ["E",1]
            p1_des +=1
            print(x, " is out of its fuel range!")


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
            pieces[x] = [5,5]
            getattr(player2,x[3:]).pos = ["E",5]
            p2_des +=1
            print(x, " is out of its fuel range!")
    return (p1_des,p2_des)

def evade(turn, unit):
    if turn == 1:
        temp = getattr(player1,unit).pos
        avail = []
        for x in tiles:
            if x[0] != temp[0] or x[1] != temp[1]:
                dist = calcDistance(ord(temp[0])-64,temp[1],ord(x[0])-64,x[1])
                print("Tile is ",x, " dist is ",dist)
                if dist == 1:
                    avail.append(x)
        # print(avail)
        for x in avail:
            temp = [x[0],x[1]]
            if player2.fighter1.pos == temp or player2.fighter2.pos == temp or player2.bomber.pos == temp:
                avail.remove(x)
        # print(avail)
    else:
        temp = getattr(player2,unit).pos
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
        # print(avail)

def detect_combat():
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
            p2_targs.append(targs)


    return [p1_targs,p2_targs]


board = [r1, r2, r3, r4, r5]
format = [e1, e2, e3, e4, e5]

player1 = player("1",1)
player2 = player("2",6)

print("Showing Board Format\nNOTE: Row E houses the two special tiles")
showFormat(format)

print("Converting to Game Demo Mode....")
print("NOTE: Player 1 will be respesented with an A\n Player 2 will be represented with a B")
printBoard(board)

gameState = 1
turn = 1
oneUnits = 0
twoUnits = 0
print("You can now generate moveable units! Their names are tanker, comms, fighter1, fighter2,jammer, and bomber!\nThe Players themselves can not move\n")

while gameState == 1:
    possible = ["A", "B", "C", "D"]
    if turn ==1:
        temp = oneUnits
    else:
        temp = twoUnits

    print("Player",turn,"currently has",temp, "units in the field","\nCommands are as follows.\ngen - make a unit\nmove - move unit\nquit - end demo\nshow - display board format\nhelp - display commands\n")

    command = input("Please input a command: ")
    if command == "help":
        print("gen - make a unit\nmove - move unit\nquit - end demo\nshow - display board format\nhelp - display commands\n")
        continue

    elif command == "quit":
        gameState = 0
        continue

    elif command == "show":
        showFormat(format)
        continue

    elif command == "gen":
        name = input("Please give the name of the unit to generate: ")
        row = input("Input a generation row: ")
        if row == "E":
            print("invalid row.... You can only generate a unit in rows A,B,C, or D")
            printBoard(board)
            continue
        column = int(input("Input a generation column: "))
        if turn == 1:
            confirm = genUnit(getattr(player1,name).pos,row,column)
            if confirm:
                key = "p1_" + name
                pieces[key] = [row,column]
                getattr(player1,name).pos = [row,column]
                oneUnits +=1
            else:
                printBoard(board)
                continue
        else:
            confirm = genUnit(getattr(player2,name).pos,row,column)
            if confirm:
                key = "p2_" + name
                pieces[key] = [row,column]
                getattr(player2,name).pos = [row,column]
                twoUnits +=1
            else:
                printBoard(board)
                continue

    elif command == "move":
        name = input("Give the name of the unit to be moved: ")
        row = input("Input destination Row: ")

        if row == "E":
            print("invalid row.... You can only move a unit to rows A,B,C, or D")
            printBoard(board)
            continue
        column = int(input("Input a destination Column: "))

        if turn == 1:
            confirm = move(getattr(player1,name).pos,row,column)
            if confirm:
                key = "p1_" + name
                pieces[key] = [row,column]
                getattr(player1,name).pos = [row,column]
            else:
                printBoard(board)
                continue
        else:
            confirm = move(getattr(player2,name).pos,row,column)
            if confirm:
                key = "p2_" + name
                pieces[key] = [row,column]
                getattr(player2,name).pos = [row,column]
            else:
                printBoard(board)
                continue

    elif command == "attack":
        nerfed = 0
        row = input("Input Target Tile Row: ")
        if row == "E":
            print("invalid row.... You can only move a unit to rows A,B,C, or D")
            printBoard(board)
            continue
        column = input("Input Target Tile Column: ")
        print("Enemy Units on tile: " + reveal(row,int(column)))
        if turn == 1:
            name = input("Choose a target: ")
            launcher = input("Choose attacker: ")

            if p2_jam == 1 and getattr(player1,launcher).pos == p2.jammer.pos:
                nerfed = 2

            target_death = False
            launcher_death = False
            p1_atk = getattr(player1,launcher).combat_val - nerfed
            p1_roll = random.randrange(1,7)
            if p1_roll <= p1_atk:
                target_death = True
                twoUnits-=1
                decrease_unit(getattr(player2,name).pos[0],getattr(player2,name).pos[1])
                getattr(player2,name).pos = ["E",5]
                pieces["p2_"+name] = [5,5]
                increase_unit("E",5)

            p2_atk = getattr(player2,name).combat_val
            p2_roll = random.randrange(1,7)
            if p2_roll <= p2_atk:
                launcher_death = True
                oneUnits-=1
                decrease_unit(getattr(player1,launcher).pos[0],getattr(player1,launcher).pos[1])
                getattr(player1,launcher).pos = ["E",1]
                pieces["p1_"+launcher] = [5,1]
                increase_unit("E",1)

            if launcher_death and target_death:
                print("Both units were destroyed")
            elif launcher_death:
                print("Your attacking unit failed to accomplish the mission")
            elif target_death:
                print("Your attack was successful")
            elif target_death == False and launcher_death == False:
                print("Both aircraft were unsuccessful in their attacks")
        else:
            name = input("Choose a target: ")
            launcher = input("Choose attacker: ")
            if p1_jam == 1 and getattr(player2,launcher).pos == player1.jammer.pos:
                nerfed = 2
            target_death = False
            launcher_death = False
            p2_atk = getattr(player2,launcher).combat_val - nerfed
            p2_roll = random.randrange(1,7)
            if p2_roll <= p2_atk:
                target_death = True
                oneUnits-=1
                decrease_unit(getattr(player1,name).pos[0],getattr(player1,name).pos[1])
                getattr(player1,name).pos = ["E",1]
                pieces["p1_"+name] = [5,1]
                increase_unit("E",1)

            p1_atk = getattr(player1,name).combat_val
            p1_roll = random.randrange(1,7)
            if p1_roll <= p1_atk:
                launcher_death = True
                twoUnits-=1
                decrease_unit(getattr(player2,launcher).pos[0],getattr(player2,launcher).pos[1])
                getattr(player2,launcher).pos = ["E",5]
                pieces["p2_"+launcher] = [5,5]
                increase_unit("E",5)

            if launcher_death and target_death:
                print("Both units were destroyed")
            elif launcher_death:
                print("Your attacking unit failed to accomplish the mission")
            elif target_death:
                print("Your attack was successful")
            elif target_death == False and launcher_death == False:
                print("Both aircraft were unsuccessful in their attacks")

    elif command == "regen":
        name = input("Input unit to be regenerated: ")
        row = input("Input row to place unit on: ")
        column = input("Input column to place unit on: ")

        if turn == 1:
            confirm = regen(getattr(player1,name).pos,row,int(column))
            if confirm:
                key = "p1_" + name
                pieces[key] = [row,column]
                getattr(player1,name).pos = [row,int(column)]
                oneUnits +=1
                decrease_unit("E",1)
            else:
                printBoard(board)
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
                printBoard(board)
                continue

    elif command == "comms":
        if turn == 1:
            if player1.comms.pos == [0,0] or player1.comms.pos == ["E",1]:
                print("Unable to relocate any units because the comms aircraft has not been deployed or is destroyed")
                continue
        else:
            if player2.comms.pos == [0,0] or player2.comms.pos == ["E",5]:
                print("Unable to relocate any units because the comms aircraft has not been deployed or is destroyed")
                continue

        names = input("Select up to 2 active units to be moved. Separate names with a comma. ")
        names = names.split(",")

        for i in range(0,len(names)):
            names[i] = names[i].strip()
        print(names)
        check = relocate(turn,names)
        if check == False:
            continue

    elif command == "jam":
        accept = input("This action will reduce combat value of enemy units on the jammer's hex tile. Type yes to confirm")
        if accept == "yes":
            jam(turn)
        else:
            continue

    elif command == "evade":
        unit = input("unit to move: ")
        evade(turn, unit)
    elif command == "stall":
        pass
    else:
        print("Invalid Command...Returning to start of turn\n")
        printBoard(board)
        continue

    if turn == 1:
        turn = 2
    else:
        turn = 1
        des = check_fuel()
        oneUnits -= des[0]
        twoUnits -= des[1]

        targets = detect_combat()
        # print(targets[0])
        # print(targets[1])
        if len(targets[0]) > 0:
            for i,x in enumerate(targets[0]):
                print("Targets for p1's ", x[0] , "are ", end=" ")
                for j,z in enumerate(x):
                    if j != 0:
                        print(z,end=", ")
                print()

        if len(targets[1]) > 0:
            for i,x in enumerate(targets[1]):
                print("Targets for p2's ", x[0] , "are ", end=" ")
                for j,z in enumerate(x):
                    if j != 0:
                        print(z,end=", ")
                print()
        print()

    printBoard(board)
