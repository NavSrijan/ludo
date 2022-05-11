from PIL import Image, ImageDraw
import sys
import random
import pdb

imageName = "baseF.png"
noOfGotisToPlayWith=4

def draw():
    #Yellow
    bl = [196, 454]
    ul = [196, 429]
    ur = [222, 429]
    br = [222, 454]

    x1,y1 = ul
    x2,y2 = br

    offset = 4
    k = 14


    #x1+=26
    y1-=(25)*k+offset*k
    #x2+=26
    y2-=(25*k)+offset*k

    with Image.open(imageName) as im:

        draw = ImageDraw.Draw(im)


        draw.ellipse([x1,y1,x2,y2], fill=(0,0,0))


        im.show()

class Goti():
    def __init__(self, color, gharNo=0, owner=None):
        self.color = color
        self.owner = owner
        self.places = createPlace(self.color)
        self.currentPlace = 0
        self.ghars = self.places[-4:]
        self.ghar = self.places.index(self.ghars[gharNo])
        self.out=False #FOR TESTING
        self.gharNo = gharNo
        self.isLaal = False

        self.gharKaro()
    def returnColorTuple(self):
        if self.color=="Red":
            return (255,0,0)
        elif self.color=="Blue":
            return (0,0,255)
        elif self.color=="Green":
            return (0,255,0)
        elif self.color=="Yellow":
            return (253,218,13)
    def printVars(self, x1=True, y1=True, x2=False, y2=False):
        if x1==True:
            print(f"x1 : {self.x1}")
        if y1==True:
            print(f"y1 : {self.y1}")
        if x2==True:
            print(f"x2 : {self.x2}")
        if y2==True:
            print(f"y2 : {self.y2}")

        print(" ")
    def moveGoti(self, place):
        self.x1 = place.x1
        self.y1 = place.y1
        self.x2 = place.x2
        self.y2 = place.y2
    def move(self, num, L):
        if self.out==True:
            self.currentPlace+=num
            self.moveGoti(self.places[num])
            allGotis = L.returnAllGotis()
            for i in allGotis:
                if self.color!=i.color:
                    p1 = self.places[self.currentPlace]
                    p2 = i.places[i.currentPlace]
                    p1x1, p1y1, p1x2, p1y2 = p1.returnVars()
                    p2x1, p2y1, p2x2, p2y2 = p2.returnVars()
                    if p1x1==p2x1 and p1y1==p2y1 and p1.safe==False:
                        i.cutGoti()
                        if L.num!=6:
                            L.turn-1
                            return True
            if self.currentPlace==56:
                self.laal()
                self.owner.checkForWin(L)
                return False
            else:
                return True

            #self.places[num].addGoti(self)
            #print(self.places[num].gotiPresent)
    def takeOut(self):
        self.out = True
        self.moveGoti(self.places[0])
        self.currentPlace=0
    def gharKaro(self):
        self.currentPlace=self.ghar
        self.out = False
    def cutGoti(self):
        self.gharKaro()
    def draww(self, draw, pos=0, size = 4, numbers=True, textOffset=5):
        self.x1,self.y1,self.x2,self.y2 = self.places[self.currentPlace].returnVars()
        cc = self.returnColorTuple()
        if pos==1:
            size = 6
        draw.ellipse([self.x1+size,self.y1+size,self.x2-size,self.y2-size], fill=cc)
        if numbers:
            draw.text((self.x1+size+textOffset,self.y1+size+textOffset),str(self.gharNo+1),fill=(0,0,0))
    def laal(self):
        self.out=False
        self.isLaal=True
        self.owner.laal+=1

