from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

class FakeFinderAlgorithm():

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
            self.master.log_success("Setting up the algorithm, loading the URL")

            self.driver.get(self.master.URL)

            self.master.log_success("URL Loaded successfully")

            self.left_bowl = []

            for n in range(0, 9):
                self.left_bowl.append(self.driver.find_element(By.ID,
                                                        f"left_{n}"))

            self.right_bowl = []

            for n in range(0, 9):
                self.right_bowl.append(self.driver.find_element(By.ID,
                                                        f"right_{n}"))

            self.selection_buttons = []
            for n in range(0, 9):
                self.selection_buttons.append(self.driver.find_element(By.ID,
                                                        f"coin_{n}"))

            self.weigh_button = self.driver.find_element(By.ID, "weigh")
            # Grabs the second element named "reset" - the reset button, not the
            # weigh-in result, which happened to also be named "reset"
            self.reset_button = self.driver.find_elements(By.ID, "reset")[1]

            self.master.log_success("Loaded components into algorithm")

        except Exception as e:
            self.master.log_error(f"An error occurred setting up algorithm: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()


    def make_selection(self, n):
        self.master.log_success(f"The fake bar is {n}")
        self.selection_buttons[n].click()
        self.master.log_success(f"{self.driver.switch_to.alert.text}")
        time.sleep(self.master.WAIT_TIME)
        try:
            self.driver.switch_to.alert.accept()
        except Exception as e:
            pass
        self.getWeighIns()


    def weigh_in(self):
        self.weigh_button.click()
        self.master.log_success("Weighing...")
        time.sleep(self.master.PAUSE_TIME)


    def getWeighIns(self):
        weighins = self.driver.find_elements(By.XPATH, "//ol/li")  # find weigh-ins as li's in an ol
        for n in range(0, len(weighins)):
            self.master.log_success(f"{n+1}. {weighins[n].get_attribute('innerText')}")


    def test_weights(self):
        """
        Asks the comparator for its value, and returns a more user-friendly
        "E" for equal, "L" for the left side being less (the side the fake is on),
        and "R" for the right side being less (the side the fake is on).
        """
        comparator = self.driver.find_element(By.ID, "reset").text
        if comparator == "=":
            return "E"
        elif comparator == "<":
            return "L"
        elif comparator == ">":
            return "R"
        elif comparator == "?":
            return None
        else:
            return None
