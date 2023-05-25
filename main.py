import sys
import os
import time
import Tech
import World
import Ants
from random import randint
import AI
from tkinter import *
import json
import glob
import PIL

#def DeleteMePls(ObjType, ID):
#    global ListDelete
#    ListDelete.append([ObjType, ID])

'''class LoadFrame(Frame):
    def __init__():
        global mainwindow
        super().__init__(master = mainwindow, width=200)
        SaveNames = FindSaves()
        for SaveName in SaveNames:
            File = open(SaveName)
            NameOfSave = File.readline()
            File.close()
            Button(master=self, text=NameOfSave,font=("ComicSansMS", 20, "bold"), command=lambda: LoadThisSave(SaveName)).pack()
        
'''
'''class TechTreeButton(Button):
    def __init__(self, TechID, m = None, w = 30, h = 7, txt = "TechName", row = 0, column = 0, desc = "test"):
        #super().__init__(master=m, width=w, height=h, text=Text, font=("ComicSansMS", 12, "bold"), command= lambda: TechButtonClick(TechID))
        self.TechID = TechID
        self.row = row
        self.column = column
        self.desc = desc'''
# Смотрите кто опять проебался как лох ^


'''def FrameLoadCreate():
    global LoadScreen
    #global LoadScroll
    FrameLoad = Frame(master = LoadScreen, width=350)
    SaveNames = FindSaves()
    for SaveName in SaveNames:
        File = open(SaveName)
        NameOfSave = File.readline()
        File.close()
        Button(master=FrameLoad, width=20, text=NameOfSave,font=("ComicSansMS", 20, "bold"), command=lambda: LoadThisSave(SaveName)).pack()'''

def UpdateHome():
    global GameCanvas
    global HomeRendered
    TechLevel = Tech.ReturnTechLevel()
    GameCanvas.itemconfigure(HomeRendered, image=HomesImgs[TechLevel])
    
    

def UpdateAntButtons():
    #print("UpdateAntButtons")
    global ButtonSolder
    global ButtonScout
    global ButtonWorker
    global AntsResearched
    AntsResearched = Tech.GetUnlockedAnts()
    if AntsResearched["Solder1"]: ButtonSolder.configure(text = AntSolderText)
    if AntsResearched["Worker1"]: ButtonWorker.configure(text = AntWorkerText)
    if AntsResearched["Watcher1"]: ButtonScout.configure(text = AntScoutText)
    #print(AntsResearched)
    

def CreateTechTreeButtons():
    #print("CreateTechTreeButtons")
    global TechTreeButtons
    global TechTreeFrame
    TechTreeButtons.clear()
    TechList = Tech.ReturnListOfTech()
    for TechID in TechList:
        Technology = TechList[TechID]
        if Technology["IsOpened"]: color = "green"
        elif Technology["TechLevel"] <= Tech.ReturnTechLevel(): color = "yellow"
        else: color ="red"
        TechTreeButtons.update({TechID: Frame(master=TechTreeFrame, width=180, height=100, bg = color)})
        TechTreeButtons[TechID].bind("<Button-1>", lambda event, ID = TechID: TechButtonClick(ID))
        Label(master=TechTreeButtons[TechID], text=Technology["TechName"], font=("ComicSansMS", 14, "bold")).pack(padx=5, pady=5)#.pack(fill=None, expand=True)
        Label(master=TechTreeButtons[TechID], text=Technology["Description"], font=("ComicSansMS", 10, "bold")).pack(padx=5, pady=5)#.pack(fill=None, expand=True)
        for child in TechTreeButtons[TechID].winfo_children(): child.bind("<Button-1>", lambda event, ID = TechID: TechButtonClick(ID))
        TechTreeButtons[TechID].grid(column=Technology["Column"], row=Technology["Row"], padx=5, pady=5, sticky =EW )
        

def TechButtonClick(TechID):
    #print("TechButtonClick")
    global TechTreeButtons
    global AntsResearched
    Antsct = Ants.ReturnAntsCount()
    Foods = World.HomeFood()
    CanI = Tech.CanIOpenThisTech(TechID, Foods, [Antsct["All"], Antsct["Worker"], Antsct["Watcher"], Antsct["Solder"]])
    if CanI != -1:
        World.StealFood(CanI)
        Tech.OpenThisTechPls(TechID)
        TechTreeButtons[TechID].configure(bg="green")
        # Change image for button
    AntsResearched = Tech.GetUnlockedAnts()
    UpdateHome()
    UpdateFood()
    UpdateAntButtons()
        

def CreateTechTree():
    #print("CreateTechTree")
    global TechTreeButtons
    global BigTechFrame
    global TechTreeFrame
    global CloseTech
    TechTreeFrame.unbind("<Button-1>")
    TechTreeFrame.unbind("<ButtonRelease-1>")
    #for child in TechTreeButtons[TechID].winfo_children(): child.unbind("<Button-1>")
    TechTreeButton = {}
    TechTreeFrame.destroy()
    CloseTech.place_forget()
    TechTreeFrame = Frame(master = BigTechFrame, bg="#F0F8FF") # pls delete them python thnks gj love u
    TechTreeFrame.bind("<Button-1>", TechDragStart)
    TechTreeFrame.bind("<ButtonRelease-1>", TechDragMove)
    CreateTechTreeButtons()
    TechTreeFrame.place(relx=.5, rely=.0, anchor = "n")
    CloseTech.place(anchor=NE, relx=1.0, rely=.0)
    
def ShowTech():
    #print("ShowTech")
    global BigTechFrame
    SetPause(True, True)
    CreateTechTree()
    BigTechFrame.place(relx=.5, rely=.5, anchor = "center")
    
def HideTech():
    #print("HideTech")
    global BigTechFrame
    SetPause(True, False)
    BigTechFrame.place_forget()

