import pyautogui
from pyscreeze import screenshot
from cv2 import resize, matchTemplate, TM_CCOEFF_NORMED, imread, minMaxLoc
from time import sleep
from warnings import simplefilter
import os

# Omit pyautogui warning
simplefilter("ignore")
pyautogui.FAILSAFE = False

# Scaling factor, windows 1 and macos 2
screenScale = 1

# Strategy tables
strategyTable1 = [
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 5
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 6
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 7
    ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],  # 8
    ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # 9
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  # 10
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  # 11
    ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 12
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 13
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],  # 14
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'S', 'H'],  # 15
    ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'S', 'S', 'H'],  # 16
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 17
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 18
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 19
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 20
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 21
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # 22
]  # From left to right, dealer's cards are 2, 3, 4, 5, 6, 7, 8, 9, T, A

strategyTable2 = [
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A2
    ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A3
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A4
    ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],  # A5
    ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'S', 'H', 'H'],  # A6
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A7
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A8
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # A9
]

strategyTable3 = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # Pair2
    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # Pair3
    ['H', 'H', 'H', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # Pair4
    ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],  # Pair5
    ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],  # Pair6
    ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],  # Pair7
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'S', 'H'],  # Pair8
    ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],  # Pair9
    ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],  # PairT
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'H'],  # PairA
]

# Hand card positions
handA = [range(895, 912), range(1028, 1040), range(744, 762)]
handB = [range(939, 953), range(1072, 1084), range(789, 803)]

def compare(target, temp):
    global max_loc, twidth, theight
    theight, twidth = target.shape[:2]
    tempheight, tempwidth = temp.shape[:2]
    scaleTemp = resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))

    res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
    mn_val, max_val, min_loc, max_loc = minMaxLoc(res)
    
    if max_val >= 0.9:
        print("Comparison successful", max_loc)
        return 1
    else:
        return 0

def clickz(top_left):
    tagHalfW = int(twidth / 2)
    tagHalfH = int(theight / 2)
    tagCenterX = top_left[0] + tagHalfW
    tagCenterY = top_left[1] + tagHalfH
    pyautogui.click(tagCenterX, tagCenterY, button='left')

def cursorPositionPause():
    # This section implements a pause loop by detecting the mouse position
    curPosition = pyautogui.position()
    i = 2
    if curPosition.y >= 1076:
        while True:
            print("Program will pause for {} seconds. Move the mouse to the top, left, or right edge of the screen and wait for {} seconds. The program will resume.".format(i, i))
            sleep(i)
            if i < 15:
                i += 1
            curPosition = pyautogui.position()
            print("Mouse position", curPosition)
            if curPosition.y <= 3 or curPosition.x >= 1916 or curPosition.x <= 3:
                print("Program resuming\n")
                break

cpause = cursorPositionPause

def poke(h):
    # Convert card value to point value
    if (h % 13 >= 10 and h % 13 <= 13) or h % 13 == 0:
        return 10
    elif h % 13 == 1:
        return 11
    else:
        return h % 13

def write_sentence(a, b, c, d, f, e):
    f_string = "win" if f else "lose"
    sentence = "Action: {}, Hand Card 1: {}, Hand Card 2: {}, Dealer Card: {}, {}, Win Rate: {:>8.4f}".format(d, a, b, c, f_string, e)
    with open('data.txt', 'a') as file:
        file.write(sentence + '\n')

def startupVerification():
    print("Usage instructions:\n"
          "Before launching this software, check the image folder. It must contain the following files: ...\n"
          "After launching, the program will provide feedback based on the current screen content. Open GOP3 and start the 21-point idle mode in order (version 1.17).\n"
          "Note: Please sit in the middle position for the script to capture smoothly. It is recommended to choose a 'non-public card room'.\n"
          "Current parameters are applicable to 1920*1080 resolution Windows computer screens.\n")
    
    # Get the current screen resolution
    screenSize = pyautogui.size()
    print("Current screen resolution is", screenSize)
    if screenSize != (1920, 1080):
        print("\n\n***********Screen resolution error. The script will not be able to capture effectively.************\n\n")
    else:
        print("Screen resolution meets requirements\n")

