from Ants import GetAntMind
from World import FindEnemies
from World import ScanRadiusAround
from World import HomeXY
from World import GetListOfWPs
from World import GetListOfObjects
from math import sqrt
from math import sin
from math import radians
from math import acos
from math import degrees
from random import randint

#So i ant and i need to do some ant stuff
# ActorType is saved as head, so...

def AutoMove(x1, y1, x2, y2): # i really need function that can return angle and distance to target, AND DONT DO THIS MANUALLY EVERY FUCKING TIME БЛЯТЬ СУКА
    DistanceX = x2 - x1
    DistanceY = y2 - y1
    Dx = abs(DistanceX)
    Dy = abs(DistanceY)
    Hptz = sqrt(Dx*Dx + Dy*Dy)
    if (DistanceX >= 0):
        if (DistanceY >= 0): # 1 y - основа (0+0)
            Angle = degrees(acos(Dx/Hptz))
            return [Angle, Hptz]
        else: # 2 x - основа (0+90)
            Angle = degrees(acos(Dy/Hptz))
            return [Angle+90, Hptz]
    else:
        if (DistanceY >= 0): #4 x - основа (0+270)
            Angle = degrees(acos(Dy/Hptz))
            return [Angle+270, Hptz]
        else: # 3 y - основа (0+180)
            Angle = degrees(acos(Dx/Hptz))
            return [Angle+180, Hptz]
    pass

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
    for ObjectID in ListOfID: 
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

def HelpAnotherAnt(Actor):
    AntsNeedHelp = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "ant", 3)
    for AntID in AntsNeedHelp:
        HelpAnt = AntHasBeenAttacked(AntID)
        if HelpAnt[0]:
            Actor.HasBeenAttacked = True
            Actor.HasBeenAttackedByID = HelpAnt[1]
            return 1
    return 0


def GoHome(Actor, Rand = False):
    Homes = HomeXY()
    HowToMove = AutoMove(Actor.posx, Actor.posy, Homes[0], Homes[1])
    if Rand:
        HowToMove[0] += randint(-20, 20)
    Actor.Move = (HowToMove[0], HowToMove[1])

def EatAndLeave(Actor, State):
    Actor.EatFood()
    Homes = HomeXY()
    if GetDistanceRaw(Actor.posx, Actor.posy, Homes[0], Homes[1]) > 7:
        Actor.State = State
    else:
        Actor.Move(Actor.AngleRand, 1)
        Actor.AngleRand += randint(-10, 10)
        
def ChooseWPRandom(WPList):
    for WPW in WPList:
        WeightList.append(WPW[3])
    AllWeight = sum(WeightList)
    RandWeight = randint(0, AllWeight)
    ID = 0
    # THIS IS SO STUPID WHAT THE FUCK MAN WHYYYYYYYYY??????
    # Please LEAVE CODING NOW!!!
    # Or at least use NumPy
    while RandWeight > 0:
        RandWeight -= WeightList[ID]
        ID+=1
    return WeightList[ID]
    
def MoveAroundHome(Actor, GoAway = False):
    Home = HomeXY(Actor.HomeID)
    HowToMove = AutoMove(Actor.posx, Actor.posy, Home[0], Home[1])
    if GoAway:
        Actor.Move(HowToMove[0]+180, HowToMove[1])
    else:
        Actor.Move(HowToMove[0]+(60 * Actor.IDKWhereToGo), HowToMove[1])

