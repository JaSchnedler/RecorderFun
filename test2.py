import os
import subprocess
import time
import signal

record = 'arecord -D hw:1,0 -r 44100 -f S16_LE temp.wav'
p = subprocess.Popen(record,stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
time.sleep(10)
os.killpg(os.getpgid(p.pid), signal.SIGTERM)
