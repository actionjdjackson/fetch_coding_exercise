from fake_finder_algorithm import FakeFinderAlgorithm

class SmartAlgorithm(FakeFinderAlgorithm):

    def __init__(self, master):
        super().__init__(self, master):


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
        try:
            self.setup_algorithm()

            self.master.log_success("Beginning the smart algorithm...")
            self.master.log_success("Splitting into three groups...")
            self.initial_fill_bowls()
            self.weigh_in()
            initial_test = self.test_weights()

            if initial_test == "E":  # Are the two sides equal?
                self.master.log_success("Fake bar is between 6 and 8")
                self.reset_and_fill_bowls(6, 7)  # 8 is off the scale
                self.weigh_in()
                second_test = self.test_weights()
                if second_test == "E":
                    self.make_selection(8)
                elif second_test == "L":
                    self.make_selection(6)
                elif second_test == "R":
                    self.make_selection(7)
                else:
                    raise ValueError("Invalid test weight value")

            elif initial_test == "L":  # is left lighter?
                self.master.log_success("Fake bar is between 0 and 2")
                self.reset_and_fill_bowls(0, 1)  # 2 is off the scale
                self.weigh_in()
                second_test = self.test_weights()
                if second_test == "E":
                    self.make_selection(2)
                elif second_test == "L":
                    self.make_selection(0)
                elif second_test == "R":
                    self.make_selection(1)
                else:
                    raise ValueError("Invalid test weight value")

            elif initial_test == "R":  # is right lighter?
                self.master.log_success("Fake bar is between 3 and 5")
                self.reset_and_fill_bowls(3, 4)  # 5 is off the scale
                self.weigh_in()
                second_test = self.test_weights()
                if second_test == "E":
                    self.make_selection(5)
                elif second_test == "L":
                    self.make_selection(3)
                elif second_test == "R":
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