def FindSaves():
    MyFiles = glob.glob("saves/*.antsave")
    return MyFiles
    
def FindLevels():
    MyFiles = glob.glob("levels/*.antlevel")
    return MyFiles

def RandomFoodAppear():
    global ListOfObjects
    x = randint(0, SizeXSize-1)
    y = randint(0, SizeXSize-1)
    Amount = randint(10, 120)
    World.CreateFood(x, y, Amount)

def UpdateFood():
    global FoodCount
    FoodCount.configure(text="Еда: "+str(World.HomeFood()))

def SolderButton():
    if AntsResearched["Solder1"] == 1:
        Ants.CreateAnt(0, AntSolder[0], AntSolder[1], AntSolder[2])
    UpdateFood()

def ScoutButton():
    if AntsResearched["Watcher1"] == 1:
        Ants.CreateAnt(0, AntScout[0], AntScout[1], AntScout[2])
    UpdateFood()

def WorkerButton():
    if AntsResearched["Worker1"] == 1:
        Ants.CreateAnt(0, AntWorker[0], AntWorker[1], AntWorker[2])
    UpdateFood()
    
def ObjectClearing():
    global DeleteAnts
    global DeleteFoods
    global DeleteBugs
    DeleteAnts.extend(Ants.AntClearing())
    DeleteFoods.extend(World.ObjectsClearing())
    DeleteBugs.extend(Ants.BugClearing())
    World.WaysClearing()

def SaveSaver(SaveName = "Save"):
    global MMB2
    global MMT1
    SavesN = MMT1.get("1.0", "end-1c")
    if SavesN != "":
        SaveName = SavesN
    MMB2.config(text="Сохранено!")
    HomesToSave = World.GetListOfHomes()
    HomesSaveData = []
    AntsToSave = Ants.GetListOfAnts()
    AntsSaveData = []
    BugsToSave = Ants.GetListOfEnteties()
    BugsSaveData = []
    FoodsToSave = World.GetListOfObjects()
    FoodSaveData = []
    WaysToSave = World.GetListOfWPs()
    WaysSaveData = []
    for Home in HomesToSave:
        HomesSaveData.append([Home.posx, Home.posy, Home.Food, Home.AntsIDs])
    for ID in AntsToSave:
        Ant = AntsToSave[ID]
        AntsSaveData.append([Ant.posx, Ant.posy, Ant.HBB, Ant.HomeID, Ant.ID, Ant.Health, Ant.Energy, Ant.Memory, Ant.FoodMemory, Ant.MemoryAnt, Ant.Inventory, Ant.TargetPoint, Ant.Speed, Ant.MaxHealth, Ant.AttackStrenght])
    for ID in BugsToSave:
        Bug = BugsToSave[ID]
        BugsSaveData.append([Bug.posx, Bug.posy, Bug.ID, Bug.Health])
    for ID in FoodsToSave:
        Food = FoodsToSave[ID]
        FoodSaveData.append([Food.posx, Food.posy, Food.Quantity, Food.Mark, Food.ID])
    for ID in WaysToSave:
        Way = WaysToSave[ID]
        WaysSaveData.append([Way.posx, Way.posy, Way.Final, Way.Weight, Way.ID])
    OmgThisObjectSoBig = {"Homes": HomesSaveData, "Ants": AntsSaveData, "Bugs": BugsSaveData, "Foods": FoodSaveData, "Ways": WaysSaveData}
    DoYouNeedMemory = json.dumps(OmgThisObjectSoBig)
    FileName = time.strftime("%S%M%H%d%m%Y", time.gmtime())
    File = open("saves/"+FileName+".antsave", "w")
    File.write(SaveName + "\n")
    File.write(DoYouNeedMemory+"\n")
    NANOMACHINES = Tech.GetOpenedTechesIDs()
    File.write(json.dumps(NANOMACHINES)+"\n")
    time.sleep(1)
    File.close()
    del OmgThisObjectSoBig
    del DoYouNeedMemory
    del NANOMACHINES
    #print("Save done!")

def DropWorld():
    global GameCanvas
    Ants.DestroyAll()
    World.DestroyAll()
    GameCanvas.delete("ant")
    GameCanvas.delete("bug")
    GameCanvas.delete("food")
    Tech.SetTechToDefault()
    Tech.SetModsToDefault()

def LoadThisSave(FilePath):
    global LoadScreen
    LoadScreen.forget()
    StartNewGame(True)
    time.sleep(1)
    SaveLoader(FilePath)

def SaveLoader(Filedir):
    global AntsResearched
    File = open(Filedir, "r")
    File.readline()
    LoadData = File.readline()
    BigObject = json.loads(LoadData)
    LoadHomes = BigObject["Homes"]
    LoadAnts = BigObject["Ants"]
    LoadBugs = BigObject["Bugs"]
    LoadFoods = BigObject["Foods"]
    LoadWays = BigObject["Ways"]
    for Home in LoadHomes:
        #print(f"Home is {Home}")
        #print(Home[2])
        World.CreateHome(Home[0], Home[1], SetAll = True, AntsIDs = Home[3], Foods=Home[2])
    for Ant in LoadAnts: # [Ant.posx, Ant.posy, Ant.HBB, Ant.HomeID, Ant.ID, Ant.Health, Ant.Energy, Ant.Memory, Ant.FoodMemory, Ant.MemoryAnt, Ant.Inventory, Ant.TargetPoint]
        Ants.CreateAnt(Ant[3], Ant[2][0], Ant[2][1], Ant[2][2], SetAll = True, ID=Ant[4], x = Ant[0], y = Ant[1], Stats = [Ant[5], Ant[6], Ant[7], Ant[8], Ant[9], Ant[10], Ant[11], Ant[12], Ant[13], Ant[14]])
    for Bug in LoadBugs:
        Ants.CreateBug(SetAll = True, ID=Bug[2], PosX=Bug[0], PosY=Bug[1], Health=Bug[3])
    for Food in LoadFoods:
        World.CreateFood(x=Food[0], y=Food[1], HowMany=Food[2], SetAll=True, Marked=Food[3],ID=Food[4])
    for Way in LoadWays:
        World.CreateWayPoint(x=Way[0], y=Way[1], Weight=Way[3], Final = Way[2], SetAll=True, ID=Way[4])
    Tech.LoadTechFromSave(Filedir)
    AntsResearched = Tech.GetUnlockedAnts()
    #print("loading done!")
    

    
