import random
class Card():
    def __init__(self, val, suit):
        self.val = val
        self.suit = suit

    def show(self):
        print("{} of {}".format(self.val, self.suit))

class Deck():
    def __init__(self):
        self.deck = []
        self.build()
        
    def build(self):
        for suits in ["Clubs","Spades","Hearts","Diamonds"]:
            for val in range(2, 15):
                if val == 14:
                    val = "Ace"
                if val == 11:
                    val = "Jack"
                if val == 12:
                    val = "Queen"
                if val == 13:
                    val = "King"
                self.deck.append(Card(val,suits))
        
    def printdeck(self):
        for c in self.deck:
            c.show()
            
    def drawcard(self):
        return self.deck.pop()
    
    def shuffle(self):
        for i in range(len(self.deck)-1, 0 ,-1):
            r = random.randint(0, i)
            self.deck[i], self.deck[r] = self.deck[r], self.deck[i]

class player():
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.moneyAMT = 100
        self.isDealer = False
        self.didFold = False
    def draw(self, deck):
        self.hand.append(deck.drawcard())
        
    def showHand(self):
        for c in self.hand:
            c.show()
            
class gamehandler():
    progress = False
    flops = 3
    won = False
    raiseAMT = 0
    pot = 0
    betting = False
    def __init__(self, playerlist):
        self.playerlist = playerlist
        self.amtCardsDrawn = 2
        self.flopturnriver = []
        for i in range(len(self.playerlist)):
            if self.playerlist[i].name == "Ki":
                self.userPlayer = self.playerlist[i]

    def deal(self, deck):
        for _ in range(self.amtCardsDrawn):
            for players in range(len(self.playerlist)):
                self.playerlist[players].draw(deck)
        for _ in range(5):
            self.flopturnriver.append(deck.drawcard())

    def showAll(self):#shows everyones hand
        for players in range(len(self.playerlist)):
            print("\n{} cards are:".format(self.playerlist[players].name))
            self.playerlist[players].showHand()
        print("\nFLOP:")
        for i in range(len(self.flopturnriver)):
            self.flopturnriver[i].show()
        
    def playHand(self):
        while self.flops != 6:
            for players in range(len(self.playerlist)):
                print("\n{} cards:".format(self.playerlist[players].name))
                print("MONEY:{}".format(self.playerlist[players].moneyAMT))
                self.playerlist[players].showHand() if (self.playerlist[players].name == "Ki") else print("[][]")
            if self.progress == True:
                print("\nFLOP:")
                for i in range(self.flops):
                    self.flopturnriver[i].show()
            print("\nPOT:"+str(self.pot))
            self.botBet()
            self.betting = False
            self.raiseInput = 0
            self.userInput = input("\n(1)Check/Call\n(2)Fold\n(3)Raise\n: ")
            self.actions = {
                "1": lambda: self.checkCall(),
                "2": lambda: self.fold(),
                "3": lambda: self.Raise()
                }
            self.data = self.actions.get(self.userInput) if self.actions.get(self.userInput) else self.playHand()
            self.data()
            
    def checkCall(self):
        print("\n" * 50)
        if self.progress == True:
            if self.flops == 5:
                self.flops +=1
                self.showAll()
            else:
                self.flops +=1 
        self.progress = True
        
    def fold(self):
        print("\n" * 50)
        self.flops = 6
        self.showAll()
        
    def Raise(self):
        self.raiseInput = int(input("\nEnter bet: "))
        if self.raiseInput > self.userPlayer.moneyAMT:
            print("Insufficient Funds")
            self.Raise()
        else:
            self.userPlayer.moneyAMT -= self.raiseInput
            self.pot +=self.raiseInput
            self.betting = True
        
    def botBet(self):
        self.tempBot = ""
        if self.betting:
            r1 = bool(random.getrandbits(1))
            r2 = bool(random.getrandbits(1))
            if r1:
                for i in range(len(self.playerlist)-1):
                    if self.playerlist[i].name != "Ki":
                        if self.playerlist[i].moneyAMT >= self.raiseInput:
                            self.playerlist[i].moneyAMT -= self.raiseInput
                            self.pot += self.raiseInput
                            self.tempBot = self.playerlist[i].name
                        else:
                            self.botFold(self.playerlist[i])
            if r2:
                for i in range(len(self.playerlist)):
                    if self.playerlist[i].name != "Ki" and self.playerlist[i].name != self.tempBot:
                        if self.playerlist[i].moneyAMT >= self.raiseInput:                            
                            self.playerlist[i].moneyAMT -= self.raiseInput
                            self.pot += self.raiseInput
                            self.tempBot = self.playerlist[i].name
                        else:
                            self.botFold(self.playerlist[i])
                                                         
    def botFold(self, botthatfolded):
        botthatfolded.didFold = True
        pass #Continue later


"""
FINISH FOLD SYSTEM
FINISH RAISE SYSTEM

GOOD WORK
"""


deck = Deck()
deck.shuffle()

ply1 = player("Michael")
ply2 = player("Max")
ply3 = player("Ki") #User Player

players = [ply1,ply2,ply3] #player list 

greg = gamehandler(players)
greg.deal(deck)
# greg.showAll() // Shows everybodys hand
greg.playHand()