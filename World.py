# Класс для всех объектов для вычисления их координат. x - горизонтальная, y - вертикальная
class WorldObject:
    def __init__(self, posx=0, posy=0):
        self.posx= posx
        self.posy = posy
        
    def ReturnXY(self):
        return[self.posx, self.posy]


# Карта блоков для взаимодействия объектов и оптимизации
class BlockMap:
    def __init__(self, x=0, y=0, size=10):
        self.x = x * size
        self.y = y * size
        self.size = size
        self.AntsInsideIDs = []
        self.FoodInside = []
        self.EntetiesInside = []
        self.WayPoints = []
        self.Open = False

    def AddAnt(self, AntID):
        ##print("Adding ant: "+str(AntID))
        ##print(self.AntsInsideIDs)
        self.AntsInsideIDs.append(AntID)
        self.Open = True

    def DeleteAnt(self, AntID):
        ##print("Removing ant: "+str(AntID))
        ##print(self.AntsInsideIDs)
        self.AntsInsideIDs.remove(AntID)

    def AddFood(self, FoodID):
        self.FoodInside.append(FoodID)

    def DeleteFood(self, FoodID):
        self.FoodInside.remove(FoodID)

    def AddObj(self, ObjID, ObjType):
        if ObjType == "ant":
            self.AntsInsideIDs.append(ObjID)
        if ObjType == "food":
            self.FoodInside.append(ObjID)
        if ObjType == "bug":
            self.EntetiesInside.append(ObjID)
        if ObjType == "way":
            self.WayPoints.append(ObjID)

    def RemoveObj(self, ObjID, ObjType):
        if ObjType == "ant":
            if ObjID in self.AntsInsideIDs:
                self.AntsInsideIDs.remove(ObjID)
        if ObjType == "food":
            if ObjID in self.FoodInside:
                self.FoodInside.remove(ObjID)
        if ObjType == "bug":
            if ObjID in self.EntetiesInside:
                self.EntetiesInside.remove(ObjID)
                #print(f"bug {ObjID} is removed!")
        if ObjType == "way":
            if ObjID in self.WayPoints:
                self.WayPoints.remove(ObjID)

    def ScanFor(self, ObjType):
        if ObjType == "ant":
            return(self.AntsInsideIDs)
        if ObjType == "food":
            return(self.FoodInside)
        if ObjType == "bug":
            return(self.EntetiesInside)
        if ObjType == "way":
            return(self.WayPoints)
            
        
class FoodPoint(WorldObject):
    def __init__(self, x = 0, y = 0, Quantity = 10, SetAll = False ,Marked = False, ID = 0, IsDeadAnt = False, IsDeadBug = False):
        super().__init__(posx=x, posy=y)
        global SuperObjectID
        #global BlockMapList
        self.Full = True
        self.MaxQuantity = Quantity
        if Quantity < 40:
            self.Texture = 11
        elif Quantity < 85:
            self.Texture = 21
        else:
            self.Texture = 31
        if IsDeadAnt:
            self.Texture = 41
        if IsDeadBug:
            self.Texture = 51
        self.Quantity = Quantity
        self.ObjType = "food"
        self.IsFoodExists = True
        self.ID = SuperObjectID
        self.Mark = False
        #print(f"Q = {Quantity}, tx = {self.Texture}")
        if SetAll:
            self.Mark = Marked
            self.ID = ID
        self.BlockMapID = GetBlockMapID(self.posx, self.posy)
        #print(f"Adding object {self.ID} {self.ObjType}")
        #BlockMapList[self.BlockMapID[0]][self.BlockMapID[1]].AddObj(self.ID, self.ObjType)
        AddObjectToBlock(self.ID, self.ObjType, self.BlockMapID[0], self.BlockMapID[1])
        ##print(f"Food point at {x} {y} was created")
        
    def TakeFood(self, Amount):
        self.Quantity -= Amount
        if self.Quantity < self.MaxQuantity // 2 and self.Full:
            self.Texture += 1
            self.Full = False
        if self.Quantity < 1:
            DeleteObjectPls(self.ObjType, self.ID)
            return 0
        return Amount
    
    def MarkThis(self):
        self.Mark = True
        
    def __del__(self):
        
        DeleteObjectFromBlock(self.ID, self.ObjType, self.BlockMapID[0], self.BlockMapID[1]) 
        #BlockMapList[self.BlockMapID[0]][self.BlockMapID[1]].RemoveObj(self.ID, self.ObjType)

