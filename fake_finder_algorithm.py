from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import logging
import json
import random

class FakeFinderAlogrithm():

    def __init__(self, master):
        self.driver = None
        self.master = master

    def setup_algorithm(self):
        """
        Sets up the necessary components for the algorithm to work with, including
        getting the webpage opened up, collecting the left and right bowls for
        weighing, the selection buttons, the weigh button, and the reset button.
        """
        try:
            self.master.log_success("Setting up the algorithm.. loading the URL...")

            self.driver.get(self.master.URL)

            self.master.log_success("URL Loaded successfully")

            self.left_bowl = []

            for n in range(0, 9):
                self.left_bowl.append(self.driver.find_element(By.ID, f"left_{n}"))

            self.right_bowl = []

            for n in range(0, 9):
                self.right_bowl.append(self.driver.find_element(By.ID, f"right_{n}"))

            self.master.log_success("Loaded bowls into algorithm")

            self.selection_buttons = []

            for n in range(0, 9):
                self.selection_buttons.append(self.driver.find_element(By.ID, f"coin_{n}"))

            self.master.log_success("Loaded bar selection buttons into algorithm")

            self.weigh_button = self.driver.find_element(By.ID, "weigh")
            self.reset_button = self.driver.find_elements(By.ID, "reset")[1]

            self.master.log_success("Loaded weigh & reset buttons into algorithm")

        except Exception as e:
            self.master.log_error(f"Something went wrong setting up the algorithm: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()

    def find_fake_bar_random(self):
        """
        This is the random guess version of the algorithm, where the bars are
        shuffled into random order, then pairs are tested sequentially until
        one is found to be less than it's mate. That is the fake bar, so return
        the number of weigh-ins to the master class, and print both the message
        in the resulting alert box and all the weigh-in details. The master class
        handles printing the number of weigh-ins, as it also is in charge of
        handling averaging the number of weigh-ins for a number of loops as defined
        in the configuration file.
        """
        self.setup_algorithm()

        selections = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        random.shuffle(selections)
        for n in range(0, len(selections) - 1, 2):
            self.reset_button.click()
            time.sleep(self.master.PAUSE_TIME)
            self.left_bowl[selections[n]].send_keys(f"{selections[n]}")
            self.right_bowl[selections[n + 1]].send_keys(f"{selections[n + 1]}")
            self.weigh_button.click()
            self.master.log_success("Weighing...")
            time.sleep(self.master.PAUSE_TIME)
            if self.test_weights() == "E":
                continue
            if self.test_weights() == "L":
                self.master.log_success(f"The fake bar is {selections[n]}")
                self.selection_buttons[selections[n]].click()
                time.sleep(self.master.WAIT_TIME)
                self.master.log_success(f"{self.driver.switch_to.alert.text}")
                self.driver.switch_to.alert.accept()
                self.getWeighIns()
                return n // 2 + 1
            if self.test_weights() == "R":
                self.master.log_success(f"The fake bar is {selections[n + 1]}")
                self.selection_buttons[selections[n + 1]].click()
                time.sleep(self.master.WAIT_TIME)
                self.master.log_success(f"{self.driver.switch_to.alert.text}")
                self.driver.switch_to.alert.accept()
                self.getWeighIns()
                return n // 2 + 1
        self.master.log_success(f"The fake bar is {selections[8]}")
        self.selection_buttons[selections[8]].click()
        time.sleep(self.master.WAIT_TIME)
        self.master.log_success(f"{self.driver.switch_to.alert.text}")
        self.driver.switch_to.alert.accept()
        self.getWeighIns()
        return 4

    def find_fake_bar(self):
        """
        This is the find fake bar algorithm, where all the action happens. First
        it sets up everything by calling setup_algorithm, then sets up the scale
        to have all but one bar, evenly divided between the two sides. Then it
        takes away a pair at a time until the test_weights function returns
        a changed value (from L to E or R to E, or E immediately, meaning the
        odd-man-out was the fake bar.)
        """
        self.setup_algorithm()

        try:
            self.master.log_success("Beginning algorithm...")
            self.master.log_success("Divvying up the bars equally...")
            self.setup_scale(0)

            self.weigh_button.click()
            self.master.log_success("Weighing...")
            time.sleep(self.master.PAUSE_TIME)
            if self.test_weights() == "E":
                self.master.log_success("The fake bar is number 8")
                self.selection_buttons[8].click()
                time.sleep(self.master.WAIT_TIME)
                self.master.log_success(f"{self.driver.switch_to.alert.text}")
                self.driver.switch_to.alert.accept()
                self.getWeighIns()
                return 1

            elif self.test_weights() == "L":
                self.master.log_success(f"The fake bar is between {0} and {3}")
                for n in range(1, 4):
                    self.setup_scale(n)
                    self.weigh_button.click()
                    self.master.log_success("Weighing...")
                    time.sleep(self.master.PAUSE_TIME)
                    if self.test_weights() == "E":
                        self.master.log_success(f"The fake bar is number {4-n}")
                        self.selection_buttons[4-n].click()
                        time.sleep(self.master.WAIT_TIME)
                        self.master.log_success(f"{self.driver.switch_to.alert.text}")
                        self.driver.switch_to.alert.accept()
                        self.getWeighIns()
                        return n + 1
                    elif self.test_weights() == "L":
                        if n == 3:
                            self.master.log_success(f"The fake bar is number {0}")
                            self.selection_buttons[0].click()
                            time.sleep(self.master.WAIT_TIME)
                            self.master.log_success(f"{self.driver.switch_to.alert.text}")
                            self.driver.switch_to.alert.accept()
                            self.getWeighIns()
                            return n + 1
                        else:
                            self.master.log_success(f"The fake bar is between {0} and {3-n}")

            elif self.test_weights() == "R":
                self.master.log_success(f"The fake bar is between {4} and {7}")
                for n in range(1, 4):
                    self.setup_scale(n)
                    self.weigh_button.click()
                    self.master.log_success("Weighing...")
                    time.sleep(self.master.PAUSE_TIME)
                    if self.test_weights() == "E":
                        self.master.log_success(f"The fake bar is number {n + 3}")
                        self.selection_buttons[n + 3].click()
                        time.sleep(self.master.WAIT_TIME)
                        self.master.log_success(f"{self.driver.switch_to.alert.text}")
                        self.driver.switch_to.alert.accept()
                        self.getWeighIns()
                        return n + 1
                    elif self.test_weights() == "R":
                        if n == 3:
                            self.master.log_success(f"The fake bar is number {7}")
                            self.selection_buttons[7].click()
                            time.sleep(self.master.WAIT_TIME)
                            self.master.log_success(f"{self.driver.switch_to.alert.text}")
                            self.driver.switch_to.alert.accept()
                            self.getWeighIns()
                            return n + 1
                        else:
                            self.master.log_success(f"The fake bar is between {n + 4} and {7}")

        except Exception as e:
            self.master.log_error(f"Something went wrong while weighing things: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()

    def getWeighIns(self):
        weighins = self.driver.find_elements(By.XPATH, "//ol/li")
        for n in range(0, len(weighins)):
            self.master.log_success(f"{n+1}. {weighins[n].get_attribute('innerText')}")

    def setup_scale(self, n):
        """
        Place the bars in corresponding locations, based on 'n' - which iteration
        we're currently on, removing one bar on each side every iteration, from
        3 down to 0, and from 4 up to 7.
        """
        self.reset_button.click()
        time.sleep(self.master.PAUSE_TIME)

        for l in range(0, 4 - n):  #working our way down from 3 to 0 on the left
            self.left_bowl[l].send_keys(f"{l}")

        for r in range(4 + n, 8):   #working our way up from 4 to 7 on the right
            self.right_bowl[r].send_keys(f"{r}")

    def test_weights(self):
        """
        Asks the comparator for its value, and returns a more user-friendly
        "E" for equal, "L" for the left side being less (the side the fake is on),
        and "R" for the right side being less (the side the fake is on).
        """
        if self.driver.find_element(By.ID, "reset").text == "=":
            return "E"
        elif self.driver.find_element(By.ID, "reset").text == "<":
            return "L"
        elif self.driver.find_element(By.ID, "reset").text == ">":
            return "R"
        elif self.driver.find_element(By.ID, "reset").text == "?":
            return None
