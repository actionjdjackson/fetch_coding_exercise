from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Safari()

driver.get("http://sdetchallenge.fetch.com/")

left_bowl = []

for n in range(0, 9):
    left_bowl.append(driver.find_element(By.ID, f"left_{n}"))

right_bowl = []

for n in range(0, 9):
    right_bowl.append(driver.find_element(By.ID, f"right_{n}"))

selection_buttons = []

for n in range(0, 9):
    selection_buttons.append(driver.find_element(By.ID, f"coin_{n}"))

def setup_board(n):
    reset_button.click()
    time.sleep(2)
    for l in range(0, 4 - n):
        left_bowl[l].send_keys(f"{l}")

    for r in range(4 + n, 8):
        right_bowl[r].send_keys(f"{r}")

weigh_button = driver.find_element(By.ID, "weigh")
reset_button = driver.find_elements(By.ID, "reset")[1]

def test_weights():
    if driver.find_element(By.ID, "reset").text == "=":
        return "E"
    elif driver.find_element(By.ID, "reset").text == "<":
        return "L"
    elif driver.find_element(By.ID, "reset").text == ">":
        return "R"
    elif driver.find_element(By.ID, "reset").text == "?":
        return None

which_side_is_lighter = None

setup_board(0)

weigh_button.click()
time.sleep(2)
if test_weights() == "E":
    print("The fake bar is number 8")
    selection_buttons[8].click()
    time.sleep(10)
    driver.switch_to.alert.accept()

elif test_weights() == "L":
    for n in range(1, 4):
        setup_board(n)
        weigh_button.click()
        time.sleep(2)
        if test_weights() == "E":
            print(f"The fake bar is number {4-n}")
            selection_buttons[4-n].click()
            time.sleep(10)
            driver.switch_to.alert.accept()
            break
        elif test_weights() == "L":
            print(f"The fake bar is between {0} and {4-n-1}")
elif test_weights() == "R":
    for n in range(1, 4):
        setup_board(n)
        weigh_button.click()
        time.sleep(2)
        if test_weights() == "E":
            print(f"The fake bar is number {n + 3}")
            selection_buttons[n + 3].click()
            time.sleep(10)
            driver.switch_to.alert.accept()
            break
        elif test_weights() == "R":
            print(f"The fake bar is between {n + 4} and {7}")