# IM GONNA BUILD OBJECT SO HUGE IT CAN FUCKING OVERFLOW YOU STACK
# HON HON HON


def LoadThisLevel(FilePath):
    global LevelFrame
    LevelFrame.forget()
    #print("432542343")
    LevelLoader(FilePath)
    #StartNewGame(True)
    #time.sleep(1)
    #SaveLoader(FilePath)

# Level Structue:
# Name
# Configs: BugsSR, FoodSR, EnergyCR
# Tiles 
# IsSave // bool
# SaveDir
def LevelLoader(Filedir):
    File = open(Filedir, "r")
    LevelName = File.readline() # 1 line
    Configs = json.loads(File.readline()) # 2 line
    TileType = json.loads(File.readline()) # 3 line
    HasSaveFile = json.loads(File.readline()) # 4 line
    SaveFileDir = File.readline() # 5 line
    WorldBoot(HasSaveFile["IsSave"], SaveFileDir, Configs["BugsSR"], Configs["FoodSR"], Configs["EnergyCR"], TileType["TT"])
    
    

def WorldBoot(HasSaveFile = 0, WorldSaveDir = "levels/default.antsave", BugsSR=1000, FoodSR=1000, EnergyCR=10, TT = "Grass"):
    # Создание мира:
    # 1. Блокмапы
    # 2. Домик CreateHome(SpawnX=0, SpawnY=0, SetAll = False, AntsIDs = [], Foods=0)
    # 3. Муравьи CreateAnt(HomeID=0, HeadID=0, BodyID=0, BellyID=0, SetAll = False, ID=0, x = 0, y = 0, Stats = [1, 1, [-1], 0, 1, 0, [-1,0,0]])
    # 4. Еда CreateFood(x, y, HowMany, SetAll=False, Marked=False,ID=0)
    # 5. Жуки CreateBug(SetAll = False, ID=0, PosX=0, PosY=0, Health=0)
    # 6. Вейпоинты CreateWayPoint(x, y, Weight, Final = False, SetAll=False, ID=0)
    global SizeOfTheWorld
    global SizeOfTheBlock
    global FoodSpawnRate
    global BugSpawnRate
    global EnergyRate
    global TileType
    FoodSpawnRate = FoodSR
    BugSpawnRate = BugsSR
    EnergyRate = EnergyCR
    TileType = TT
    #World.CreateBlockMaps(SizeOfTheWorld, SizeOfTheBlock) << Делается в StartNewGame()
    #World.GetListOfHomes()
        
        
    StartNewGame(True)
    
    if HasSaveFile:
        SaveLoader(WorldSaveDir)
    else:
        World.CreateHome(SizeXSize // 2, SizeXSize // 2) # Ну а чего.
        
    
    # Ant__init__(self, SpawnPointX, SpawnPointY, HeadID=0, BodyID=0, BellyID=0, MyHomeID=0, SetAll = False, ID = 0, Health = 1, Energy = 1, Memory = ([-1]*MemorySize), FoodMemory = 0, MemoryAnt = -1, Inventory = 0, TargetPoint = [-1,0,0]):
    
    # Le Level:
    #ln LevelName
    #ln Data 
    #ln path to level save
def ClickLoadLevel(WorldPresetDir):
    #print("ClickLoadLevel")
    LvlFile = open(WorldPresetDir, "r")
    LvlName = LvlFile.readline()
    LvlData = LvlFile.readline()
    LvlPath = LvlFile.readline()
    LevelData = json.loads(LvlData)
    WorldBoot(False, LvlPath, LevelData["BugSR"], LevelData["FoodSR"], LevelData["EnergyCR"], LevelData["TT"])
    
    
def MoveLoadFrameWithMouse(event):
    #print("MoveLoadFrameWithMouse")
    global FrameLoad
    global ScrollY
    if event.num == 5 or event.delta == -120:
        ScrollY -= 20
 
    if event.num == 4 or event.delta == 120:
        ScrollY += 20
    FrameLoad.place(relx=.5, y=ScrollY, anchor = N)
    
def LoadLevel():
    #print("LoadLevel")
    global mainwindow
    global LevelFrame
    global FrameLevel
    global MenuFrame
    MenuFrame.place_forget()
    FrameLevelClear()
    FrameLevel = FrameLevelCreate()
    FrameLevel.place(relx=.5, anchor=N)
    LevelFrame.pack(fill=BOTH, expand=True)
    
def LoadGame():
    #print("LoadGame")
    global ScrollY
    global mainwindow
    global MenuFrame
    global FrameLoad
    global LoadScreen
    ScrollY = 0
    mainwindow.bind("<MouseWheel>", MoveLoadFrameWithMouse)
    MenuFrame.place_forget()
    FrameLoadClear()
    FrameLoad = FrameLoadCreate()
    FrameLoad.place(relx=.5, y=ScrollY, anchor= N)
    LoadScreen.pack(fill=BOTH, expand=True)
    #print(FrameLoad.winfo_geometry())

def BackFromLoad():
    #print("BackFromLoad")
    global mainwindow
    global MenuFrame
    global FrameLoad
    global LoadScreen
    LoadScreen.forget()
    mainwindow.unbind("<MouseWheel>")
    MenuFrame.place(relx=.5, rely=.5,anchor= CENTER)

def BackFromLevel():
    #print("BackFromLevel")
    global mainwindow
    global MenuFrame
    global FrameLevel
    global LevelFrame
    LevelFrame.forget()
    MenuFrame.place(relx=.5, rely=.5,anchor= CENTER)

def ShowMiniMenu():
    #print("ShowMiniMenu")
    global MiniMenu
    global MainWindow
    MiniMenu.place(relx=.5, rely=.5,anchor= CENTER)
    SetPause(True, True)
    
def HideMiniMenu():
    #print("HideMiniMenu")
    global MiniMenu
    global MainWindow
    global MMB2
    MMB2.config(text="Сохранить")
    MiniMenu.place_forget()
    SetPause(True, False)

def BackToMenu():
    #print("BackToMenu")
    global mainwindow
    global MiniMenu
    global GameCanvas
    global GameFrame
    global Exit
    global AttackDefend
    Exit = True
    mainwindow.after_cancel(UpdateEveryTick)
    DropWorld()
    GameCanvas.place_forget()
    MiniMenu.place_forget()
    GameFrame.forget()
    AttackDefend.place_forget()
    CreateNewMenu()

def StartNewGame(IsLoad = False):
    global mainwindow
    global MenuFrame
    global GameCanvas
    global StopSpin
    global ListOfObjects
    global Worker
    global Scout
    global Solder
    global FoodCount
    global GameFrame
    global ButtonWorker
    global ButtonScout
    global ButtonSolder
    global ButtonPause
    global ButtonGO
    global CanvasSize
    global Exit
    global Pause
    global HomeRendered
    global TileType
    HomeRendered = 0
    Exit = False
    Pause = False
    DropWorld()
    #print("Starting new game...")
    #print("World creating")
    #Grass
    GrassX = 0
    GrassY = 0
    for i in range(SizeXSize//100):
        for i in range (SizeXSize//100):
            GameCanvas.create_image(GrassX, GrassY, image=Tiles[TileType], anchor=NW, tags = "grass")
            GrassX += 100
            ##print(f"x{GrassX}, y{GrassY}")
        GrassY += 100
        GrassX = 0
    # Touch it NOW
    World.CreateBlockMaps(SizeOfTheWorld, SizeOfTheBlock)
    if not IsLoad:
        World.CreateHome(SizeXSize // 2, SizeXSize // 2)
        #print("Home Created at center of map")
    #for i in range(50): # Наспавним еды
    #    RandomFoodAppear()
    #for i in range(15): # Наспавним рабочих
    #    Ants.CreateAnt(0, AntWorker[0], AntWorker[1], AntWorker[2])
    #for i in range(10): # Наспавним разведчиков
    #    Ants.CreateAnt(0, AntScout[0], AntScout[1], AntScout[2])
    #for i in range(5): # Наспавним солдат
    #    Ants.CreateAnt(0, AntSolder[0], AntSolder[1], AntSolder[2])
    #print("Item placing done!")
    ButtonWorker.grid(column=0, row=0)
    ButtonScout.grid(column=1, row=0)
    ButtonSolder.grid(column=2, row=0)
    FoodCount.grid(column=3, row=0)
    ButtonPause.grid(column=4,row=0)
    #ButtonGO.grid(column=5,row=0)
    ButtonToMenu.grid(column=5, row=0)
    ButtonToTech.grid(column=6, row=0)
    StopSpin = True
    MenuFrame.place_forget()
    #print(GameCanvas.winfo_geometry())
    GameCanvas.place(x=0,y=0)
    GameFrame.pack(anchor=N)
    GameFrame.lift()
    GameFrame.lift()
    
    AttackDefend.place(relx=0.0, rely=1.0, anchor=SW)
    AttackDefend.lift()
    AttackDefend.lift()
    #print("World done!")
    xeee = -(SizeXSize//2-400)
    yeee = -(SizeXSize//2-400)
    GameCanvas.place(x=xeee, y=yeee)
    #print(GameCanvas.winfo_geometry())
    #print("Starting...")
    UpdateAntButtons()
    UpdateEveryTick()

def RenderableBlocks(FromX, FromY, ToX, ToY):
    pass


def UpdateEveryTick():
    global mainwindow
    global updatetime
    global FoodTime
    global EnergyTime
    global BugTime
    
    if not Exit:
        Ants.THINKNOW()
        ObjectClearing()
        UpdateFood()
        Render()
        if FoodTime != -1:
            FoodTime += 1
            if FoodTime > EnergyRate:
                FoodSpawner()
                FoodTime = 0
            
        if EnergyTime != -1:
            EnergyTime += 1
            if EnergyTime > FoodSpawnRate:
                EnergyConsumer()
                EnergyTime = 0
            
        if BugTime != -1:
            BugTime += 1
            if BugTime > BugSpawnRate:
                BugSpawner()
                BugTime = 0
            
        if not Exit:
            if not Pause:
                mainwindow.after(updatetime, UpdateEveryTick)

def ForcedTickUpdate():
    Ants.THINKNOW()
    ObjectClearing()
    UpdateFood()
    Render()
    
def EnergyConsumer():
    Ants.AntsEnergy()

def FoodSpawner():
    Ants.AntsEnergy()
    RandomFoodAppear()
    #Ants.CreateBug()
    
def BugSpawner():
    Ants.CreateBug()
    #RandomFoodAppear()

def SetPause(Set=False, SetTo=True):
    #print("SetPause")
    global mainwindow
    global updatetime
    global Pause
    Pause = not (Pause)
    if Set:
        Pause = SetTo
    if not Pause:
        mainwindow.after(updatetime, UpdateEveryTick)

def Render():
    global GameCanvas
    global HomeRendered
    #GameCanvas.delete("all")
    RenderBugs = Ants.BugsRender()
    #print(RenderBugs)
    for Bug in RenderBugs:
        if Bug[0] in BugsRendered:
            ID = BugsRendered[Bug[0]]
            GameCanvas.moveto(ID, Bug[1]-25, Bug[2]-25)
            GameCanvas.itemconfigure(ID, image=BugTextures[Bug[3]])
        else:
            ID = Bug[0]
            ID2 = GameCanvas.create_image(Bug[1], Bug[2], image=BugTextures[Bug[3]], anchor=NW, tags = "bug")
            BugsRendered.update({ID: ID2})
    RenderAnts = Ants.AntsRender()
    for Ant in RenderAnts:
        if Ant[0] in AntsRendered:
            ID = AntsRendered[Ant[0]]
            GameCanvas.moveto(ID, Ant[1]-13, Ant[2]-13)
            GameCanvas.itemconfigure(ID, image=AntTextures[Ant[3]])
        else:
            ID = Ant[0]
            ID2 = GameCanvas.create_image(Ant[1], Ant[2], image=AntTextures[Ant[3]], anchor=NW, tags = "ant")
            AntsRendered.update({ID: ID2})
            # lmao
    RenderFoods = World.FoodRender()
    for Food in RenderFoods:
        if not(Food[0] in FoodRendered):
            ID = Food[0]
            ID2 = GameCanvas.create_image(Food[1]-25, Food[2]-25, image=FoodTextures[Food[3]], anchor=NW, tags = "food")
            FoodRendered.update({ID: ID2})
        else:
            ID2 = FoodRendered[Food[0]]
            GameCanvas.itemconfigure(ID2, image = FoodTextures[Food[3]])
    # Do something with this pls
    if not HomeRendered:
        HomeRendered = GameCanvas.create_image(SizeXSize//2, SizeXSize//2, image=HomeImg, anchor=CENTER, tags = "home")

    
    for ID in DeleteAnts:
        ID2 = AntsRendered[ID]
        GameCanvas.delete(ID2)
    for ID in DeleteFoods:
        ID2 = FoodRendered[ID]
        GameCanvas.delete(ID2)
    for ID in DeleteBugs:
        ID2 = BugsRendered[ID]
        GameCanvas.delete(ID2)
    DeleteFoods.clear()
    DeleteAnts.clear()
    DeleteBugs.clear()

def kill():
    mainwindow.destroy()
    sys.exit(0)


def CreateNewMenu():
    global mainwindow
    global MenuFrame
    MenuFrame.place(relx=.5, rely=.5,anchor= CENTER)

def AntSPIN():
    #print("AntSPIN")
    global mainwindow
    global AntSpin
    if not StopSpin:
        if AntSpin == 0:
            MenuLabel.configure(image=AntToLeftImg)
            AntSpin = 1
            ##print(1)
        elif AntSpin == 1:
            MenuLabel.configure(image=AntToUpImg)
            AntSpin = 2
            ##print(2)
        elif AntSpin == 2:
            MenuLabel.configure(image=AntToRightImg)
            AntSpin = 3
            ##print(3)
        elif AntSpin == 3:
            MenuLabel.configure(image=AntToDownImg)
            AntSpin = 0
            ##print(0)
        mainwindow.after(250,AntSPIN)

def StartSPIN(event):
    #print("StartSPIN")
    global StopSpin
    if StopSpin == True:
        StopSpin = False
        AntSPIN()
    else:
        StopSpin = True

def DragStart(event):
    #print("DragStart")
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y
    #print(f"x = {event.x}\ny = {event.y}\n")

def DragMove(event):
    #print("DragMove")
    global mainwindow
    widget = event.widget
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    if x > 0:
        x = 0
    if y > 0:
        y = 0
    if x < -(widget.winfo_width() - mainwindow.winfo_width()):
        x = -(widget.winfo_width() - mainwindow.winfo_width())
    if y < -(widget.winfo_height() - mainwindow.winfo_height()):
        y = -(widget.winfo_height() - mainwindow.winfo_height())
    widget.place(x=x,y=y)
    ##print(widget.winfo_height())
    ##print(widget.winfo_width())
    ##print(mainwindow.winfo_height())
    ##print(mainwindow.winfo_width())
    ##print(f"x = {x}\ny = {y}\n")
    ##print(widget.winfo_geometry())
	
def MoveUp(event):
    #print("MoveUp")
    global GameCanvas
    global mainwindow
    widget = GameCanvas
    x = widget.winfo_x()
    y = widget.winfo_y() + 10
    if y > 0:
        y = 0
    widget.place(x=x,y=y)
    ##print(f"x = {x}\ny = {y}\n")
    ##print(widget.winfo_geometry())


# Появился, значит, на зоне Чёрный Сталкер

def MoveDown(event):
    #print("MoveDown")
    global GameCanvas
    global mainwindow
    widget = GameCanvas
    x = widget.winfo_x()
    y = widget.winfo_y() - 10
    if y < -(widget.winfo_height() - mainwindow.winfo_height()):
        y = -(widget.winfo_height() - mainwindow.winfo_height())
    widget.place(x=x,y=y)
    ##print(f"x = {x}\ny = {y}\n")
    ##print(widget.winfo_geometry())

def MoveLeft(event):
    #print("MoveLeft")
    global GameCanvas
    global mainwindow
    widget = GameCanvas
    x = widget.winfo_x() + 10
    y = widget.winfo_y()
    if x > 0:
        x = 0
    widget.place(x=x,y=y)
    ##print(f"x = {x}\ny = {y}\n")
    ##print(widget.winfo_geometry())

def MoveRight(event):
    #print("MoveRight")
    global GameCanvas
    global mainwindow
    widget = GameCanvas
    x = widget.winfo_x() - 10
    y = widget.winfo_y()
    if x < -(widget.winfo_width() - mainwindow.winfo_width()):
        x = -(widget.winfo_width() - mainwindow.winfo_width())
    widget.place(x=x,y=y)
    ##print(f"x = {x}\ny = {y}\n")
    ##print(widget.winfo_geometry())

def FrameLoadCreate():
    global LoadScreen
    #global LoadScroll
    FrameLoad = Frame(master = LoadScreen, width=350)
    SaveNames = FindSaves()
    for SaveName in SaveNames:
        File = open(SaveName)
        NameOfSave = File.readline()
        File.close()
        Button(master=FrameLoad, width=20, text=NameOfSave,font=("ComicSansMS", 20, "bold"), command=lambda: LoadThisSave(SaveName)).pack()

    ButtonBackToMenu.place(x=10, y=10)
    return FrameLoad

def FrameLoadClear():
    global FrameLoad
    FrameLoad.destroy()
    
def FrameLevelCreate():
    global LevelFrame
    FrameLevel = Frame(master = LevelFrame)
    LevelNames = FindLevels()
    for LevelName in LevelNames:
        File = open(LevelName)
        NameOfLevel = File.readline()
        File.close()
        Button(master=FrameLevel, width=20, text=NameOfLevel, font=("ComicSansMS", 20, "bold"), command = lambda: LoadThisLevel(LevelName)).pack()

    ButtonBackFromLevel.place(x=10, y=10)
    return FrameLevel
    
def FrameLevelClear():
    global FrameLevel
    FrameLevel.destroy()
    
def SetAttackDefence(SetIsAttack=False, SetIsDefend=False):
    Ants.SetIsAttack(SetIsAttack)
    Ants.SetIsDefend(SetIsDefend)

def ClickAttackPoint(event):
    #print("ClickAttackPoint")
    SetAttackDefence(True, False)
    Ants.SetAttackPoint(event.x, event.y)
    #print(f"DEBUG: AttackPoint x = {event.x}, y = {event.y}")
    ClickAttack()

def ClickAttack():
    global AttackBindID
    global GameCanvas
    global IsAttackClicked
    if IsAttackClicked:
        GameCanvas.unbind("<Button-1>")
        IsAttackClicked = False
        GameCanvas.bind("<Button-1>", DragStart)
        #GameCanvas.bind("<ButtonRelease-1>", DragMove)
    else:
        #SetAttackDefence(True, False) << Not now!! 
        #GameCanvas.unbind("<Button-1>")
        #GameCanvas.unbind("<ButtonRelease-1>")
        AttackBindID = GameCanvas.bind("<Button-1>", ClickAttackPoint, add="+")
        IsAttackClicked = True

def ClickDefence():
    global IsAttackClicked
    if IsAttackClicked:
        ClickAttack()
    SetAttackDefence(False, True)
    
def ClickNeutral():
    global IsAttackClicked
    if IsAttackClicked:
        ClickAttack()
    SetAttackDefence(False,False)

def TechDragStart(event): pass
    #print("TechDragStart")
def TechDragMove(event): pass
    #print("TechDragMove")
# Params
AntsResearched = Tech.GetUnlockedAnts()
TileType = "Grass"
HomeRendered = 0
AttackBindID = 0
EnergyRate = 50
BugSpawnRate = 500
FoodSpawnRate = 500
AntSpin = 0
StopSpin = True
IsAttackClicked = False
ListDelete = [] # Type, ID
SizeOfTheWorld = 100
SizeOfTheBlock = 30
SizeXSize = SizeOfTheBlock*SizeOfTheWorld
RenderScale = 1
CanvasSize = SizeXSize * RenderScale
FPS = 30
BACKGROUND_COLOR = "#000000"
tickrate = 30 
updatetime = 1000 // tickrate
if updatetime < 20:
    updatetime = 20
Exit = False
FoodTime = 0
BugTime = 0
EnergyTime = 0
AntsRendered = {}
FoodRendered = {}
HomesRendered = {}
BugsRendered = {}
DeleteAnts = []
DeleteFoods = []
DeleteBugs = []
AntsHeads = [["default", 1, 1, 1, 1, 1, 1], ["Solder", 6, 5, 2, 4, 8, 1], ["Worker", 1, 1, 1, 2, 2, 3], ["Watcher", 0, 1, 1, 1, 1, 1, 1]] # Name, HealthBonus, Attack, AttackRange, Cost, EnergyNeed, WorkEfficiency
AntsBodies = [["default", 1, 2, 2, 1], ["armored", 6, 1, 12, 4], ["scout", 1, 4, 4, 3] ] # Name, HealthBonus, SpeedBonus, Cost, EnergyNeed
AntsBellies = [["default", 1, 100, 0], ["light", -1, 80, 1], ["worker", 0, 200, 0], ["heavy", 4, 500, -2]] # Name, HealthBonus, EnergyStorage, SpeedBonus
States = ["default","Attack","Defend","Scout", "FoodFound","CreatingWay", "Worker", "GoingWay", "WhereFood","NoFood","YesFood", "TakeFood", "InHome", "Solder", "NeedFood", "Lost"]
AntSolder = [1, 1, 3]
AntWorker = [2, 0, 2]
AntScout = [3, 2, 1]
SolderCost = AntsHeads[1][4] + AntsBodies[1][3]
ScoutCost = AntsHeads[3][4] + AntsBodies[2][3]
WorkerCost = AntsHeads[2][4] + AntsBodies[0][3]
NEDOSTUPNO = "НЕДОСТУПНО"

# GUI PART
mainwindow = Tk()
mainwindow.geometry("800x600")
#mainwindow.resizable(False,False)
mainwindow.title("Ants")
mainwindow.iconbitmap("imgs/anticon.ico")
#mainwindow.attributes("-fullscreen", 1)

AntToLeftImg = PhotoImage(file="imgs/antleft.png")
AntToUpImg = PhotoImage(file="imgs/antup.png")
AntToRightImg = PhotoImage(file="imgs/antright.png")
AntToDownImg = PhotoImage(file="imgs/antdown.png")
AntToUpLeftImg = PhotoImage(file="imgs/antupleft.png")
AntToUpRightImg = PhotoImage(file="imgs/antupright.png")
AntToDownRightImg = PhotoImage(file="imgs/antdownright.png")
AntToDownLeftImg = PhotoImage(file="imgs/antdownleft.png")

SAntToLeftImg = PhotoImage(file="imgs/Santleft.png")
SAntToUpImg = PhotoImage(file="imgs/Santup.png")
SAntToRightImg = PhotoImage(file="imgs/Santright.png")
SAntToDownImg = PhotoImage(file="imgs/Santdown.png")
SAntToUpLeftImg = PhotoImage(file="imgs/Santupleft.png")
SAntToUpRightImg = PhotoImage(file="imgs/Santupright.png")
SAntToDownRightImg = PhotoImage(file="imgs/Santdownright.png")
SAntToDownLeftImg = PhotoImage(file="imgs/Santdownleft.png")

BugToUp = PhotoImage(file="imgs/bugup.png")
BugToDown = PhotoImage(file="imgs/bugdown.png")
BugToLeft = PhotoImage(file="imgs/bugleft.png")
BugToRight = PhotoImage(file="imgs/bugright.png")

HomeImg = PhotoImage(file="imgs/home.png")
Home1Img = PhotoImage(file="imgs/home1.png")
Home2Img = PhotoImage(file="imgs/home2.png")
Home3Img = PhotoImage(file="imgs/home3.png")
HomesImgs = {1: Home1Img, 2: Home2Img, 3: Home3Img}
FoodImg11 = PhotoImage(file="imgs/foodsmol1.png").subsample(2,2)
FoodImg12 = PhotoImage(file="imgs/foodsmol2.png").subsample(2,2)
FoodImg21 = PhotoImage(file="imgs/mediumfood1.png").subsample(2,2)
FoodImg22 = PhotoImage(file="imgs/mediumfood2.png").subsample(2,2)
FoodImg31 = PhotoImage(file="imgs/bigfood1.png").subsample(2,2)
FoodImg32 = PhotoImage(file="imgs/bigfood2.png").subsample(2,2)

GrassImg = PhotoImage(file="imgs/grass.png")
AsphaltImg = PhotoImage(file="imgs/32xAsphalt.png")
SandImg = PhotoImage(file="imgs/32xSand.png")
Tiles = {"Grass": GrassImg, "Asphalt": AsphaltImg, "Sand": SandImg}

AttackImg = PhotoImage(file="imgs/ATK.png").zoom(2,2)
DefendImg = PhotoImage(file="imgs/DEF.png").zoom(2,2)
NeutralImg = PhotoImage(file="imgs/NT.png").zoom(2,2)

FoodTextures = { 11: FoodImg11,
12: FoodImg12,
21: FoodImg21,
22: FoodImg22,
31: FoodImg31,
32: FoodImg32, } 

BugTextures = {"up": BugToUp,
"down":BugToDown,
"left":BugToLeft,
"right":BugToRight,
"Bup": BugToUp.zoom(2, 2),
"Bdown":BugToDown.zoom(2, 2),
"Bleft":BugToLeft.zoom(2, 2),
"Bright":BugToRight.zoom(2, 2) }

AntTextures = {110: AntToDownImg.subsample(2,2),
112: AntToDownRightImg.subsample(2,2),
111: AntToDownLeftImg.subsample(2,2),
120: AntToUpImg.subsample(2,2),
122: AntToUpRightImg.subsample(2,2),
121: AntToUpLeftImg.subsample(2,2),
102: AntToRightImg.subsample(2,2),
101: AntToLeftImg.subsample(2,2),
210: SAntToDownImg.subsample(2,2),
212: SAntToDownRightImg.subsample(2,2),
211: SAntToDownLeftImg.subsample(2,2),
220: SAntToUpImg.subsample(2,2),
222: SAntToUpRightImg.subsample(2,2),
221: SAntToUpLeftImg.subsample(2,2),
202: SAntToRightImg.subsample(2,2),
201: SAntToLeftImg.subsample(2,2),
310: AntToDownImg.subsample(3,3),
312: AntToDownRightImg.subsample(3,3),
311: AntToDownLeftImg.subsample(3,3),
320: AntToUpImg.subsample(3,3),
322: AntToUpRightImg.subsample(3,3),
321: AntToUpLeftImg.subsample(3,3),
302: AntToRightImg.subsample(3,3),
301: AntToLeftImg.subsample(3,3) }

# Menu
MenuFrame = Frame(master=mainwindow, width=200, height=200)
MenuLabel = Label(master=MenuFrame, image = AntToUpImg, compound="left", text="ANTS", font=("ComicSansMS", 40, "bold"))
ButtonLevel = Button(master=MenuFrame, text="Уровень", font=("ComicSansMS", 20, "bold"), width=10, command=LoadLevel)
ButtonStart = Button(master=MenuFrame, text="Новая игра",font=("ComicSansMS", 20, "bold"),width=10, command=StartNewGame)
ButtonLoad = Button(master=MenuFrame, text="Загрузить",font=("ComicSansMS", 20, "bold"),width=10, command=LoadGame)
ButtonExit = Button(master=MenuFrame, text="Exit",font=("ComicSansMS", 20, "bold"),width=10, command=kill)
MenuLabel.pack()
ButtonLevel.pack()
ButtonStart.pack()
ButtonLoad.pack()
ButtonExit.pack()
MenuLabel.bind("<Button-1>", StartSPIN)
CreateNewMenu()
Pause = False
#Other
AntWorkerText = "Рабочий "+str(WorkerCost)
AntScoutText = "Разведчик "+str(ScoutCost)
AntSolderText = "Солдат "+str(SolderCost)
GameFrame = Frame(master=mainwindow, width=200, height=40)
FoodCount = Label(master=GameFrame, text="0", font=("ComicSansMS", 12, "bold"),width=10)
ButtonWorker = Button(master=GameFrame, text=NEDOSTUPNO,font=("ComicSansMS", 12, "bold"),width=10, command=WorkerButton)
ButtonScout = Button(master=GameFrame, text=NEDOSTUPNO,font=("ComicSansMS", 12, "bold"),width=10, command=ScoutButton)
ButtonSolder = Button(master=GameFrame, text=NEDOSTUPNO,font=("ComicSansMS", 12, "bold"),width=10, command=SolderButton)
ButtonPause = Button(master=GameFrame, text="Пауза",font=("ComicSansMS", 12, "bold"),width=10, command=SetPause)
ButtonGO = Button(master=GameFrame, text="Сохранить",font=("ComicSansMS", 12, "bold"),width=10, command=SaveSaver)
ButtonToMenu = Button(master=GameFrame, text="Меню",font=("ComicSansMS", 12, "bold"),width=10, command=ShowMiniMenu) 
ButtonToTech = Button(master=GameFrame, text="Технологии",font=("ComicSansMS", 12, "bold"),width=10, command=ShowTech) 
# Canvas
GameCanvas = Canvas(mainwindow, width = CanvasSize, height = CanvasSize, bg="black")
GameCanvas.bind("<Button-1>", DragStart)
GameCanvas.bind("<ButtonRelease-1>", DragMove)
mainwindow.bind("<Up>",MoveUp)
mainwindow.bind("<Down>",MoveDown)
mainwindow.bind("<Left>",MoveLeft)
mainwindow.bind("<Right>",MoveRight)

## Load Frame

LoadScreen = Frame(master = mainwindow)
#LoadScroll = Scrollbar(master=LoadScreen, orient='vertical')
#LoadScroll.config(command=LoadScreen.xview)
#LoadScroll.pack(side = RIGHT, fill = Y)
ButtonBackToMenu = Button(master=LoadScreen, text="Назад",font=("ComicSansMS", 20, "bold"), command=BackFromLoad)
ScrollY = 0
FrameLoad = FrameLoadCreate()
FrameLoad.place(relx=.5, y=0, anchor= CENTER)
'''FrameLoad = Frame(master = LoadScreen, width=350)
SaveNames = FindSaves()
for SaveName in SaveNames:
    File = open(SaveName)
    NameOfSave = File.readline()
    File.close()
    Button(master=FrameLoad, text=NameOfSave,font=("ComicSansMS", 20, "bold"), command=lambda: LoadThisSave(SaveName)).pack()

ButtonBackToMenu.place(x=10, y=10)
FrameLoad.place(relx=.5, rely=.5, anchor= CENTER)'''
## End load frame

# LevelFrame

LevelFrame = Frame(master = mainwindow)
ButtonBackFromLevel = Button(master=LevelFrame, text="Назад",font=("ComicSansMS", 20, "bold"), command=BackFromLevel)
FrameLevel = FrameLevelCreate()
FrameLevel.place(relx=.5, y=0, anchor=N)


# End Level Frame

# Mini Menu
MiniMenu = Frame(master=mainwindow, bg="white")
MMB1 = Button(master=MiniMenu, text="Продолжить",font=("ComicSansMS", 12, "bold"),width=10, command=HideMiniMenu)
MML = Label(master=MiniMenu, text="Имя сохранения:", font=("ComicSansMS", 12, "bold"))
MMT1 = Text(master=MiniMenu, height=1, width=20, font=("ComicSansMS", 12, "bold"))
MMB2 = Button(master=MiniMenu, text="Сохранить",font=("ComicSansMS", 12, "bold"),width=10, command=SaveSaver)
MMB3 = Button(master=MiniMenu, text="Выход",font=("ComicSansMS", 12, "bold"),width=10, command=BackToMenu)
MMB1.pack()
MML.pack()
MMT1.pack()
MMB2.pack()
MMB3.pack()
# Mini end

# Attack & Defend 
AttackDefend = Frame(master = mainwindow)
AttackButton = Button(master= AttackDefend, image=AttackImg, command=ClickAttack)
DefendButton = Button(master= AttackDefend, image=DefendImg, command=ClickDefence)
NeutralButton = Button(master= AttackDefend, image=NeutralImg, command=ClickNeutral)
StateLabel = Label(master= AttackDefend, text="")
AttackButton.grid(column=0, row=1)
DefendButton.grid(column=1, row=1)
NeutralButton.grid(column=2, row=1)
#Attack & Defend End

#TechTreeFrame
TechTreeButtons = {}
BigTechFrame = Frame(master = mainwindow, bg="#F0F8FF", width = 700, height = 500)
TechTreeFrame = Frame(master = BigTechFrame, bg="#F0F8FF")
TechTreeFrame.bind("<Button-1>", TechDragStart)
TechTreeFrame.bind("<ButtonRelease-1>", TechDragMove)
CloseTech = Button(master = BigTechFrame, text = "X", command=HideTech)
#CloseTech.pack(anchor=NE, ipadx=1, ipady=1)
#TechTreeFrameEnd
UpdateAntButtons()
print("Startup sucsessfull!")
mainwindow.mainloop()
