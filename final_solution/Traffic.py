from mitmproxy import http, ctx
import time, re
import os
import subprocess
import numpy as np

class TrafficShaping:
    def Speed_limit(script, speed, password, t = None):
        command = 'sh ' + script + " " + str(speed)
        with open (password, "r") as f:
            sudoPass = f.read()
        os.system('echo %s|sudo -S %s' % (sudoPass, command))
    def Videos(link, password): #Открытие видео 
        print ('Videos')
        command = '-g throttle open -j ' + link
        with open (password, "r") as f:
            sudoPass = f.read()
        os.system('echo %s | sudo -S %s' % (sudoPass, command))
    def Stop_limit(password):
        with open (password, "r") as f:
            sudoPass = f.read()
        command = 'pfctl -F all'
        command2 = 'pfctl -q -f /etc/pf.conf'
#         command = 'dnctl -q flush'
#         command2 = 'pfctl -f /etc/pf.conf'
        os.system('echo %s|sudo -S %s' % (sudoPass, command))
        os.system('echo %s|sudo -S %s' % (sudoPass, command2))

class MitmDump:
    def StartMITMDump(file, audio = True):
        if audio: 
            subprocess.Popen(["mitmdump", "-p 8890",  "-w", file, "~t video/webm | ~t audio/"])
        else:
            subprocess.Popen(["mitmdump", "-p 8890",  "-w", file, "~t video/webm "])
    def StopMITMDump(t):
        time.sleep(t)
        os.system("kill -2 $(ps -ax | grep 'mitmdump' | awk '{print $1}' | head -1)")
    def ReceiveData(script, file, speed): #Получение отфильтрованных данных из всех пакетов
        with open('speed.txt', 'w') as f:
            f.write(speed)
        os.system("mitmdump -s " + script + " -nr " + file)