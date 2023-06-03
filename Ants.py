#from AI import AntAI
from World import *
from math import sin
from math import radians
from math import ceil
from random import randint
from math import sqrt
from math import acos
from math import degrees
from Tech import ReturnMod
from Tech import ReturnTechLevel
# Vision???????????????????*(???)
class Ant(WorldObject):
    def __init__(self, SpawnPointX, SpawnPointY, HeadID=0, BodyID=0, BellyID=0, MyHomeID=0, SetAll = False, ID = 0, Health = 1, Energy = 1, Memory = ([-1]*MemorySize), FoodMemory = 0, MemoryAnt = -1, Inventory = 0, TargetPoint = [-1,0,0], Speed = 3, MaxHealth = 10, AttackStrenght = 1, TechLevel = 1):
        super().__init__(posx=SpawnPointX, posy=SpawnPointY)
        global SuperAntID
        global AntCount
        Modifiers = ReturnMod("All")
        LeMode = AntsHeads[HeadID][0]
        if LeMode == "Watcher": LeMode = "Scout"
        ClassModifiers = ReturnMod(LeMode)
        AntCount += 1
        #
        self.HBB = [HeadID, BodyID, BellyID]
        self.Mind = AntsHeads[HeadID][0]
        self.MaxHealth = 1 + AntsHeads[HeadID][1] +AntsBodies[BodyID][1] + AntsBellies[BellyID][1] + Modifiers["Health"]
        self.Speed = 2 + AntsBodies[BodyID][2] + AntsBellies[BellyID][3] + randint(-1, 1) + Modifiers["Speed"] + ClassModifiers["Speed"]
        self.MaxEnergy = AntsBellies[BellyID][2]
        self.EnergyNeed = AntsHeads[HeadID][5] + AntsBodies[BodyID][4]
        self.AttackStrenght = AntsHeads[HeadID][2] + Modifiers["Strenght"] + ClassModifiers["Strenght"]
        self.AttackRange = AntsHeads[HeadID][3]
        self.WorkEfficiency = AntsHeads[HeadID][6] + ReturnMod(LeMode, "WorkEfficiency")
        self.Health = self.MaxHealth + Modifiers["Health"] + ClassModifiers["Health"]
        self.Energy = self.MaxEnergy
        #
        self.ID = SuperAntID
        self.side = 111
        if self.Mind == "Solder":
            self.side += 100
        if self.Mind == "Watcher":
            self.side += 200
        self.HomeID = MyHomeID
        self.IsAlive = True
        self.HasBeenAttacked = False
        self.HasBeenAttackedByID = -1
        self.ObjType = "ant"
        self.AngleRand = randint(0, 360)
        self.Angle = self.AngleRand
        self.State = "InHome" # InHome
        self.Memory = [-1] * MemorySize
        self.FoodMemory = 0
        self.MemoryAnt = -1
        self.Inventory = 0
        self.TargetPoint = [-1, 0, 0]
        self.IDKWhereToGo = IDK[randint(0,1)]
        self.DefendPoint = [0, 0, 0]
        self.TechLevel = TechLevel
        if SetAll:
            self.Health = Health
            self.Energy = Energy
            self.ID = ID
            self.Memory = Memory
            self.FoodMemory = FoodMemory
            self.MemoryAnt = MemoryAnt
            self.Inventory = Inventory
            self.TargetPoint = TargetPoint
            self.Speed = Speed
            self.MaxHealth = MaxHealth
            self.AttackStrenght = AttackStrenght
            
        self.side += (self.TechLevel - 1) * 1000
        self.BlockMapID = GetBlockMapID(self.posx, self.posy)
        AddAntToBlock(self.ID, self.BlockMapID[0], self.BlockMapID[1])
        UpdateAntsCount(AntsHeads[HeadID][0], 1)
            

    '''def OldMove(self, Direction, Speed):
        if(Direction == 1):
            self.posy += Speed
            LastID = self.BlockMapID
            self.BlockMapID = BlockMapGetID(self.posx, self.posy)
            if self.BlockMapID != LastID:
                DeleteAntFromBlock(self.ID, LastID)
                AddAntToBlock(self.ID, self.BlockMapID)
            
        if(Direction == 2):
            self.posx += Speed
            LastID = self.BlockMapID
            self.BlockMapID = BlockMapGetID(self.posx, self.posy)
            if self.BlockMapID != LastID:
                DeleteAntFromBlock(self.ID, LastID)
                AddAntToBlock(self.ID, self.BlockMapID)
            
        if(Direction == 3):
            self.posy -= Speed
            LastID = self.BlockMapID
            self.BlockMapID = BlockMapGetID(self.posx, self.posy)
            if self.BlockMapID != LastID:
                DeleteAntFromBlock(self.ID, LastID)
                AddAntToBlock(self.ID, self.BlockMapID)
            
        if(Direction == 4):
            self.posx -= Speed
            LastID = self.BlockMapID
            self.BlockMapID = BlockMapGetID(self.posx, self.posy)
            if self.BlockMapID != LastID:
                DeleteAntFromBlock(self.ID, LastID)
                AddAntToBlock(self.ID, self.BlockMapID)'''
    # ^ STOOPID

    def Move(self, Angle, Distance=10):
        global SizeOfTheBlock
        global SizeOfTheWorld
        ##print(f"MOVE: Angle = {Angle}")
        MoveLeft = 0
        while Angle < 0:
            Angle += 360
        while Angle > 360:
            Angle -= 360
        if Distance > self.Speed:
            ##print(f"Distance is more than speed, so: {Distance} >> {self.Speed}")
            Distance = self.Speed
        else: 
            MoveLeft = self.Speed - Distance
        self.Angle = Angle
        #if self.State == "NeedFood":
        #    ###print(f"Actor {self.ID} at pos [{self.posx}, {self.posy}]moving at {Distance} and {Angle}")
        
        if (Angle <= 90):
            SecAngle = 90 - Angle
            ##print("MOVE: Angle1")
            ymove = round(Distance * sin(radians(SecAngle)),2) #vertical move
            xmove = round(Distance * sin(radians(Angle)),2) #horizontal move
        if (Angle <= 180 and Angle > 90):
            SecAngle = 180 - Angle
            ##print("MOVE: Angle2")
            ymove = -round(Distance * sin(radians(Angle-90)),2) #vertical move
            xmove = round(Distance * sin(radians(SecAngle)),2) #horizontal move
        if (Angle <= 270 and Angle > 180):
            SecAngle = 270 - Angle
            ##print("MOVE: Angle3")
            ymove = -round(Distance * sin(radians(SecAngle)),2) #vertical move
            xmove = -round(Distance * sin(radians(Angle-180)),2) #horizontal move
        if (Angle > 270):
            SecAngle = 360 - Angle
            ##print("MOVE: Angle4")
            ymove = round(Distance * sin(radians(Angle-270)),2) #vertical move
            xmove = -round(Distance * sin(radians(SecAngle)),2) #horizontal move
        #Перемещение из одного блока в другой
        ##print(f"Deleting {self.ID} from:")
        ##print(self.BlockMapID)
        DeleteAntFromBlock(self.ID, self.BlockMapID[0], self.BlockMapID[1])
        self.posx += xmove
        self.posy += ymove
        self.BlockMapID.clear()
        
        self.BlockMapID = GetBlockMapID(self.posx, self.posy)
        ##print("Adding to:")
        ##print(self.BlockMapID)
        AddAntToBlock(self.ID, self.BlockMapID[0], self.BlockMapID[1])
        if Angle > 340 or Angle <= 20:
            self.side = 110#"up"
        elif Angle > 20 and Angle <= 70:
            self.side = 112#"upright"
        elif Angle > 70 and Angle <= 110:
            self.side = 102#"right"
        elif Angle > 110 and Angle <= 160:
            self.side = 122#"downright"
        elif Angle > 160 and Angle <= 200:
            self.side = 120#"down"
        elif Angle > 200 and Angle <= 250:
            self.side = 121#"downleft"
        elif Angle > 250 and Angle <= 290:
            self.side = 101#"left"
        elif Angle > 290 and Angle <= 340:
            self.side = 111#"upleft"
        ##print(f"Ant was moved. Distance = {Distance}, x = {xmove}, y = {ymove}")
        ##print(f"MOVE: 165. Ant moved  [x:{self.posx},y:{self.posy}] + [x:{xmove},y:{ymove}]")
        ##print(f"MOVE: 166. Angle was {Angle} >> {SecAngle}\n Side = {self.side}")
        ##print(f"MOVE: 167. Distance = {Distance}\n\n")
        ##print(f"Ant in {self.BlockMapID}")
        if self.Mind == "Solder":
            self.side += 100
        if self.Mind == "Watcher":
            self.side += 200
        self.side += ((self.TechLevel - 1) * 1000)
        return MoveLeft
        
    def Attack(self, TargetID): # Do damage to target and add your id to HasBeenAttackedByID
        DoDamage(self.ID, TargetID, "bug", self.AttackStrenght, True)
        if self.Mind == "Solder":
            self.Energy += 50
    
    def TakeDamage(self, damage, FromEnemy=False, EnemyID=-1):
        self.HasBeenAttacked = FromEnemy
        self.HasBeenAttackedByID = EnemyID
        self.Health -= damage
        if (self.Health < 0):
            self.IsAlive = False 
            DeleteAntPls(self.ObjType, self.ID)
            ###print(f"Ant {self.ID} is dead! So sad.")

    def EatFood(self):
        global FoodToEnergy
        ###print("pls tell me that he is eating")
        FoodNeed = (self.MaxEnergy - self.Energy) // FoodToEnergy
        self.Energy += AntEatsFood(self.HomeID, FoodNeed) * FoodToEnergy
        ###print(FoodNeed)
        ###print(self.Energy)
        
    def PutFoodHome(self):
        ###print(f"Ant gonna leave some food {self.Inventory} in home\n!!!")
        AntLeavesFood(self.HomeID, self.Inventory)
        self.Inventory = 0
        
    def TakeFood(self, FPID, Amount = 8):
        ###print(f"Taking food! We({self.ID}) have {self.Inventory} of food")
        LeFood = AntTakesFood(FPID, self.WorkEfficiency)
        self.Inventory += LeFood
        ###print(f"Taking food! We add {LeFood} to Inventory\n")
        if LeFood == 0: # Еда кончилась
            return 0
        if self.Inventory >= Amount: # Еды полный инвентарь
            return 1
        return -1 # Еды ещё не полный инвентарь

    def Enrg(self):
        self.Energy -= self.EnergyNeed
        if self.Energy < 0:
            self.TakeDamage(1)
            
    def GoWayPoint(self, NewWPID):
        ##print(self.Memory.pop(0))
        self.Memory.append(NewWPID)
        ##print(f" ^WP passed, NewWP is {NewWPID}")
        pass
        
    def MemoryClear(self):
        self.Memory.clear()
        self.Memory = [-1] * MemorySize
        
    def CreateWP(self, Weight, Final = False):
        CreateWayPoint(self.posx, self.posy, Weight, Final)
        
    def AddToWP(self, WPID, Weight = 1):
        AddToWayPoint(WPID, Weight)
        
    def ClearWP(self, WPID, Weight = 2):
        ClearWayPoint(WPID, Weight)

    def __del__(self):
        global AntCount
        AntCount -= 1
        DeleteAntFromBlock(self.ID, self.BlockMapID[0], self.BlockMapID[1])
        DeleteAntFromHome(self.ID, self.HomeID)
        UpdateAntsCount(self.Mind, -1)
  
