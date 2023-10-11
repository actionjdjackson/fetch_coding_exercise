from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import logging
import json

class FindTheFakeBarAutomator:

    def __init__(self):
        self.FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
        self.LOG_DIRECTORY = os.path.join(self.FILE_DIRECTORY, 'Logs')
        self.LOG_FILE = os.path.join(self.LOG_DIRECTORY, 'Logs.log')
        self.CONFIG_FILE = os.path.join(self.FILE_DIRECTORY, 'config.json')
        os.makedirs(self.LOG_DIRECTORY, exist_ok = True)

        self.URL = None
        self.DEFAULT_BROWSER = None
        self.RANDOM_GUESS = None
        self.WAIT_TIME = None
        self.PAUSE_TIME = None
        self.LOOP = None

        self.setup_logging()
        self.load_configuration()
        self.main()

    def setup_logging(self):
        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, 'w') as log_file:
                log_file.write('')
        logging.basicConfig(filename=self.LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

    def load_configuration(self):
        try:
            with open(self.CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)

            self.URL = config.get('URL')
            self.DEFAULT_BROWSER = config.get('DEFAULT_BROWSER')
            self.RANDOM_GUESS = config.get('RANDOM_GUESS')
            self.WAIT_TIME = config.get('WAIT_TIME')
            self.PAUSE_TIME = config.get('PAUSE_TIME')
            self.LOOP = config.get('LOOP')

            if None in (self.DEFAULT_BROWSER, self.RANDOM_GUESS, self.WAIT_TIME, self.PAUSE_TIME, self.URL, self.LOOP):
                raise ValueError("One or more required values are missing in the config file")
        except ValueError as e:
            self.log_error(f"An error occurred while reading the config file: {e}")
            self.DEFAULT_BROWSER = self.RANDOM_GUESS = self.WAIT_TIME = self.PAUSE_TIME = self.URL = self.LOOP = None

    def log_error(self, message):
        print(f"Error(s) occurred, please check '{self.LOG_FILE}' for more details")
        logging.error(message)

    def log_success(self, message):
        print(message)
        logging.info(message)

    def main(self):
        try:
            if not self.DEFAULT_BROWSER or not self.RANDOM_GUESS or not self.WAIT_TIME or not self.PAUSE_TIME or not self.URL or not self.LOOP:
                raise ValueError("Configuration is incomplete")

            if self.DEFAULT_BROWSER.upper() == "ASK":

                self.log_success("Asking for browser in the terminal...")

                while True:
                    input_string = input(f"What browser would you like to use? [S]afari, [F]irefox, [C]hrome, [E]dge, [I]nternet Exploder: ")

                    if input_string.upper() == "S":
                        self.driver = webdriver.Safari()
                        print("Okay, Safari it is. Please make sure you go to the Develop menu, and enable 'Allow Remote Automation'")
                        break
                    elif input_string.upper() == "F":
                        self.driver = webdriver.Firefox()
                        print("Okay, Firefox it is. ")
                        break
                    elif input_string.upper() == "C":
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                        self.driver = webdriver.Chrome(options=chrome_options)
                        print("Okay, Chrome it is. ")
                        break
                    elif input_string.upper() == "E":
                        self.driver = webdriver.Edge()
                        print("Okay, Edge it is. ")
                        break
                    elif input_string.upper() == "I":
                        print("Okay, Internet Explorer it is. ")
                        self.driver = webdriver.IE()
                        break
                    else:
                        print(f"Ooops, I didn't understand that response.")
                        continue

            elif self.DEFAULT_BROWSER.upper() == "SAFARI":
                self.driver = webdriver.Safari()
                self.log_success("Loaded Safari webdriver as configured... Please make sure you go to the Develop menu, and enable 'Allow Remote Automation")
            elif self.DEFAULT_BROWSER.upper() == "FIREFOX":
                self.driver = webdriver.Firefox()
                self.log_success("Loaded Firefox webdriver as configured...")
            elif self.DEFAULT_BROWSER.upper() == "CHROME":
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                self.driver = webdriver.Chrome(options=chrome_options)
                self.log_success("Loaded Chrome webdriver as configured...")
            elif self.DEFAULT_BROWSER.upper() == "EDGE":
                self.driver = webdriver.Edge()
                self.log_success("Loaded Edge webdriver as configured...")
            elif self.DEFAULT_BROWSER.upper() == "INTERNET EXPLORER":
                self.driver = webdriver.IE()
                self.log_success("Loaded Internet Explorer webdriver as configured...")
            else:
                raise ValueError("Invalid browser entered in configuration file.")

            if self.WAIT_TIME <= 0:
                raise ValueError("Invalid wait time entered in configuration file.")
            if self.PAUSE_TIME <= 0:
                raise ValueError("Invalid pause time entered in configuration file.")
            if self.URL.isspace():
                raise ValueError("Invalid URL entered in configuration file.")
            if self.RANDOM_GUESS.upper() == "Y":
                raise Exception("Currently do not support random guess.")
            if self.RANDOM_GUESS.upper() == "N":
                self.log_success("Currently running without random guess...")
            if self.LOOP.upper() == "Y":
                self.log_success("Running on a loop...")
            elif self.LOOP.upper() == "N":
                self.log_success("Running only once...")
            else:
                raise ValueError("Invalid value for loop option in configuration file")

        except ValueError as e_value:
            self.log_error(f"Value Error: {e_value}")
        except Exception as e:
            self.log_error(f"An unexpected error occurred: {e}\n")
        finally:
            if self.LOOP.upper() == "N":
                self.log_success("We're all done. Bye.")
                exit()
        self.find_fake_bar()

    def find_fake_bar(self):

        self.log_success("Finding the fake bar... loading the URL...")

        self.driver.get(self.URL)

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

        self.setup_board(0)

        self.weigh_button.click()
        time.sleep(self.PAUSE_TIME)
        if self.test_weights() == "E":
            self.log_success("The fake bar is number 8")
            self.selection_buttons[8].click()
            time.sleep(10)
            self.driver.switch_to.alert.accept()

        elif self.test_weights() == "L":
            self.log_success(f"The fake bar is between {0} and {3}")
            for n in range(1, 4):
                self.setup_board(n)
                self.weigh_button.click()
                time.sleep(self.PAUSE_TIME)
                if self.test_weights() == "E":
                    self.log_success(f"The fake bar is number {4-n}")
                    self.selection_buttons[4-n].click()
                    time.sleep(self.WAIT_TIME)
                    self.driver.switch_to.alert.accept()
                    break
                elif self.test_weights() == "L":
                    if n == 3:
                        self.log_success(f"The fake bar is number {0}")
                        self.selection_buttons[0].click()
                        time.sleep(self.WAIT_TIME)
                        self.driver.switch_to.alert.accept()
                        break
                    else:
                        self.log_success(f"The fake bar is between {0} and {3-n}")
        elif self.test_weights() == "R":
            self.log_success(f"The fake bar is between {4} and {7}")
            for n in range(1, 4):
                self.setup_board(n)
                self.weigh_button.click()
                time.sleep(self.PAUSE_TIME)
                if self.test_weights() == "E":
                    self.log_success(f"The fake bar is number {n + 3}")
                    self.selection_buttons[n + 3].click()
                    time.sleep(self.WAIT_TIME)
                    self.driver.switch_to.alert.accept()
                    break
                elif self.test_weights() == "R":
                    if n == 3:
                        self.log_success(f"The fake bar is number {7}")
                        self.selection_buttons[7].click()
                        time.sleep(self.WAIT_TIME)
                        self.driver.switch_to.alert.accept()
                        break
                    else:
                        self.log_success(f"The fake bar is between {n + 4} and {7}")

    def setup_board(self, n):
        self.reset_button.click()
        time.sleep(self.PAUSE_TIME)

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

if __name__ == "__main__":
    finder = FindTheFakeBarAutomator()
    finder.main()
