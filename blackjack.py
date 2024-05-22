from time import sleep
from numpy import where as np_where
from numpy import sqrt as np_sqrt
import pyautogui
from pyscreeze import screenshot
from cv2 import resize, matchTemplate, TM_CCOEFF_NORMED, imread, minMaxLoc
from PyQt5.QtCore import QThread, pyqtSignal
from constant import (
    NUMBER,
    COLOR,
    CHEAT_SHEET,
    OP_POS,
    FIRST_HAND_POS,
    SECOND_HAND_POS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)


def is_close(pt1, pt2, threshold=8):
    return np_sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) < threshold


def clickz(top_left):
    x = top_left[0] + BUTTON_WIDTH / 2
    y = top_left[1] + BUTTON_HEIGHT / 2
    pyautogui.click(x, y, button="left", duration=0.25)
    pyautogui.moveTo(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, duration=0.25)


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
        return str(card_num1 + card_num2)


class ProgramThread(QThread):
    statUpdated = pyqtSignal(float, str)
    roundInformUpdated = pyqtSignal(str, str, str)

    def __init__(self, bet_amount, language):
        super().__init__()
        self.bet_amount = bet_amount
        self.language = language
        self.running = True
        self.card_images = {}
        self.image_prefix = "image/" + self.language + "/"
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
        is_split = False

        win = imread(self.image_prefix + "win.png", 0)
        lose = imread(self.image_prefix + "lose.png", 0)
        bust = imread(self.image_prefix + "bust.png", 0)
        draw = imread(self.image_prefix + "draw.png", 0)
        double = imread(self.image_prefix + "double.png", 0)
        stand = imread(self.image_prefix + "stand.png", 0)
        blackjack = imread(self.image_prefix + "blackjack.png", 0)
        bet = imread(r"image/bet/bet" + self.bet_amount + ".png", 0)

        while self.running:
            screenshot("image/screen.png")
            screen = imread(r"image/screen.png", 0)
            screen = resize(screen, (WINDOW_WIDTH, WINDOW_HEIGHT))

            if self.compare(win, screen):
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2
                is_doubled = False
                is_split = False
                self.statUpdated.emit(amount_rate, "win")
                sleep(2)
            elif self.compare(lose, screen):
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2
                is_doubled = False
                is_split = False
                self.statUpdated.emit(amount_rate, "lose")
                sleep(2)
            elif self.compare(bust, screen):
                _, y = self.compare(bust, screen)
                if y < WINDOW_HEIGHT / 2:
                    continue
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2
                is_doubled = False
                is_split = False
                self.statUpdated.emit(amount_rate, "lose")
                sleep(2)
            elif self.compare(draw, screen):
                amount_rate = 1
                if is_doubled:
                    amount_rate = 2
                is_doubled = False
                is_split = False
                self.statUpdated.emit(amount_rate, "draw")
                sleep(2)
            elif self.compare(blackjack, screen):
                _, y = self.compare(blackjack, screen)
                if y < WINDOW_HEIGHT / 2:
                    continue
                amount_rate = 1.5
                is_doubled = False
                is_split = False
                self.statUpdated.emit(amount_rate, "win")
                sleep(2)
            elif self.compare(double, screen):
                first_card = ""
                second_card = ""
                dealer_card = ""
                for card_name, card_image in self.card_images.items():
                    res = matchTemplate(screen, card_image, TM_CCOEFF_NORMED)
                    loc = np_where(res >= 0.95)
                    for x, y in zip(*loc[::-1]):
                        # magic number to determine the position of the card
                        if y < WINDOW_HEIGHT / 2:
                            dealer_card = card_name
                        elif x in [d1 for d2 in FIRST_HAND_POS for d1 in d2]:
                            first_card = card_name
                        elif x in [d3 for d4 in SECOND_HAND_POS for d3 in d4]:
                            second_card = card_name
                    if dealer_card and first_card and second_card:
                        break
                if "" in [first_card, second_card, dealer_card]:
                    continue
                card_num1, card_num2 = card_num_from_card_name(
                    first_card
                ), card_num_from_card_name(second_card)
                if card_num1 + card_num2 == 21:
                    self.roundInformUpdated.emit(
                        dealer_card, first_card + "," + second_card, "stand"
                    )
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
                self.roundInformUpdated.emit(
                    dealer_card, first_card + "," + second_card, strategy
                )
                clickz(OP_POS[strategy])
            elif self.compare(stand, screen):
                # which means it's the second round and could have mulitple cards
                dealer_card = ""
                total_points = 0
                detected_cards = []
                for card_name, card_image in self.card_images.items():
                    res = matchTemplate(screen, card_image, TM_CCOEFF_NORMED)
                    loc = np_where(res >= 0.95)
                    for x, y in zip(*loc[::-1]):
                        already_detected = False
                        for detected_card in detected_cards:
                            detect_card_name, detect_card_pos = detected_card
                            if detect_card_name == card_name and is_close(
                                detect_card_pos, (x, y)
                            ):
                                already_detected = True
                                break
                        if not already_detected:
                            if y < WINDOW_HEIGHT / 2:
                                dealer_card = card_name
                            else:
                                total_points += card_num_from_card_name(card_name)
                            detected_cards.append((card_name, (x, y)))
                cards = [name for name, pt in detected_cards if name != dealer_card]
                if dealer_card == "" or total_points == 0 or len(cards) < 2:
                    continue
                if total_points >= 21:
                    if total_points % 10 == 1:
                        self.roundInformUpdated.emit(
                            dealer_card, ",".join(cards), "stand"
                        )
                        continue
                    elif total_points % 10 == 0:
                        total_points = 20
                    else:
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
            elif self.compare(bet, screen) is not None:
                loc = self.compare(bet, screen)
                clickz(loc)

    def stop(self):
        self.terminate()
        self.wait()