class Bug(WorldObject):
    def __init__(self,SpawnX, SpawnY, SetAll = False,ID = 0, MaxHealth=25, Health=25, AttackStrenght=2, MoveSpeed=2, Mind="bug"):
        super().__init__(posx=SpawnX, posy=SpawnY)
        global SuperBugID
        self.AttackRange = 2
        self.ID = SuperBugID
        self.MaxHealth = MaxHealth
        self.Health = MaxHealth
        self.AttackStrenght = AttackStrenght
        self.MoveSpeed = MoveSpeed
        self.Mind = Mind
        self.ObjType = "bug"
        self.side = "up"
        self.Angle = 1
        self.Leader = -1
        self.RandomPoint = [randint(0, SizeOfTheWorld) * SizeOfTheBlock, randint(0, SizeOfTheWorld) * SizeOfTheBlock]
        if randint(0, 144) > 135:
            #self.Mind = "bigbug"
            self.Health=50
        self.IsAlive = True
        if SetAll:
            self.ID = ID
            self.Health = Health
        self.BlockMapID = GetBlockMapID(self.posx, self.posy)
        AddObjectToBlock(self.ID, self.ObjType,self.BlockMapID[0], self.BlockMapID[1])
            
    def Move(self, Angle, Distance=10):
        global SizeOfTheBlock
        global SizeOfTheWorld
        ##print(f"MOVE: Angle = {Angle}")
        MoveLeft = 0
        while Angle < 0:
            Angle += 360
        while Angle > 360:
            Angle -= 360
        if Distance > self.MoveSpeed:
            ##print(f"Distance is more than speed, so: {Distance} >> {self.Speed}")
            Distance = self.MoveSpeed
        else: 
            MoveLeft = self.MoveSpeed - Distance
        self.Angle = Angle
        #if self.State == "NeedFood":
        ##print(f"Actor {self.ID} at pos [{self.posx}, {self.posy}]moving at {Distance} and {Angle}")
        
        if (Angle <= 90):
            SecAngle = 90 - Angle
            ##print("MOVE: Angle1")
            ymove = round(Distance * sin(radians(SecAngle)),2) #vertical move
            xmove = round(Distance * sin(radians(Angle)),2) #horizontal move
        if (Angle <= 180 and Angle > 90):
            SecAngle = 180 - Angle
            ##print("MOVE: Angle2")
            ymove = -round(Distance * sin(radians(Angle-90)),2) #vertical move
            xmove = round(Distance * sin(radians(SecAngle)),2) #horizontal move
        if (Angle <= 270 and Angle > 180):
            SecAngle = 270 - Angle
            ##print("MOVE: Angle3")
            ymove = -round(Distance * sin(radians(SecAngle)),2) #vertical move
            xmove = -round(Distance * sin(radians(Angle-180)),2) #horizontal move
        if (Angle > 270):
            SecAngle = 360 - Angle
            ##print("MOVE: Angle4")
            ymove = round(Distance * sin(radians(Angle-270)),2) #vertical move
            xmove = -round(Distance * sin(radians(SecAngle)),2) #horizontal move
        #Перемещение из одного блока в другой
        ##print(f"Deleting {self.ID} from:")
        ##print(self.BlockMapID)
        DeleteObjectFromBlock(self.ID, self.ObjType,self.BlockMapID[0], self.BlockMapID[1])
        self.posx += xmove
        self.posy += ymove
        self.BlockMapID.clear()
        
        self.BlockMapID = GetBlockMapID(self.posx, self.posy)
        ##print("Adding to:")
        ##print(self.BlockMapID) Block
        AddObjectToBlock(self.ID, self.ObjType, self.BlockMapID[0], self.BlockMapID[1])
        if Angle > 315 or Angle <= 45:
            self.side = "down"
        elif Angle > 45 and Angle <= 135:
            self.side = "right"
        elif Angle > 135 and Angle <= 225:
            self.side = "up"
        elif Angle > 225 and Angle <= 315:
            self.side = "left"
            
        if self.Mind == "bigbug":
            self.side = "B" + self.side
        # Move taken from ants. Wow.
        # Извините, простите, наследование для кого?
        # Спасибо за ценнейший опыт как не надо делать.
        # Что может быть лучше бесполезных комментариев.
        return MoveLeft
    
    def Attack(self, TargetID):
        DoDamage(self.ID, TargetID, "ant", self.AttackStrenght, True)
        
    def TakeDamage(self, damage, FromEnemy=False,EnemyID = -1):
        self.Health -= damage
        if (self.Health < 0):
            self.IsAlive = False 
            DeleteBugPls(self.ObjType, self.ID)
    
    def NewRandomPoint(self):
        
        self.RandomPoint = [randint(0, SizeOfTheWorld) * SizeOfTheBlock, randint(0, SizeOfTheWorld) * SizeOfTheBlock]
    
    def __del__(self):
        #print(f"bug {self.ID} was deleted!")
        DeleteObjectFromBlock(self.ID, self.ObjType, self.BlockMapID[0], self.BlockMapID[1])

        
