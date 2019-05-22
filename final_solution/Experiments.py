from mitmproxy import http, ctx
import time, re
import os
import pickle
import subprocess
import pandas as pd
import numpy as np

from Traffic import TrafficShaping, MitmDump
from proxy import *

mapp = {"133":"240 px", "134":"360 px", "135": "480 px", "136": "720 px", "137": "1080 px", "160": "144 px", 
       "264": "1440 px", "298": "720 px", "299": "1080 px", "167": "360 px", "168": "480 px", "169": "720 px",
       "170" : "1080 px", "218": "480 px", "219": "144 px", "242": "240 px", "243": "360 px", "244": "480 px", 
       "245": "480 px", "246": "480 px", "247": "720 px", "248": "1080 px", "271": "1440 px", "278": "144 px"}
# Itag закодирован числом, словарь служит для сопоставления кодировки разрешению
start_file = 'flow.txt' #Файл, в который пойдёт весь отфильтрованый поток
data_file = 'data.txt' #Файл, куда будут сохранены нужные, раскодированные данные
script = "youtube_script.py" #Скрипт, при помощи которого достаём необходимые данные
bscript = "tshape.sh" #Bash-скрипт для траффик-шейпинга
pword = "pass.txt" #Файл с паролем

class Experiments:
    def __init__(self, database = None, links = None, const_exp = None, var_exp = None, time_change = None, dbfile = None,
                audio = True, video_hdr = None):
        self.links = links
        self.const_exp = const_exp
        self.var_exp = var_exp
        self.tc = time_change #Время до изменения скорости для переменного эксперимента
        self.filename = dbfile #Файл с базой данных
        self.db = database #Словарь с базой данных (необходимо что-то одно)
        self.audio = audio #Извлекать аудио сегменты или нет
        self.video_hdr = video_hdr #база с tbr
    def Const_exp(self):
        with open ("save.txt", "w") as f: #Файл для передачи названия конечного файла скрипту
            f.write(data_file)
        SetProxy() #Установка прокси
        for num, link in enumerate(self.links):
            l = {}
            for speed in self.const_exp:
                MitmDump.StartMITMDump(start_file, self.audio)
                time.sleep(5)
                TrafficShaping.Videos(link[0], pword)
                TrafficShaping.Speed_limit(bscript, speed, pword)
                MitmDump.StopMITMDump(link[1])
                MitmDump.ReceiveData(script, start_file, str(speed))
                d = {}
                a = []
                video_id = link[0].replace('https://www.youtube.com/watch?v=','')
                video_hdr2 = self.video_hdr.loc[(self.video_hdr['Id']== video_id)]
                if not os.path.exists(data_file):
                    continue
                with open(data_file, "r") as f:
                    a = [line.replace("\n","").split(",") for line in f.readlines()]
                for idx, val in enumerate(a):
                    if (any(video_hdr2.Format_id == float(val[1]))):
                        tbr = video_hdr2.loc[(video_hdr2['Format_id'] == float(val[1]))]['Tbr'].tolist()[0]/8.0                   
                        btr = video_hdr2.loc[(video_hdr2['Format_id'] == float(val[1]))]['Filesize'].tolist()[0]/video_hdr2.loc[(video_hdr2['Format_id'] == float(val[1]))]['Duration'].tolist()[0]
                    else:
                        print(val[1])
                        tbr = 0
                        btr = 0
                    d[idx] = {"mime":val[0], "aitag":mapp[val[1]] if val[1] in mapp else 0, "duration":val[2], 
                              "range_begin":val[3], "range_end":val[4], "buffer":val[5], 
                             "first request byte":val[6], "request complete":val[7], "first response byte":val[8],
                             "response complete":val[9] if val[9] != 'None' 
                              else str(float(val[8]) + 1.5), 'buffer':val[10], 'speed':val[11],
                             'tbr': tbr, 'avbtr':btr}
                l[speed] = d
                os.system('rm ' + start_file)
                os.system('rm ' + data_file)
                os.system('killall "Google Chrome"')
            self.db['const'][num] = l
            l = {}
    def Var_exp(self):
        with open ("save.txt", "w") as f: #Файл для передачи названия конечного файла скрипту
            f.write(data_file)
        SetProxy()
        for num, link in enumerate(self.links):
            l = {}
            for exp in self.var_exp:
                MitmDump.StartMITMDump(start_file, self.audio)
                time.sleep(5)
                TrafficShaping.Videos(link[0], pword)
                MitmDump.StopMITMDump(6)
                #Строчки выше необходимы для того, чтобы видео успело прогрузиться 
                for speed in exp:
                    MitmDump.StartMITMDump(start_file, self.audio)
                    TrafficShaping.Speed_limit(bscript, speed, pword)
                    time_ch = self.tc if self.tc != None else int(link[1]/len(exp))
                    MitmDump.StopMITMDump(time_ch)
                    MitmDump.ReceiveData(script, start_file, str(speed))
                d = {}
                a = []
                video_id = link[0].replace('https://www.youtube.com/watch?v=','')
                video_hdr2 = self.video_hdr.loc[(self.video_hdr['Id']== video_id)]

                if not os.path.exists(data_file):
                    continue
                with open(data_file, "r") as f:
                    a = [line.replace("\n","").split(",") for line in f.readlines()]
                for idx, val in enumerate(a):
                    if (any(video_hdr2.Format_id == float(val[1]))):
                        tbr = video_hdr2.loc[(video_hdr2['Format_id'] == float(val[1]))]['Tbr'].tolist()[0]/8.0
                        btr = video_hdr2.loc[(video_hdr2['Format_id'] == float(val[1]))]['Filesize'].tolist()[0]/video_hdr2.loc[(video_hdr2['Format_id'] == float(val[1]))]['Duration'].tolist()[0]
                    else:
                        print(val[1])
                        tbr = 0  
                        btr = 0
                    d[idx] = {"mime":val[0], "aitag":mapp[val[1]] if val[1] in mapp else 0, "duration":val[2], 
                              "range_begin":val[3], "range_end":val[4], "buffer":val[5], 
                             "first request byte":val[6], "request complete":val[7], "first response byte":val[8],
                             "response complete":val[9] if val[9] != 'None' 
                              else str(float(val[8]) + 1.5), 'buffer':val[10], 'speed':val[11], 
                             'tbr':tbr, 'avbtr':btr}
                l[exp] = d
                os.system('rm ' + start_file)
                os.system('rm ' + data_file)
                os.system('killall "Google Chrome"')   
            self.db['var'][num] = l
            l = {}
    def StopLimitTraffic():
        TrafficShaping.Stop_limit(pword)
    def Saving(self):
        with open (self.filename, 'wb') as f:
            pickle.dump(self.db, f)
    def DataOutput(self):
        with open (self.filename, 'rb') as f:
            db = pickle.load(f)
        return db
    def __del__(self):
        os.system('rm save.txt')
        os.system('rm speed.txt')
        DisableProxy()