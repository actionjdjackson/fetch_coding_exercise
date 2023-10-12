from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_finder_algorithm import FakeFinderAlgorithm
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
        self.N_LOOPS = None

        self.setup_logging()
        self.load_configuration()

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
            self.N_LOOPS = config.get('N_LOOPS')

            if None in (self.N_LOOPS, self.DEFAULT_BROWSER, self.RANDOM_GUESS, self.WAIT_TIME, self.PAUSE_TIME, self.URL, self.LOOP):
                raise ValueError("One or more required values are missing in the config file")
        except ValueError as e:
            self.log_error(f"An error occurred while reading the config file: {e}")
            self.N_LOOPS = self.DEFAULT_BROWSER = self.RANDOM_GUESS = self.WAIT_TIME = self.PAUSE_TIME = self.URL = self.LOOP = None

    def log_error(self, message):
        print(f"Error(s) occurred, please check '{self.LOG_FILE}' for more details")
        logging.error(message)

    def log_success(self, message):
        print(message)
        logging.info(message)

    def run(self):
        try:
            if not self.DEFAULT_BROWSER or not self.RANDOM_GUESS or not self.WAIT_TIME or not self.PAUSE_TIME or not self.URL or not self.LOOP:
                raise ValueError("Configuration is incomplete")

            algorithm = FakeFinderAlgorithm(self)

            if self.DEFAULT_BROWSER.upper() == "ASK":

                self.log_success("Asking for browser in the terminal...")

                while True:
                    input_string = input(f"What browser would you like to use? [S]afari, [F]irefox, [C]hrome, [E]dge, [I]nternet Exploder: ")
                    if input_string.upper() == "S":
                        self.log_success("Okay, Safari it is. Please make sure you go to the Develop menu, and enable 'Allow Remote Automation'")
                        algorithm.driver = webdriver.Safari()
                        break
                    elif input_string.upper() == "F":
                        self.log_success("Okay, Firefox it is. ")
                        algorithm.driver = webdriver.Firefox()
                        break
                    elif input_string.upper() == "C":
                        self.log_success("Okay, Chrome it is. ")
                        chrome_options = webdriver.ChromeOptions()
                        chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                        algorithm.driver = webdriver.Chrome(options=chrome_options)
                        break
                    elif input_string.upper() == "E":
                        self.log_success("Okay, Edge it is. ")
                        algorithm.driver = webdriver.Edge()
                        break
                    elif input_string.upper() == "I":
                        self.log_success("Okay, Internet Explorer it is. ")
                        algorithm.driver = webdriver.IE()
                        break
                    else:
                        self.log_error(f"Ooops, I didn't understand that response.")
                        continue

            elif self.DEFAULT_BROWSER.upper() == "SAFARI":
                algorithm.driver = webdriver.Safari()
                self.log_success("Loaded Safari webdriver as configured... Please make sure you go to the Develop menu, and enable 'Allow Remote Automation")
            elif self.DEFAULT_BROWSER.upper() == "FIREFOX":
                algorithm.driver = webdriver.Firefox()
                self.log_success("Loaded Firefox webdriver as configured...")
            elif self.DEFAULT_BROWSER.upper() == "CHROME":
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
                algorithm.driver = webdriver.Chrome(options=chrome_options)
                self.log_success("Loaded Chrome webdriver as configured...")
            elif self.DEFAULT_BROWSER.upper() == "EDGE":
                algorithm.driver = webdriver.Edge()
                self.log_success("Loaded Edge webdriver as configured...")
            elif self.DEFAULT_BROWSER.upper() == "INTERNET EXPLORER":
                algorithm.driver = webdriver.IE()
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
                self.log_success("Currently running with random guess...")
            if self.RANDOM_GUESS.upper() == "N":
                self.log_success("Currently running without random guess...")
            if self.LOOP.upper() == "Y":
                self.log_success("Running on a loop...")
            elif self.LOOP.upper() == "N":
                self.log_success("Running only once...")
            else:
                raise ValueError("Invalid value for loop option in configuration file")
            if self.N_LOOPS <= 0:
                raise ValueError("Invalid number of loops (must be at least 1)")

            if self.LOOP.upper() == "Y":
                self.weighs_list = []
                while len(self.weighs_list) < self.N_LOOPS:
                    if self.RANDOM_GUESS.upper() == "Y":
                        weighs = algorithm.find_fake_bar_random()
                    elif self.RANDOM_GUESS.upper() == "N":
                        weighs = algorithm.find_fake_bar()
                    else:
                        raise ValueError("RANDOM_GUESS config value not valid")
                    self.log_success(f"Found fake bar in {weighs} weighs.")
                    self.weighs_list.append(weighs)
                    self.log_success("Restarting the game (in loop mode).")
                self.log_success(f"Average number of weighs in {len(self.weighs_list)} trials: {sum(self.weighs_list) / len(self.weighs_list)}")
            elif self.LOOP.upper() == "N":
                if self.RANDOM_GUESS.upper() == "Y":
                    self.log_success(f"Found fake bar in {algorithm.find_fake_bar_random()} weighs.")
                elif self.RANDOM_GUESS.upper() == "N":
                    self.log_success(f"Found fake bar in {algorithm.find_fake_bar()} weighs.")
                else:
                    raise ValueError("RANDOM_GUESS config value not valid")

        except ValueError as e_value:
            self.log_error(f"Value Error: {e_value}")
        except Exception as e:
            self.log_error(f"An unexpected error occurred: {e}\n")
        except KeyboardInterrupt as kb:
            self.log_success(f"Average number of weighs: {sum(self.weighs_list) / len(self.weighs_list)}")
            self.log_success(f"\nExiting program gracefully, goodbye!")
            exit()
        finally:
            if self.LOOP.upper() == "N":
                self.log_success("We're all done. Bye.")
                exit()


if __name__ == "__main__":
    finder = FindTheFakeBarAutomator()
    finder.run()
