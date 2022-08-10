import keep_alive
from datetime import datetime
import logging

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y|%H:%M:%S")
logging.basicConfig(filename="logs/{}.txt".format(dt_string))
stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)

print("SleepyAttendix Launched!")
keep_alive.keep_alive()