class Place():
    def __init__(self, x, y, safe=False, ghar=False):
        self.x1 = x
        self.y1 = y
        self.x2 = x+25
        self.y2 = y+25

        self.safe=safe
        self.ghar=ghar

        self.gotiPresent = []
    def returnVars(self):
        return self.x1,self.y1,self.x2,self.y2
    def printVars(self, x1=True, y1=True, x2=False, y2=False):
        if x1==True:
            print(f"x1 : {self.x1}")
        if y1==True:
            print(f"y1 : {self.y1}")
        if x2==True:
            print(f"x2 : {self.x2}")
        if y2==True:
            print(f"y2 : {self.y2}")
        print(" ")
    def addGoti(self, goti:Goti):
        self.gotiPresent.append(goti)
def createPlace(color):
    red0 = [254, 52]
    blue0 = [51, 197]
    yellow0 = [196, 429]
    green0 = [399, 255]

    offsety = 4
    offsetx = 4
    differencey = 25+offsety
    differencex = 25+offsetx

    def generateYellowPlaces():
        ##########################
        # Generating yellow places
        ##########################

        yellowLL = []

        #rightColumn
        x1,y1 = yellow0
        x1+=differencex*2
        y1-=differencey*6
        for i in range(6):
            y1+=differencey

            yellowLL.append(Place(x1,y1))

        #bottom
        x1,y1 = yellow0
        x1+=differencex
        yellowLL.append(Place(x1,y1))

        #left
        x1,y1 = yellow0
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            #x1+=differencex*i
            y1-=differencey

            yellowLL.append(Place(x1,y1))
        #homeRow
        x1,y1 = yellow0
        x1+=differencex
        y1-=differencey
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            #x1+=differencex
            y1-=differencey

            yellowLL.append(Place(x1,y1))

        #Ghar
        x1,y1=[72, 335]
        x2,y2=[116, 335]
        x3,y3=[72, 380]
        x4,y4=[116, 380]

        yellowLL.append(Place(x1,y1, ghar=True))
        yellowLL.append(Place(x2,y2, ghar=True))
        yellowLL.append(Place(x3,y3, ghar=True))
        yellowLL.append(Place(x4,y4, ghar=True))

        off = 17

        # Safe house declaration
        yellowLL[3].safe=True

        #for i in yellowLL:
        #    (i.printVars())
        return yellowLL
    def generateRedPlaces():
        ##########################
        # Generating red places
        ##########################

        yellowLL = []
        yellow0 = red0

        #left
        x1,y1 = yellow0
        y1+=differencey*5
        x1-=differencex*2
        for i in range(6):
            #x1+=differencex*i
            y1-=differencey

            yellowLL.append(Place(x1,y1))

        #up
        x1,y1 = yellow0
        x1-=differencex
        y1-=differencey
        yellowLL.append(Place(x1,y1))

        #rightColumn
        x1,y1 = yellow0
        y1-=differencey
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            y1+=differencey

            yellowLL.append(Place(x1,y1))

        #homeRow
        x1,y1 = yellow0
        x1-=differencex
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            #x1+=differencex
            y1+=differencey

            yellowLL.append(Place(x1,y1))

        #Ghar
        x1,y1=[335, 72]
        x2,y2=[335+44, 72]
        x3,y3=[335, 116]
        x4,y4=[335+44, 116]

        yellowLL.append(Place(x1,y1, ghar=True))
        yellowLL.append(Place(x2,y2, ghar=True))
        yellowLL.append(Place(x3,y3, ghar=True))
        yellowLL.append(Place(x4,y4, ghar=True))
        
        # Safe house declaration
        yellowLL[3].safe=True

        #for i in yellowLL:
        #    (i.printVars())
        return yellowLL
    def generateGreenPlaces():
        ##########################
        # Generating Green places
        ##########################

        yellowLL = []
        yellow0 = green0

        #top
        x1,y1 = yellow0
        y1-=differencey*2
        x1-=differencex*5
        for i in range(6):
            x1+=differencex
            #y1-=differencey

            yellowLL.append(Place(x1,y1))

        #right
        x1,y1 = yellow0
        x1+=differencex
        y1-=differencey
        yellowLL.append(Place(x1,y1))

        #bottom
        x1,y1 = yellow0
        x1+=differencex
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            x1-=differencex

            yellowLL.append(Place(x1,y1))

        #homeRow
        x1,y1 = yellow0
        y1-=differencey
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            x1-=differencex
            #y1+=differencey

            yellowLL.append(Place(x1,y1))

        #Ghar
        x1,y1=[335, 335]
        x2,y2=[335+44, 335]
        x3,y3=[335, 380]
        x4,y4=[335+44, 380]

        yellowLL.append(Place(x1,y1, ghar=True))
        yellowLL.append(Place(x2,y2, ghar=True))
        yellowLL.append(Place(x3,y3, ghar=True))
        yellowLL.append(Place(x4,y4, ghar=True))
        
        # Safe house declaration
        yellowLL[3].safe=True        

        #for i in yellowLL:
        #    (i.printVars())
        return yellowLL
    def generateBluePlaces():
        ##########################
        # Generating Blue places
        ##########################

        yellowLL = []
        yellow0 = blue0

        #bottom
        x1,y1 = yellow0
        y1+=differencey*2
        x1+=differencex*5
        for i in range(6):
            x1-=differencex
            #y1-=differencey

            yellowLL.append(Place(x1,y1))

        #left
        x1,y1 = yellow0
        x1-=differencex
        y1+=differencey
        yellowLL.append(Place(x1,y1))

        #top
        x1,y1 = yellow0
        x1-=differencex
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            x1+=differencex

            yellowLL.append(Place(x1,y1))
        
        #homeRow
        x1,y1 = yellow0
        y1+=differencey
        yellowLL.append(Place(x1,y1))
        for i in range(5):
            x1+=differencex
            #y1+=differencey

            yellowLL.append(Place(x1,y1))

        #Ghar
        x1,y1=[72, 72]
        x2,y2=[116, 72]
        x3,y3=[72, 116]
        x4,y4=[116, 116]

        yellowLL.append(Place(x1,y1, ghar=True))
        yellowLL.append(Place(x2,y2, ghar=True))
        yellowLL.append(Place(x3,y3, ghar=True))
        yellowLL.append(Place(x4,y4, ghar=True))

        # Safe house declaration
        yellowLL[3].safe=True
        

        #for i in yellowLL:
        #    (i.printVars())
        return yellowLL

    red = generateRedPlaces()
    green = generateGreenPlaces()
    blue = generateBluePlaces()
    yellow = generateYellowPlaces()
    finalLL = []


    if color=="Red":
        finalLL+=red[8:13]
        finalLL+=green[0:13]
        finalLL+=yellow[0:13]
        finalLL+=blue[0:13]
        finalLL+=red[0:7]
        finalLL+=red[13:]
    elif color=="Blue":
        finalLL+=blue[8:13]
        finalLL+=red[0:13]
        finalLL+=green[0:13]
        finalLL+=yellow[0:13]
        finalLL+=blue[0:7]
        finalLL+=blue[13:]
    elif color=="Yellow":
        finalLL+=yellow[8:13]
        finalLL+=blue[0:13]
        finalLL+=red[0:13]
        finalLL+=green[0:13]
        finalLL+=yellow[0:7]
        finalLL+=yellow[13:]
    elif color=="Green":
        finalLL+=green[8:13]
        finalLL+=yellow[0:13]
        finalLL+=blue[0:13]
        finalLL+=red[0:13]
        finalLL+=green[0:7]
        finalLL+=green[13:]

    return finalLL

