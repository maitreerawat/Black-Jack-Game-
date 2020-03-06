##This code uses 
##pygame: which is a cross-platform set of Python modules designed for writing video games.
##cytpe: ctypes is a foreign function library for Python. It provides C compatible data types, and allows calling functions in DLLs or shared libraries.
##       It can be used to wrap these libraries in pure Python.

import ctypes, os, pygame, random, sys

# Find the root working directory. We need this for PyInstaller to work.
# Adapted from https://stackoverflow.com/a/50034378/2941352
if getattr(sys, 'frozen', False):
    root_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable)) # Root directory of temporary directory (when running PyInstaller binary)
else:
    root_dir = os.getcwd() + '\\' # Root directory of this Python script (when running normally)

pygame.init()          #initialize all imported pygame modules

##################Intialisation###################################

###Game Variables

user_cards = []
dealer_cards = []
user_value = []
dealer_value = []
user_cards_pos = [[550,530],[680,530],[810,530],[420,530],[290,530],[940,530],[160,530],[1070,530],[1200,530],[30,530]]
dealer_cards_pos = [[550,50],[680,50],[810,50],[420,50],[290,50],[940,50],[160,50],[1070,50],[1200,50],[30,50]]
now = False
deck = list(range(1,53))
random.shuffle(deck)   
card_back = ''
pause = True
used_decks = 0
bet_money = 100
bet_value = 5

###Screen Variables

display_width = 1300
display_height = 800
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (31,101,47)

###Images

icon = pygame.image.load(os.path.join(root_dir, 'images\\icon.png'))
start_image = pygame.image.load(os.path.join(root_dir, 'images\\start_image.gif'))
rule_image = pygame.image.load(os.path.join(root_dir, 'images\\rules.png'))
arena = pygame.image.load(os.path.join(root_dir, 'images\\arena3.png'))
blackjack_dealer = pygame.image.load(os.path.join(root_dir, 'images\\blackjack_dealer.png'))
blackjack_user = pygame.image.load(os.path.join(root_dir, 'images\\blackjack_user.png'))
money = pygame.image.load(os.path.join(root_dir, 'images\\money.png'))
front = pygame.image.load(os.path.join(root_dir, 'images\\wallpaper.jpg'))
front = pygame.transform.scale(front, (1300,800))

###Fonts

verysmallText = pygame.font.SysFont("arial",15)
largeText = pygame.font.SysFont('bradleyhanditc',40)
smallText = pygame.font.SysFont("elephant",20)

###Display Functions

gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.RESIZABLE)
pygame.display.set_caption('Black Jack')
clock = pygame.time.Clock()
pygame.display.set_icon(icon)

####################Functions#####################################

###Basic

def Quit_loop():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit()               
def Quit():
    pygame.quit()
    sys.exit()

def text_objects(text, font, color):
    #This creates a new Surface with the specified text rendered on it(create an image (Surface) of the text, then blit this image onto another Surface).
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def display_image(image,x,y):
    gameDisplay.blit(image,(x,y))

def Update(time):
    pygame.display.update()
    clock.tick(time) #FPS

def button_action(x,y,w,h,mouse_pos,action):
    if pygame.Rect(x,y,w,h).collidepoint(mouse_pos):
        return action() 
                    
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x+w>mouse[0]>x and y+h>mouse[1]>y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if click[0]==1 and action!=None:
           action()
    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))
    smallText = pygame.font.SysFont("bookantiqua",20)
    textSurf, textRect = text_objects(msg,smallText,white)
    textRect.center=(x+(w/2),y+(h/2))
    gameDisplay.blit(textSurf,textRect)
    
##################################################################
    
##Card Functions
    
def empty_deck():
    global used_decks,deck
    if len(deck)== 0:
        used_decks += 1
        deck = list(range(1,53))
        random.shuffle(deck)       
    
def select_card():
    global deck
    empty_deck()
    selected = deck[0]
    del(deck[0])
    return str(selected)

def select_back():
    return str(random.randrange(1,7))+'_back'

def cards(c):
    card = pygame.image.load(os.path.join(root_dir, 'cards\\'+c+'.png'))
    card = pygame.transform.scale(card, (80,100))
    return card

