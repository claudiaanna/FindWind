import matplotlib.pyplot as plt
import numpy as np
from random import randint
import matplotlib.colors as colors
from numpy import ma
from windy import yrno, wfinder
import os


def get_fullpath(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, filename)

def plot(forecasts, path):
    date = []
    temp = []
    c_temp = []
    speed = []
    c_speed = []
    prec = []
    c_prec = []
    dire = []
    u, v = [], []

    dir_vec = {'N': [0,-0.1] ,'NNW': [0.025,-0.075],'NW': [0.05,-0.05],'WNW': [0.075,-0.025],
                'W': [0.1,0],'WSW': [0.075,0.025],'SW': [0.05,0.05],'SSW': [0.025,0.075],
                'S': [0,0.1],'SSE': [-0.025,0.075],'SE': [-0.05,0.05],'ESE': [-0.075,0.025],
                'E': [-0.1,0],'ENE': [-0.075,-0.025],'NE': [-0.05,-0.05],'NNE': [-0.025,-0.075]}

    for f in forecasts:
        date.append(f.comb_date)
       
        temp.append(f.temp)
        c_temp.append(f.temp)

        speed.append(f.wind_speed_mps)
        c_speed.append(f.wind_speed_mps)

        prec.append(f.prec)
        c_prec.append(f.prec)
       
        dire.append(f.wind_dir)

    for i in dire:
        u.append(dir_vec[i][0])
        v.append(dir_vec[i][1])

    cm_temp = plt.cm.get_cmap('jet')
    cm_speed = plt.cm.get_cmap('inferno')
    cm_prec = plt.cm.get_cmap('Blues')

    temp_max = max(temp)
    temp_min = min(temp)
    prec_max = max(prec)
    prec_min = min(prec)
    speed_max = max(speed)
    speed_min = min(speed)

    font = {'family': 'sans-serif',
        'weight': 'normal',
        'color' : '#F39C12'
        }

    plt.rcParams['figure.figsize'] = (15,22)
    fig, ax = plt.subplots(nrows=4, ncols=1, sharex=True, sharey=False,gridspec_kw={'height_ratios': [1.5,1,2.5,0.6]})
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.15, top=0.95, hspace=0.5)
    plt.xticks(rotation = 90)
    plt.tick_params(labelsize = 20, labelcolor = '#9ab3d5')
    

    ax[0].scatter(date, temp, vmin=-25, vmax=40, s = 500, c = c_temp, cmap = cm_temp, alpha = 0.75)
    ax[0].set_ylabel('Temperatura [*C]', size = 30, rotation=0, fontdict=font)
    ax[0].get_yaxis().set_label_coords(0.5,1)
    ax[0].tick_params(labelsize = 20, labelcolor = '#9ab3d5')
    ax[0].yaxis.set_ticks(np.arange(temp_min-5,temp_max+5, 2))

    ax[1].scatter(date, prec, vmin=-40, vmax=20, s = 500, c = c_prec, alpha = 0.75, cmap = cm_prec)
    ax[1].set_ylabel('Opady [mm/h]', size = 30, rotation=0, fontdict=font)
    ax[1].get_yaxis().set_label_coords(0.5,1)
    ax[1].tick_params(labelsize = 20, labelcolor = '#9ab3d5')
    ax[1].yaxis.set_ticks(np.arange(prec_min,prec_max+2, 2))

    ax[2].scatter(date, speed, vmin=0, vmax=30, s = 500, c = c_speed, alpha = 0.75, cmap = cm_speed)
    ax[2].set_ylabel('Prędkość wiatru [m/s]', size = 30, rotation=0, fontdict=font)
    ax[2].get_yaxis().set_label_coords(0.5,1)
    ax[2].tick_params(labelsize = 20, labelcolor = '#9ab3d5')
    ax[2].yaxis.set_ticks(np.arange(speed_min,speed_max+5, 2))

    ax[3].quiver(date, len(date)*[0], u*4, v*4, scale = 0.2,scale_units = 'inches', width = 0.002)
    ax[3].set_ylabel('Kierunek wiatru', size = 30, rotation=0, fontdict=font)
    ax[3].get_yaxis().set_label_coords(0.5,1)
    ax[3].axes.get_yaxis().set_ticks([])

    ax[0].grid()
    ax[1].grid()
    ax[2].grid()

    plt.savefig(path,facecolor ='#002750')