# Finding The Fake Gold Bar

Test Code Exercise for Fetch

## Prerequisites

Before using this script, ensure you have the following:

- Python 3 installed on your system

    ***On macOS, run:***
    1. [Install Homebrew](https://brew.sh/#install) if you haven't already
    2. Run `brew install python`

    ***On Ubuntu, run:***
    1. Run `sudo apt-get update`
    2. Run `sudo apt-get install python3.6`

    ***On Fedora, RHEL, and CentOS, run:***
    1. Run `sudo dnf install python3`

    ***On Windows:***
    1. Go to <https://www.python.org> and download the Windows installer.
    2. Double-click on the downloaded file and install Python for all users,
    and ensure that Python is added to your path. Click on **Install Now**.
    3. After the installation is complete, click Disable path length limit,
    and then **Close**.
    4. Click **Close** to end the installation.

- Required Python packages installed. The only one not included in python is
selenium webdriver. You can install it using `pip3 install selenium` or, after
you clone the repo, run: `pip3 install -r requirements.txt`

- Configuration file (`config.json`) with valid optional settings. This will be visible in the repo's main directory after you clone the repository.

---

## Usage

1. Clone this repository to your local machine
    ```bash
    git clone https://github.com/actionjdjackson/fetch_coding_exercise.git
    ```
2. Configure the `config.json` file with the settings you wish to use:
  ```json
  {
    "URL": "http://sdetchallenge.fetch.com/",
    "DEFAULT_BROWSER": "Ask",
    "ALGORITHM": "S",
    "WAIT_TIME": 5,
    "PAUSE_TIME": 2,
    "LOOP": "Y",
    "N_LOOPS": 5
  }
  ```
  - `URL`: "The URL of the game website"
  - `DEFAULT_BROWSER`: "Ask", "Chrome", "Firefox", "Edge", "Safari", or "Internet Explorer"
  - `ALGORITHM`: "S" or "B" or "R" for using the smart algorithm (S), versus brute force (B) or random (R) algorithms
  - `WAIT_TIME`: # of seconds to wait after finding the fake bar, before exiting or looping
  - `PAUSE_TIME`: # of seconds to pause in between weighings, to allow the interface to "catch up"
  - `LOOP`: "Y" or "N" for looping the algorithm on a fresh load of the page
  - `N_LOOPS`: # of loops to execute (a loop is a complete refresh of the URL and its components, and re-running of the selected algorithm)

3. If you are running Safari, please make sure you go to the Develop menu, and enable 'Allow Remote Automation'

4. Run the script:
    ```bash
    python3 find_fake_test.py
    ```
    or, depending on your installation, you may be able to run it as:
    ```bash
    python find_fake_test.py
    ```
5. If you're configured to ask for a browser, enter the browser's first letter in the prompt.

6. The program will automatically enter values, click buttons, etc. to run the chosen algorithm and find the fake bar. When the alert dialog box closes after a few seconds, you'll see in the terminal/command prompt the fake bar number, the text from the alert dialog box, and the list of weigh-ins, as well as the number of weigh-ins that were used to find the result.

6. If you want the alert dialog box for winning the game to go away sooner, change the WAIT_TIME variable in the configuration file. Clicking "Close" or "OK" on the alert dialog box is ok, too.

7. If you are in loop mode, and all the loops are finished, you'll also receive the average number of weigh-ins for the algorithm you chose. If you want to quit it sooner, use Ctrl-C in the terminal/command prompt to exit the program, and it will exit gracefully. If possible, you'll get the current running average of weigh-ins.

---

## How it Works - The Smart Way

1. Split the bars into three groups of three values each - left, right, and off-the-scale

2. If one side is initially lighter:

3. That group of 3 is then split into 3 locations - left, right, and off-the-scale, if one side is lighter, that's the fake bar, if it's equal, the off-the-scale value is the fake bar.

4. If the sides are initially equal:

5. Split the off-the-scale values into 3 locations - left, right, and off-the-scale, and if one side is lighter, that's the fake bar, if it's equal, the off-the-scale value is the fake bar.


---

## How it Works - The Brute Force Way

1. Split the bars in half, one half on each side of the scale, leaving out the last bar

2. If the two halves are equal in weight, the odd-man-out is the fake bar

3. If one side is less than the other, take out pairs of bars until the two
    sides are equal, and the bar that was taken out last (before they were
    equal) is the fake bar.

4. It will always find the fake bar within 4 weigh-ins, if not less. It averages 3.0 weigh-ins over 20 loops.

---

## How it Works - The Random Way

1. Shuffle the bars randomly

2. Put one pair of bars in the left and right bowls

3. If one bar is less than the other, we've found the fake bar

4. If the bars are equal, repeat steps 2 & 3. It also will always find the fake bar within 4 weigh-ins, if not less. It averages 2.95 weigh-ins over 20 loops.

---

This is all accomplished by way of Selenium WebDriver, for interacting with
the webpage's components, Python's built-in time library, for waiting
until the interface updates, Python's built-in logging, os, and json libraries
are also used for configuration and logging purposes. There doesn't seem to be much
difference between random and brute force algorithms for searching for the fake bar, but
the smart way is consistently giving correct answers in only two iterations. Every time.
