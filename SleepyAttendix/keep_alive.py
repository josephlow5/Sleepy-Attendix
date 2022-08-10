from flask import Flask, request
from threading import Thread
import codecs, attendix

app = Flask('')


@app.route('/')
def main():
  action = request.args.get("action")

  if action:
    if(action=="register"):
      f=codecs.open("html/register.html", 'r')
      return f.read()
    elif(action=="otp"):
      f=codecs.open("html/otp.html", 'r')
      return f.read()
  else:
      f=codecs.open("html/home.html", 'r')
      return f.read()

@app.route('/post/otp', methods=['POST'])
def post_request_otp():
  otp = request.form.get('otp')

  if otp:
    return '<script>alert("Updated attendance for {} users!");window.location.replace("https://SleepyAttendix.josephlow5.repl.co/");</script>'.format(attendix.TakeAttendance(otp))

@app.route('/post/register', methods=['POST'])
def post_request_reg():
  email = request.form.get('email')
  tpno = request.form.get('tpno')
  pw = request.form.get('pw')

  if email and tpno and pw:
    if attendix.VerifyLogin(tpno,pw):
      if attendix.SaveUser(tpno,pw,email):
        return '<script>alert("Register Successfully! From now on we will take attendance for you if anyone gave us the otp.");window.location.replace("https://SleepyAttendix.josephlow5.repl.co/");</script>'
      else:
        return '<script>alert("register failed!");window.location.replace("https://SleepyAttendix.josephlow5.repl.co/?action=register");</script>'
    else:
      return '<script>alert("invalid login!");window.location.replace("https://SleepyAttendix.josephlow5.repl.co/?action=register");</script>'
  


def run():
  app.run(host="0.0.0.0", port=8000)

def keep_alive():
  server = Thread(target=run)
  server.start()