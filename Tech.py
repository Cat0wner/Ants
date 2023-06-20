import json

# All Worker Watcher Solder

# Tech File Structure

# Head (idk just something)

# Body
# { "TechName/TechID": {"TechLevel": 1, "TechName": "Технология", "TechCost": 100, "IsOpened": 1, "TechRequired": ["TechID1", "TechID2"], "AntsRequired|: [0, 0, 0, 0], "Description": "TextDesc", "Column": 0, "Row": 0, "Mod": {11: {"Health": 1}}, "Comands": {"OpenSolders": 1, "SetTechLevel": 2}} ,  }

# End
def TechOpener(FileDir = "technology/Tech.anttech"):
    TechFile = open(FileDir, "r")
    #Idk = TechFile.readline()
    Teches = TechFile.readline()
    #print("TechOpener")
    return json.loads(Teches)
    
def LoadTechFromSaveOld(FileDir = "technology/default.antsave"):
    global Tech
    File = open(FileDir, "r")
    File.readline()
    File.readline()
    Teches = File.readline()
    if Teches:
        Tech = json.loads(Teches)
    else:
        SetTechToDefault()
    #print("LoadTechFromSaveOld")
    
def LoadTechFromSave(FileDir):
    global Tech
    File = open(FileDir, "r")
    File.readline()
    File.readline()
    Teches = File.readline() # Ну канешн третья строка, первая и вторая заняты названием и данными
    if Teches:
        OpenedTeches = json.loads(Teches)
        for Technology in OpenedTeches:
            #print(Technology)
            OpenThisTechPls(Technology)
    else:
        SetTechToDefault()
    #print("LoadTechFromSave")
        
    
def GetOpenedTechesIDs():
    global Tech
    ReturnThis = []
    for LeTech in Tech:
        if Tech[LeTech]["IsOpened"] == 1:
            ReturnThis.append(LeTech)
    #print("GetOpenedTechesIDs")
    return ReturnThis
    
    
def SetTechToDefault():
    global Tech
    global TechLevel
    global AntsResearched
    AntsResearched = {"Worker1": 0, "Worker2": 0, "Worker3": 0, "Solder1": 0, "Solder2": 0, "Solder3": 0, "Watcher1": 0, "Watcher2": 0, "Watcher3": 0, }
    Tech = TechOpener()
    TechLevel = 1
    OpenTechByDefault()
    #for th in Tech: print(th)
    #print("Tech now default")
    #print("SetTechToDefault")
    
def GetOpenedTeches(Opened = True):
    ReturnThis = {}
    if Opened:
        for LeTech in Tech:
            if Tech[LeTech]["IsOpened"] == 1:
                ReturnThis.update({LeTech: Tech[LeTech]})
    else:
        for LeTech in Tech:
            if Tech[LeTech]["IsOpened"] != 1:
                ReturnThis.update({LeTech: Tech[LeTech]})
    #print("GetOpenedTeches")
    return ReturnThis

def IsTechOpen(TechID):
    global Tech
    #print("IsTechOpen")
    return Tech[TechID]["IsOpened"]

def CanIOpenThisTech(TechID, Food=0, Ants=[0,0,0,0]): # All, Worker Scout Solder
    global Tech
    global TechLevel
    #print("CanIOpenThisTech")
    TheTech = Tech[TechID]
    if IsTechOpen(TechID) == 1: return -2
    if TheTech["TechCost"] < Food and TechLevel >= TheTech["TechLevel"]:
        if (TheTech["AntsRequired"][0] <= Ants[0] and TheTech["AntsRequired"][1] <= Ants[1]) and (TheTech["AntsRequired"][2] <= Ants[2] and TheTech["AntsRequired"][3] <= Ants[3]):
            for ReqTech in TheTech["TechRequired"]:
                if IsTechOpen(ReqTech) != 1:
                    return -1
            return TheTech["TechCost"] # Возращаем стоимость в еде, да-да. 
    return -1
# В main мы тыкаем кнопку технологии
# Вызывается CanIOpenThisTech
# Возвращается количество еды
# Если не равно -1 => Вызываем OpenThisTechPls
# Технология открывается
# И дальше вызывается возврат всех модов, чтобы заменить ими те, что в main
# О, и это будет низкий уровень, как World, все вызывают, но Tech не вызывает никого
# И муравьи при создании вызывают свои модификаторы
# Да, звучит как план.


def OpenThisTechPls(TechID):
    global Tech
    Tech[TechID]["IsOpened"] = 1
    UpdateModsFromTech(Tech[TechID]["Mod"])
    DoAllTheCommands(Tech[TechID]["Comands"])
    return 0
    #print("OpenThisTechPls")
    
def ReturnListOfTech():
    global Tech
    #print("ReturnListOfTech")
    return Tech