# Esli uzh proebalsya - to idi do konca, nikogda ne ostanavlivaysya!
def CreateAnt(HomeID=0, HeadID=0, BodyID=0, BellyID=0, SetAll = False, ID=0, x = 0, y = 0, Stats = [1, 1, [-1], 0, 1, 0, [-1,0,0], 1], TechLevel = 1):
    #Ant.posx, Ant.posy, Ant.HBB, Ant.HomeID, Ant.ID, [Ant.Health, Ant.Energy, Ant.Memory, Ant.FoodMemory, Ant.MemoryAnt, Ant.Inventory, Ant.TargetPoint, Ant.Speed, Ant.MaxHealth, Ant.AttackStrenght], Ant.TechLevel
    global SuperAntID
    global ListOfAnts
    if not SetAll:
        Cost = AntsHeads[HeadID][4] + AntsBodies[BodyID][3]
        if HomeFood(HomeID) >= Cost:
            xy = HomeXY(HomeID)
            ###print(xy)
            ListOfAnts.update({SuperAntID: Ant(xy[0],xy[1],HeadID,BodyID,BellyID,HomeID)})
            AddAntToHome(SuperAntID, Cost)
            SuperAntID += 1
        else:
            print("No Food?\n"+str(HomeFood(HomeID))+" food, need "+str(Cost))
            pass
    else:
        if not ID in ListOfAnts:
            ListOfAnts.update({ID: Ant(x,y,HeadID,BodyID,BellyID,HomeID, SetAll ,ID, Stats[0], Stats[1], Stats[2], Stats[3], Stats[4], Stats[5], Stats[6], Stats[7], Stats[8], Stats[9], TechLevel)})
            if ID >= SuperAntID: SuperAntID = ID + 1


def CreateBug(SetAll = False, ID=0, PosX=0, PosY=0, Health=0):
    global SuperBugID
    global ListOfEnteties
    if SetAll:
        ListOfEnteties.update({ID: Bug(PosX, PosY, SetAll, ID, 25, Health)})
        if ID >  SuperBugID: SuperBugID = ID + 1
    else:
        side = randint(0,3)
        if side == 0:
            x = 1
            y = randint(1, SizeOfTheWorld-1) * SizeOfTheBlock
        if side == 1:
            x = SizeXSize - 1
            y = randint(1, SizeOfTheWorld-1) * SizeOfTheBlock
        if side == 2:
            x = randint(1, SizeOfTheWorld-1) * SizeOfTheBlock
            y = 1
        if side == 3:
            x = randint(1, SizeOfTheWorld-1) * SizeOfTheBlock
            y = SizeXSize - 1
        ListOfEnteties.update({SuperBugID: Bug(x, y, SetAll)})
        SuperBugID += 1
        #print(SuperBugID)
    #print(ListOfEnteties)
        

    

def ForgetAboutAnt(ID):
    global ListOfAnts
    del ListOfAnts[ID]

def ForgetAboutBug(ID):
    global ListOfEnteties
    del ListOfEnteties[ID]

def THINKNOW():
    global ListOfAnts
    global ListOfEnteties
    ####print(ListOfAnts)
    for Ant in ListOfAnts:
        ####print(ListOfAnts[Ant])
        AntAI(ListOfAnts[Ant])
    for Bug in ListOfEnteties:
        BugAI(ListOfEnteties[Bug])

def BugXY(ID):
    global ListOfEnteties
    if ID in ListOfEnteties:
        return ListOfEnteties[ID].ReturnXY()
    else:
        return -1
    
def AntXY(ID):
    global ListOfAnts
    if ID in ListOfAnts:
        return ListOfAnts[ID].ReturnXY()
    else:
        return -1

def GetListOfAnts():
    global ListOfAnts
    return ListOfAnts
    
def GetListOfEnteties():
    global ListOfEnteties
    return ListOfEnteties

def AntHasBeenAttacked(ID):
    global ListOfAnts
    return [ListOfAnts[ID].HasBeenAttacked, ListOfAnts[ID].HasBeenAttackedByID]
    
def GetAntMind(ID):
    global ListOfAnts
    return ListOfAnts[ID].Mind
    
def GetAntState(ID):
    global ListOfAnts
    return ListOfAnts[ID].State

def FindNotLostAnt(BMx, BMy, ObjType="ant", Range=2, ignore=[-1]):
    ReturnThisArray = []
    # Что же, нужно просканить центр и блоки вокруг вплоть до Range
    # Range 1 - 1 блок, Range 2 - 9 блоков и т.д.
    Scan = ScanRadiusAround(BMx, BMy, ObjType, Range, ignore)
    ReturnThisArray.extend(Scan)
    for Ant in ReturnThisArray:
        if GetAntMind(Ant) == "Solder":
            return Ant
        if GetAntState(Ant) != "Lost":
            return Ant
    return -1

def AutoMove(x1, y1, x2, y2): # i really need function that can return angle and distance to target, AND DONT DO THIS MANUALLY EVERY FUCKING TIME БЛЯТЬ СУКА
    DistanceX = x2 - x1
    DistanceY = y2 - y1
    Dx = abs(DistanceX)
    Dy = abs(DistanceY)
    Hptz = sqrt(Dx*Dx + Dy*Dy)
    ##print(f"AUTOMOVE. Dx, Dy, HPTZ, DX, DY => {Dx},{Dy},{Hptz},{DistanceX},{DistanceY}")
    if Hptz == 0: return(0, 0)
    ##print(f"AUTOMOVE: Distance is {Hptz}")
    if (DistanceX >= 0): # ВПРАВО
        if (DistanceY >= 0): # ВВЕРХ
            Angle = degrees(acos(Dy/Hptz))
            ##print(f"1AUTOMOVE: Angle and distance == {Angle}, {Hptz}")
            return [Angle, Hptz]
        else: #  ВНИЗ
            Angle = degrees(acos(Dx/Hptz))
            ##print(f"2AUTOMOVE: Angle and distance == {Angle}+90, {Hptz}")
            return [Angle+90, Hptz]
    else: # ВЛЕВО
        if (DistanceY >= 0): # ВВЕРХ
            Angle = degrees(acos(Dx/Hptz))
            ##print(f"3AUTOMOVE: Angle and distance == {Angle}+270, {Hptz}")
            return [Angle+270, Hptz]
        else: # ВНИЗ
            Angle = degrees(acos(Dy/Hptz))
            ##print(f"4AUTOMOVE: Angle and distance == {Angle}+180, {Hptz}")
            return [Angle+180, Hptz]