def AntAI(Actor):
    #print(Actor)
    MyX = Actor.posx
    MyY = Actor.posy
    # BY PRIORITY
    #ATTACK
    # Если муравей не разведчик и был атакован - 
    # Муравей получает от врага ID и атакует в ответ.
    if (Actor.HasBeenAttacked == True and (Actor.Mind == 1111 or Actor.Mind == "Solder")): 
        # Теперь мы ищем ближайшего врага в нашем блоке, кому дать пизды
        
        # FAST ATTACK
        
        EnemyID = Actor.HasBeenAttackedByID
        TheyXY = BugXY(EnemyID)
        if TheyXY != -1:# Проверяем то, что враг ещё существует
        
            # Distance Check
            TheyX = TheyXY[0]
            TheyY = TheyXY[1]
            # Если можно атаковать в ответ = атакуем. Нет - движемся к атаковавшему противнику.
            if DistanceCheckForAttack(MyX, MyY, TheyX, TheyY, Actor.AttackRange):
                Actor.Attack(EnemyID)
                return 0
            else:
                HowToMove = AutoMove(MyX, MyY, EnemyX, EnemyY)
                Actor.Move = (HowToMove[0], HowToMove[1])
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
                Actor.Move = (HowToMove[0], HowToMove[1])
                return 0
        else: # Если враг не найден - выключаем бой
            Actor.HasBeenAttacked = False
            
    if (Actor.HasBeenAttacked == True and Actor.Mind == 2222): # Ну а если муравей - разведчик - побег
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
                Actor.Move = (HowToMove[0], HowToMove[1])
                return 0
            else: # Если нет - атакует.
                if (ClosestEnemy[3] < Actor.AttackRange*2):
                    Actor.Attack(EnemyID)
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, EnemyX, EnemyY)
                    Actor.Move = (HowToMove[0], HowToMove[1])
                    return 0
        
    if (Actor.Energy < (Actor.MaxEnergy // 4)) and (Actor.State != "Lost"): # Муравьхи гхолодные????
        Actor.State = "NeedFood"

    if (Actor.Mind == "Solder"): # Основной ИИ Солдата
    
        if Actor.State == "InHome":
            EatAndLeave(Actor, "Solder")
            return 0

        if Actor.State == "Solder":
            EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 2)
            if (EnemyList):
                ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
                if ClosestEnemy[3] < Actor.AttackRange*2:
                    Actor.Attack(ClosestEnemy[0])
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                    Actor.Move = (HowToMove[0], HowToMove[1])
                    return 0
            if HelpAnotherAnt(Actor) == 1:
                return 0
            else: # Patrol waypoints
                WPs = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
                if (WPs):
                    ClosestWP = GetClosest(MyX, MyY, WPs, "way")
                    DistanceToWP = GetDistance(Actor, ListOfWPs[ClosestWP[0]])
                    if DistanceToWP > 2:
                        HowToMove = AutoMove(MyX, MyY, ClosestWP[1], ClosestWP[2])
                        Actor.Move = (HowToMove[0], HowToMove[1])
                        return 0
                    else:
                        Actor.GoWayPoint(ClosestWP) # WP добавляется в память и при скане исключается из списка, после чего муравей идёт к следующему ближайшему WP
                else: # Если их нет, то муравей направляется к дому
                    HomeX = ListOfHomes[Actor.HomeID].posx
                    HomeY = ListOfHomes[Actor.HomeID].posy
                    HowToMove = AutoMove(MyX, MyY, HomeX, HomeY)
                    Actor.Move = (HowToMove[0], HowToMove[1])
                    return 0

        if Actor.State == "NeedFood":
            EnemyList = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "bug", 1)
            if (EnemyList):
                ClosestEnemy = GetClosest(MyX, MyY, EnemyList, "bug")
                if ClosestEnemy[3] < Actor.AttackRange*2:
                    Actor.Attack(ClosestEnemy[0])
                    return 0
                else:
                    HowToMove = AutoMove(MyX, MyY, ClosestEnemy[1], ClosestEnemy[2])
                    Actor.Move = (HowToMove[0], HowToMove[1])
                    return 0
            if HelpAnotherAnt(Actor) == 1:
                return 0
            else:
                if (GetDistance(Actor, ListOfHomes[Actor.HomeID]) > 5):
                    GoHome(Actor)
                    return 0
                else:
                    Actor.State = "InHome"
                    return 0
                

    #FOR WORKER
    if (Actor.Mind == 1111):
    
        if Actor.State == "InHome":
            EatAndLeave(Actor, 1111)
            Actor.PutFoodHome()
            return 0
            
        if Actor.State == 1111: # Ищем первый попавшийся WP
            WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
            if (WayPoints):
                WPArray = []
                for WPID in WayPoints:
                    WPArray.append(ListOfWPs(WPID).GetIDXYW())
                WP = ChooseWPRandom(WPArray) # ID, X, Y, Weight
                Actor.GoWayPoint(WP[0])
                HowToMove = AutoMove(Actor.posx, Actor.posy, WP[1], WP[2])
                Actor.Move(HowToMove[0]+randint(-15, 15), HowToMove[1])
                Actor.State = "GoingWay"
                return 0
            else: 
                if GetDistance(Actor, ListOfHomes[Actor.HomeID]) > 10:
                    MoveAroundHome(Actor)
                    return 0
                else:
                    MoveAroundHome(Actor, True)
                    return 0
                    
        if Actor.State == "GoingWay": #Идём по WP
            if Actor.TargetPoint[0] != -1:
                if GetDistanceRaw(Actor.posx, Actor.posy, TargetPoint[1], TargetPoint[2]) < 1:
                    Actor.GoWayPoint(TargetPoint[0])
                    if ListOfWPs[TargetPoint[0]].FinalPoint:
                        Actor.State = "WhereFood"
                    Actor.TargetPoint = -1
                    return 0
            WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 1, Actor.Memory)
            if not WayPoints:
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
            if (WayPoints): # Нашли WP - идём по нему. Не нашли - очищаем память
                WPArray = []
                for WPID in WayPoints:
                    WPArray.append(ListOfWPs(WPID).GetIDXYW())
                GoToWP = ChooseWPRandom(WPArray)
                HowToMove = AutoMove(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2])
                Actor.Move(HowToMove[0]+randint(-15, 15), HowToMove[1])
                Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                if GetDistanceRaw(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2]) < 1: # Слишком близко - считаем пройденной
                    Actor.GoWayPoint(GoToWP[0])
                    if ListOfWPs[GoToWP[0]].FinalPoint:
                        Actor.State = "WhereFood"
                return 0
            else: # Зачем? Чтобы муравей мог продолжить искать вейпоинты если зашёл в тупик, где их нет.
                Actor.MemoryClear()
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
                if not WayPoints:
                    Actor.State = "Lost"
                return 0
        
        if Actor.State == "WhereFood":
            FoodFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "food", 2)
            if FoodFound:
                Actor.State = "YesFood"
                ClosestFood = GetClosest(MyX, MyY, FoodFound, "food")
                Actor.FoodMemory = ClosestFood[0]
            else:
                Actor.State = "NoFood"
            Actor.MemoryClear()
                
        if Actor.State == "NoFood":
            if GetDistance(Actor, ListOfHomes[Actor.HomeID]) < 15: # Близко к дому - похуй, идём кушать
                Actor.State = "NeedFood"
                return 0
            if TargetPoint[0] != -1: # Короч если есть таргет - чистим его (если близко) или идём к нему (если далеко)
                if GetDistanceRaw(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2]) < 1:
                    ListOfWPs[Actor.TargetPoint[0]].LoseWeight(2)
                    Actor.GoWayPoint(TargetPoint[0])
                    TargetPoint[0] = -1
                    return 0
                else:
                    HowToMove = AutoMove(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2])
                    Actor.Move(HowToMove[0] + randint(-15, 15), HowToMove[1])
                    return 0
            WPs = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
            if WPs: # Ну таргета нет, ищем вейпоинты. И идём к понравившемуся (добавив его в таргет)
                WPArray = []
                for WPID in WPs:
                    WPArray.append(ListOfWPs(WPID).GetIDXYW())
                GoToWP = ChooseWPRandom(WPArray)
                Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                HowToMove = AutoMove(Actor.posx, Actor.posy, Actor.TargetPoint[1], Actor.TargetPoint[2])
                Actor.Move(HowToMove[0] + randint(-15, 15), HowToMove[1])
                return 0
                
        if Actor.State == "YesFood":
            OurFood = ListOfObjects[Actor.FoodMemory]
            if GetDistance(Actor, OurFood) > 2:
                HowToMove = AutoMove(Actor.posx, Actor.posy, OurFood.posx, OurFood.posy)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
            else:
                FoodSuccess = Actor.TakeFood(Actor.FoodMemory) # Need to check food
                if FoodSuccess == 0:
                    Actor.State = "NoFood"
                    Actor.FoodMemory = -1
                if FoodSuccess == 1:
                    Actor.State = "TakeFood"
                return 0
            
        if Actor.State == "TakeFood": # Да-да, ctrl+c > ctrl+v, иди нахуй, я уже заебался.
            if Actor.TargetPoint[0] != -1:
                if GetDistanceRaw(Actor.posx, Actor.posy, TargetPoint[1], TargetPoint[2]) < 1:
                    ListOfWPs[Actor.TargetPoint[0]].AddWeight()
                    Actor.GoWayPoint(TargetPoint[0])
                    if ListOfWPs[Actor.TargetPoint[0]].FinalPoint:
                        Actor.State = "NeedFood"
                    Actor.TargetPoint = -1
                    return 0
                else:
                    HowToMove = AutoMove(Actor.posx, Actor.posy)
                    Actor.Move(HowToMove[0]+randint(-15, 15), HowToMove[1])
                    return 0
            WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 1, Actor.Memory)
            if not WayPoints:
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2, Actor.Memory)
            if (WayPoints): # Нашли WP - идём по нему. Не нашли - очищаем память
                WPArray = []
                for WPID in WayPoints:
                    WPArray.append(ListOfWPs(WPID).GetIDXYW())
                GoToWP = ChooseWPRandom(WPArray)
                HowToMove = AutoMove(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2])
                Actor.Move(HowToMove[0]+randint(-15, 15), HowToMove[1])
                Actor.TargetPoint = [GoToWP[0], GoToWP[1], GoToWP[2]]
                if GetDistanceRaw(Actor.posx, Actor.posy, GoToWP[1], GoToWP[2]) < 1: # Слишком близко - считаем пройденной
                    Actor.GoWayPoint(GoToWP[0])
                    if ListOfWPs[GoToWP[0]].FinalPoint:
                        Actor.State = "NeedFood"
                return 0
            else: # Зачем? Чтобы муравей мог продолжить искать вейпоинты если зашёл в тупик, где их нет.
                Actor.MemoryClear()
                WayPoints = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
                if not WayPoints:
                    Actor.State = "Lost"
                return 0
            
                
        if Actor.State == "NeedFood":
            if (GetDistance(Actor, ListOfHomes[Actor.HomeID]) > 5):
                GoHome(Actor)
                return 0
            else:
                Actor.State = "InHome"
                return 0
            
        if Actor.State == "Lost":
            if Actor.MemoryAnt != -1:
                NotLostAnt = ListOfAnts[Actor.MemoryAnt]
                if NotLostAnt.State != "Lost":
                    HowToMove = AutoMove(Actor.posx, Actor.posy, NotLostAnt.posx, NotLostAnt.posy)
                    Actor.Move(HowToMove[0], HowToMove[1])
                    return 0
                Actor.MemoryAnt = -1
                return 0
                    
            MyHomeXY = HomeXY(Actor.HomeID)
            if GetDistanceRaw(Actor.posx, Actor.posy, MyHomeXY[0], MyHomeXY[1]) < 40:
                Actor.State = "NeedFood"
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
    if (Actor.Mind == 2222):
    
        if Actor.State == "InHome":
            EatAndLeave(Actor, 2222)
            return 0
            
        if Actor.State == 2222:
            FoodFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "food", 2)
            WPFound = ScanRadiusAround(Actor.BlockMapID[0], Actor.BlockMapID[1], "way", 2)
            if FoodFound and not WPFound:
                Actor.State = "FoodFound"
                ClosestFood = GetClosest(MyX, MyY, FoodFound, "food") # [ObjID, ObjX, ObjY, NewDiffSum]
                Actor.FoodMemory = ClosestFood[0]
            else:
                Actor.Angle += randint(-20, 20)
                Actor.Move(Actor.Angle, Actor.Speed)
                return 0
                
        if Actor.State == "FoodFound":
            FoodX = ListOfObjects[Actor.FoodMemory].posx
            FoodY = ListOfObjects[Actor.FoodMemory].posy
            DistanceToFood = GetDistance(Actor, ListOfObjects[Actor.FoodMemory])
            if DistanceToFood < 2:
                Actor.State = "CreatingWay"
                Actor.CreateWayPoint(20, True)
            else:
                HowToMove = AutoMove(MyX, MyY, FoodX, FoodY)
                HowToMove[0] += randint(-20, 20)
                Actor.Move(HowToMove[0], HowToMove[1])
                return 0
                
        if Actor.State == "CreatingWay":
            if (GetDistance(Actor, ListOfHomes[Actor.HomeID]) > 15):
                GoHome(Actor, True)
                Actor.CreateWayPoint(20)
                return 0
            else:
                Actor.CreateWayPoint(20, True)
                Actor.State = "NeedFood"
                return 0
                
        if Actor.State == "NeedFood":
            if (GetDistance(Actor, ListOfHomes[Actor.HomeID]) > 5):
                GoHome(Actor)
                return 0
            else:
                Actor.State = "InHome"
                return 0

    
    



LastStandDistance = 30
FoodToEnergy = 200
MemorySize = 15
#print("AI loaded!")
# Да, я знаю, так нельзя делать. И я понимаю, как делать правильно.
# Но когда я начинал - нихера я не понимал. Спасибо тебе, Никита, за то, что научил, как не надо делать.