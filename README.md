# Finding The Fake Gold Bar

Test Code Exercise from Fetch

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

- Required Python packages installed. You can install them using `pip3 install -r requirements.txt` or, in some cases you can use `pip install -r requirements.txt`

- Configuration file (`config.json`) with optional settings

---

## Usage

1. Clone this repository to your local machine
    ```bash
      git clone https://github.com/actionjdjackson/fetch_coding_exercise
    ```
2. Configure the `config.json` file with the settings you wish to use:
  ```json
  {
    "URL": "http://sdetchallenge.fetch.com/",
    "DEFAULT_BROWSER": "Ask",
    "RANDOM_GUESS": "Y",
    "WAIT_TIME": 5,
    "PAUSE_TIME": 2,
    "LOOP": "Y"
  }
  ```
  - `URL`: The URL of the game website
  - `DEFAULT_BROWSER`: Ask, Chrome, Firefox, Edge, Safari, or Internet Explorer
  - `RANDOM_GUESS`: Y or N for randomly guessing which is the lightest bar
  - `WAIT_TIME`: # of seconds to wait after finding the fake bar, before exiting or looping
  - `PAUSE_TIME`: # of seconds to pause inbetween weighings, to allow the interface to "catch up"
  - `LOOP`: Y or N for looping the algorithm on a fresh load of the page

3. If you are running Safari, please make sure you go to the Develop menu, and enable 'Allow Remote Automation'

4. Run the script:
    ```bash
    python3 find_fake_bar_test.py
    ```
    or, depending on your installation, you may be able to run it as:
    ```bash
    python find_fake_bar_test.py
    ```
5. If you're configured to ask for a browser, enter the browser's first letter in the prompt.

6. If you want the dialog box for winning the game to go away sooner, change the WAIT_TIME variable in the configuration file. Clicking "Close" or "OK" on the dialog will cause an error in Firefox and Chrome, and possibly also Edge and IE. Safari asks you wether you want to continue the session or stop it - make sure you click continue, or a similar error will occur in Safari, too. The error causes the program to exit gracefully. So, it's best to just wait for the program to accept the "Close" or "OK" button itself and start on the next loop, or close down if you aren't looping.

7. If you're looping. If you are in loop mode, use Ctrl-C in the terminal/command prompt to exit the program, and it will exit gracefully.

---

## How it Works

1. Split the bars in half, one half on each side of the scale, leaving out
    either the last bar or a random guess (Like Deal or No Deal).

2. If the odd-man-out is the fake bar (i.e. the two halves are equal in weight),
    then click that bar's number.

3. If one side is less than the other, take out pairs of bars until the two
    sides are equal, and click the bar that was taken out last (before they were
    equal) on the lighter side.

4. It will always find the fake bar within 4 weigh-ins, if not less.

5. This is all accomplished by way of Selenium WebDriver, for interacting with
    the webpage's components, Python's built-in time library, for waiting
    until the interface updates, Python's built-in logging, os, and json libraries
    are also used for configuration and logging purposes.