def GetClosest(x, y, ListOfID, ObjType):
    # Оптимизировать 
    if ObjType == "ant":
        CheckList = GetListOfAnts()
    if ObjType == "food":
        CheckList = GetListOfObjects()
    if ObjType == "bug":
        CheckList = GetListOfEnteties()
    if ObjType == "way":
        CheckList = GetListOfWPs()
    # ant food bug way
    First = True
    for ObjectID in ListOfID: 
        if not ObjectID in CheckList: print(f"Something gone wrong! Cannot find {ObjectID} in {ObjType}!")
        DifferenceX = abs(x - CheckList[ObjectID].posx)
        DifferenceY = abs(y - CheckList[ObjectID].posy)
        DiffSum = DifferenceY + DifferenceX
        if First:
            First = False
            ObjID = ObjectID
            NewDiffSum = DiffSum
            ObjX = CheckList[ObjectID].posx
            ObjY = CheckList[ObjectID].posy
            continue
        if (DiffSum < NewDiffSum):
            ObjID = ObjectID
            NewDiffSum = DiffSum
            ObjX = CheckList[ObjectID].posx
            ObjY = CheckList[ObjectID].posy
    return [ObjID, ObjX, ObjY, NewDiffSum]

def DistanceCheckForAttack(X, Y, EnemyX, EnemyY, Range):
    DifferenceX = abs(X - EnemyX)
    DifferenceY = abs(Y - EnemyY)
    DiffSum = DifferenceY + DifferenceX
    if DiffSum < Range:
        return True
    return False

def GetDistance(Obj1, Obj2):
    DistanceX = Obj2.posx - Obj1.posx
    DistanceY = Obj2.posy - Obj1.posy
    Dx = abs(DistanceX)
    Dy = abs(DistanceY)
    Hptz = sqrt(Dx*Dx + Dy*Dy)
    return Hptz

def GetDistanceRaw(posx1, posy1, posx2, posy2):
    DistanceX = posx2 - posx1
    DistanceY = posy2 - posy1
    Dx = abs(DistanceX)
    Dy = abs(DistanceY)
    Hptz = sqrt(Dx*Dx + Dy*Dy)
    return Hptz

def HelpAnotherAnt(BMx, BMy):
    AntsNeedHelp = ScanRadiusAround(BMx, BMy, "ant", 3)
    for AntID in AntsNeedHelp:
        HelpAnt = AntHasBeenAttacked(AntID)
        if HelpAnt[0]:
            return [1, HelpAnt[0], HelpAnt[1]]
    return [0]


def GoHome(Actor, Rand = False):
    Homes = HomeXY(Actor.HomeID)
    HowToMove = AutoMove(Actor.posx, Actor.posy, Homes[0], Homes[1])
    if Rand:
        HowToMove[0] += randint(-10, 10)
    return HowToMove

def EatAndLeave(Actor, State):
    ###print(f"Actor {Actor.ID} is eating!")
    Actor.EatFood()
    Homes = HomeXY()
    if GetDistanceRaw(Actor.posx, Actor.posy, Homes[0], Homes[1]) > 7:
        Actor.State = State
        ###print(f"Actor {Actor.ID} is SUCSESSFULLY EAT")
    else:
        ###print(f"Actor {Actor.ID} is not leaving now {Actor.posx}, {Actor.posy}")
        Actor.Move(Actor.AngleRand, 1)
        Actor.AngleRand += randint(-5, 5)
        
def ChooseWPRandom(WPList):
    if len(WPList) == 1:
        return WPList[0]
    ###print(f"WPList = {WPList} inside")
    WeightList = []
    for WPW in WPList:
        if WPW and WPW[0] != None:
            WeightList.append(WPW[3])
        #else: ##print(WPList)
    AllWeight = sum(WeightList)
    RandWeight = randint(0, AllWeight)
    ID = 0
    # THIS IS SO STUPID WHAT THE FUCK MAN WHYYYYYYYYY??????
    # Please LEAVE CODING NOW!!!
    # Or at least use NumPy
    while RandWeight > 0:
        RandWeight -= WeightList[ID]
        ID+=1
    ID -= 1
    return WPList[ID]
    
def MoveAroundHome(Actor, GoAway = False):
    Home = HomeXY(Actor.HomeID)
    HowToMove = AutoMove(Actor.posx, Actor.posy, Home[0], Home[1])
    if GoAway:
        Actor.Move(HowToMove[0]+180, HowToMove[1])
    else:
        Actor.Move(HowToMove[0]+(60 * Actor.IDKWhereToGo), HowToMove[1])

