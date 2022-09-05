import subprocess
from time import sleep
from datetime import date
from datetime import timedelta

SLEEP_TIME_IN_SECONDS = 1
NEXT_X_MONTHS = 2*30

def get_char(process):
    character = process.stdout.read1()
    print(
            character.decode("utf-8"),
            end="",
            flush=True,
            )
    return character.decode("utf-8")

def search_for_output(strings, process):
    buffer = ""
    while not any(string in buffer for string in strings):
        buffer = buffer + get_char(process)
        
while True:
    today = date.today().strftime("%Y-%m-%d")
    next2month = (date.today() + timedelta(NEXT_X_MONTHS)).strftime("%Y-%m-%d")
    tomorrow = (date.today() + timedelta(1)).strftime("%Y-%m-%d")

    start_date = today
    end_date = next2month

    with subprocess.Popen([
        "python3", 
        "-m",
        "camply",
        "campsites",
        "--campground=233116", 
        "--campground=231959", 
        "--start-date",
        start_date,
        "--end-date",
        end_date,
        "--weekends", 
        #"--continuous", 
        #"--notifications", 
        #"email", 
        #"--search-forever", 
        #"--polling-interval=5"
        ], stdout=subprocess.PIPE) as process:
        while process.poll() is None:
            get_char(process)
            today = date.today().strftime("%Y-%m-%d")
            next2month = (date.today() + timedelta(NEXT_X_MONTHS)).strftime("%Y-%m-%d")
            if today != process.args[7]:
                print(f"weekend_monitor.py: searching date range has changed: [{process.args[7]}, {process.args[9]}] to [{today}, {next2month}], restart search")
                process.terminate()
            sleep(SLEEP_TIME_IN_SECONDS)


    if process.poll() != 0 and process.poll() is not None:
        print(f"weekend_monitor.py: Process ends with error code:{process.poll()}, restarting in {SLEEP_TIME_IN_SECONDS} seconds")
        sleep(SLEEP_TIME_IN_SECONDS)
    else:
        print(f"weekend_monitor.py: Process ends successfully with code:{process.poll()}")
        break

