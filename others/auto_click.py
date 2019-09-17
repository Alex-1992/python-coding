import keyboard
import pyautogui


class Pos:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


chance_pos = Pos()
equip_pos = Pos()
reset_pos = Pos()


def get_pos():
    keyboard.wait('s')
    chance_pos = pyautogui.postion()
    print(chance_pos)
    keyboard.wait('s')
    equip_pos = pyautogui.postion()
    keyboard.wait('s')
    reset_pos = pyautogui.postion()


def start_click():
    while True:
        pyautogui.click(chance_pos.x, chance_pos.y, button='right')
        pyautogui.click(equip_pos.x, equip_pos.y, button='left')
        pyautogui.click(reset_pos.x, reset_pos.y, button='right')
        pyautogui.click(equip_pos.x, equip_pos.y, button='left')


get_pos()
# start_click()