def AntAI(Actor):
    ###print(f"Ant {Actor.ID}, {Actor.Mind} is in state {Actor.State}")
    ####print(Actor)
    MyX = Actor.posx
    MyY = Actor.posy
    if Actor.posx < 0 or Actor.posy < 0 or Actor.posx > SizeXSize or Actor.posy > SizeXSize:
        Actor.State = "NeedFood"
    # BY PRIORITY
    #ATTACK
    if Actor.Mind == "Solder" and IsAttack == True:
        Actor.State = "Attack"
    if Actor.Mind == "Solder" and IsDefend == True:
        Actor.State = "Defend"
    # Если муравей не разведчик и был атакован - 
    # Муравей получает от врага ID и атакует в ответ.
    if (Actor.HasBeenAttacked == True and (Actor.Mind == "Worker" or Actor.Mind == "Solder")): 
        # Теперь мы ищем ближайшего врага в нашем блоке, кому дать пизды
        
        # FAST ATTACK
        
        EnemyID = Actor.HasBeenAttackedByID
        TheyXY = BugXY(EnemyID)
        if TheyXY != -1:# Проверяем то, что враг ещё существует
            TheyX = TheyXY[0]
            TheyY = TheyXY[1]
        
            # Distance Check
            # Если можно атаковать в ответ = атакуем. Нет - движемся к атаковавшему противнику.
            if DistanceCheckForAttack(MyX, MyY, TheyX, TheyY, Actor.AttackRange):
                Actor.Attack(EnemyID)
                return 0
            else:
                HowToMove = AutoMove(MyX, MyY, TheyX, TheyY)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
        else: # Если врага нет - убираем его ID из памяти
            Actor.HasBeenAttackedByID = -1
            
        # Но всё ещё в боевом режиме, поэтому ищем врага в своём блоке.
        EnemyList = FindEnemies(Actor.BlockMapID[0], Actor.BlockMapID[1])
        if(EnemyList):
            # Враг есть - выбираем ближайшего и атакуем его
            ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
            if ClosestEnemy[3] < Actor.AttackRange*2:
                Actor.Attack(ClosestEnemy[0])
                return 0
            else:
                HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
        else: # Если враг не найден - выключаем бой
            Actor.HasBeenAttacked = False
            
    if (Actor.HasBeenAttacked == True and Actor.Mind == "Watcher"): # Ну а если муравей - разведчик - побег
        # Нужно проверить, есть ли враги рядом
        EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 2)
        if not EnemyList:
            Actor.HasBeenAttacked = False
            Actor.HasBeenAttackedByID = -1
            # Если врагов рядом нет - то забываем о них и продолжаем как обычно.
            # Если же есть >
        else:
            # Check how far is HOME
            HomeX = ListOfHomes[Actor.HomeID].posx
            HomeY = ListOfHomes[Actor.HomeID].posy
            ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
            if ClosestEnemy[3] > 30: # Если дом достаточно далеко - убегает в его сторону
                HowToMove = AutoMove(MyX, MyY, HomeX, HomeY)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
            else: # Если нет - атакует.
                if (ClosestEnemy[3] < Actor.AttackRange*2):
                    Actor.Attack(EnemyID)
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, EnemyX, EnemyY)
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
        
    if (Actor.Energy < (Actor.MaxEnergy // 2)) and (Actor.State != "Lost" and Actor.State != "InHome" and Actor.State != "NeedFood"): # Муравьхи гхолодные????
        Actor.State = "NeedFood"
        #print (f"Need food. Actor {Actor.ID} now need food!")

    if (Actor.Mind == "Solder"): # Основной ИИ Солдата
    
        if Actor.State == "InHome":
            ##print(f"Actor {Actor.ID} is Solder InHome and eating???")
            Actor.EatFood()
            Homes = HomeXY()
            if GetDistanceRaw(Actor.posx, Actor.posy, Homes[0], Homes[1]) > 7:
                Actor.State = "Solder"
                ##print(f"Solder {Actor.ID} is SUCSESSFULLY EAT and is Solder")
            else:
                ##print(f"Actor {Actor.ID} is not leaving now {Actor.posx}, {Actor.posy}")
                Actor.Move(Actor.AngleRand, 1)
                Actor.AngleRand += randint(-5, 5)
            return 0

        if Actor.State == "Solder":
            ##print(f"Actor {Actor.ID} is Solder")
            EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 4)
            if (EnemyList):
                ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
                if ClosestEnemy[3] < Actor.AttackRange*2:
                    Actor.Attack(ClosestEnemy[0])
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
            #NeedForHelp = HelpAnotherAnt(Actor.BlockMapID[0], Actor.BlockMapID[1])
            #if NeedForHelp[0] == 1:
            #    Actor.HasBeenAttacked = NeedForHelp[1]
            #    Actor.HasBeenAttackedByID = NeedForHelp[2]
            #    return 0
            else: # Patrol waypoints
                if Actor.TargetPoint[0] != -1:
                    if GetDistanceRaw(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2]) < 10:
                        Actor.GoWayPoint(Actor.TargetPoint[0])
                        Actor.TargetPoint[0] = -1
                        return 0
                ##print(f"Actors memory = {Actor.Memory}")
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 1, Actor.Memory)
                if not WayPoints:
                    WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
                if (WayPoints): # Нашли WP - идём по нему. Не нашли - очищаем память
                    WPArray = []
                    for WPID in WayPoints:
                        WayP = GetIDXYW(WPID)
                        WPArray.append(WayP)
                        if (GetDistanceRaw(Actor.posx, Actor.posy, WayP[1], WayP[2]) < 20):
                            WayP[3]= WayP[3] * WayP[3] + 10
                    ###print(f"WPList = {WPArray} outside worker going way")
                    GoToWP = ChooseWPRandom(WPArray)
                    HowToMove = AutoMove(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2])
                    Actor.Move(HowToMove[0]+randint(-5, 5), HowToMove[1])
                    Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                    if GetDistanceRaw(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2]) < 10: # Слишком близко - считаем пройденной
                        Actor.GoWayPoint(GoToWP[0])
                        Actor.TargetPoint[0] = -1
                    return 0
                else: # Если их нет, то муравей направляется к дому
                    HomeCoords = HomeXY(Actor.HomeID)
                    HowToMove = AutoMove(MyX, MyY, HomeCoords[0], HomeCoords[1])
                    Actor.Move(HowToMove[0], HowToMove[1])
                    if GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0], HomeCoords[1]) < 10:
                        Actor.MemoryClear()
                    return 0

        if Actor.State == "NeedFood":
            ###print(f"Actor {Actor.ID} is Solder need food")
            EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 2)
            if (EnemyList):
                ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
                if ClosestEnemy[3] < Actor.AttackRange*2:
                    Actor.Attack(ClosestEnemy[0])
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
            NeedForHelp = HelpAnotherAnt(Actor.BlockMapID[0], Actor.BlockMapID[1])
            if NeedForHelp[0] == 1:
                Actor.HasBeenAttacked = NeedForHelp[1]
                Actor.HasBeenAttackedByID = NeedForHelp[2]
                return 0
            else:
                HomeCoords = HomeXY(Actor.HomeID)
                if (GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0], HomeCoords[1]) > 5):
                    HowToMove = GoHome(Actor)
                    HowToMove1 = HowToMove[0]
                    HowToMove2 = HowToMove[1]
                    Actor.Move(HowToMove1, HowToMove2)                    
                    return 0
                else:
                    Actor.State = "InHome"
                    return 0
        
        if Actor.State == "Attack":
            if not IsAttack: Actor.State = "Solder"
            EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 5)
            if (EnemyList):
                #print(EnemyList)
                ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
                if ClosestEnemy[3] < Actor.AttackRange*2:
                    Actor.Attack(ClosestEnemy[0])
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
            else:
                HowToMove = AutoMove(Actor.posx, Actor.posy, AttackPoint[0], AttackPoint[1])
                if HowToMove[1] > 10:
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
                elif HowToMove[1] < 3:
                    Actor.Move(HowToMove[0] + (randint(0, 10) * 30), HowToMove[1])
                    return 0
                else:
                    Actor.Move(HowToMove[0] + (randint(-1, 1) * 20), HowToMove[1])
                    return 0
                    
        if Actor.State == "Defend":
            if not IsDefend: 
                Actor.State = "Solder"
                Actor.DefendPoint[0] = 0
                return 0
            EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 5)
            if (EnemyList):
                ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
                if ClosestEnemy[3] < Actor.AttackRange*2:
                    Actor.Attack(ClosestEnemy[0])
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
            if Actor.DefendPoint[0] == 0:
                Actor.DefendPoint[0] = 1
                HomeCoords = HomeXY(Actor.HomeID)
                Actor.DefendPoint[1] = HomeCoords[0] + randint(-3, +3) * 10
                Actor.DefendPoint[2] = HomeCoords[1] + randint(-3, +3) * 10
                return 0
            else:
                HowToMove = AutoMove(Actor.posx, Actor.posy, Actor.DefendPoint[1], Actor.DefendPoint[2])
                if HowToMove[1] < 2:
                    Actor.DefendPoint[0] = 0
                    return 0
                else:
                    Actor.Move(HowToMove[0] + (randint(-2, 2) * 23), HowToMove[1])
                    return 0
            
        

    #FOR WORKER
    if (Actor.Mind == "Worker"):
    
        if Actor.State == "InHome":
            Actor.MemoryClear()
            ###print(Actor.Inventory)
            ##print(f"Actor {Actor.ID} is Worker InHome")
            ###print(f"Actor {Actor.ID} is Solder InHome and eating???")
            Actor.EatFood()
            Homes = HomeXY()
            if GetDistanceRaw(Actor.posx, Actor.posy, Homes[0], Homes[1]) > 7:
                Actor.State = "Worker"
                ##print(f"618. Worker {Actor.ID} is SUCSESSFULLY EAT")
            else:
                ###print(f"Actor {Actor.ID} is not leaving now {Actor.posx}, {Actor.posy}")
                Actor.Move(Actor.AngleRand, 1)
                Actor.AngleRand += randint(-5, 5)
            if Actor.Inventory > 0:
                ###print(f"Actor.Inventory = {Actor.Inventory}")
                Actor.PutFoodHome()
            ###print(Actor.Inventory)
            return 0
            
        if Actor.State == "Worker": # Ищем первый попавшийся WP
            ##print(f"Actor {Actor.ID} is Worker")
            WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 3)
            if (WayPoints):
                ###print(f"WayPoints = {WayPoint}")
                WPArray = []
                for WPID in WayPoints:
                    WayP = GetIDXYW(WPID)
                    if (GetDistanceRaw(Actor.posx, Actor.posy, WayP[1], WayP[2]) < 11):
                        WayP[3]= WayP[3] * WayP[3] + 10
                    WPArray.append(WayP)
                ###print(f"WPList = {WPArray} outside worker")
                WP = ChooseWPRandom(WPArray) # ID, X, Y, Weight
                ###print(f"WPreturn = {WP}")
                Actor.GoWayPoint(WP[0])
                HowToMove = AutoMove(Actor.posx, Actor.posy, WP[1], WP[2])
                Actor.Move(HowToMove[0]+randint(-5, 5), HowToMove[1])
                Actor.State = "GoingWay"
                ##print(f"Worker {Actor.ID} is GoingWay")
                return 0
            else: 
                HomeCoords = HomeXY(Actor.HomeID)
                if GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0], HomeCoords[1]) > 10:
                    MoveAroundHome(Actor)
                    return 0
                else:
                    MoveAroundHome(Actor, True)
                    return 0
                    
        if Actor.State == "GoingWay": #Идём по WP
            ##print(f"Actor {Actor.ID} is Worker GoingWay")
            ##print(f"Actor Target is {Actor.TargetPoint} ")
            if Actor.TargetPoint[0] != -1:
                if GetDistanceRaw(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2]) < 10:
                    Actor.GoWayPoint(Actor.TargetPoint[0])
                    if GetWPIsFinal(Actor.TargetPoint[0]):
                        Actor.State = "WhereFood"
                        ##print(f"Worker {Actor.ID} is WhereFood")
                    Actor.TargetPoint[0] = -1
                    return 0
            ##print(f"Actors memory = {Actor.Memory}")
            WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 1, Actor.Memory)
            if not WayPoints:
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
            if (WayPoints): # Нашли WP - идём по нему. Не нашли - очищаем память
                WPArray = []
                for WPID in WayPoints:
                    WayP = GetIDXYW(WPID)
                    WPArray.append(WayP)
                    if (GetDistanceRaw(Actor.posx, Actor.posy, WayP[1], WayP[2]) < 11):
                        WayP[3]= WayP[3] * WayP[3] + 10
                ###print(f"WPList = {WPArray} outside worker going way")
                GoToWP = ChooseWPRandom(WPArray)
                HowToMove = AutoMove(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2])
                Actor.Move(HowToMove[0]+randint(-5, 5), HowToMove[1])
                Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                if GetDistanceRaw(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2]) < 10: # Слишком близко - считаем пройденной
                    Actor.GoWayPoint(GoToWP[0])
                    if GetWPIsFinal(GoToWP[0]):
                        Actor.State = "WhereFood"
                        Actor.MemoryClear()
                        ##print(f"Worker {Actor.ID} is WhereFood")
                    Actor.TargetPoint[0] = -1
                return 0
            else: # xyz.
                Actor.State = "WhereFood"
                    ##print(f"Worker {Actor.ID} is Lost")
                return 0
        
        if Actor.State == "WhereFood":
            Actor.MemoryClear()
            ##print(f"Actor {Actor.ID} is Worker WhereFood")
            FoodFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "food", 2)
            if FoodFound:
                Actor.State = "YesFood"
                ##print(f"Worker {Actor.ID} is YesFood")
                ##print(FoodFound)
                ClosestFood = GetClosest(MyX, MyY, FoodFound, "food")
                Actor.FoodMemory = ClosestFood[0]
            else:
                Actor.State = "NoFood"
                ##print(f"Worker {Actor.ID} is NoFood")
                
        if Actor.State == "NoFood":
            ##print(f"Actor {Actor.ID} is Worker NoFood")
            HomeCoords = HomeXY(Actor.HomeID)
            if GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0], HomeCoords[1]) < 5: # Близко к дому - похуй, идём кушать
                Actor.State = "NeedFood"
                ##print(f"Worker {Actor.ID} is NeedFood")
                return 0
            if Actor.TargetPoint[0] != -1: # Короч если есть таргет - чистим его (если близко) или идём к нему (если далеко)
                if GetDistanceRaw(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2]) < 5:
                    Actor.ClearWP(Actor.TargetPoint[0], 2)
                    Actor.GoWayPoint(Actor.TargetPoint[0])
                    Actor.TargetPoint[0] = -1
                    return 0
                else:
                    HowToMove = AutoMove(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2])
                    Actor.Move(HowToMove[0] + randint(-5, 5), HowToMove[1])
                    return 0
            WPs = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
            if WPs: # Ну таргета нет, ищем вейпоинты. И идём к понравившемуся (добавив его в таргет)
                WPArray = []
                for WPID in WPs:
                    WayP = GetIDXYW(WPID)
                    WPArray.append(WayP)
                    if (GetDistanceRaw(Actor.posx, Actor.posy, WayP[1], WayP[2]) < 11):
                        WayP[3]= WayP[3] * WayP[3] + 10
                ###print(f"WPList = {WPArray} outside worker no food")
                GoToWP = ChooseWPRandom(WPArray)
                Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                HowToMove = AutoMove(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2])
                Actor.Move(HowToMove[0] + randint(-5, 5), HowToMove[1])
                return 0
            else:
                Actor.State = "Lost"
                ##print(f"Worker {Actor.ID} is Lost")
                
        if Actor.State == "YesFood":
            ##print(f"Actor {Actor.ID} is Worker YesFood")
            OurFood = FoodXY(Actor.FoodMemory)
            if OurFood:
                if GetDistanceRaw(Actor.posx, Actor.posy, OurFood[0], OurFood[1]) > 5:
                    HowToMove = AutoMove(Actor.posx, Actor.posy, OurFood[0], OurFood[1])
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
                else:
                    FoodSuccess = Actor.TakeFood(Actor.FoodMemory) # Need to check food
                    if FoodSuccess == 0:
                        Actor.State = "NoFood"
                        ##print(f"Worker {Actor.ID} is NoFood")
                        Actor.FoodMemory = -1
                    if FoodSuccess == 1:
                        Actor.State = "TakeFood"
                        ##print(f"Worker {Actor.ID} is TakeFood")
                    return 0
            else: 
                Actor.State = "NoFood"
                ##print(f"Worker {Actor.ID} is NoFood")
            
        if Actor.State == "TakeFood": # Да-да, ctrl+c > ctrl+v, иди нахуй, я уже заебался.
            ##print(f"Actor {Actor.ID} is Worker TakeFood")
            if Actor.TargetPoint[0] != -1:
                if GetDistanceRaw(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2]) < 5:
                    Actor.AddToWP(Actor.TargetPoint[0], 1)
                    Actor.GoWayPoint(Actor.TargetPoint[0])
                    Actor.TargetPoint[0] = -1
                    return 0
                else:
                    HowToMove = AutoMove(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2])
                    Actor.Move(HowToMove[0]+randint(-5, 5), HowToMove[1])
                    return 0
            WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 1, Actor.Memory)
            if not WayPoints:
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
            if (WayPoints): # Нашли WP - идём по нему. Не нашли - очищаем память
                WPArray = []
                for WPID in WayPoints:
                    WayP = GetIDXYW(WPID)
                    WPArray.append(WayP)
                    if (GetDistanceRaw(Actor.posx, Actor.posy, WayP[1], WayP[2]) < 11):
                        WayP[3]= WayP[3] * WayP[3] + 10
                ###print(f"WPList = {WPArray} outside worker take food")
                GoToWP = ChooseWPRandom(WPArray)
                HowToMove = AutoMove(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2])
                Actor.Move(HowToMove[0]+randint(-5, 5), HowToMove[1])
                Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                if GetDistanceRaw(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2]) < 5: # Слишком близко - считаем пройденной
                    Actor.GoWayPoint(GoToWP[0])
                    if GetWPIsFinal(GoToWP[0]):
                        Actor.State = "NeedFood"
                        ##print(f"Worker {Actor.ID} is NeedFood")
                return 0
            else: # Зачем? Чтобы муравей мог продолжить искать вейпоинты если зашёл в тупик, где их нет.
                Actor.MemoryClear()
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
                if not WayPoints:
                    Actor.State = "Lost"
                    ##print(f"Worker {Actor.ID} is Lost")
                return 0
            
                
        if Actor.State == "NeedFood":
            ##print(f"Actor {Actor.ID} is Worker NeedFood")
            HomeCoords = HomeXY(Actor.HomeID)
            if (GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0],HomeCoords[1]) > 5):
                HowToMove = GoHome(Actor)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
            else:
                Actor.State = "InHome"
                ##print(f"Worker {Actor.ID} is InHome")
                return 0
            
        if Actor.State == "Lost":
            Actor.State = "NeedFood"
            return 0
            MyHomeXY = HomeXY(Actor.HomeID)
            if GetDistanceRaw(Actor.posx, Actor.posy, MyHomeXY[0], MyHomeXY[1]) < 50:
                ##print(f"Actor {Actor.ID} is no longer lost")
                Actor.State = "NeedFood"
                return 0
            ###print(f"Actor {Actor.ID} is Worker Lost")
            if Actor.MemoryAnt != -1:
                NotLostAnt = ListOfAnts[Actor.MemoryAnt]
                if NotLostAnt.State != "Lost":
                    HowToMove = AutoMove(Actor.posx, Actor.posy, NotLostAnt.posx, NotLostAnt.posy)
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
                Actor.MemoryAnt = -1
                return 0
                    
            MyHomeXY = HomeXY(Actor.HomeID)
            AntID = FindNotLostAnt(Actor.BlockMapID[0], Actor.BlockMapID[1], "ant", 2)
            if AntID == -1:
                Actor.Move(randint(0, 360))
            else:
                NotLostAnt = ListOfAnts[AntID]
                Actor.MemoryAnt = AntID
                HowToMove = AutoMove(Actor.posx, Actor.posy, NotLostAnt.posx, NotLostAnt.posy)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
        

    #FIND FOOD
    if (Actor.Mind == "Watcher"):
    
        if Actor.State == "InHome":
            ###print(f"Actor {Actor.ID} is Scout InHome")
            ###print(f"Actor {Actor.ID} is Solder InHome and eating???")
            Actor.EatFood()
            Homes = HomeXY()
            if GetDistanceRaw(Actor.posx, Actor.posy, Homes[0], Homes[1]) > 7:
                Actor.State = "Scout"
                ##print(f"Scout {Actor.ID} is SUCSESSFULLY EAT")
            else:
                ###print(f"Actor {Actor.ID} is not leaving now {Actor.posx}, {Actor.posy}")
                Actor.Move(Actor.AngleRand, 1)
                Actor.AngleRand += randint(-5, 5)
            return 0
            
        if Actor.State == "Scout":
            ###print(f"Actor {Actor.ID} is Scout")
            FoodFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "food", 3, [-1],True)
            WPFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
            if FoodFound and (not WPFound):
                Actor.State = "FoodFound"
                ##print(f"Scout {Actor.ID} is FOUND FOOD")
                ###print(FoodFound)
                ClosestFood = GetClosest(MyX, MyY, FoodFound, "food") # [ObjID, ObjX, ObjY, NewDiffSum]
                Actor.FoodMemory = ClosestFood[0]
                #print(f"Scout {Actor.ID} at [{Actor.posx},{Actor.posy} is FOUND FOOD at {ClosestFood}\nHis BlockMap is {Actor.BlockMapID}")
            else:
                Actor.Angle += randint(-5, 5)
                Actor.Move(Actor.Angle, Actor.Speed)
                return 0
                
        if Actor.State == "FoodFound":
            WPFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
            if WPFound:
                Actor.State = "Scout"
                ##print(f"879. Scout {Actor.ID} is Scout because there is WP")
                ##print(WPFound[0])
                return()
            ###print(f"Actor {Actor.ID} is Scout FoodFound")
            Foodxy = FoodXY(Actor.FoodMemory)
            FoodX = Foodxy[0]
            FoodY = Foodxy[1]
            DistanceToFood = GetDistanceRaw(Actor.posx, Actor.posy, FoodX, FoodY)
            ##print(f"FOOD FOUND.890: Distance = {DistanceToFood}")
            ##print(f"FOODFOUND: Distance = ({Actor.posx},{Actor.posy}) - ({FoodX},{FoodY})")
            if DistanceToFood < 2:
                Actor.State = "CreatingWay"
                LeaveMarkOnFood(Actor.FoodMemory)
                ##print(f"890. Scout {Actor.ID} ({Actor.posx},{Actor.posy}) is CreatingWay to food at {FoodX} {FoodY}")
                Actor.CreateWP(20, True)
            else:
                HowToMove = AutoMove(MyX, MyY, FoodX, FoodY)
                HowToMove[0] += randint(-5, 5)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
                
        if Actor.State == "CreatingWay":
            ###print(f"Actor {Actor.ID} is Scout CreatingWay")
            HomeCoords = HomeXY(Actor.HomeID)
            if (GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0], HomeCoords[1]) > 15):
                HowToMove = GoHome(Actor, True)
                Actor.Move(HowToMove[0], HowToMove[1])
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 1)
                if not WayPoints:
                    Actor.CreateWP(20)
                return 0
            else:
                Actor.CreateWP(20)
                Actor.State = "NeedFood"
                ##print(f"909. Scout {Actor.ID} is Done creating way")
                return 0
                
        if Actor.State == "NeedFood":
            ###print(f"Actor {Actor.ID} is Scout NeedFood")
            HomeCoords = HomeXY()
            if (GetDistanceRaw(Actor.posx, Actor.posy, HomeCoords[0], HomeCoords[1]) > 5):
                HowToMove = GoHome(Actor)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
            else:
                Actor.State = "InHome"
                ##print(f"921. Scout {Actor.ID} is in home")
                return 0

