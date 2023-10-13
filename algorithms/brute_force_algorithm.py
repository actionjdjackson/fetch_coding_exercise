from fake_finder_algorithm import FakeFinderAlgorithm
import time

class BruteForceAlgorithm(FakeFinderAlgorithm):
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

    def __init__(self, master):
        super().__init__(master)


    def find_fake(self):
        """
        Do the stuff. Find the fake - the brute force way.
        """
        self.setup_algorithm()

        try:
            self.master.log_success("Beginning brute force algorithm...")
            self.master.log_success("Divvying up the bars equally...")

            self.setup_scale_brute_force(0)
            self.weigh_in()

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
                                                    f" {0} and {3-n}")

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
                                                    f" {n + 4} and {7}")

        except Exception as e:
            self.master.log_error(f"Something went wrong in the brute force" +
                                  f"algorithm: {e}")
            self.master.log_error("Exiting program gracefully, goodbye!")
            exit()

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