class Player():
    def __init__(self, id):
        self.id = id
        self.color = None
        self.gotis = []
        self.laal = 0
    def makeGotis(self):
        for i in range(noOfGotisToPlayWith):
            self.gotis.append(Goti(self.color, gharNo=i, owner=self))
    def move(self):
        self.gotis[0].moveGoti()
    def countOut(self, num):
        out = 0
        tl = [0,0,0,0]
        j=0
        if num!=6:
            for i in self.gotis:
                if i.out==True and i.isLaal==False:
                    tl[j]=1
                    out+=1
                j+=1
            return out, tl
        else:
            for i in self.gotis:
                if i.isLaal==False:
                    tl[j]=1
                    out+=1
                j+=1
            return out, tl
    def checkForWin(self, L):
        if self.laal==len(self.gotis):
            L.winners.append(self)
            L.players.pop(L.players.index(self))
            try:
                if len(L.players)<=1:
                    L.winners.append(L.players[0])
                    L.players.pop(0)
            except:
                pass

class Ludo:
    def __init__(self):
        self.players = []
        self.winners = []
        self.colors = ["Yellow","Blue", "Red","Green"]
        self.turn = 0
        self.started = False
        self.message = None

        self.j = False

    def start(self):
        self.started=True
    def addPlayer(self, playerObject):
        if len(self.players)<=4 and self.started==False:
            if playerObject in self.players:
                return False
            cc = self.colors[0]
            self.colors.pop(0)
            #cc="Red"
            playerObject.color = cc
            playerObject.makeGotis()
            self.players.append(playerObject)
            print("The player was added.")
            return True
        else: 
            return False
            self.playersEnlisting=False
    def nextTurn(self):
        self.turn+=1
        if self.turn>=len(self.players):
            self.turn=0
    def rollDice(self, player):
        if player==self.players[self.turn].id and self.started==True:
            num = random.randint(1,6)   
            #self.players[self.turn].gotis[0].move(int(num))
            #if num==6:
            #    self.players[self.turn].gotis[0].takeOut() 
            
            #self.nextTurn()
            return num
        else:
            return "nope"
    def moveMain(self, num, gotiNo):
        single = False
        out = 0
        tl=[0,0,0,0]
        j=0
        for i in self.players[self.turn].gotis:
            if i.out==True:
                out+=1
                tl[j] = 1
            j+=1
        if out==0 and num==6:
            self.players[self.turn].gotis[gotiNo-1].takeOut()
            return True
        elif out==1:
            self.players[self.turn].gotis[gotiNo-1].move(int(num))
            return True
        elif out>1:
            if self.players[self.turn].gotis[gotiNo-1].out==True:
                self.players[self.turn].gotis[gotiNo-1].move(int(num))
                self.nextTurn()
                return True
            if self.players[self.turn].gotis[gotiNo-1].out==False and num==6:
                self.players[self.turn].gotis[gotiNo-1].takeOut()
                return True
            else:
                return False

    def moveMainNEW(self, num, gotiNo):
        '''
        0 goti:
            6:     Take out (Turn stays)
            [1,5]: Next turn
        1 goti:
            [1,5]: Auto move
            6:     Ask for input if want to move or take new goti out. (Turn stays)
        2,3,4 goti:
            [1,5]: Ask for which goti to move
            6:     Ask for input. Take out or move (Turn stays)

        Illegal moves...
        When it's in home row, it can't move if number of rows ahead is less than num
        '''
        
        
        pass

    def chal(self, num, gotiNo=1):
        self.players[self.turn].gotis[gotiNo-1].takeOut()
        self.players[self.turn].gotis[gotiNo-1].move(int(num), self)
    def gharK(self):
        for i in range(4):
            self.players[self.turn].gotis[i].gharKaro()
    def returnAllGotis(self):
        allGotis = []
        for i in self.players:
            for j in i.gotis:
                if j.out==True:
                    allGotis.append(j)
        return allGotis

def Ddraw(L):
    with Image.open(imageName) as im:

        draw = ImageDraw.Draw(im)
        for i in L.players:
            for goti in i.gotis:
                goti.draww(draw)

        im.save("1.png")

#L = Ludo()
#L.addPlayer(Player("1"))
#L.start()
#L.chal(2, gotiNo=1)
#L.rollDice("1")
#Ddraw(L)

#g=5
#y=44