def BugAI(Actor):
    MyX = Actor.posx
    MyY = Actor.posy
    if Actor.Mind == "bug":
        AntsFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "ant", 6)
        if AntsFound:
            ClosestEnemy = GetClosest(Actor.posx, Actor.posy, AntsFound, "ant")
            if GetDistanceRaw(Actor.posx, Actor.posy, ClosestEnemy[1], ClosestEnemy[2]) < Actor.AttackRange*2:
                Actor.Attack(ClosestEnemy[0])
                return 0
            else:
                HowToMove = AutoMove(Actor.posx, Actor.posy, ClosestEnemy[1], ClosestEnemy[2])
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
        else: 
            if GetDistanceRaw(Actor.posx, Actor.posy,Actor.RandomPoint[0], Actor.RandomPoint[1]) < 10:
                Actor.NewRandomPoint()
                return 0
            else:
                HowToMove = AutoMove(Actor.posx, Actor.posy,Actor.RandomPoint[0], Actor.RandomPoint[1])
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0

def DeleteAntPls(ObjType, ID):
    global ListAntsDelete
    if not ID in ListAntsDelete:
        ListAntsDelete.append(ID)

def DeleteBugPls(ObjType, ID):
    global ListBugsDelete
    if not ID in ListBugsDelete:
        ListBugsDelete.append(ID)

