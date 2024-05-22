from PyQt5.QtWidgets import (
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsView,
    QGraphicsScene,
    QComboBox,
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from constant import SUPPORTED_LANGUAGE, LANGUAGE_MAP, CHEAT_SHEET, BET_AMOUNT
from blackjack import ProgramThread


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

        self.system_config_label = QLabel("System Configuration")
        self.system_config_label.setStyleSheet("font-weight: bold;")
        self.resolution_label = QLabel("Resolution: ")
        self.resolution_input = QComboBox()
        self.resolution_input.addItems(["1920x1080", "1280x720", "800x600"])
        self.language_label = QLabel("GOP3 Interface Language")
        self.language_input = QComboBox()
        for language in SUPPORTED_LANGUAGE:
            self.language_input.addItem(language)
        self.language_input.setFixedWidth(150)
        self.round_config_label = QLabel("Round Configuration")
        self.round_config_label.setStyleSheet("font-weight: bold;")
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
                "20M",
                "50M",
                "100M",
            ]
        )
        self.bet_amount_input.setFixedWidth(150)

        self.num_games_label = QLabel("Round Hands: ")
        self.num_games_input = QLineEdit()
        self.num_games_input.setText("1000")
        self.num_games_input.setValidator(QIntValidator())
        self.num_games_input.setFixedWidth(150)

        self.stop_win_label = QLabel(
            "Stop at Net Profit Multiple(Based on Bet Amount):"
        )
        self.stop_win_input = QLineEdit()
        self.stop_win_input.setText("100")
        self.stop_win_input.setValidator(QIntValidator())
        self.stop_win_input.setFixedWidth(150)

        self.stop_lose_label = QLabel("Stop at Net Lose Multiple(Based on Bet Amount):")
        self.stop_lose_input = QLineEdit()
        self.stop_lose_input.setText("100")
        self.stop_lose_input.setValidator(QIntValidator())
        self.stop_lose_input.setFixedWidth(150)

        input_layout.addWidget(self.system_config_label, 0, 0, 1, 2)
        input_layout.addWidget(self.resolution_label, 1, 0)
        input_layout.addWidget(self.resolution_input, 1, 1)
        input_layout.addWidget(self.round_config_label, 2, 0, 1, 2)
        input_layout.addWidget(self.bet_amount_label, 3, 0)
        input_layout.addWidget(self.bet_amount_input, 3, 1)
        input_layout.addWidget(self.language_label, 4, 0)
        input_layout.addWidget(self.language_input, 4, 1)
        input_layout.addWidget(self.num_games_label, 5, 0)
        input_layout.addWidget(self.num_games_input, 5, 1)
        input_layout.addWidget(self.stop_win_label, 6, 0)
        input_layout.addWidget(self.stop_win_input, 6, 1)
        input_layout.addWidget(self.stop_lose_label, 7, 0)
        input_layout.addWidget(self.stop_lose_input, 7, 1)

        # Cheat Sheet Layout
        self.cheat_sheet_layout = QVBoxLayout()
        self.cheat_sheet_label = QLabel("Strategy Configuration Cheatsheet:")
        self.cheat_sheet_table = QTableWidget()
        self.cheat_sheet_table.setColumnCount(11)
        self.cheat_sheet_table.setHorizontalHeaderLabels(
            ["", "2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]
        )
        self.cheat_sheet_table.verticalHeader().setVisible(False)
        self.cheat_sheet_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cheat_sheet_table.setFixedHeight(500)
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
        self.statistics_label = QLabel("Round Statistics")
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
        self.bet_amount = "1k"
        self.num_games = 1000
        self.stop_net_profit = 100
        self.stop_net_lose = 100
        self.language = "en-US"
        self.program_thread = None
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
            self.language = LANGUAGE_MAP[self.language_input.currentText()]
            self.program_thread = ProgramThread(self.bet_amount, self.language)
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

    def update_stat(self, bet_rate, condition):
        self.total_hand += 1
        self.round_hand += 1
        self.total_hand_label.setText(f"Total Hands: {self.total_hand}")
        self.remaining_hands_label.setText(
            f"Remaining Hands: {self.num_games - self.total_hand}"
        )
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
        net_win = win_rate - bet_rate
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
        ax.set_xlabel("Bet Amount (in 1k)", fontsize=12)
        ax.set_ylabel("Win Amount (in 1k)", fontsize=12)
        ax.set_title("Bet Amount vs Win Amount")

        plt.subplots_adjust(left=0.15, right=0.95, bottom=0.15, top=0.95)

        self.graph_scene.addWidget(canvas)

    def populate_cheat_sheet(self):
        rows = [
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
            "13",
            "14",
            "15",
            "16",
            "17",
            "18",
            "19",
            "20",
            "A,2",
            "A,3",
            "A,4",
            "A,5",
            "A,6",
            "A,7",
            "A,8",
            "A,9",
            "A,10",
            "A,A",
            "2,2",
            "3,3",
            "4,4",
            "5,5",
            "6,6",
            "7,7",
            "8,8",
            "9,9",
            "10,10",
        ]
        self.cheat_sheet_table.setRowCount(len(rows))

        for row, player_hand in enumerate(rows):
            self.cheat_sheet_table.setItem(row, 0, QTableWidgetItem(str(player_hand)))
            for col, dealer_card in enumerate(
                ["2", "3", "4", "5", "6", "7", "8", "9", "10", "A"]
            ):
                key = (player_hand, dealer_card)
                if key in CHEAT_SHEET:
                    action = CHEAT_SHEET[key]
                    item = QTableWidgetItem(action)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.cheat_sheet_table.setItem(row, col + 1, item)

        self.cheat_sheet_table.resizeColumnsToContents()

    def update_button_styles(self):
        if self.start_button.isChecked():
            self.start_button.setStyleSheet(
                "background-color: #388E3C; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
            )
        else:
            self.start_button.setStyleSheet(
                "background-color: #4CAF50; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
            )

        if self.stop_button.isChecked():
            self.stop_button.setStyleSheet(
                "background-color: #D32F2F; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
            )
        else:
            self.stop_button.setStyleSheet(
                "background-color: #F44336; color: white; font-weight: bold; padding: 10px 20px; border-radius: 5px;"
            )