class Home(WorldObject):
    def __init__(self, posx, posy, FoodInside=50000, SetAll = False, AntsIDs = []):
        super().__init__(posx = posx, posy = posy)
        #print(FoodInside)
        self.AntsIDs = []
        self.Food = FoodInside
        if SetAll:
            self.AntsIDs = AntsIDs
        
    def AddAnt(self, AntID, Food = 0):
        self.AntsIDs.append(AntID)
        self.Food -= Food
        
    def RemoveAnt(self, AntID):
        self.AntsIDs.remove(AntID)
        
    def GiveFood(self, FoodAmount):
        if self.Food >= FoodAmount:
            self.Food -= FoodAmount
            return FoodAmount
        else:
            RetFood = self.Food
            self.Food = 0
            return RetFood
            
    def AddFood(self, Amount):
        ##print(f"Adding {Amount} food to {self.Food}")
        self.Food += Amount
        ##print(f"Now we have {self.Food}")
        
    def NoFood(self, Amount):
        self.Food -= Amount

# Путь для муравьёв, потом с этим разберёмся
# Бля, ну, пора разбираться // 05.04.2023
# Ok // 06.04
class WayPoint(WorldObject):
    def __init__(self, SpawnPointX, SpawnPointY, Target="food", FinalPoint=False, Weight=10, SetAll = False, ID = 0):
        super().__init__(posx=SpawnPointX, posy=SpawnPointY)
        global SuperWPID
        self.Target = Target
        self.Final = FinalPoint
        self.Weight = Weight
        self.ObjType = "way"
        self.ID = SuperWPID
        if SetAll:
            self.ID = ID
        self.BlockMapID = GetBlockMapID(self.posx, self.posy)
        AddObjectToBlock(self.ID, self.ObjType, self.BlockMapID[0], self.BlockMapID[1])
        
    def LoseWeight(self, Amount=1):
        global ListDelete
        self.Weight -= Amount
        if self.Weight < 1:
            DeleteWayPls(self.ObjType, self.ID)

    def AddWeight(self, Amount=1):
        self.Weight += Amount

    def GetIDXYW(self):
        Return = [self.ID, self.posx, self.posy, self.Weight]
        return Return


    def __del__(self):
        DeleteObjectFromBlock(self.ID, self.ObjType, self.BlockMapID[0], self.BlockMapID[1])


#def CreateBlockMapsOld(SizeOfTheWorld, SizeOfTheBlock):
#    global BlockMapList
#    for BlockMapRow in range(SizeOfTheWorld):
#        for BlockMapColumn in range(SizeOfTheWorld):
#            BlockMapList.append(BlockMap((BlockMapColumn * SizeOfTheBlock), (BlockMapRow * SizeOfTheBlock), SizeOfTheBlock))

#Why
#y3
#^2
#^123
#0>> x
def CreateBlockMaps(SizeOfTheWorld, SizeOfTheBlock): # Fuck.
    global BlockMapList
    global BMExists
    BlockMapRow = []
    for XColumns in range(SizeOfTheWorld):
        for YRows in range(SizeOfTheWorld):
            BlockMapRow.append(BlockMap((XColumns), (YRows), SizeOfTheBlock))
        BlockMapList.append(BlockMapRow.copy()) # Change Da world, moi funnal messag, gutbuy (C) RAM
        BlockMapRow.clear()
    BMExists = True


def CreateFood(x, y, HowMany, SetAll=False, Marked=False,ID=0):
    global ListOfObjects
    global SuperObjectID
    if SetAll:
        ListOfObjects.update({ID: FoodPoint(x,y,HowMany,SetAll,Marked,ID)})
        if ID > SuperObjectID: SuperObjectID = ID + 1
    else:
        ListOfObjects.update({SuperObjectID: FoodPoint(x,y,HowMany)})
        SuperObjectID += 1

def DeleteAntFromBlock(AntID, xID, yID):
    global BlockMapList
    BlockMapList[yID][xID].DeleteAnt(AntID)

def DeleteAntFromHome(AntID, HomeID):
    global ListOfHomes
    ListOfHomes[HomeID].RemoveAnt(AntID)

def AddAntToBlock(AntID, xID, yID):
    global BlockMapList
    BlockMapList[yID][xID].AddAnt(AntID)

def AddObjectToBlock(ID, ObjType, xID, yID):
    global BlockMapList
    BlockMapList[yID][xID].AddObj(ID, ObjType)

def DeleteObjectFromBlock(ID, ObjType, xID, yID):
    global BlockMapList
    BlockMapList[yID][xID].RemoveObj(ID, ObjType)

