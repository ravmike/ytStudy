from mitmproxy import http, ctx
import time, re
import os
import pickle
import subprocess
import pandas as pd
import numpy as np
import plotly
from plotly.offline import iplot, plot, init_notebook_mode
from plotly.graph_objs import Scatter
init_notebook_mode()

from Experiments import Experiments

class Exp_plot:
    def __init__(self, dur, tot_size, tbr, dur_p, dbase = None, video_hdr = None, links = None):
        self.dur = dur #Продолжительность видео
        self.tot_size = tot_size #Размер видео в байтах
        self.tbr = tbr #fps
        self.dur_p = dur_p #Продолжительность сегмента (взято среднее по всем сегментам)
        self.db = dbase #Словарь с базой данных
        self.video_hdr = video_hdr
        self.links = links
    def Const_plot(self, filename = None):
        db_const = Experiments(dbfile = filename).DataOutput()['const'] if self.db == None else self.db['const']
        for i, video in enumerate(db_const):
            for speed in db_const[video]:
                rng = []
                res_rec_tup = []
                res_res_tup = []
                
                speed_byus = [float(speed)/8]
                rng = np.array([float(db_const[video][speed][num]['range_end']) -  
                           float(db_const[video][speed][num]['range_begin']) for num in db_const[video][speed]])/1000
                res_rec_tup = [(float(db_const[video][speed][num]['response complete']), 
                           float(db_const[video][speed][num]['first request byte'])) 
                               for num in db_const[video][speed]]
                res_res_tup = [(float(db_const[video][speed][num]['response complete']), 
                           float(db_const[video][speed][num]['first response byte'])) 
                               for num in db_const[video][speed]]
                rbu = [float(db_const[video][speed][num]['buffer'])/1000 for num in db_const[video][speed]]
                rbuffer = []
                for n in range(len(rbu)):
                    rbuffer.append(rbu[n])
                    rbuffer.append(rbu[n])
                rmax = []
                resolution = []
                for v in db_const[video][speed]:
                    rmax.append(db_const[video][speed][v]['aitag'])
                    resolution.append(db_const[video][speed][v]['aitag'])
                    resolution.append(db_const[video][speed][v]['aitag'])
                resolution = [int(val.replace(' px', '')) if type(val) == str else val for val in resolution]
                
     
                rmax = max([int(val.replace(' px', '')) if type(val) == str else val for val in rmax])
                s_v = rng/list(map(lambda x: x[0] - x[1], res_rec_tup))
                s = rng/list(map(lambda x: x[0] - x[1], res_res_tup))
                res_rec = np.array(list(map(lambda x: [x[1], x[0]], res_rec_tup))).reshape(1,-1)          
                res_rec = res_rec - res_rec[0][0]
                res_rec_lst = []
                for n in range(res_rec.shape[1]):
                    res_rec_lst.append(res_rec[0][n])
                s_1 = []
                for n in range(s.shape[0]):
                    s_1.append(s[n])
                    s_1.append(s[n])
                s_v_1 = []
                for n in range(s_v.shape[0]):
                    s_v_1.append(s_v[n])
                    s_v_1.append(s_v[n])    
                btr = rng/self.dur_p[i]
                btr_1=[]
                for n in range(btr.shape[0]):
                    btr_1.append(btr[n])
                    btr_1.append(btr[n])
                btr_glob = np.array([float(db_const[video][speed][num]['avbtr']) for num in db_const[video][speed]])/1000
                btr_glob1 = []
                for n in range(btr_glob.shape[0]):
                    btr_glob1.append(btr_glob[n])
                    btr_glob1.append(btr_glob[n])

                tbr_0 = [float(db_const[video][speed][num]['tbr']) for num in db_const[video][speed]]
                tbr1 = []
                for n in range(len(tbr_0)):
                    tbr1.append(tbr_0[n])
                    tbr1.append(tbr_0[n])
                
                s_avg = np.mean(s)
                s_v_avg = np.mean(s_v)    
                data = [Scatter(x=res_rec_lst, y=s_v_1, name = 'experimental throughput', mode='lines+markers'), 
                      Scatter(x=res_rec_lst, y = rbuffer, name = 'video buffer level (s)',mode='lines+markers'),
                      Scatter(x=res_rec_lst, y = s_1, name = 'response throughput',mode='lines+markers'),
                      Scatter(x=res_rec_lst, y = btr_1, name = 'segment bitrate', mode='lines+markers'),
                      Scatter(x=res_rec_lst, y= speed_byus* len(res_rec_lst), name = 'bandwidth restriction'),
                      Scatter(x=res_rec_lst, y= btr_glob1,name = 'average bitrate'),
                      Scatter(x=res_rec_lst, y= tbr1, name = 'tbr'),
                      Scatter(x=res_rec_lst, y=[rmax] * len(res_rec_lst),name = 'max resolution'),
                      Scatter(x=res_rec_lst, y=[s_avg] * len(res_rec_lst),name = 'response throughput average'),
                      Scatter(x=res_rec_lst, y=[s_v_avg] * len(res_rec_lst), name = 'experimental throughput average'),
                       Scatter(x=res_rec_lst, y = resolution, name = 'resolution')]
                layout = plotly.graph_objs.Layout(
                    title = plotly.graph_objs.layout.Title(text = 'const_' + str(video) + '_' + str(speed),
                                                           xref = 'paper', x = 0),
                        xaxis=dict(
                            title='Time, sec',
                            titlefont=dict(
                                family='Arial, sans-serif',
                                size=18,
                                color='black'
                            ),
                            showticklabels=True,
                            tickangle=0,
                            tickfont=dict(
                                family='Old Standard TT, serif',
                                size=14,
                                color='black'
                            ),
                            exponentformat='e',
                            showexponent='all'
                        ),
                        yaxis=dict(
                            title='Speed, kbyte/s',
                            titlefont=dict(
                                family='Arial, sans-serif',
                                size=18,
                                color='black'
                            ),
                            showticklabels=True,
                            tickangle=0,
                            tickfont=dict(
                                family='Old Standard TT, serif',
                                size=14,
                                color='black'
                            ),
                            exponentformat='e',
                            showexponent='all'
                        )
                    )
                fig = plotly.graph_objs.Figure(data=data, layout=layout)
                plot(fig, filename = 'const_' + str(video) + '_' + str(speed) + '.html')
    def Var_plot(self, filename = None):
        db_var = Experiments(dbfile = filename).DataOutput()['var'] if self.db == None else self.db['var']
        for i, video in enumerate(db_var):
            for speed in db_var[video]:
                rng = []
                res_rec_tup = []
                res_res_tup = []
                
                speed_byus = np.array([float(db_var[video][speed][num]['speed']) for num in db_var[video][speed]])/8
                speed_byus1 = []
                for n in range(speed_byus.shape[0]):
                    speed_byus1.append(speed_byus[n])
                    speed_byus1.append(speed_byus[n])
                rng = np.array([float(db_var[video][speed][num]['range_end']) -  
                           float(db_var[video][speed][num]['range_begin']) for num in db_var[video][speed]])/1000
                res_rec_tup = [(float(db_var[video][speed][num]['response complete']), 
                           float(db_var[video][speed][num]['first request byte'])) 
                               for num in db_var[video][speed]]
                res_res_tup = [(float(db_var[video][speed][num]['response complete']), 
                           float(db_var[video][speed][num]['first response byte'])) 
                               for num in db_var[video][speed]]
                rbu = [float(db_var[video][speed][num]['buffer'])/1000 for num in db_var[video][speed]]
                rbuffer = []
                for n in range(len(rbu)):
                    rbuffer.append(rbu[n])
                    rbuffer.append(rbu[n])
                rmax = []
                resolution = []
                for v in db_var[video][speed]:
                    rmax.append(db_var[video][speed][v]['aitag'])
                    resolution.append(db_var[video][speed][v]['aitag'])
                    resolution.append(db_var[video][speed][v]['aitag'])
                resolution = [int(val.replace(' px', '')) if type(val) == str else val for val in resolution]
                rmax = max([int(val.replace(' px', '')) if type(val) == str else val for val in rmax])
                s_v = rng/list(map(lambda x: x[0] - x[1], res_rec_tup))
                s = rng/list(map(lambda x: x[0] - x[1], res_res_tup))
                res_rec = np.array(list(map(lambda x: [x[1], x[0]], res_rec_tup))).reshape(1,-1)          
                res_rec = res_rec - res_rec[0][0]
                res_rec_lst = []
                for n in range(res_rec.shape[1]):
                    res_rec_lst.append(res_rec[0][n])
                s_1 = []
                for n in range(s.shape[0]):
                    s_1.append(s[n])
                    s_1.append(s[n])
                s_v_1 = []
                for n in range(s_v.shape[0]):
                    s_v_1.append(s_v[n])
                    s_v_1.append(s_v[n])    
                btr = rng/self.dur_p[i]
                btr_1=[]
                for n in range(btr.shape[0]):
                    btr_1.append(btr[n])
                    btr_1.append(btr[n])
                btr_glob = np.array([float(db_var[video][speed][num]['avbtr']) for num in db_var[video][speed]])/1000
                btr_glob1 = []
                for n in range(btr_glob.shape[0]):
                    btr_glob1.append(btr_glob[n])
                    btr_glob1.append(btr_glob[n])
                tbr_0 = [float(db_var[video][speed][num]['tbr']) for num in db_var[video][speed]]
                tbr1 = []
                for n in range(len(tbr_0)):
                    tbr1.append(tbr_0[n])
                    tbr1.append(tbr_0[n])
                s_avg = np.mean(s)
                s_v_avg = np.mean(s_v)    
                data = [Scatter(x=res_rec_lst, y=s_v_1, name = 'experimental throughput', mode='lines+markers'), 
                      Scatter(x=res_rec_lst, y = rbuffer, name = 'video buffer level (s)',mode='lines+markers'),
                      Scatter(x=res_rec_lst, y = s_1, name = 'response throughput',mode='lines+markers'),
                      Scatter(x=res_rec_lst, y = btr_1, name = 'segment bitrate', mode='lines+markers'),
                      Scatter(x=res_rec_lst, y= speed_byus1, name = 'bandwidth restriction'),
                      Scatter(x=res_rec_lst, y= btr_glob1,name = 'average bitrate'),
                      Scatter(x=res_rec_lst, y= tbr1, name = 'tbr'),
                      Scatter(x=res_rec_lst, y=[rmax] * len(res_rec_lst),name = 'max resolution'),
                      Scatter(x=res_rec_lst, y=[s_avg] * len(res_rec_lst),name = 'response throughput average'),
                      Scatter(x=res_rec_lst, y=[s_v_avg] * len(res_rec_lst), name = 'experimental throughput average'),
                       Scatter(x=res_rec_lst, y = resolution, name = 'resolution')]
                layout = plotly.graph_objs.Layout(
                    title = plotly.graph_objs.layout.Title(text = 'var_' + str(video) + '_' + str(speed),
                                                           xref = 'paper', x = 0),
                        xaxis=dict(
                            title='Time, sec',
                            titlefont=dict(
                                family='Arial, sans-serif',
                                size=18,
                                color='black'
                            ),
                            showticklabels=True,
                            tickangle=0,
                            tickfont=dict(
                                family='Old Standard TT, serif',
                                size=14,
                                color='black'
                            ),
                            exponentformat='e',
                            showexponent='all'
                        ),
                        yaxis=dict(
                            title='Speed, kbyte/s',
                            titlefont=dict(
                                family='Arial, sans-serif',
                                size=18,
                                color='black'
                            ),
                            showticklabels=True,
                            tickangle=0,
                            tickfont=dict(
                                family='Old Standard TT, serif',
                                size=14,
                                color='black'
                            ),
                            exponentformat='e',
                            showexponent='all'
                        )
                    )
                fig = plotly.graph_objs.Figure(data=data, layout=layout)
                plot(fig, filename = 'var_' + str(video) + '_' + str(speed) + '.html')