def shuffle():
    global now
    now = False
    cards_clear()
    card_value()

def card_value():
    global user_cards,dealer_cards,card_back,user_value,dealer_value
    user_value = [select_card(),select_card()]
    user_cards = list(map(cards,user_value)) #iterating
    dealer_value = [select_card(),select_card()]
    dealer_cards = list(map(cards,dealer_value))
    card_back = cards(select_back())

def cards_clear():
    global user_cards,dealer_cards,user_value,dealer_value
    user_cards = []
    dealer_cards = []
    user_value = []
    dealer_value = []

def add_cards(c):
    global user_cards,dealer_cards,user_value,dealer_value
    if c =='user':
        user_value.append(select_card())
        user_cards.append(cards(user_value[-1]))
    elif c =='dealer':
        dealer_value.append(select_card())
        dealer_cards.append(cards(dealer_value[-1]))

def show_cards():
    global user_cards,dealer_cards,user_cards_pos,dealer_cards_pos,card_back,dealer_value
    for i in range(len(user_cards)):
        display_image(user_cards[i],user_cards_pos[i][0],user_cards_pos[i][1])
    for i in range(len(dealer_cards)):
        if now == True:
            display_image(dealer_cards[i],dealer_cards_pos[i][0],dealer_cards_pos[i][1])            
    if now == False:
        display_image(dealer_cards[0],dealer_cards_pos[0][0],dealer_cards_pos[0][1])
        display_image(card_back,dealer_cards_pos[1][0],dealer_cards_pos[1][1])

##################################################################
        
##Calculate Functions
        
def check_game(value):
    if len(value)== 2 and (int(value[0]) in [1,14,27,40] and int(value[1]) in [11,12,13,24,25,26,37,38,39,50,51,52]) or (int(value[1]) in [1,14,27,40] and int(value[0]) in [11,12,13,24,25,26,37,38,39,50,51,52]):
            return 'Black Jack'
    else:
        a = calculate(value)
        if a > 21:
            return 'Busted'
        return str(a)
        
def calculate(value):
    a = value
    a = sorted((list(map(int,a))))
    know = 0
    score = 0
    for i in a:
        if i%13 >= 10:
            score += 10
        elif i%13 > 1:
            score += i%13
        else:
            if i in [1,14,27,40]:
                know = know+1
            else:
                score += 10                
    if know*11+score <= 21:
        score += know*11
    else:
        score += know
    return score

##def unpause():
##    global pause
##    pause = False
##    cards_clear()
##    card_value()

def bet_clear():
    global bet_money,bet_value,used_decks
    bet_money = 100
    bet_value = 5
    used_decks = 0
    
def paused(c=None):
    global pause
    while pause:
        Quit_loop()
        display_image(money,100,50)
        if c == None:
            c = "Paused"
        TextSurf, TextRect = text_objects(c,largeText,black)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("New Game!",500,550,150,50,green, red,game)
        button("QUIT!",700,550,100,50,green, red,Quit)
        pygame.display.update()
        clock.tick(15)
        
##################################################################
        
##Hit Functions
        
def hit():
    return add_cards('user')

def hit_dealer():
    return add_cards('dealer')

def stand():
    global now,user_value,dealer_value
    now = True
    cv = check_game(user_value)
    dv = check_game(dealer_value)
    if dv == 'Black Jack':
        return "Dealers' Black Jack"
    else:
        dv = calculate(dealer_value)
        cv = calculate(user_value)
        while dv < cv or dv > 21:
            hit_dealer()
            dv = calculate(dealer_value)
            show_cards()
            Update(10)
            if (dv == cv)and((dv) >= 18):
                return'Push'
            if dv > 21:
                return'Dealer Busted , Player Won'
        if (dv) > (cv):
            return'Dealer won'
        else:
            return 'Push'
    return 0

##################################################################

##Bet Functions

