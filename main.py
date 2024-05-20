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

# Hand card positions
FIRST_HAND_POS = [range(895, 912), range(1028, 1040), range(744, 762)]
SECOND_HAND_POS = [range(939, 953), range(1072, 1084), range(789, 803)]

max_loc = None

OP_POS = {
    'stand': (852, 969),
    'hit': (594, 967),
    'double': (1123, 969),
    'split': (1373, 969),
}

CHEAT_SHEET = {
    ('8', '2'): "hit", ('8', '3'): "hit", ('8', '4'): "hit", ('8', '5'): "hit", ('8', '6'): "hit", ('8', '7'): "hit", ('8', '8'): "hit", ('8', '9'): "hit", ('8', '10'): "hit", ('8', 'A'): "hit",
    ('9', '2'): "hit", ('9', '3'): "double", ('9', '4'): "double", ('9', '5'): "double", ('9', '6'): "double", ('9', '7'): "hit", ('9', '8'): "hit", ('9', '9'): "hit", ('9', '10'): "hit", ('9', 'A'): "hit",
    ('10', '2'): "double", ('10', '3'): "double", ('10', '4'): "double", ('10', '5'): "double", ('10', '6'): "double", ('10', '7'): "double", ('10', '8'): "double", ('10', '9'): "double", ('10', '10'): "hit", ('10', 'A'): "hit",
    ('11', '2'): "double", ('11', '3'): "double", ('11', '4'): "double", ('11', '5'): "double", ('11', '6'): "double", ('11', '7'): "double", ('11', '8'): "double", ('11', '9'): "double", ('11', '10'): "double", ('11', 'A'): "double",
    ('12', '2'): "hit", ('12', '3'): "hit", ('12', '4'): "stand", ('12', '5'): "stand", ('12', '6'): "stand", ('12', '7'): "hit", ('12', '8'): "hit", ('12', '9'): "hit", ('12', '10'): "hit", ('12', 'A'): "hit",
    ('13', '2'): "stand", ('13', '3'): "stand", ('13', '4'): "stand", ('13', '5'): "stand", ('13', '6'): "stand", ('13', '7'): "hit", ('13', '8'): "hit", ('13', '9'): "hit", ('13', '10'): "hit", ('13', 'A'): "hit",
    ('14', '2'): "stand", ('14', '3'): "stand", ('14', '4'): "stand", ('14', '5'): "stand", ('14', '6'): "stand", ('14', '7'): "hit", ('14', '8'): "hit", ('14', '9'): "hit", ('14', '10'): "hit", ('14', 'A'): "hit",
    ('15', '2'): "stand", ('15', '3'): "stand", ('15', '4'): "stand", ('15', '5'): "stand", ('15', '6'): "stand", ('15', '7'): "hit", ('15', '8'): "hit", ('15', '9'): "hit", ('15', '10'): "hit", ('15', 'A'): "hit",
    ('16', '2'): "stand", ('16', '3'): "stand", ('16', '4'): "stand", ('16', '5'): "stand", ('16', '6'): "stand", ('16', '7'): "hit", ('16', '8'): "hit", ('16', '9'): "hit", ('16', '10'): "hit", ('16', 'A'): "hit",
    ('17', '2'): "stand", ('17', '3'): "stand", ('17', '4'): "stand", ('17', '5'): "stand", ('17', '6'): "stand", ('17', '7'): "stand", ('17', '8'): "stand", ('17', '9'): "stand", ('17', '10'): "stand", ('17', 'A'): "stand",
    ('A,2', '2'): "hit", ('A,2', '3'): "hit", ('A,2', '4'): "hit", ('A,2', '5'): "double", ('A,2', '6'): "double", ('A,2', '7'): "hit", ('A,2', '8'): "hit", ('A,2', '9'): "hit", ('A,2', '10'): "hit", ('A,2', 'A'): "hit",
    ('A,3', '2'): "hit", ('A,3', '3'): "hit", ('A,3', '4'): "hit", ('A,3', '5'): "double", ('A,3', '6'): "double", ('A,3', '7'): "hit", ('A,3', '8'): "hit", ('A,3', '9'): "hit", ('A,3', '10'): "hit", ('A,3', 'A'): "hit",
    ('A,4', '2'): "hit", ('A,4', '3'): "hit", ('A,4', '4'): "double", ('A,4', '5'): "double", ('A,4', '6'): "double", ('A,4', '7'): "hit", ('A,4', '8'): "hit", ('A,4', '9'): "hit", ('A,4', '10'): "hit", ('A,4', 'A'): "hit",
    ('A,5', '2'): "hit", ('A,5', '3'): "hit", ('A,5', '4'): "double", ('A,5', '5'): "double", ('A,5', '6'): "double", ('A,5', '7'): "hit", ('A,5', '8'): "hit", ('A,5', '9'): "hit", ('A,5', '10'): "hit", ('A,5', 'A'): "hit",
    ('A,6', '2'): "hit", ('A,6', '3'): "hit", ('A,6', '4'): "double", ('A,6', '5'): "double", ('A,6', '6'): "double", ('A,6', '7'): "hit", ('A,6', '8'): "hit", ('A,6', '9'): "hit", ('A,6', '10'): "hit", ('A,6', 'A'): "hit",
    ('A,7', '2'): "stand", ('A,7', '3'): "stand", ('A,7', '4'): "stand", ('A,7', '5'): "stand", ('A,7', '6'): "stand", ('A,7', '7'): "stand", ('A,7', '8'): "stand", ('A,7', '9'): "stand", ('A,7', '10'): "stand", ('A,7', 'A'): "stand",
    ('A,8', '2'): "stand", ('A,8', '3'): "stand", ('A,8', '4'): "stand", ('A,8', '5'): "stand", ('A,8', '6'): "stand", ('A,8', '7'): "stand", ('A,8', '8'): "stand", ('A,8', '9'): "stand", ('A,8', '10'): "stand", ('A,8', 'A'): "stand",
    ('A,9', '2'): "stand", ('A,9', '3'): "stand", ('A,9', '4'): "stand", ('A,9', '5'): "stand", ('A,9', '6'): "stand", ('A,9', '7'): "stand", ('A,9', '8'): "stand", ('A,9', '9'): "stand", ('A,9', '10'): "stand", ('A,9', 'A'): "stand",
    ('A,10', '2'): "stand", ('A,10', '3'): "stand", ('A,10', '4'): "stand", ('A,10', '5'): "stand", ('A,10', '6'): "stand", ('A,10', '7'): "stand", ('A,10', '8'): "stand", ('A,10', '9'): "stand", ('A,10', '10'): "stand", ('A,10', 'A'): "stand",
    ('A,A', '2'): "split", ('A,A', '3'): "split", ('A,A', '4'): "split", ('A,A', '5'): "split", ('A,A', '6'): "split", ('A,A', '7'): "split", ('A,A', '8'): "split", ('A,A', '9'): "split", ('A,A', '10'): "stand", ('A,A', 'A'): "split",
    ('2,2', '2'): "split", ('2,2', '3'): "split", ('2,2', '4'): "hit", ('2,2', '5'): "hit", ('2,2', '6'): "hit", ('2,2', '7'): "split", ('2,2', '8'): "split", ('2,2', '9'): "hit", ('2,2', '10'): "hit", ('2,2', 'A'): "hit",
    ('3,3', '2'): "split", ('3,3', '3'): "split", ('3,3', '4'): "hit", ('3,3', '5'): "hit", ('3,3', '6'): "hit", ('3,3', '7'): "split", ('3,3', '8'): "split", ('3,3', '9'): "hit", ('3,3', '10'): "hit", ('3,3', 'A'): "hit",
    ('4,4', '2'): "hit", ('4,4', '3'): "hit", ('4,4', '4'): "hit", ('4,4', '5'): "hit", ('4,4', '6'): "hit", ('4,4', '7'): "hit", ('4,4', '8'): "hit", ('4,4', '9'): "hit", ('4,4', '10'): "hit", ('4,4', 'A'): "hit",
    ('5,5', '2'): "double", ('5,5', '3'): "double", ('5,5', '4'): "double", ('5,5', '5'): "double", ('5,5', '6'): "double", ('5,5', '7'): "double", ('5,5', '8'): "double", ('5,5', '9'): "double", ('5,5', '10'): "hit", ('5,5', 'A'): "hit",
    ('6,6', '2'): "split", ('6,6', '3'): "split", ('6,6', '4'): "hit", ('6,6', '5'): "hit", ('6,6', '6'): "split", ('6,6', '7'): "split", ('6,6', '8'): "hit", ('6,6', '9'): "hit", ('6,6', '10'): "hit", ('6,6', 'A'): "hit",
    ('7,7', '2'): "split", ('7,7', '3'): "split", ('7,7', '4'): "split", ('7,7', '5'): "split", ('7,7', '6'): "split", ('7,7', '7'): "hit", ('7,7', '8'): "hit", ('7,7', '9'): "hit", ('7,7', '10'): "hit", ('7,7', 'A'): "hit",
    ('8,8', '2'): "split", ('8,8', '3'): "split", ('8,8', '4'): "split", ('8,8', '5'): "split", ('8,8', '6'): "split", ('8,8', '7'): "split", ('8,8', '8'): "split", ('8,8', '9'): "split", ('8,8', '10'): "split", ('8,8', 'A'): "split",
    ('9,9', '2'): "split", ('9,9', '3'): "split", ('9,9', '4'): "split", ('9,9', '5'): "split", ('9,9', '6'): "split", ('9,9', '7'): "stand", ('9,9', '8'): "split", ('9,9', '9'): "split", ('9,9', '10'): "stand", ('9,9', 'A'): "stand",
    ('10,10', '2'): "stand", ('10,10', '3'): "stand", ('10,10', '4'): "stand", ('10,10', '5'): "stand", ('10,10', '6'): "stand", ('10,10', '7'): "stand", ('10,10', '8'): "stand", ('10,10', '9'): "stand", ('10,10', '10'): "stand", ('10,10', 'A'): "stand",
    ('A,A', '2'): "split", ('A,A', '3'): "split", ('A,A', '4'): "split", ('A,A', '5'): "split", ('A,A', '6'): "split", ('A,A', '7'): "split", ('A,A', '8'): "split", ('A,A', '9'): "split", ('A,A', '10'): "stand", ('A,A', 'A'): "split",
}