# Короче:
# Технологии грузятся
# При новой игре - ставятся по умолчанию
# Как делать модификаторы? 
# Можно получать их все вместе, наверное. Можно при улучшении выдавать модификаторы
# Как его сделать? Ну, хер знает. А впрочем...
# Mods: Модифицируют некоторое значение в main на +/-
# Comands: Выполняют некоторые функции - например, устанавливают уровень технологий на другой или делают что-то ещё.
# Как же всё это возвращать обратно в уехавшую крышу main? А не ебу, пара функций поможет.

def UpdateModsFromTech(TechMods):
    global Mods
    for ModTarget in TechMods:
        for Mod in TechMods[ModTarget]:
            Mods[ModTarget][Mod] += TechMods[ModTarget][Mod]
    #print("UpdateModsFromTech")
            

def DirectModUpdate(Target, Mod, Number):
    global Mods
    Mods[Target][Mod] = Number
    #print("DirectModUpdate")

def SetModsToDefault():
    global Mods
    AllMods = {"Speed": 0, "Strenght": 0, "Health": 0}
    SolderMods = {"Speed": 0, "Strenght": 0, "Health": 0, "Armor": 0}
    ScoutMods = {"Speed": 0, "Strenght": 0, "Health": 0, "Vision": 0}
    WorkerMods = {"Speed": 0, "Strenght": 0, "Health": 0, "Cost": 0, "WorkEfficiency": 0}
    Mods = {"11": AllMods, "3333": SolderMods, "2222": ScoutMods, "1111": WorkerMods }
    #print("Mods now default")
    #print("SetModsToDefault")

def ReturnAllMods(): 
    # Lmao. Rofl. Но тип норм на всякий случай после нажатия апдейта возвращать все модификаторы обратно в main
    global Mods
    #print("ReturnAllMods")
    return Mods
    
def ReturnMod(Target, Mod = ""):
    global Mods
    #print("ReturnMod")
    #print(Target)
    #print(Mod)
    if Mod == "":
        if str(Target) in Mods: return Mods[str(Target)]
        else: return {"Speed": 0, "Strenght": 0, "Health": 0}
    else:
        if Mod in Mods[str(Target)]: return Mods[str(Target)][Mod]
        else: return 0
        
#def SetT ????

def ReturnTechLevel():
    global TechLevel
    #print("ReturnTechLevel")
    return TechLevel

def OpenTechByDefault():
    OpenThisTechPls("AntWorker")
    OpenThisTechPls("AntScout")
    #print("Am i in console?")
    #print("OpenTechByDefault")
    
#================|
#  /\        /\  |
#                |
#  >!<     >!<   |
#                |
#      v--v      |
#                |
#________________|
def DoAllTheCommands(TextCommand):
    global AwaitingForOrders
    for Com in TextCommand:
        if Com in AwaitingForOrders:
            AwaitingForOrders[Com](TextCommand[Com])
        else:
            pass
            #print("You fucked up with comands man")
    #print("DoAllTheCommands")
    
def SetTechLevel(To):
    global TechLevel
    if To in range(TechLevel, TechLevelMax+1) and To >= TechLevel:
        TechLevel = To
        #print(f"TechLevel now is {To}!")
    #print("SetTechLevel")
        
def UnlockAnt(WhichOne, UnLock = 1):
    global AntsResearched
    if WhichOne in AntsResearched:
        AntsResearched[WhichOne] = UnLock
        #print(f"{WhichOne} unlocked!")
    else:
        pass
        #print("The fuck?!")
    #print("UnlockAnt")

def GetUnlockedAnts():
    global AntsResearched
    return AntsResearched
    #print("GetUnlockedAnts")

'''def DoSomethingPlsIDunno():
    So if tech did something - how did we know that? Answer: We dont
    But we know what the tech dont do, so we can calculate
    by some of the ev'''

AwaitingForOrders = {"OpenAnt": UnlockAnt, "SetTechLevel": SetTechLevel}
TechLevel = 1
TechLevelMax = 5
AntsResearched = {"Worker1": 0, "Worker2": 0, "Worker3": 0, "Solder1": 0, "Solder2": 0, "Solder3": 0, "Watcher1": 0, "Watcher2": 0, "Watcher3": 0, }
AllMods = {"Speed": 0, "Strenght": 0, "Health": 0} # ACHUALLY, why just dont return this??? No reason. See. Just save it. Redact it. Use it.
SolderMods = {"Speed": 0, "Strenght": 0, "Health": 0, "Armor": 0}
ScoutMods = {"Speed": 0, "Strenght": 0, "Health": 0, "Vision": 0}
WorkerMods = {"Speed": 0, "Strenght": 0, "Health": 0, "Cost": 0, "WorkEfficiency": 0}
Mods = {"11": AllMods, "3333": SolderMods, "2222": ScoutMods, "1111": WorkerMods }
ModsCopy = Mods.copy()
# So, when we first open this - all mods sets to default
Tech = TechOpener()
OpenTechByDefault()