def bet():
    global bet_money,bet_value
    TextSurf, TextRect = text_objects("Money = "+str(bet_money)+" Rs",smallText,red)
    TextRect.center = (200,200)
    gameDisplay.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects("Bet Money= "+str(bet_value)+" Rs",smallText,red)
    TextRect.center = (200,250)
    gameDisplay.blit(TextSurf, TextRect)
    TextSurf, TextRect = text_objects("You can only bet money as much as you have!",verysmallText,red)
    TextRect.center = (200,280)
    gameDisplay.blit(TextSurf, TextRect)

def addfivedollars():
    global bet_value,bet_money
    if bet_money < bet_value + 5:
        bet_value = bet_money
    else:
        bet_value += 5

def addtendollars():
    global bet_value,bet_money
    if bet_money < bet_value + 10:
        bet_value = bet_money
    else:
        bet_value += 10


def addhundreddollars():
    global bet_value,bet_money
    if bet_money < bet_value + 100:
        bet_value = bet_money
    else:
        bet_value += 100

def reset():
    global bet_value
    bet_value = 5

def check_bank():
    global bet_money
    if bet_money <= 0:
        return -1
    return 1

def restart():
    n = ctypes.windll.user32.MessageBoxW(0,"Do you really want to restart?","Restart",1)
    if n == 1:
        start()
        
##################################################################

###Game functions
        
def game():
    global pause,user_value,now,used_decks,bet_money,bet_value
    bet_clear()
    card_value()
    while True:
        pause = True
        text = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                button_action(1000,450,100,50,mouse_pos,hit)
                text=button_action(1000,350,100,50,mouse_pos,stand)
                button_action(1000,250,100,50,mouse_pos,shuffle)
                button_action(100,300,70,50,mouse_pos,addfivedollars)
                button_action(200,300,70,50,mouse_pos,addtendollars)
                button_action(300,300,70,50,mouse_pos,addhundreddollars)
                button_action(180,370,100,50,mouse_pos,reset)
        display_image(arena,0,0)
        button("HIT!",1000,450,100,50,black, red)
        button("STAND!",1000,350,100,50,black, red)
        button("SHUFFLE!",1000,250,100,50,black, red)
        button("New Game!",980,150,150,50,black, red,restart)
        button("+5 Rs",100,300,70,50,black,red)
        button("+10 Rs",200,300,70,50,black,red)
        button("+100 Rs",300,300,70,50,black,red)
        button("Reset",180,370,100,50,black,red)
        button("Quit",180,450,100,50,black,red,Quit) 
        TextSurf, TextRect = text_objects("Number of decks used: "+str(used_decks),smallText,red)
        TextRect.center = (650,30)
        gameDisplay.blit(TextSurf, TextRect)
        if check_bank() != -1:
            value = check_game(user_value)
            if value == 'Black Jack':
                text = 'Black Jack'
                bet_money += bet_value
            elif value == 'Busted':
                text = 'Busted'
                bet_money -= bet_value
            button(str(calculate(user_value)),618,448,60,50,green,green)
            if now == True:
                button(str(calculate(dealer_value)),618,280,60,50,green,green)
        else:
            pygame.time.delay(1200)
            paused("You are out of money")
        if text != 0 and text != None:
            button(text,400,350,500,50,red,red)
            if text in ["Dealers' Black Jack","Dealer won"]:
                bet_money -= bet_value
            elif text == "Dealer Busted , Player Won":
                bet_money += bet_value
            show_cards()
            Update(10)
            pygame.time.delay(1500)
            shuffle()
            
        bet()
        show_cards()
        Update(10)

def second():
    while True:
        Quit_loop()
        gameDisplay.fill(white)
        display_image(rule_image,250,40)
        button("LET'S GO!",500,530,200,50,black, red,game)
        Update(10)
    
def start():
    while True:
        Quit_loop()
        display_image(front,0,0)
        display_image(start_image,500,100)
        TextSurf, TextRect = text_objects("A game developed and maintained by Maitree Rawat", largeText,white)
        TextRect.center = (650,400)
        gameDisplay.blit(TextSurf, TextRect)  
        button("GO!",400,450,100,50,black, red,second)
        button("QUIT!",800,450,100,50,black, red,Quit)
        Update(10)

##########################CALL####################################
start()