NUMBER = ['a', '2', '3', '4', '5', '6', '7', '8', '9', 't', 'j', 'q', 'k']

COLOR = ['c', 'd', 'h', 's']

BUTTON_WIDTH = 215
BUTTON_HEIGHT = 115

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

def clickz(top_left):
    x = top_left[0] + BUTTON_WIDTH / 2
    y = top_left[1] + BUTTON_HEIGHT / 2
    pyautogui.click(x, y, button="left", duration=0.25)
    pyautogui.moveTo(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, duration=0.25)


def card_num_from_card_name(card_name):
    if card_name[1] in ["t", "j", "q", "k"]:
        return 10
    elif card_name[1] == "a":
        return 11
    else:
        return int(card_name[1])


def card_num_str_from_card_name(card_name):
    if card_name[1] in ["t", "j", "q", "k"]:
        return "10"
    elif card_name[1] == "a":
        return "A"
    else:
        return card_name[1]


def card_suite_from_two_card_num(card_num1: int, card_num2: int) -> str:
    if card_num1 == card_num2:
        return str(card_num1) + "," + str(card_num2)
    elif card_num1 == 11 or card_num2 == 11:
        return (
            "A" + "," + str(card_num1)
            if card_num2 == 11
            else "A" + "," + str(card_num2)
        )
    else:
        minn = min(card_num1, card_num2)
        maxx = max(card_num1, card_num2)
        return str(minn + maxx)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack Bot")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.bet_amount_label = QLabel("Bet Amount:")
        self.bet_amount_input = QComboBox()
        self.bet_amount_input.addItems(
            [
                "1k",
                "2.5k",
                "5k",
                "10k",
                "25k",
                "50k",
                "100k",
                "200k",
                "500k",
                "1M",
                "2.5M",
                "5M",
                "10M",
                "25M",
                "50M",
                "100M",
            ]
        )
        input_layout.addWidget(self.bet_amount_label)
        input_layout.addWidget(self.bet_amount_input)
        main_layout.addLayout(input_layout)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_program)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_program)
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.stop_button)

        self.statistics_layout = QVBoxLayout()
        self.total_games_label = QLabel("Total Games: 0")
        self.total_wins_label = QLabel("Total Wins: 0")
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
        bet_amount = self.bet_amount_input.currentText()
        self.program_thread = ProgramThread(bet_amount)
        self.program_thread.statUpdated.connect(self.update_stat)
        self.program_thread.start()

    def stop_program(self):
        if hasattr(self, 'program_thread') and self.program_thread.isRunning():
            self.program_thread.terminate()

    def update_stat(self, total_games, total_wins):
        self.total_games_label.setText(f"Total Games: {total_games}")
        self.total_wins_label.setText(f"Total Wins: {total_wins}")
        self.update_graph(total_games, total_wins)

    def update_graph(self, total_games, total_wins):
        self.graph_scene.clear()
        win_rate = total_wins / total_games * 100 if total_games > 0 else 0
        bar_width = 100
        bar_height = win_rate * 2
        bar_item = QGraphicsRectItem(0, 200 - bar_height, bar_width, bar_height)
        bar_item.setBrush(QColor("green"))
        self.graph_scene.addItem(bar_item)


