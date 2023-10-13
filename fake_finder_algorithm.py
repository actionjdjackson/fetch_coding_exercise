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
            self.reset_button = self.driver.find_elements(By.ID, "reset")[1]

            self.master.log_success("Loaded components into algorithm")

        except Exception as e:
            self.master.log_error(f"Something went wrong setting up the algorithm: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()

    def find_fake_smart(self):
        """
        This is the way to do it! Separates into three groups of three values
        each: left, right, and off the scale which narrows it down immediately
        to a range of only 3 values, which is also separated into three positions
        - left, right, and off the scale, giving the final answer based on them
        being balanced, or left/right leaning. It always works after two weigh-ins,
        and so averages 2.0 over any number of trials. It cannot produce an answer
        in only one weigh-in, as the brute force and random ways of going about
        it can at times return an answer in one weigh-in, but they average to be
        3.0 and 2.95 over 20 trials, respectively, and so the smart way wins!
        """
        try:
            self.setup_algorithm()

            self.master.log_success("Beginning the smart algorithm...")
            self.master.log_success("Splitting into three groups...")
            self.initial_fill_bowls()

            if self.test_weights() == "E":
                self.master.log_success("Fake bar is between 6 and 8")
                self.reset_and_fill_bowls(6, 7)
                self.weigh_in()
                if self.test_weights() == "E":
                    self.make_selection(8)
                elif self.test_weights() == "L":
                    self.make_selection(6)
                elif self.test_weights() == "R":
                    self.make_selection(7)
                else:
                    raise ValueError("Invalid test weight value")

            elif self.test_weights() == "L":
                self.master.log_success("Fake bar is between 0 and 2")
                self.reset_and_fill_bowls(0, 1)
                self.weigh_in()
                if self.test_weights() == "E":
                    self.make_selection(2)
                elif self.test_weights() == "L":
                    self.make_selection(0)
                elif self.test_weights() == "R":
                    self.make_selection(1)
                else:
                    raise ValueError("Invalid test weight value")

            elif self.test_weights() == "R":
                self.master.log_success("Fake bar is between 3 and 5")
                self.reset_and_fill_bowls(3, 4)
                self.weigh_in()
                if self.test_weights() == "E":
                    self.make_selection(5)
                elif self.test_weights() == "L":
                    self.make_selection(3)
                elif self.test_weights() == "R":
                    self.make_selection(4)
                else:
                    raise ValueError("Invalid test weight value")

            else:
                raise ValueError("Invalid test weight value")

            return 2

        except ValueError as val_e:
            self.master.log_error(f"Value Error encountered in smart " +
                                  f"algorithm: {val_e}")
            self.master.log_error("\nShutting down gracefully. Bye.")
            exit()
        except Exception as e:
            self.master.log_error(f"An unexpected error occurrred in smart " +
                                  f"algorithm: {e}")
            self.master.log_error("\nShutting down gracefully. Bye.")
            exit()

    def find_fake_random(self):
        """
        This is the random guess version of the algorithm, where the bars are
        shuffled into random order, then pairs are tested sequentially until
        one is found to be less than it's mate. That is the fake bar, so return
        the number of weigh-ins to the master class, and print both the message
        in the resulting alert box and all the weigh-in details. The master class
        handles printing the number of weigh-ins, as it also is in charge of
        handling averaging the number of weigh-ins for a number of loops as defined
        in the configuration file. Sometimes it gets lucky and produces an immediate
        answer after one weigh-in, but it averages to 2.95 weigh-ins over 20 trials.
        The smart way wins overall, always answering in 2 weigh-ins.
        """
        try:
            self.setup_algorithm()

            self.master.log_success("Beginning random algorithm...")
            selections = [0, 1, 2, 3, 4, 5, 6, 7, 8]

            self.master.log_success("Shuffling the bars...")
            random.shuffle(selections)

            for n in range(0, len(selections) - 1, 2):
                self.reset_button.click()
                time.sleep(self.master.PAUSE_TIME)
                self.left_bowl[selections[n]].send_keys(f"{selections[n]}")
                self.right_bowl[selections[n + 1]].send_keys(f"{selections[n + 1]}")
                self.weigh_in()
                if self.test_weights() == "E":
                    continue
                if self.test_weights() == "L":
                    self.make_selection(selections[n])
                    return n // 2 + 1
                if self.test_weights() == "R":
                    self.make_selection(selections[n + 1])
                    return n // 2 + 1
            self.make_selection(selections[8])
            return 4
        except Exception as e:
            self.master.log_error(f"Something went wrong in the random algorithm: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()

    def find_fake_brute_force(self):
        """
        This is the brute force algorithm. It is not the smart way to do it. First
        it sets up everything by calling setup_algorithm, then sets up the scale
        to have all but one bar, evenly divided between the two sides. Then it
        takes away a pair at a time until the test_weights function returns
        a changed value (from L to E or R to E, or E immediately, meaning the
        odd-man-out was the fake bar.) This is a brute force method that averages
        about 3 weigh-ins over 20 trials. It is not the smart way to do it. The
        master class handles printing the number of weigh-ins, as it also is in
        charge of handling averaging the number of weigh-ins for a number of loops
        as defined in the configuration file.
        """
        self.setup_algorithm()

        try:
            self.master.log_success("Beginning brute force algorithm...")
            self.master.log_success("Divvying up the bars equally...")

            self.setup_scale_brute_force(0)
            self.weigh_button.click()
            self.master.log_success("Weighing...")
            time.sleep(self.master.PAUSE_TIME)

            if self.test_weights() == "E":
                self.make_selection(8)
                return 1

            elif self.test_weights() == "L":
                self.master.log_success(f"The fake bar is between {0} and {3}")
                for n in range(1, 4):
                    self.setup_scale_brute_force(n)
                    self.weigh_in()
                    if self.test_weights() == "E":
                        self.make_selection(4 - n)
                        return n + 1
                    elif self.test_weights() == "L":
                        if n == 3:
                            self.make_selection(0)
                            return n + 1
                        else:
                            self.master.log_success(f"The fake bar is between" +
                                                    f"{0} and {3-n}")

            elif self.test_weights() == "R":
                self.master.log_success(f"The fake bar is between {4} and {7}")
                for n in range(1, 4):
                    self.setup_scale_brute_force(n)
                    self.weigh_in()
                    if self.test_weights() == "E":
                        self.make_selection(n + 3)
                        return n + 1
                    elif self.test_weights() == "R":
                        if n == 3:
                            self.make_selection(7)
                            return n + 1
                        else:
                            self.master.log_success(f"The fake bar is between" +
                                                    f"{n + 4} and {7}")

        except Exception as e:
            self.master.log_error(f"Something went wrong in the brute force" +
                                  f"algorithm: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()

    def initial_fill_bowls(self):
        for l in range(0, 3):
            self.left_bowl[l].send_keys(f"{l}")
        for r in range(3, 6):
            self.right_bowl[r].send_keys(f"{r}")
        self.weigh_button.click()
        self.master.log_success("Weighing...")
        time.sleep(self.master.PAUSE_TIME)

    def reset_and_fill_bowls(self, l, r):
        self.reset_button.click()
        time.sleep(self.master.PAUSE_TIME)
        self.left_bowl[0].send_keys(f"{l}")
        self.right_bowl[0].send_keys(f"{r}")

    def make_selection(self, n):
        self.master.log_success(f"The fake bar is {n}")
        self.selection_buttons[n].click()
        self.master.log_success(f"{self.driver.switch_to.alert.text}")
        time.sleep(self.master.WAIT_TIME)
        try:
            self.driver.switch_to.alert.accept()
        except Exception as e:
            self.master.log_success(f"You closed the alert dialog box.")
        self.getWeighIns()

    def weigh_in(self):
        self.weigh_button.click()
        self.master.log_success("Weighing...")
        time.sleep(self.master.PAUSE_TIME)

    def getWeighIns(self):
        weighins = self.driver.find_elements(By.XPATH, "//ol/li") #find weigh-ins
        for n in range(0, len(weighins)):
            self.master.log_success(f"{n+1}. {weighins[n].get_attribute('innerText')}")

    def setup_scale_brute_force(self, n):
        """
        Place the bars in corresponding locations, based on 'n' - which iteration
        we're currently on, removing one bar on each side every iteration, from
        3 down to 0, and from 4 up to 7. This is only for the brute force algorithm.
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
