import pyautogui
from pyscreeze import screenshot
from cv2 import resize, matchTemplate, TM_CCOEFF_NORMED, imread, minMaxLoc
from time import sleep
from warnings import simplefilter
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

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

def clickz(top_left):
    tagHalfW = int(twidth / 2)
    tagHalfH = int(theight / 2)
    tagCenterX = top_left[0] + tagHalfW
    tagCenterY = top_left[1] + tagHalfH
    pyautogui.click(tagCenterX, tagCenterY, button='left')

def poke(h):
    if (h % 13 >= 10 and h % 13 <= 13) or h % 13 == 0:
        return 10
    elif h % 13 == 1:
        return 11
    else:
        return h % 13

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Blackjack Bot')
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.bet_amount_label = QLabel('Bet Amount (in thousands):')
        self.bet_amount_input = QLineEdit()
        self.bet_amount_map = {'1': 1, '10': 10, '100': 100, '1000': 1000, '10000': 10000}
        
        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_program)
        
        layout.addWidget(self.bet_amount_label)
        layout.addWidget(self.bet_amount_input)
        layout.addWidget(self.start_button)
        
        self.setLayout(layout)

    def start_program(self):
        global betAmount, betValue
        betAmount = self.bet_amount_input.text()
        betValue = self.bet_amount_map.get(betAmount)
        self.run_program()
    
    def start_program(self):
        global betAmount, betValue
        betAmount = self.bet_amount_input.text()
        betValue = self.bet_amount_map.get(betAmount)
        
        self.program_thread = ProgramThread()
        self.program_thread.start()

            
class ProgramThread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def compare(self, target, temp):
        global max_loc, twidth, theight
        theight, twidth = target.shape[:2]
        tempheight, tempwidth = temp.shape[:2]
        scaleTemp = resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
        
        res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
        mn_val, max_val, min_loc, max_loc = minMaxLoc(res)
        
        if max_val >= 0.9:
            return 1
        else:
            return 0
        
    def handleUnfocused():
        global max_loc
        temp = imread(r'image/screen.png', 0)
        i = 0
        while i < 5:
            i += 1
            target = imread(r'image/off' + str(i) + '.png', 0)
            if self.compare(target, temp) == 1:
                top_left = max_loc
                clickz(top_left)
                sleep(0.01)
                return 0
        if self.compare(doubleexp, temp) == 1:
            pyautogui.click(130, 1011, button='left')
            sleep(3)
            return 0
        pyautogui.click(92, 52, button='left')

    def run(self):
        global max_loc, numWins, numLosses, errors, unrecognizable, prevDealerCard, prevHandCard1, prevHandCard2, prevAction, prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action
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
                stand = imread(r"image/stand.png", 0)
                bet = imread(r"image/bet" + str(betValue) + "k.png", 0)
                
                try:
                    screenshot('image/screen.png')
                except:
                    errors += 1
                    continue
                
                temp = imread(r'image/screen.png', 0)
                
                if self.compare(stand, temp) == 1:
                    dealerCard = -1
                    handCard1 = -1
                    handCard2 = -1
                    totalPoints = 0
                    tempheight, tempwidth = temp.shape[:2]
                    scaleTemp = resize(temp, (int(tempwidth / screenScale), int(tempheight / screenScale)))
                    
                    i = 0
                    while i < 52:
                        i += 1
                        target = imread(r'image/' + str(i) + '.png', 0)
                        theight, twidth = target.shape[:2]
                        
                        res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
                        mn_val, max_val, min_loc, max_loc = minMaxLoc(res)
                        
                        if max_val >= 0.95:
                            if max_loc[1] < 353 and dealerCard == -1:
                                x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + 15, max_loc[1] + 15
                                scaleTemp[y1:y2, x1:x2] = 0
                                dealerCard = poke(i)
                                prevDealerCard = dealerCard
                                i -= 1
                            elif (max_loc[0] in [d1 for d2 in handA for d1 in d2]) and handCard1 == -1:
                                x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + 15, max_loc[1] + 15
                                scaleTemp[y1:y2, x1:x2] = 0
                                handCard1 = poke(i)
                                prevHandCard1 = handCard1
                                totalPoints += handCard1
                                i -= 1
                            elif (max_loc[0] in [d3 for d4 in handB for d3 in d4]) and handCard2 == -1:
                                x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + 15, max_loc[1] + 15
                                scaleTemp[y1:y2, x1:x2] = 0
                                handCard2 = poke(i)
                                prevHandCard2 = handCard2
                                totalPoints += handCard2
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
                        clickz(position)
                        prevAction = 'S'
                        sleep(0.9)
                    elif strategyTable[temp - 2][dealerCard - 2] == 'H':  # Hit
                        position = (594, 967)
                        clickz(position)
                        prevAction = 'H'
                        sleep(1.6)
                        clickz((854, 969))
                    elif strategyTable[temp - 2][dealerCard - 2] == 'D':  # Double
                        position = (1123, 969)
                        prevAction = 'D'
                        clickz(position)
                        sleep(0.6)
                    elif strategyTable[temp - 2][dealerCard - 2] == 'P':  # Split
                        position = (1373, 969)
                        clickz(position)
                        prevAction = 'P'
                        sleep(0.6)
                
                elif self.compare(bet, temp) == 1:
                    top_left = max_loc
                    clickz(top_left)
                    sleep(0.01)
                
                elif self.compare(win, temp) == 1:
                    if [prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action] == [prevDealerCard, prevHandCard1, prevHandCard2, prevAction]:
                        continue
                    numWins += 1
                    winRate = numWins / (numLosses + numWins)
                    prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action = prevDealerCard, prevHandCard1, prevHandCard2, prevAction
                    sleep(2)
                
                elif self.compare(lose, temp) == 1:
                    if [prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action] == [prevDealerCard, prevHandCard1, prevHandCard2, prevAction]:
                        continue
                    numLosses += 1
                    winRate = numWins / (numLosses + numWins)
                    prev2DealerCard, prev2HandCard1, prev2HandCard2, prev2Action = prevDealerCard, prevHandCard1, prevHandCard2, prevAction
                    sleep(2)
                else:
                    sleep(0.2)
            self.handleUnfocused()

if __name__ == '__main__':
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()