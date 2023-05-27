# Logging
from datetime import datetime
import logging

now = datetime.now()
dt_string = now.strftime("%d-%m-%Y|%H:%M:%S")
logging.basicConfig(filename="logs/{}.txt".format(dt_string))
stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)


# Flask Body
from flask import Flask, request
from threading import Thread
import codecs, attendix

app = Flask('')

@app.route('/')
def main():
  action = request.args.get("action")

@app.route('/post/otp', methods=['POST'])
def post_request_otp():
  otp = request.form.get('otp')
  


# Starts Webserver
def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()

print("SleepyAttendix Launched!")
keep_alive.keep_alive()