def GetBlockMapID(posx, posy):
    global SizeOfTheBlock
    global SizeOfTheWorld
    if posy < 0 or posx < 0:
        return [0, 0]
    if posy > (SizeOfTheBlock*SizeOfTheWorld) or posx > (SizeOfTheBlock*SizeOfTheWorld):
        return [0, 0]
    xID = int(posx // SizeOfTheBlock)
    yID = int(posy // SizeOfTheBlock)
    ##print(f"x {posx} => {xID} \n y {posy} => {yID}")
    return [xID, yID]
    
def FindEnemies(BMx, BMy):
    global BlockMapList # Здесь не нужен global
    return BlockMapList[BMy][BMx].ScanFor("bug")
    
def ScanRadiusAround(BMx, BMy, ObjType, Range, ignore=[-1], IgnoreMark = False):
    global BlockMapList
    global SizeOfTheWorld
    ReturnThisArray = []
    # Что же, нужно просканить центр и блоки вокруг вплоть до Range
    # Range 1 - 1 блок, Range 2 - 9 блоков и т.д.
    #print(f"Range = {Range}")
    for i in range(-(Range-1), (Range)):
        for i2 in range(-(Range-1), (Range)):
            x = i+BMx
            y = i2+BMy
            if (x < 0 or y < 0 or x >= SizeOfTheWorld or y >= SizeOfTheWorld):
                continue
            #print(f"Scanned block[{x}][{y}]")
            ReturnThisArray.extend(BlockMapList[y][x].ScanFor(ObjType))
    if ObjType == "food":
        if IgnoreMark:
            for obj in ReturnThisArray:
                if GetIfMarked(obj):
                    ignore.append(obj)
    
    for Ignored in ignore:
        if Ignored in ReturnThisArray:
            ReturnThisArray.remove(Ignored)
    #print("Scan done!")
    #if ReturnThisArray:
    #    print(f"Result = {ReturnThisArray}")
    return ReturnThisArray
    
def GetIfMarked(ID):
    global ListOfObjects
    return ListOfObjects[ID].Mark

def FoodXY(ID):
    global ListOfObjects
    if ID in ListOfObjects:
        return ListOfObjects[ID].ReturnXY()

def HomeXY(ID=0):
    global ListOfHomes
    return ListOfHomes[ID].ReturnXY()
    
def HomeFood(ID=0):
    global ListOfHomes
    if ListOfHomes:
        return ListOfHomes[ID].Food
    else:
        return 0

def AddAntToHome(AntID, Cost=0,HomeID=0):
    global ListOfHomes
    ListOfHomes[HomeID].AddAnt(AntID, Cost)

def ForgetAboutFood(ID):
    global ListOfObjects
    if ID in ListOfObjects:
        del ListOfObjects[ID]

def ForgetAboutWay(ID):
    global ListOfWPs
    if ID in ListOfWPs:
        del ListOfWPs[ID]

def CreateHome(SpawnX=0, SpawnY=0, SetAll = False, AntsIDs = [], Foods=0):
    global ListOfHomes
    if not SetAll:
        ListOfHomes.append(Home(SpawnX, SpawnY))
    else:
        ListOfHomes.append(Home(SpawnX, SpawnY, Foods, SetAll, AntsIDs))
        print(f"Home with {Foods} food created!")

def GetListOfHomes():
    global ListOfHomes
    return ListOfHomes

def GetListOfObjects():
    global ListOfObjects
    return ListOfObjects
    
def GetListOfWPs():
    global ListOfWPs
    return ListOfWPs
    
def AntEatsFood(ID, FoodNeed):
    global ListOfHomes
    ##print("Someone just eats some food!")
    return ListOfHomes[ID].GiveFood(FoodNeed)
    
def AntLeavesFood(ID, Food):
    global ListOfHomes
    return ListOfHomes[ID].AddFood(Food)
    
def StealFood(Count):
    global ListOfHomes
    ListOfHomes[0].NoFood(Count) 
    
def AntTakesFood(ID, WorkEff):
    global ListOfObjects
    return ListOfObjects[ID].TakeFood(WorkEff)
    
def CreateWayPoint(x, y, Weight, Final = False, SetAll=False, ID=0):
    global ListOfWPs
    global SuperWPID
    if SetAll:
        ListOfWPs.update({ID: WayPoint(x, y, "food", Final, Weight, SetAll, ID)})
        if ID > SuperWPID: SuperWPID = ID + 1
    else:
        ListOfWPs.update({SuperWPID: WayPoint(x, y, "food", Final, Weight)})
        ##print(f"Created WP at {x} {y}")
        SuperWPID += 1

    
def AddToWayPoint(ID, Weight = 1):
    global ListOfWPs
    ListOfWPs[ID].AddWeight(Weight)
    
def ClearWayPoint(ID, Weight = 2):
    global ListOfWPs
    if ID in ListOfWPs:
        ListOfWPs[ID].LoseWeight(Weight)
    
def DeleteObjectPls(ObjType, ID):
    global ListObjectsDelete
    if not ID in ListObjectsDelete:
        ListObjectsDelete.append(ID)
    
def DeleteWayPls(ObjType, ID):
    global ListWPsDelete
    if not ID in ListWPsDelete:
        ListWPsDelete.append(ID)
    
def ObjectsClearing():
    global ListObjectsDelete
    for Object in ListObjectsDelete:
        ##print(f"Deleting food {Object}")
        ForgetAboutFood(Object)
    LeReturn = ListObjectsDelete.copy()
    ListObjectsDelete.clear()
    return LeReturn
        
def WaysClearing():
    global ListWPsDelete
    for Object in ListWPsDelete:
        ##print(f"Deleting way {Object}")
        ForgetAboutWay(Object)
    LeReturn = ListWPsDelete.copy()
    ListWPsDelete.clear()
    return LeReturn
   
def GetIDXYW(ID):
    if ID in ListOfWPs:
        return ListOfWPs[ID].GetIDXYW()
    
def GetWPIsFinal(ID):
    if ID in ListOfWPs:
        return ListOfWPs[ID].Final
    
def FoodRender():
    global ListOfObjects
    RenderThis = []
    for Obj in ListOfObjects:
        RenderThis.append([ListOfObjects[Obj].ID, ListOfObjects[Obj].posx, ListOfObjects[Obj].posy, ListOfObjects[Obj].Texture])
    return RenderThis
    
def LeaveMarkOnFood(ID):
    ListOfObjects[ID].MarkThis()
    
    
def DestroyAll():
    global ListWPsDelete
    global ListObjectsDelete
    global BlockMapList
    global ListOfObjects
    global ListOfWPs
    global ListOfHomes
    global BMExists
    ListWPsDelete.clear()
    ListObjectsDelete.clear()
    ListOfObjects.clear()
    ListOfWPs.clear()
    ListOfHomes.clear()
    BlockMapList.clear()
    BMExists = False

# def GetBlockMapID(ObjectX, ObjectY, SizeOfTheWorld, SizeOfTheBlock):
    # RangeOfWorld = SizeOfTheBlock * SizeOfTheWorld 
    # if RangeOfWorld < ObjectX or RangeOfWorld < ObjectY or ObjectX < 0 or ObjectY < 0:
        # return 0
    # ID = (ObjectX // SizeOfTheBlock) + ((ObjectY // SizeOfTheBlock) * SizeOfTheBlock)
    # return ID

#def BlockMapGetID(ObjectX, ObjectY, SizeOfTheWorld, SizeOfTheBlock):
#    RangeOfWorld = SizeOfTheBlock * SizeOfTheWorld 
#    if RangeOfWorld < ObjectX or RangeOfWorld < ObjectY or ObjectX < 0 or ObjectY < 0:
#        return 0
#    ID = (ObjectX // SizeOfTheBlock) + ((ObjectY // SizeOfTheBlock) * SizeOfTheWorld * 10)
#    return ID
#
#def BlockMapGetIDX(ObjectX, SizeOfTheWorld, SizeOfTheBlock):
#    RangeOfWorld = SizeOfTheBlock * SizeOfTheWorld 
#    if RangeOfWorld < ObjectX or ObjectX < 0:
#        return 0
#    ID = (ObjectX // SizeOfTheBlock)
#    return ID
#
#def BlockMapGetIDY(ObjectY, SizeOfTheWorld, SizeOfTheBlock):
#    RangeOfWorld = SizeOfTheBlock * SizeOfTheWorld 
#    if RangeOfWorld < ObjectY or ObjectY < 0:
#        return 0
#    ID = ((ObjectY // SizeOfTheBlock) * SizeOfTheWorld * 10)
#    return ID
# Old block maps SUCKS
# Why 00x00y id is better than x,y? I mean it somewhat easier to use, but fuck it


'''
# Testing
count = 0
##print(GetBlockMapID(25, 64, 10, 100))
BlockMapList = []
CreateBlockMaps(10, 10)
##print(BlockMapList)
for i in range(len(BlockMapList)):
    ##print(BlockMapList[i])
    for i2 in range(len(BlockMapList[i])):
        #print("ID1 = {0}\nID2 = {1}\n X = {2}\n Y = {3}\n\n".format(i, i2, BlockMapList[i][i2].x, BlockMapList[i][i2].y))
    count += 1
#print(count)

#print(ScanRadiusAround(5,5, "bug", 2))'''
BMExists = False
ListWPsDelete = []
ListObjectsDelete = []
BlockMapList = []
ListOfObjects = {}
ListOfWPs = {}
ListOfHomes = []
SuperObjectID = 0
SuperWPID = 0
LastStandDistance = 30
FoodToEnergy = 200
MemorySize = 15
SizeOfTheWorld = 100
SizeOfTheBlock = 30
SizeXSize = SizeOfTheBlock*SizeOfTheWorld
#print("World loaded!")