import pyautogui
from pyscreeze import screenshot
from cv2 import resize, matchTemplate, TM_CCOEFF_NORMED, imread, minMaxLoc
from time import sleep
from warnings import simplefilter
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QComboBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# Omit pyautogui warning
simplefilter("ignore")
pyautogui.FAILSAFE = False

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

max_loc = None

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
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.bet_amount_label = QLabel('Bet Amount:')
        self.bet_amount_input = QComboBox()
        self.bet_amount_input.addItems(['1k', '2.5k', '5k', '10k', '25k', '50k', '100k', '200k', '500k', '1M', '2.5M', '5M', '10M', '25M', '50M', '100M'])
        input_layout.addWidget(self.bet_amount_label)
        input_layout.addWidget(self.bet_amount_input)
        main_layout.addLayout(input_layout)

        self.start_button = QPushButton('Start')
        self.start_button.clicked.connect(self.start_program)
        main_layout.addWidget(self.start_button)

        self.statistics_layout = QVBoxLayout()
        self.total_games_label = QLabel('Total Games: 0')
        self.total_wins_label = QLabel('Total Wins: 0')
        self.statistics_layout.addWidget(self.total_games_label)
        self.statistics_layout.addWidget(self.total_wins_label)
        
        self.graph_view = QGraphicsView()
        self.graph_scene = QGraphicsScene()
        self.graph_view.setScene(self.graph_scene)
        self.graph_view.setFixedHeight(200)
        self.statistics_layout.addWidget(self.graph_view)

        main_layout.addLayout(self.statistics_layout)
        self.setLayout(main_layout)

    def start_program(self):
        betAmount = self.bet_amount_input.currentText()
        self.program_thread = ProgramThread(betAmount)
        self.program_thread.statUpdated.connect(self.update_stat)
        self.program_thread.start()

    def update_stat(self, total_games, total_wins):
        self.total_games_label.setText(f'Total Games: {total_games}')
        self.total_wins_label.setText(f'Total Wins: {total_wins}')
        self.update_graph(total_games, total_wins)

    def update_graph(self, total_games, total_wins):
        self.graph_scene.clear()
        win_rate = total_wins / total_games * 100 if total_games > 0 else 0
        bar_width = 100
        bar_height = win_rate * 2
        bar_item = QGraphicsRectItem(0, 200 - bar_height, bar_width, bar_height)
        bar_item.setBrush(QColor('green'))
        self.graph_scene.addItem(bar_item)