def handleUnfocused():
    temp = imread(r'image/screen.png', 0)
    i = 0
    while i < 5:
        i += 1
        target = imread(r'image/off' + str(i) + '.png', 0)
        if compare(target, temp) == 1:  # Match successful
            top_left = max_loc
            clickz(top_left)
            sleep(0.01)
            return 0
    if compare(doubleexp, temp) == 1:
        pyautogui.click(130, 1011, button='left')
        sleep(3)
        return 0
    pyautogui.click(92, 52, button='left')

startupVerification()

if not os.path.isfile('data.txt'):
    open('data.txt', 'w').close()

with open('data.txt', 'r') as f:
    lines = f.readlines()

betAmount = input("Enter the default bet amount (1k press 1, 2.5k press 2, 5k press 3, 10k press 4, 25k press 5, 50k press 6, 100k press 7, 200k press 8, 500k press 9, 1M press 10, 2.5M press 11, 5M press 12, 10M press 13, 20M press 14, 50M press 15, 100M press 16):\n")

betAmountMap = {
    '1': 1,
    '2': 2.5,
    '3': 5,
    '4': 10,
    '5': 25,
    '6': 50,
    '7': 100,
    '8': 200,
    '9': 500,
    '10': 1000,
    '11': 2500,
    '12': 5000,
    '13': 10000,
    '14': 20000,
    '15': 50000,
    '16': 100000
}

betValue = betAmountMap.get(betAmount)
print("You will continuously bet", betValue, "k and stop when out of chips.")
print("Started running. Please launch the game.")

hit = imread(r"image/hit.png", 0)
double = imread(r"image/double.png", 0)
split = imread(r"image/split.png", 0)
buyin = imread(r"image/buyin.png", 0)
win = imread(r"image/win.png", 0)
lose = imread(r"image/lose.png", 0)
unfocused = imread(r"image/unfocused.png", 0)
doubleexp = imread(r"image/doubleexp.png", 0)

numWins = 0
numLosses = 0
errors = 0
unrecognizable = 0

prevDealerCard = -1
prevHandCard1 = -1
prevHandCard2 = -1
prevAction = -1

prev2DealerCard = -1
prev2HandCard1 = -1
prev2HandCard2 = -1
prev2Action = -1

