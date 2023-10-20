from fake_finder_algorithm import FakeFinderAlgorithm
import time

class SmartAlgorithm(FakeFinderAlgorithm):

    def __init__(self, master):
        super().__init__(master)


    def find_fake(self):
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
        self.setup_algorithm()

        try:

            self.master.log_success("Beginning the smart algorithm...")
            self.master.log_success("Splitting into three groups...")
            self.bars = list(range(len(self.selection_buttons)))
            left_bars = self.bars[:3]
            right_bars = self.bars[3:6]
            off_bars = self.bars[6:9]
            self.fill_bowls(left_bars, right_bars)
            self.weigh_in()
            initial_test = self.test_weights()

            if initial_test == "E":  # Are the two sides equal?

                self.second_test(off_bars)

            elif initial_test == "L":  # is left lighter?

                self.second_test(left_bars)

            elif initial_test == "R":  # is right lighter?

                self.second_test(right_bars)

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


    def second_test(self, bars_to_test):
        try:
            self.bars = bars_to_test
            second_left_bars = self.bars[0:1]
            second_right_bars = self.bars[1:2]
            second_off_bars = self.bars[2:3]

            self.master.log_success(f"Fake bar is between {second_left_bars} and {second_off_bars}")
            self.reset_and_fill_bowls(second_left_bars, second_right_bars)  # 8 is off the scale
            self.weigh_in()
            second_test = self.test_weights()
            if second_test == "E":
                self.make_selection(second_off_bars[0])
            elif second_test == "L":
                self.make_selection(second_left_bars[0])
            elif second_test == "R":
                self.make_selection(second_right_bars[0])
            else:
                raise ValueError("Invalid test weight value")

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


    def fill_bowls(self, left, right):
        for l in left:
            self.left_bowl[l].send_keys(f"{l}")
        for r in right:
            self.right_bowl[r].send_keys(f"{r}")

    def reset_and_fill_bowls(self, left, right):
        self.reset_button.click()
        time.sleep(self.master.PAUSE_TIME)
        self.fill_bowls(left, right)