def AntClearing():
    global ListAntsDelete
    for Object in ListAntsDelete:
        ForgetAboutAnt(Object)
    LeReturn = ListAntsDelete.copy()
    ListAntsDelete.clear()
    return LeReturn

def BugClearing():
    global ListBugsDelete
    for Object in ListBugsDelete:
        ForgetAboutBug(Object)
    LeReturn = ListBugsDelete.copy()
    ListBugsDelete.clear()
    return LeReturn
    

def AntsRender():
    global ListOfAnts
    RenderThis = []
    for Ant in ListOfAnts:
        RenderThis.append([ListOfAnts[Ant].ID, ListOfAnts[Ant].posx, ListOfAnts[Ant].posy, ListOfAnts[Ant].side])
    #print(f"RenderThisAnt {RenderThis}")
    return RenderThis

def BugsRender():
    global ListOfEnteties
    RenderThis = []
    for Bug in ListOfEnteties:
        RenderThis.append([ListOfEnteties[Bug].ID, ListOfEnteties[Bug].posx, ListOfEnteties[Bug].posy, ListOfEnteties[Bug].side])
    #print(f"RenderThisBug {RenderThis}")
    return RenderThis

def AntsEnergy():
    global ListOfAnts
    for Ant in ListOfAnts:
        ListOfAnts[Ant].Enrg()

