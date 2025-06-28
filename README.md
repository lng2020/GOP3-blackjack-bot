# If You Want to Buy Chips

contact me at t.me/dumbass2002

# GOP3 Blackjack Bot
This is a simple blackjack bot for the game "Governor of Poker 3". 

It uses `pyautogui` to take screenshots and click buttons, and `opencv` to recognize the cards and buttons. Then it uses a [strategy configuration cheatsheet](./assets/cheatsheet.png) to decide the next move. To self-define strategy, you can replace the const `CHEAT_SHEET` in `constant.py`. The self-defined strategy in GUI is on [TODO](#todo).

The `v2` tag is a quite stable version. From my several 10000 hand tests, the expectation is around 0.98. The main branch is for more features and improvements but the expectation will not change much.

![demo](./assets/demo.png)
## Binary
You can download the binary version and use it directly. The binary version is built with `pyinstaller` and contains all the dependencies. You can find the binary version in the GitHub release page.

## Usage
1. Requirements in GOP3:
    - The game must be in fullscreen mode(1920*1080).
    - The game must be in English or Chinese([other language contributions are welcome!](#translation)).
    - The game must be in the personal blackjack room.
2. Run the bot:
```bash
pip install -r requirements.txt
python main.py
```
## TODO
- [x] Add i18n support(supported languages: English, Chinese)
- [ ] Self-defined strategy in GUI
- [ ] Adapt different resolutions
- [x] Better distinguish win/draw conditions
- [x] Better splitting cards recognitions

## Known issues
1. if this hand contains more than 5 cards, the bot will not recognize the cards correctly. That's because the cards begin to overlap, making recognition difficult.
2. the win/lose recognition is not right after splitting cards. After splitting cards, there are two win/lose hands on the table but the bot only recognizes one. So the behavior is (win, win) or (win, lose) detect a single win and (lose, lose) detect a single loss. This probably causes the `net win` to be about 10% higher than the actual net win from my tests.

## Translation
This is a guide for translating the bot to other languages. If you want to contribute, please follow the steps below:
1. screenshot the game interface and save it to `image/{language_name}` folder. Required images are:
    - `hit.png`
    - `stand.png`
    - `double.png`
    - `split.png`
    - `win.png`
    - `lose.png`
    - `draw.png`
    - `blackjack.png`
    - `bust.png`
2. Add this language to the constants in `main.py`:
```python
SUPPORTED_LANGUAGE = ["English", "Chinese"]
LANGUAGE_MAP = {
    "English": "en-us",
    "Chinese": "zh-cn",
}
```

you can see the `image/zh-cn` folder for reference.
## Credits
https://github.com/weeeeeesterly/GOP3blackjack-21-
