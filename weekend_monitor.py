import subprocess
from time import sleep
from datetime import date
from datetime import datetime
from datetime import timedelta

SLEEP_TIME_IN_SECONDS = 1
NEXT_X_MONTHS = 2*30
DATE_FORMAT = "%Y-%m-%d"
HOLIDAY_START_DATE = datetime.strptime("2022-11-17", DATE_FORMAT).date()
HOLIDAT_END_DATE = datetime.strptime("2022-12-01", DATE_FORMAT).date()

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
    today = date.today()
    next2month = date.today() + timedelta(NEXT_X_MONTHS)
    tomorrow = date.today() + timedelta(1)

    start_date = today
    end_date = next2month

    # Holiday logic: reduce search window if overlapping with that of the holiday 
    print(min([HOLIDAY_START_DATE, HOLIDAT_END_DATE, today, next2month]))
    print(max([HOLIDAY_START_DATE, HOLIDAT_END_DATE, today, next2month]))

    with subprocess.Popen([
        "python3", 
        "-m",
        "camply",
        "campsites",
        "--campground=233116", 
        "--campground=231959", 
        "--start-date",
        start_date.strftime(DATE_FORMAT),
        "--end-date",
        end_date.strftime(DATE_FORMAT),
        "--weekends", 
        #"--continuous", 
        #"--notifications", 
        #"email", 
        #"--search-forever", 
        #"--polling-interval=5"
        ], stdout=subprocess.PIPE) as process:
        while process.poll() is None:
            get_char(process)
            today = date.today()
            next2month = (date.today() + timedelta(NEXT_X_MONTHS))

            if today.strftime(DATE_FORMAT) != process.args[7]:
                print(f"weekend_monitor.py: searching date range has changed: [{process.args[7]}, {process.args[9]}] to [{today}, {next2month}], restart search")
                process.terminate()
            sleep(SLEEP_TIME_IN_SECONDS)


    if process.poll() != 0 and process.poll() is not None:
        print(f"weekend_monitor.py: Process ends with error code:{process.poll()}, restarting in {SLEEP_TIME_IN_SECONDS} seconds")
        sleep(SLEEP_TIME_IN_SECONDS)
    else:
        print(f"weekend_monitor.py: Process ends successfully with code:{process.poll()}")
        break