def DoDamage(FromID, ToID, AntOrBug, HowMuch, SetHasBeenAttacked):
    if AntOrBug == "bug":
        if ToID in ListOfEnteties:
            ListOfEnteties[ToID].TakeDamage(HowMuch, SetHasBeenAttacked, FromID)
            return 1
        else:
            return 0
    if AntOrBug == "ant":
        if ToID in ListOfAnts:
            ListOfAnts[ToID].TakeDamage(HowMuch, SetHasBeenAttacked, FromID)
            return 1
        else:
            return 0
    
def DestroyAll():
    global ListOfAnts
    global ListAntsDelete
    global ListBugsDelete
    global ListOfEnteties
    ListOfAnts.clear()
    ListAntsDelete.clear()
    ListBugsDelete.clear()
    ListOfEnteties.clear()

def GetAntCount():
    global AntCount
    return AntCount
    
def SetAttackPoint(x, y):
    global AttackPoint
    AttackPoint = [x, y]
    
def SetIsAttack(IsTrue):
    global IsAttack
    IsAttack = IsTrue
    
def SetIsDefend(IsTrue):
    global IsDefend
    IsDefend = IsTrue
    
def UpdateAntsCount(Ant, Count):
    global AntsCount
    AntsCount[Ant] += Count
    AntsCount["All"] += Count

def ReturnAntsCount():
    global AntsCount
    return AntsCount

LastStandDistance = 30
FoodToEnergy = 200
MemorySize = 30
###print("AI loaded!")
SizeOfTheWorld = 100
SizeOfTheBlock = 30
SizeXSize = SizeOfTheBlock*SizeOfTheWorld

AttackPoint = [0,0]
IsAttack = False
IsDefend = False

ListOfAnts = {}
ListAntsDelete = []
ListBugsDelete = []
SuperAntID = 0
SuperBugID = 0
AntCount = 0 
ListOfEnteties = {}
LastStandDistance = 30
FoodToEnergy = 200
AntsHeads = [["default", 1, 1, 1, 1, 1, 1], ["Solder", 6, 5, 2, 4, 8, 1], ["Worker", 1, 1, 1, 2, 2, 3], ["Watcher", 0, 1, 1, 1, 1, 1, 1], ["Solder", 10, 6, 2, 5, 10, 1], ["Worker", 2, 2, 1, 5, 3, 5], ["Watcher", 0, 1, 1, 1, 2, 1, 1]] # Name, HealthBonus, Attack, AttackRange, Cost, EnergyNeed, WorkEfficiency
AntsBodies = [["default", 1, 2, 2, 1], ["armored", 6, 1, 12, 4], ["scout", 1, 4, 4, 3], ["worker2", 3, 2, 3, 2], ["scout2", 1, 6, 10, 6], ["solder3", 20, 1, 25, 10], ["worker3", 4, 3, 5, 3], ["scout3", 2, 7, 15, 7]] # Name, HealthBonus, SpeedBonus, Cost, EnergyNeed
AntsBellies = [["default", 1, 1000, 0], ["light", -1, 1400, 1], ["worker", 0, 3000, 0], ["heavy", 4, 5000, -1], ["Solder2", 10, 7000, 0]] # Name, HealthBonus, EnergyStorage, SpeedBonus
States = ["default","Attack","Defend","Scout", "FoodFound","CreatingWay", "Worker", "GoingWay", "WhereFood","NoFood","YesFood", "TakeFood", "InHome", "Solder", "NeedFood", "Lost"]
AntSolder = [1, 1, 3]
AntWorker = [2, 0, 2]
AntScout = [3, 2, 1]
AntSolder2 = [4, 1, 5]
AntWorker2 = [5, 3, 2]
AntScout2 = [6, 4, 1]
AntSolder3 = [4, 5, 5]
AntWorker3 = [5, 6, 2]
AntScout3 = [6, 7, 1]

SolderCost = AntsHeads[1][4] + AntsBodies[1][3]
WorkerCost = AntsHeads[2][4] + AntsBodies[0][3]
ScoutCost = AntsHeads[3][4] + AntsBodies[2][3]
SolderCost2 = AntsHeads[4][4] + AntsBodies[1][3]
WorkerCost2 = AntsHeads[5][4] + AntsBodies[3][3]
ScoutCost2 = AntsHeads[6][4] + AntsBodies[4][3]
SolderCost3 = AntsHeads[4][4] + AntsBodies[5][3]
WorkerCost3 = AntsHeads[5][4] + AntsBodies[6][3]
ScoutCost3 = AntsHeads[6][4] + AntsBodies[7][3]

IDK = [-1, 1] # Необходим для движения по/против часовой стрелки
AntsCount = {"All": 0,"Worker": 0, "Watcher": 0, "Solder": 0}
###print("Ants loaded!")