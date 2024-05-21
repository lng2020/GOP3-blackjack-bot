import pyautogui
from pyscreeze import screenshot
from cv2 import resize, matchTemplate, TM_CCOEFF_NORMED, imread, minMaxLoc
from time import sleep
from warnings import simplefilter
import os
from PyQt5.QtWidgets import QApplication, QGridLayout, QTableWidget, QTableWidgetItem, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QComboBox
from PyQt5.QtGui import QColor, QIntValidator
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import where as np_where

# Omit pyautogui warning
simplefilter("ignore")
pyautogui.FAILSAFE = False

CHEAT_SHEET = {
    ('5', '2'): "hit", ('5', '3'): "hit", ('5', '4'): "hit", ('5', '5'): "hit", ('5', '6'): "hit", ('5', '7'): "hit", ('5', '8'): "hit", ('5', '9'): "hit", ('5', '10'): "hit", ('5', 'A'): "hit",
    ('6', '2'): "hit", ('6', '3'): "hit", ('6', '4'): "hit", ('6', '5'): "hit", ('6', '6'): "hit", ('6', '7'): "hit", ('6', '8'): "hit", ('6', '9'): "hit", ('6', '10'): "hit", ('6', 'A'): "hit",
    ('7', '2'): "hit", ('7', '3'): "hit", ('7', '4'): "hit", ('7', '5'): "hit", ('7', '6'): "hit", ('7', '7'): "hit", ('7', '8'): "hit", ('7', '9'): "hit", ('7', '10'): "hit", ('7', 'A'): "hit",
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
    ('18', '2'): "stand", ('18', '3'): "stand", ('18', '4'): "stand", ('18', '5'): "stand", ('18', '6'): "stand", ('18', '7'): "stand", ('18', '8'): "stand", ('18', '9'): "stand", ('18', '10'): "stand", ('18', 'A'): "stand",
    ('19', '2'): "stand", ('19', '3'): "stand", ('19', '4'): "stand", ('19', '5'): "stand", ('19', '6'): "stand", ('19', '7'): "stand", ('19', '8'): "stand", ('19', '9'): "stand", ('19', '10'): "stand", ('19', 'A'): "stand",
    ('20', '2'): "stand", ('20', '3'): "stand", ('20', '4'): "stand", ('20', '5'): "stand", ('20', '6'): "stand", ('20', '7'): "stand", ('20', '8'): "stand", ('20', '9'): "stand", ('20', '10'): "stand", ('20', 'A'): "stand",
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

BET_AMOUNT = {
    "1k": 1,
    "2.5k": 2.5,
    "5k": 5,
    "10k": 10,
    "25k": 25,
    "50k": 50,
    "100k": 100,
    "200k": 200,
    "500k": 500,
    "1M": 1000,
    "2.5M": 2500,
    "5M": 5000,
    "10M": 10000,
    "20M": 20000,
    "50M": 50000,
    "100M": 100000,
}

BUTTON_WIDTH_PERCENT = 0.112 
BUTTON_HEIGHT_PERCENT = 0.106 

FIRST_HAND_POS_PERCENT = [
    (0.466, 0.475), 
    (0.952, 0.962),
    (0.388, 0.396)
]

SECOND_HAND_POS_PERCENT = [
    (0.489, 0.496),
    (0.993, 1.003),
    (0.411, 0.418)
]

OP_POS_PERCENT = {
    'stand': (0.444, 0.897),
    'hit': (0.309, 0.895),
    'double': (0.585, 0.897),
    'split': (0.715, 0.897)
}

FIRST_HAND_POS = [range(895, 912), range(1028, 1040), range(744, 762)]
SECOND_HAND_POS = [range(939, 953), range(1072, 1084), range(789, 803)]

OP_POS = {
    'stand': (852, 969),
    'hit': (594, 967),
    'double': (1123, 969),
    'split': (1373, 969),
}

BUTTON_WIDTH = 215
BUTTON_HEIGHT = 115

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

def clickz(top_left):
    x = top_left[0] + BUTTON_WIDTH / 2
    y = top_left[1] + BUTTON_HEIGHT / 2
    pyautogui.click(x, y, button="left", duration=0.1)
    pyautogui.moveTo(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, duration=0.1)

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
        if card_num1 == 11 and card_num2 == 11:
            return "A,A"
        return str(card_num1) + "," + str(card_num2)
    elif card_num1 == 11 or card_num2 == 11:
        if card_num1 == 11 and card_num2 == 11:
            return "A,A"
        elif card_num1 == 11:
            return "A," + str(card_num2)
        else:
            return "A," + str(card_num1)
    else:
        return str(card_num1+card_num2)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blackjack Bot")
        self.setGeometry(100, 100, 1200, 800)

        main_layout = QHBoxLayout()

        # Left Layout
        left_layout = QVBoxLayout()

        # Input Layout
        input_layout = QGridLayout()

        self.round_config_label = QLabel("Round Configuration")
        self.round_config_label.setStyleSheet("font-weight: bold;")
        self.bet_amount_label = QLabel("Bet Amount:")
        self.bet_amount_input = QComboBox()
        self.bet_amount_input.addItems([
            "1k", "2.5k", "5k", "10k", "25k", "50k", "100k",
            "200k", "500k", "1M", "2.5M", "5M", "10M", "20M", "50M", "100M"
        ])
        self.bet_amount_input.setFixedWidth(150)

        self.num_games_label = QLabel("Round Hands: ")
        self.num_games_input = QLineEdit()
        self.num_games_input.setText("1000")
        self.num_games_input.setValidator(QIntValidator())
        self.num_games_input.setFixedWidth(150)

        self.stop_win_label = QLabel("Stop at Net Profit Multiple(Based on Bet Amount):")
        self.stop_win_input = QLineEdit()
        self.stop_win_input.setText("100")
        self.stop_win_input.setValidator(QIntValidator())
        self.stop_win_input.setFixedWidth(150)

        self.stop_lose_label = QLabel("Stop at Net Lose Multiple(Based on Bet Amount):")
        self.stop_lose_input = QLineEdit()
        self.stop_lose_input.setText("100")
        self.stop_lose_input.setValidator(QIntValidator())
        self.stop_lose_input.setFixedWidth(150)

        input_layout.addWidget(self.round_config_label, 0, 0, 1, 2)
        input_layout.addWidget(self.bet_amount_label, 1, 0)
        input_layout.addWidget(self.bet_amount_input, 1, 1)
        input_layout.addWidget(self.num_games_label, 2, 0)
        input_layout.addWidget(self.num_games_input, 2, 1)
        input_layout.addWidget(self.stop_win_label, 3, 0)
        input_layout.addWidget(self.stop_win_input, 3, 1)
        input_layout.addWidget(self.stop_lose_label, 4, 0)
        input_layout.addWidget(self.stop_lose_input, 4, 1)

        # Cheat Sheet Layout
        self.cheat_sheet_layout = QVBoxLayout()
        self.cheat_sheet_label = QLabel("Strategy Configuration Cheatsheet:")
        self.cheat_sheet_table = QTableWidget()
        self.cheat_sheet_table.setColumnCount(11)
        self.cheat_sheet_table.setHorizontalHeaderLabels(["", "2", "3", "4", "5", "6", "7", "8", "9", "10", "A"])
        self.cheat_sheet_table.verticalHeader().setVisible(False)
        self.cheat_sheet_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cheat_sheet_table.setFixedHeight(580)
        self.cheat_sheet_table.setFixedWidth(540)
        self.cheat_sheet_table.setStyleSheet("border: 1px solid #ccc;")
        self.cheat_sheet_layout.addWidget(self.cheat_sheet_label)
        self.cheat_sheet_layout.addWidget(self.cheat_sheet_table)
        self.populate_cheat_sheet()

        # Button Layout
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_program)
        self.start_button.setCheckable(True)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_program)
        self.stop_button.setCheckable(True)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.setAlignment(Qt.AlignCenter)
        self.update_button_styles()

        left_layout.addLayout(input_layout)
        left_layout.addLayout(self.cheat_sheet_layout)
        left_layout.addLayout(button_layout)

        # Right Layout
        right_layout = QVBoxLayout()

        # Round Information Layout
        self.round_info_layout = QGridLayout()
        self.round_info_label = QLabel("Round Information")
        self.round_info_label.setStyleSheet("font-weight: bold;")
        self.dealer_card_label = QLabel("Dealer Card: ")
        self.player_cards_label = QLabel("Player Cards: ")
        self.strategy_label = QLabel("Strategy: ")
        self.remaining_hands_label = QLabel("Remaining Hands: ")
        self.net_win_label = QLabel("Net Win: ")
        self.round_info_layout.addWidget(self.round_info_label, 0, 0, 1, 2)
        self.round_info_layout.addWidget(self.dealer_card_label, 1, 0)
        self.round_info_layout.addWidget(self.player_cards_label, 1, 1)
        self.round_info_layout.addWidget(self.strategy_label, 2, 0)
        self.round_info_layout.addWidget(self.remaining_hands_label, 2, 1)
        self.round_info_layout.addWidget(self.net_win_label, 2, 3)

        # Statistics Layout
        self.statistics_layout = QGridLayout()
        self.statistics_label = QLabel("Game Statistics")
        self.statistics_label.setStyleSheet("font-weight: bold;")
        self.total_hand_label = QLabel("Total Hands: 0")
        self.total_win_label = QLabel("Total Wins: 0")
        self.total_lose_label = QLabel("Total Lose: 0")
        self.total_draw_label = QLabel("Total Draw: 0")
        self.statistics_layout.addWidget(self.statistics_label, 0, 0, 1, 2)
        self.statistics_layout.addWidget(self.total_hand_label, 1, 0)
        self.statistics_layout.addWidget(self.total_win_label, 1, 1)
        self.statistics_layout.addWidget(self.total_lose_label, 2, 0)
        self.statistics_layout.addWidget(self.total_draw_label, 2, 1)

        # Graph View
        self.graph_view = QGraphicsView()
        self.graph_scene = QGraphicsScene()
        self.graph_view.setScene(self.graph_scene)
        self.graph_view.setFixedSize(600, 600)
        self.graph_view.setStyleSheet("border: 1px solid #ccc;")

        right_layout.addLayout(self.round_info_layout)
        right_layout.addLayout(self.statistics_layout)
        right_layout.addWidget(self.graph_view)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.total_hand = 0
        self.total_win = 0
        self.total_lose = 0
        self.total_draw = 0
        self.bet_amounts = []
        self.win_amounts = []
        self.net_win = 0
        self.round_hand = 0

    def start_program(self):
        if self.start_button.isChecked():
            self.bet_amount = self.bet_amount_input.currentText()
            self.num_games = int(self.num_games_input.text())
            self.stop_net_profit = int(self.stop_win_input.text())
            self.stop_net_lose = int(self.stop_lose_input.text())
            self.program_thread = ProgramThread(self.bet_amount)
            self.program_thread.statUpdated.connect(self.update_stat)
            self.program_thread.roundInformUpdated.connect(self.update_round_info)
            self.program_thread.start()
        else:
            self.stop_program()
        self.update_button_styles()

    def stop_program(self):
        if hasattr(self, "program_thread"):
            self.program_thread.running = False
        self.start_button.setChecked(False)
        self.stop_button.setChecked(False)
        self.update_button_styles()
        self.net_win = 0
        self.round_hand = 0
    
    def update_stat(self, bet_rate, condition):
        self.total_hand += 1
        self.round_hand += 1
        self.total_hand_label.setText(f"Total Hands: {self.total_hand}")
        self.remaining_hands_label.setText(f"Remaining Hands: {self.num_games - self.total_hand}")
        win_rate = 0
        win_amount = 0
        if condition == "win":
            self.total_win += 1
            win_rate = 2 * bet_rate
        elif condition == "lose":
            self.total_lose += 1
        else:
            self.total_draw += 1
            win_rate = bet_rate
        win_amount = win_rate * BET_AMOUNT[self.bet_amount]   
        bet_amount = BET_AMOUNT[self.bet_amount]
        self.total_win_label.setText(f"Total Wins: {self.total_win}")
        self.total_lose_label.setText(f"Total Lose: {self.total_lose}")
        self.total_draw_label.setText(f"Total Draw: {self.total_draw}")
        last_bet_amount = self.bet_amounts[-1] if self.bet_amounts else 0
        last_win_amount = self.win_amounts[-1] if self.win_amounts else 0
        self.bet_amounts.append(last_bet_amount + bet_amount)
        self.win_amounts.append(last_win_amount + win_amount)
        self.update_graph(self.bet_amounts, self.win_amounts)

        if self.round_hand >= self.num_games:
            self.stop_program()
        net_win = win_rate - 1
        self.net_win += net_win
        self.net_win_label.setText(f"Net Win: {self.net_win}")
        if self.net_win >= self.stop_net_profit or self.net_win <= -self.stop_net_lose:
            self.stop_program()
    
    def update_round_info(self, dealer_card, player_cards, strategy):
        self.dealer_card_label.setText(f"Dealer Card: {dealer_card}")
        self.player_cards_label.setText(f"Player Cards: {player_cards}")
        self.strategy_label.setText(f"Strategy: {strategy}")

    def update_graph(self, bet_amounts, win_amounts):
        self.graph_scene.clear()

        figure = plt.figure(figsize=(6, 6))
        canvas = FigureCanvas(figure)

        ax = figure.add_subplot(111)
        ax.plot(bet_amounts, win_amounts)
        ax.set_xlabel('Bet Amount (in 1k)', fontsize=12)
        ax.set_ylabel('Win Amount (in 1k)', fontsize=12)
        ax.set_title('Bet Amount vs Win Amount')

        plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)

        self.graph_scene.addWidget(canvas)
    
    def populate_cheat_sheet(self):
        rows = ["5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                "A,2", "A,3", "A,4", "A,5", "A,6", "A,7", "A,8", "A,9", "A,10", "A,A",
                "2,2", "3,3", "4,4", "5,5", "6,6", "7,7", "8,8", "9,9", "10,10"]
        self.cheat_sheet_table.setRowCount(len(rows))

        for row, player_hand in enumerate(rows):
            self.cheat_sheet_table.setItem(row, 0, QTableWidgetItem(str(player_hand)))
            for col, dealer_card in enumerate(["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]):
                key = (player_hand, dealer_card)
                if key in CHEAT_SHEET:
                    action = CHEAT_SHEET[key]
                    item = QTableWidgetItem(action)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.cheat_sheet_table.setItem(row, col + 1, item)

        self.cheat_sheet_table.resizeColumnsToContents()

    def update_button_styles(self):
        if self.start_button.isChecked():
            self.start_button.setStyleSheet("background-color: #388E3C; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;")
        else:
            self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;")

        if self.stop_button.isChecked():
            self.stop_button.setStyleSheet("background-color: #D32F2F; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;")
        else:
            self.stop_button.setStyleSheet("background-color: #F44336; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;")

class ProgramThread(QThread):
    statUpdated = pyqtSignal(int, str)
    roundInformUpdated = pyqtSignal(str, str, str)

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
        res = matchTemplate(screen, target, TM_CCOEFF_NORMED)
        _, val, _, loc = minMaxLoc(res)
        return loc if val >= 0.9 else None

    def run(self):
        is_doubled = False
        is_blackjack = False
        is_split = False

        win = imread(r"image/win.png", 0)
        lose = imread(r"image/lose.png", 0)
        draw = imread(r"image/draw.png", 0)
        stand = imread(r"image/stand.png", 0)
        double = imread(r"image/double.png", 0)
        bet = imread(r"image/bet/bet" + self.bet_amount + ".png", 0)

        while self.running:
            screenshot("image/screen.png")
            screen = imread(r"image/screen.png", 0)
            screen = resize(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

            if self.compare(win, screen):
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2 
                elif is_blackjack:
                    amount_rate = 2.5
                is_doubled = False
                is_blackjack = False
                is_split = False
                self.statUpdated.emit(amount_rate, "win")
                sleep(1.5)
            elif self.compare(lose, screen):
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2 
                is_doubled = False
                is_blackjack = False
                is_split = False
                self.statUpdated.emit(amount_rate, "lose")
                sleep(1.5)
            elif self.compare(draw, screen):
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2
                is_doubled = False
                is_blackjack = False
                is_split = False
                self.statUpdated.emit(amount_rate * BET_AMOUNT[self.bet_amount], "draw")
                sleep(1.5)
            elif self.compare(double, screen):
                first_card = ""
                second_card = ""
                dealer_card = ""
                for (card_name, card_image) in self.card_images.items():
                    res = matchTemplate(screen, card_image, TM_CCOEFF_NORMED)
                    loc = np_where(res >= 0.95)
                    for pt in zip(*loc[::-1]):
                        # magic number to determine the position of the card
                        if pt[1] < 353:
                            dealer_card = card_name
                        elif pt[0] in [d1 for d2 in FIRST_HAND_POS for d1 in d2]:
                            first_card = card_name
                        elif pt[0] in [d3 for d4 in SECOND_HAND_POS for d3 in d4]:
                            second_card = card_name
                    if dealer_card and first_card and second_card:
                            break
                if "" in [first_card, second_card, dealer_card]:
                    continue
                card_num1, card_num2 = card_num_from_card_name(first_card), card_num_from_card_name(second_card)
                if card_num1 + card_num2 == 21:
                    is_blackjack = True
                    self.roundInformUpdated.emit(dealer_card, first_card + "," + second_card, "stand")
                    continue
                dealer_card_num_str = card_num_str_from_card_name(dealer_card)
                strategy = CHEAT_SHEET[
                    (
                        card_suite_from_two_card_num(card_num1, card_num2),
                        dealer_card_num_str,
                    )
                ]
                if strategy == "double":
                    is_doubled = True
                if strategy == "split" and not is_split:
                    is_split = True
                elif strategy == "split" and is_split:
                    # we can't split again
                    if card_num1 + card_num2 < 12:
                        strategy = "hit"
                    else:
                        strategy = "stand"
                self.roundInformUpdated.emit(dealer_card, first_card + "," + second_card, strategy)
                clickz(OP_POS[strategy])
            elif self.compare(stand, screen):
                # which means it's the second round and could have mulitple cards
                dealer_card = ""
                total_points = 0
                cards = []

                for (card_name, card_image) in self.card_images.items():
                    res = matchTemplate(screen, card_image, TM_CCOEFF_NORMED)
                    loc = np_where(res >= 0.95)
                    for pt in zip(*loc[::-1]):
                        # magic number to determine the position of the card
                        if pt[1] < 353:
                            dealer_card = card_name
                        else:
                            total_points += card_num_from_card_name(card_name)
                            cards += [card_name]
                if dealer_card == "" or total_points == 0 or len(cards) < 2:
                    continue
                if total_points == 21:
                    self.roundInformUpdated.emit(dealer_card, ",".join(cards), "stand")
                    continue
                elif total_points > 21:
                    total_points = total_points % 10 + 10
                dealer_card_num_str = card_num_str_from_card_name(dealer_card)
                strategy = CHEAT_SHEET[
                    (
                        str(total_points),
                        dealer_card_num_str,
                    )
                ]
                if strategy == "double":
                    strategy = "hit"
                self.roundInformUpdated.emit(dealer_card, ",".join(cards), strategy)
                clickz(OP_POS[strategy])
            elif (res := self.compare(bet, screen)) is not None:
                clickz(res)
            
    def stop(self):
        self.terminate()
        self.wait()

if __name__ == "__main__":
    app = QApplication([])
    window = App()
    window.show()
    app.exec_()
