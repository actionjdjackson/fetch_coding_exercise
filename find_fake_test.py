from selenium import webdriver
from selenium.webdriver.common.by import By
from algorithms.brute_force_algorithm import BruteForceAlgorithm
from algorithms.smart_algorithm import SmartAlgorithm
from algorithms.random_algorithm import RandomAlgorithm
from statistics import mean
from statistics import StatisticsError
from math import isnan
import time
import os
import logging
import json

class FindTheFakeBarAutomator:

    def __init__(self):
        """
        Init function for the FindTheFakeBarAutomator.
        Sets up the log and log directory, and the config file.
        Initializes program constants,
        URL = The URL to the weighing game website
        DEFAULT_BROWSER = The browser you wish to use, or ask for a terminal entry
        ALGORITHM = The type of algorithm to use, "S" for Smart, "B" for Brute
        Force, "R" for Random
        WAIT_TIME = How long (in seconds) to wait between loops, after the
        success alert dialog box opens, and before it is automatically closed
        PAUSE_TIME = How long (in seconds) to wait between weigh-ins and resets,
        for the interface to "catch up."
        LOOP = "Y" for looping, "N" for a single-shot
        N_LOOPS = How many times to loop, must be an integer >= 1
        Also sets up the logging system, and loads values into the program
        constants from the config.json file. Checks to see if they are valid.
        """
        self.FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
        self.LOG_DIRECTORY = os.path.join(self.FILE_DIRECTORY, 'Logs')
        self.LOG_FILE = os.path.join(self.LOG_DIRECTORY, 'Logs.log')
        self.CONFIG_FILE = os.path.join(self.FILE_DIRECTORY, 'config.json')
        os.makedirs(self.LOG_DIRECTORY, exist_ok = True)

        self.URL = None
        self.DEFAULT_BROWSER = None
        self.ALGORITHM = None
        self.WAIT_TIME = None
        self.PAUSE_TIME = None
        self.LOOP = None
        self.N_LOOPS = None

        self.setup_logging()
        self.load_configuration()

        self.weighs_list = []


    def setup_logging(self):
        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE, 'w') as log_file:
                log_file.write('')
        logging.basicConfig(filename=self.LOG_FILE, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s: %(message)s')


    def load_configuration(self):
        try:
            with open(self.CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)

            self.URL = config.get('URL')
            self.DEFAULT_BROWSER = config.get('DEFAULT_BROWSER')
            self.ALGORITHM = config.get('ALGORITHM')
            self.WAIT_TIME = config.get('WAIT_TIME')
            self.PAUSE_TIME = config.get('PAUSE_TIME')
            self.LOOP = config.get('LOOP')
            self.N_LOOPS = config.get('N_LOOPS')

            if None in (self.N_LOOPS, self.DEFAULT_BROWSER, self.ALGORITHM,
                        self.WAIT_TIME, self.PAUSE_TIME, self.URL, self.LOOP):
                raise ValueError("Some required value(s) is(are) missing in config file")

            if self.WAIT_TIME <= 0 or isnan(self.WAIT_TIME):
                raise ValueError("Invalid WAIT_TIME entered in configuration file.")

            if self.PAUSE_TIME <= 0 or isnan(self.PAUSE_TIME):
                raise ValueError("Invalid PAUSE_TIME entered in configuration file.")

            if self.URL.isspace():
                raise ValueError("Invalid URL entered in configuration file.")

            if self.ALGORITHM.upper() == "S":
                self.log_success("Currently running with smart algorithm...")
            elif self.ALGORITHM.upper() == "B":
                self.log_success("Currently running brute force algorithm...")
            elif self.ALGORITHM.upper() == "R":
                self.log_success("Currently running random algorithm...")
            else:
                raise ValueError("ALGORITHM does not have a valid value. Must be "
                               + "'S', 'B', or 'R'. Check config.json file")

            if self.LOOP.upper() == "Y":
                self.log_success("Running on a loop...")
            elif self.LOOP.upper() == "N":
                self.log_success("Running only once...")
            else:
                raise ValueError("Invalid value for LOOP option in configuration file")

            if self.N_LOOPS <= 0 or not isinstance(self.N_LOOPS, int):
                raise ValueError("Invalid N_LOOPS value in configuration file "
                               + "(must be an integer >= 1)")

        except ValueError as val_e:
            self.log_error(f"A Value Error occurred while reading the config "
                         + f"file: {val_e}")
            self.log_error(f"Exiting program gracefully, goodbye!")
            exit()
        except Exception as e:
            self.log_error(f"An unexpected error occurred while reading the "
                         + f"config file: {e}")
            self.log_error(f"Exiting program gracefully, goodbye!")
            exit()


    def log_error(self, message):
        print(f"Error(s) occurred, please check '{self.LOG_FILE}' for more details")
        logging.error(message)


    def log_success(self, message):
        print(message)
        logging.info(message)


    def ask_for_browser(self):
        while True:
            input_string = input(f"What browser would you like to use?\n"
                + "[S]afari, [F]irefox, [C]hrome, [E]dge, [I]nternet Exploder: ")
            if input_string.upper() == "S":
                self.log_success("Okay, Safari it is. "
                    + "Please make sure you go to the Develop menu, and "
                    + "enable 'Allow Remote Automation'")
                self.algorithm.driver = webdriver.Safari()
                break
            elif input_string.upper() == "F":
                self.log_success("Okay, Firefox it is. ")
                self.algorithm.driver = webdriver.Firefox()
                break
            elif input_string.upper() == "C":
                self.log_success("Okay, Chrome it is. ")
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("excludeSwitches",
                                                    ['enable-automation'])
                self.algorithm.driver = webdriver.Chrome(options=chrome_options)
                break
            elif input_string.upper() == "E":
                self.log_success("Okay, Edge it is. ")
                self.algorithm.driver = webdriver.Edge()
                break
            elif input_string.upper() == "I":
                self.log_success("Okay, Internet Explorer it is. ")
                self.algorithm.driver = webdriver.IE()
                break
            else:
                self.log_error(f"Ooops, I didn't understand that response.")
                continue


    def run(self):
        try:
            if not self.DEFAULT_BROWSER or not self.ALGORITHM or not self.WAIT_TIME or not self.PAUSE_TIME or not self.URL or not self.LOOP:
                raise ValueError("Configuration is incomplete")

            if self.ALGORITHM == "S":
                self.algorithm = SmartAlgorithm(self)
            elif self.ALGORITHM == "B":
                self.algorithm = BruteForceAlgorithm(self)
            elif self.ALGORITHM == "R":
                self.algorithm = RandomAlgorithm(self)

            if self.DEFAULT_BROWSER.upper() == "ASK":

                self.ask_for_browser()

            elif self.DEFAULT_BROWSER.upper() == "SAFARI":

                self.algorithm.driver = webdriver.Safari()
                self.log_success("Loaded Safari webdriver as configured... "
                    + "Please make sure you go to the Develop menu, and enable "
                    + "'Allow Remote Automation'")

            elif self.DEFAULT_BROWSER.upper() == "FIREFOX":
                self.algorithm.driver = webdriver.Firefox()
                self.log_success("Loaded Firefox webdriver as configured...")

            elif self.DEFAULT_BROWSER.upper() == "CHROME":
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_experimental_option("excludeSwitches",
                                                        ['enable-automation'])
                self.algorithm.driver = webdriver.Chrome(options=chrome_options)
                self.log_success("Loaded Chrome webdriver as configured...")

            elif self.DEFAULT_BROWSER.upper() == "EDGE":
                self.algorithm.driver = webdriver.Edge()
                self.log_success("Loaded Edge webdriver as configured...")

            elif self.DEFAULT_BROWSER.upper() == "INTERNET EXPLORER":
                self.algorithm.driver = webdriver.IE()
                self.log_success("Loaded Internet Explorer webdriver as configured...")

            else:
                raise ValueError("Invalid browser entered in configuration file.")

            if self.LOOP.upper() == "Y":

                while len(self.weighs_list) < self.N_LOOPS:

                    self.log_success(f"(Loop {len(self.weighs_list) + 1} "
                                   + f"of {self.N_LOOPS})")

                    if self.ALGORITHM.upper() == "S":
                        weighs = self.algorithm.find_fake()
                        self.log_success(f"Found fake bar in {weighs} weighs "
                                       + f"using the smart algorithm.")

                    elif self.ALGORITHM.upper() == "B":
                        weighs = self.algorithm.find_fake()
                        self.log_success(f"Found fake bar in {weighs} weighs "
                                       + f"using the brute force algorithm.")

                    elif self.ALGORITHM.upper() == "R":
                        weighs = self.algorithm.find_fake()
                        self.log_success(f"Found fake bar in {weighs} weighs "
                                       + f"using the random algorithm.")

                    self.weighs_list.append(weighs)

                self.log_success(f"Average number of weighs in " +
                    f"{len(self.weighs_list)} trials: {mean(self.weighs_list)}"
                  + f" using the {self.ALGORITHM.upper()} algorithm.")

            elif self.LOOP.upper() == "N":  # Running only once

                if self.ALGORITHM.upper() == "S":
                    weighs = self.algorithm.find_fake()
                    self.log_success(f"Found fake bar in {weighs} weighs "
                                    + f"using the smart algorithm.")

                elif self.ALGORITHM.upper() == "B":
                    weighs = self.algorithm.find_fake()
                    self.log_success(f"Found fake bar in {weighs} weighs "
                                   + f"using the brute force algorithm.")

                elif self.ALGORITHM.upper() == "R":
                    weighs = self.algorithm.find_fake()
                    self.log_success(f"Found fake bar in {weighs} weighs "
                                    + f"using the random algorithm.")

        except ValueError as val_e:
            self.log_error(f"Value Error: {val_e}")
            self.log_error(f"Exiting program gracefully, goodbye!")
            exit()
        except Exception as e:
            self.log_error(f"An unexpected error occurred: {e}")
            if "'Allow Remote Automation'" in str(e):
                print("Ooops, you forgot to enable 'Allow Remote Automation' "
                    + "in the Develop menu, in Safari")
            self.log_error(f"Exiting program gracefully, goodbye!")
            exit()
        except KeyboardInterrupt as kb:
            try:
                self.log_success(f"\nAverage number of weighs in "
                               + f"{len(self.weighs_list)} trials: "
                               + f"{mean(self.weighs_list)} using "
                               + f"{self.ALGORITHM.upper()} algorithm.")
                self.log_success(f"Exiting program gracefully, goodbye!")
                exit()
            except StatisticsError as stat_e:
                self.log_success(f"\nYou didn't run through at least one loop "
                               + f"succesfully. Oh well. No average.")
                self.log_success(f"Exiting program gracefully, goodbye!")
                exit()

if __name__ == "__main__":
    finder = FindTheFakeBarAutomator()
    finder.run()
