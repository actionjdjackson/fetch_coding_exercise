from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import logging
import json

class FakeFinderAlogrithm():

    def __init__(self, master):
        self.driver = None
        self.master = master

    def find_fake_bar(self):

        self.master.log_success("Finding the fake bar... loading the URL...")

        self.driver.get(self.master.URL)

        self.left_bowl = []

        for n in range(0, 9):
            self.left_bowl.append(self.driver.find_element(By.ID, f"left_{n}"))

        self.right_bowl = []

        for n in range(0, 9):
            self.right_bowl.append(self.driver.find_element(By.ID, f"right_{n}"))

        self.selection_buttons = []

        for n in range(0, 9):
            self.selection_buttons.append(self.driver.find_element(By.ID, f"coin_{n}"))

        self.weigh_button = self.driver.find_element(By.ID, "weigh")
        self.reset_button = self.driver.find_elements(By.ID, "reset")[1]

        self.which_side_is_lighter = None

        self.setup_scale(0)

        self.weigh_button.click()
        time.sleep(self.master.PAUSE_TIME)
        if self.test_weights() == "E":
            self.master.log_success("The fake bar is number 8")
            self.selection_buttons[8].click()
            time.sleep(10)
            self.driver.switch_to.alert.accept()

        elif self.test_weights() == "L":
            self.master.log_success(f"The fake bar is between {0} and {3}")
            for n in range(1, 4):
                self.setup_scale(n)
                self.weigh_button.click()
                time.sleep(self.master.PAUSE_TIME)
                if self.test_weights() == "E":
                    self.master.log_success(f"The fake bar is number {4-n}")
                    self.selection_buttons[4-n].click()
                    time.sleep(self.master.WAIT_TIME)
                    self.driver.switch_to.alert.accept()
                    break
                elif self.test_weights() == "L":
                    if n == 3:
                        self.master.log_success(f"The fake bar is number {0}")
                        self.selection_buttons[0].click()
                        time.sleep(self.master.WAIT_TIME)
                        self.driver.switch_to.alert.accept()
                        break
                    else:
                        self.master.log_success(f"The fake bar is between {0} and {3-n}")
        elif self.test_weights() == "R":
            self.master.log_success(f"The fake bar is between {4} and {7}")
            for n in range(1, 4):
                self.setup_scale(n)
                self.weigh_button.click()
                time.sleep(self.master.PAUSE_TIME)
                if self.test_weights() == "E":
                    self.master.log_success(f"The fake bar is number {n + 3}")
                    self.selection_buttons[n + 3].click()
                    time.sleep(self.master.WAIT_TIME)
                    self.driver.switch_to.alert.accept()
                    break
                elif self.test_weights() == "R":
                    if n == 3:
                        self.master.log_success(f"The fake bar is number {7}")
                        self.selection_buttons[7].click()
                        time.sleep(self.master.WAIT_TIME)
                        self.driver.switch_to.alert.accept()
                        break
                    else:
                        self.master.log_success(f"The fake bar is between {n + 4} and {7}")

    def setup_scale(self, n):
        self.reset_button.click()
        time.sleep(self.master.PAUSE_TIME)

        for l in range(0, 4 - n):
            self.left_bowl[l].send_keys(f"{l}")

        for r in range(4 + n, 8):
            self.right_bowl[r].send_keys(f"{r}")

    def test_weights(self):
        if self.driver.find_element(By.ID, "reset").text == "=":
            return "E"
        elif self.driver.find_element(By.ID, "reset").text == "<":
            return "L"
        elif self.driver.find_element(By.ID, "reset").text == ">":
            return "R"
        elif self.driver.find_element(By.ID, "reset").text == "?":
            return None