class ProgramThread(QThread):
    statUpdated = pyqtSignal(int, int)

    def __init__(self, bet_amount):
        super().__init__()
        self.bet_amount = bet_amount
        self.running = True
        self.card_images = {}
        for num in NUMBER:
            for col in COLOR:
                card_name = col + num
                card_image = imread(r"image/card/" + card_name + ".png", 0)
                self.card_images[card_name] = card_image

    def compare(self, target, screen):
        global max_loc
        res = matchTemplate(screen, target, TM_CCOEFF_NORMED)
        _, val, _, max_loc = minMaxLoc(res)
        return True if val >= 0.9 else False

    def run(self):
        global max_loc
        total_win = 0
        total_lose = 0

        win = imread(r"image/win.png", 0)
        lose = imread(r"image/lose.png", 0)
        stand = imread(r"image/stand.png", 0)
        double = imread(r"image/double.png", 0)
        bet = imread(r"image/bet/bet" + self.bet_amount + ".png", 0)

        while self.running:
            screenshot("image/screen.png")
            screen = imread(r"image/screen.png", 0)
            screen = resize(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

            if self.compare(double, screen) is True:
                # which means it's the first round
                # in first round, we should only have 2 cards
                first_card = ""
                second_card = ""
                dealer_card = ""
                for (card_name, card_image) in self.card_images.items():
                    res = matchTemplate(screen, card_image, TM_CCOEFF_NORMED)
                    _, val, _, loc = minMaxLoc(res)
                    if val >= 0.95:
                        # magic number to determine the position of the card
                        if loc[1] < 353 and dealer_card == "":
                            dealer_card = card_name
                        elif (
                            loc[0] in [d1 for d2 in FIRST_HAND_POS for d1 in d2]
                        ) and first_card == "":
                            first_card = card_name
                        elif (
                            loc[0] in [d3 for d4 in SECOND_HAND_POS for d3 in d4]
                        ) and second_card == "":
                            second_card = card_name
                if "" in [first_card, second_card, dealer_card]:
                    continue
                strategy = ""
                card_num1, card_num2 = card_num_from_card_name(first_card), card_num_from_card_name(second_card)
                if card_num1 + card_num2 > 17:
                    strategy = "stand"
                elif card_num1 + card_num2 < 8:
                    strategy = "hit"
                else:
                    dealer_card_num_str = card_num_str_from_card_name(dealer_card)
                    strategy = CHEAT_SHEET[
                        (
                            card_suite_from_two_card_num(card_num1, card_num2),
                            dealer_card_num_str,
                        )
                    ]
                clickz(OP_POS[strategy])
            elif self.compare(stand, screen) is True:
                # which means it's the second round
                # in second round, we could have mulitple cards
                dealer_card = ""
                total_points = 0

                for (card_name, card_image) in self.card_images.items():
                    res = matchTemplate(screen, card_image, TM_CCOEFF_NORMED)
                    _, max_val, _, loc = minMaxLoc(res)
                    if max_val >= 0.95:
                        # magic number to determine the position of the card
                        if loc[1] < 353 and dealer_card == "":
                            dealer_card = card_name
                        else:
                            total_points += card_num_from_card_name(card_name)
                if dealer_card == "":
                    continue
                strategy = ""
                if total_points > 17:
                    strategy = "stand"
                elif total_points < 8:
                    strategy = "hit"
                else:
                    dealer_card_num_str = card_num_str_from_card_name(dealer_card)
                    strategy = CHEAT_SHEET[
                        (
                            str(total_points),
                            dealer_card_num_str,
                        )
                    ]
                clickz(OP_POS[strategy])
            elif self.compare(bet, screen) is True:
                clickz(max_loc)
                # sleep to avoid multi counting
                sleep(2)
            elif self.compare(win, screen) == 1:
                total_win += 1
                self.statUpdated.emit(total_win + total_lose, total_win)
                # sleep to avoid multi counting
                sleep(2)
            elif self.compare(lose, screen) == 1:
                total_lose += 1
                self.statUpdated.emit(total_win + total_lose, total_win)
    def stop(self):
        self.terminate()
        self.wait()

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