while True:
    while True:
        # Preload button screenshots
        stand = imread(r"image/stand.png", 0)
        bet = imread(r"image/bet" + str(betValue) + "k.png", 0)
        
        # Pause the program based on mouse position
        cpause()
        
        # Main functionality: place bets and make playing decisions
        try:
            screenshot('image/screen.png')
        except:
            errors += 1
            print("Screenshot error", errors)
            continue
        
        # Read the image (grayscale is faster)
        temp = imread(r'image/screen.png', 0)
        
        if compare(stand, temp) == 1:
            dealerCard = -1
            handCard1 = -1
            handCard2 = -1
            totalPoints = 0
            print("Found the stand button")
            tempheight, tempwidth = temp.shape[:2]
            scaleTemp = resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
            
            i = 0
            while i < 52:
                i += 1
                target = imread(r'image/' + str(i) + '.png', 0)
                theight, twidth = target.shape[:2]
                
                # Match the image
                res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
                mn_val, max_val, min_loc, max_loc = minMaxLoc(res)
                
                if max_val >= 0.95:  # Match successful
                    if max_loc[1] < 353 and dealerCard == -1:
                        x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + 15, max_loc[1] + 15
                        scaleTemp[y1:y2, x1:x2] = 0
                        print("Matched dealer's card successfully", max_loc, i)
                        dealerCard = poke(i)
                        prevDealerCard = dealerCard
                        print("Dealer's card is", dealerCard)
                        i -= 1
                    elif (max_loc[0] in [d1 for d2 in handA for d1 in d2]) and handCard1 == -1:
                        x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + 15, max_loc[1] + 15
                        scaleTemp[y1:y2, x1:x2] = 0
                        print("Matched hand card A successfully", max_loc, i)
                        handCard1 = poke(i)
                        prevHandCard1 = handCard1
                        totalPoints += handCard1
                        print("Hand card A is", handCard1)
                        i -= 1
                    elif (max_loc[0] in [d3 for d4 in handB for d3 in d4]) and handCard2 == -1:
                        x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + 15, max_loc[1] + 15
                        scaleTemp[y1:y2, x1:x2] = 0
                        print("Matched hand card B successfully", max_loc, i)
                        handCard2 = poke(i)
                        prevHandCard2 = handCard2
                        totalPoints += handCard2
                        print("Hand card B is", handCard2)
                        i -= 1
                if totalPoints > 20:
                    totalPoints = 20
            
            if handCard1 == -1 or handCard2 == -1 or dealerCard == -1:
                continue
            
            if handCard1 == handCard2:  # Two hand cards are equal, use table 3
                temp = handCard1
                strategyTable = strategyTable3
            elif handCard1 == 11 or handCard2 == 11:  # Contains an Ace, use table 2
                if handCard1 == 11:
                    temp = handCard2
                if handCard2 == 11:
                    temp = handCard1
                strategyTable = strategyTable2
            else:  # Other situations, use table 1
                temp = totalPoints - 3
                strategyTable = strategyTable1
            
            if strategyTable[temp - 2][dealerCard - 2] == 'S':  # Stand
                position = (852, 969)
                print("Executing stand\n")
                clickz(position)
                prevAction = 'S'
                sleep(0.9)
            elif strategyTable[temp - 2][dealerCard - 2] == 'H':  # Hit
                position = (594, 967)
                print("Executing hit (every 1.6 seconds)\n")
                clickz(position)
                prevAction = 'H'
                sleep(1.6)
                clickz((854, 969))
            elif strategyTable[temp - 2][dealerCard - 2] == 'D':  # Double
                position = (1123, 969)
                print("Executing double\n")
                prevAction = 'D'
                clickz(position)
                sleep(0.6)
            elif strategyTable[temp - 2][dealerCard - 2] == 'P':  # Split
                position = (1373, 969)
                print("Executing split\n")
                clickz(position)
                prevAction = 'P'
                sleep(0.6)
        
        elif compare(bet, temp) == 1:
            print("Found the bet button and clicking (every 0.01 seconds)")
            top_left = max_loc
            clickz(top_left)
            sleep(0.01)
        
        elif compare(win, temp) == 1:
            if [prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action] == [prevDealerCard, prevHandCard1, prevHandCard2, prevAction]:
                continue
            numWins += 1
            winRate = numWins / (numLosses + numWins)
            print("Win, number of wins: " + str(numWins) + ", Win rate: %.4f" % winRate)
            write_sentence(prevHandCard1, prevHandCard2, prevDealerCard, prevAction, True, winRate)
            prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action = prevDealerCard, prevHandCard1, prevHandCard2, prevAction
            sleep(2)
        
        elif compare(lose, temp) == 1:
            if [prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action] == [prevDealerCard, prevHandCard1, prevHandCard2, prevAction]:
                continue
            numLosses += 1
            winRate = numWins / (numLosses + numWins)
            print("Loss, number of losses: " + str(numLosses) + ", Win rate: %.4f" % winRate)
            write_sentence(prevHandCard1, prevHandCard2, prevDealerCard, prevAction, False, winRate)
            prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action = prevDealerCard, prevHandCard1, prevHandCard2, prevAction
            sleep(2)
        
        else:
            print("Not found, or launch GOP3 and 21-point first (every 0.2 seconds)")
            sleep(0.2)
    
    handleUnfocused()