class ProgramThread(QThread):
    statUpdated = pyqtSignal(int, int)

    def __init__(self, betAmount):
        super().__init__()
        self.betAmount = betAmount
        
    def compare(self, target, temp):
        global max_loc, twidth, theight
        theight, twidth = target.shape[:2]
        tempheight, tempwidth = temp.shape[:2]
        scaleTemp = resize(
            temp, (int(tempwidth), int(tempheight)))

        res = matchTemplate(scaleTemp, target, TM_CCOEFF_NORMED)
        mn_val, max_val, min_loc, max_loc = minMaxLoc(res)

        if max_val >= 0.9:
            return 1
        else:
            return 0

    def run(self):
        global max_loc

        total_win = 0
        total_lose = 0

        win = imread(r"image/win.png", 0)
        lose = imread(r"image/lose.png", 0)

        prev_dealer_card = -1
        prev_hand_card_1 = -1
        prev_hand_card_2 = -1
        prev_action = -1

        prev_2_dealer_card = -1
        prev_2_hand_card_1 = -1
        prev_2_hand_card_2 = -1
        prev_2_action = -1

        while True:
            stand = imread(r"image/stand.png", 0)
            bet = imread(r"image/bet/bet" + self.betAmount + ".png", 0)

            screenshot('image/screen.png')
            temp = imread(r'image/screen.png', 0)

            if self.compare(stand, temp) == 1:
                dealer_card = -1
                hand_card_1 = -1
                hand_card_2 = -1
                total_points = 0
                tempheight, tempwidth = temp.shape[:2]
                scaleTemp = resize(
                    temp, (int(tempwidth), int(tempheight)))

                i = 0
                while i < 52:
                    i += 1
                    target = imread(r'image/card/' + str(i) + '.png', 0)
                    theight, twidth = target.shape[:2]

                    res = matchTemplate(
                        scaleTemp, target, TM_CCOEFF_NORMED)
                    mn_val, max_val, min_loc, max_loc = minMaxLoc(res)

                    if max_val >= 0.95:
                        if max_loc[1] < 353 and dealer_card == -1:
                            x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + \
                                15, max_loc[1] + 15
                            scaleTemp[y1:y2, x1:x2] = 0
                            dealer_card = poke(i)
                            prev_dealer_card = dealer_card
                            i -= 1
                        elif (max_loc[0] in [d1 for d2 in handA for d1 in d2]) and hand_card_1 == -1:
                            x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + \
                                15, max_loc[1] + 15
                            scaleTemp[y1:y2, x1:x2] = 0
                            hand_card_1 = poke(i)
                            prev_hand_card_1 = hand_card_1
                            total_points += hand_card_1
                            i -= 1
                        elif (max_loc[0] in [d3 for d4 in handB for d3 in d4]) and hand_card_2 == -1:
                            x1, y1, x2, y2 = max_loc[0], max_loc[1], max_loc[0] + \
                                15, max_loc[1] + 15
                            scaleTemp[y1:y2, x1:x2] = 0
                            hand_card_2 = poke(i)
                            prev_hand_card_2 = hand_card_2
                            total_points += hand_card_2
                            i -= 1
                    if total_points > 20:
                        total_points = 20

                if hand_card_1 == -1 or hand_card_2 == -1 or dealer_card == -1:
                    continue

                if hand_card_1 == hand_card_2:  # Two hand cards are equal, use table 3
                    temp = hand_card_1
                    strategy_table = strategyTable3
                elif hand_card_1 == 11 or hand_card_2 == 11:  # Contains an Ace, use table 2
                    if hand_card_1 == 11:
                        temp = hand_card_2
                    if hand_card_2 == 11:
                        temp = hand_card_1
                    strategy_table = strategyTable2
                else:  # Other situations, use table 1
                    temp = total_points - 3
                    strategy_table = strategyTable1
                if strategy_table[temp - 2][dealer_card - 2] == 'S':  # Stand
                    position = (852, 969)
                    clickz(position)
                    prev_action = 'S'
                    sleep(0.9)
                elif strategy_table[temp - 2][dealer_card - 2] == 'H':  # Hit
                    position = (594, 967)
                    clickz(position)
                    prev_action = 'H'
                    sleep(1.6)
                    clickz((854, 969))
                elif strategy_table[temp - 2][dealer_card - 2] == 'D':  # Double
                    position = (1123, 969)
                    prev_action = 'D'
                    clickz(position)
                    sleep(0.6)
                elif strategy_table[temp - 2][dealer_card - 2] == 'P':  # Split
                    position = (1373, 969)
                    clickz(position)
                    prev_action = 'P'
                    sleep(0.6)
            elif self.compare(bet, temp) == 1:
                top_left = max_loc
                clickz(top_left)
                sleep(0.01)
            elif self.compare(win, temp) == 1:
                total_win += 1
                self.statUpdated.emit(total_win + total_lose, total_win)
                if [prev_2_dealer_card, prev_2_hand_card_1, prev_2_hand_card_2, prev_2_action] == [prev_dealer_card, prev_hand_card_1, prev_hand_card_2, prev_action]:
                    continue
                prev_2_dealer_card, prev_2_hand_card_1, prev_2_hand_card_2, prev_2_action = prev_dealer_card, prev_hand_card_1, prev_hand_card_2, prev_action
                sleep(2)

            elif self.compare(lose, temp) == 1:
                total_lose += 1
                self.statUpdated.emit(total_win + total_lose, total_win)
                if [prev_2_dealer_card, prev_2_hand_card_1, prev_2_hand_card_2, prev_2_action] == [prev_dealer_card, prev_hand_card_1, prev_hand_card_2, prev_action]:
                    continue
                prev_2_dealer_card, prev_2_hand_card_1, prev_2_hand_card_2, prev_2_action = prev_dealer_card, prev_hand_card_1, prev_hand_card_2, prev_action
                sleep(2)
            else:
                sleep(0.2)

if __name__ == '__main__':
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
