#! /usr/bin/env python

# default imports
import sys, time, os, datetime, json, logging, threading, socket

# non default imports
from flask import Flask, Response, render_template, jsonify # pip install flask

log = logging.getLogger(__name__)

app = Flask(__name__)

def get_now():
	return datetime.datetime.now().strftime("%Y:%m:%d %H:%M:%S.%f")

def get_now_iso():
    return datetime.datetime.utcnow().isoformat()

def get_epoch():
	return '%f' % time.time()

def get_pid():
	return os.getpid()

def get_hostname():
	return socket.gethostname()

# *** logging ***
def log_cfg():

  log.setLevel(logging.DEBUG)
  fmt = logging.Formatter('%(message)s')

  ch = logging.StreamHandler()
  ch.setFormatter(fmt)
  log.addHandler(ch)

def dump(message, level="INFO", **kwargs):
	if(kwargs):
		out = { "timestamp":get_now(), "epoch":get_epoch(), "pid": get_pid(), "level": level, "message": message, "kwargs": kwargs }
	else:
		out = { "timestamp":get_now(), "epoch":get_epoch(), "pid": get_pid(), "level": level, "message": message }
	log.debug(json.dumps(out))
	return True

# *** ### ***

def get_message():
	msg = { "timestamp": get_now(), "epoch": get_epoch() }
	#dump(msg) # debug
	time.sleep(1.0)
	return json.dumps(msg)

@app.route('/stream')
def stream():
    def eventStream():
        while True:
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")

@app.route("/")
def index():
	
	return render_template('data.html', title="see flask example", now=get_now(), host = get_hostname())

if __name__ == "__main__":

	log_cfg()
		
	dump("Starting Flask")

	app.run(host='0.0.0.0', port=7001, debug=True)

