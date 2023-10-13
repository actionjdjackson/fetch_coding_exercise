from fake_finder_algorithm import FakeFinderAlgorithm
import random
import time

class RandomAlgorithm(FakeFinderAlgorithm):

    def __init__(self, master):
        super().__init__(master)


    def find_fake(self):
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
