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
    1. `sudo dnf install python3`

    ***On Windows***
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
  - `DEFAULT_BROWSER`: Ask, Chrome, Firefox, Edge, Safari, Internet Explorer
  - `RANDOM_GUESS`: Y or N for randomly guessing which is the lightest bar
  - `WAIT_TIME`: # of seconds to wait after finding the fake bar, before exiting
  - `PAUSE_TIME`: # of seconds to pause inbetween weighings
  - `LOOP`: Y or N for looping the main method

3. If you are running Safari, please make sure you go to the Develop menu, and enable 'Allow Remote Automation'

4. Run the script:
    ```bash
    python find_fake_bar_test.py
    ```
    or, depending on your installation, you may need to run it as:
    ```bash
    python3 find_fake_bar_test.py
    ```
5. If you're configured to ask for a browser, enter the browser's first letter in the prompt.
   If you want the dialog box for winning the game to go away sooner, change the WAIT_TIME variable in the configuration file. Clicking "OK" on the dialog will cause an error. If you are in loop mode, use Ctrl-C to exit the program.

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
    the webpage's components, and Python's built-in time library, for waiting
    until the interface updates.
