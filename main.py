from flask import Flask, flash, redirect, render_template, request, url_for
from windy import yrno, wfinder
from plot import plot
import os

app = Flask(__name__)

IMG_DIR = os.path.join(app.root_path, 'static', 'img')
WF_PLOT_NAME = "wf.png"
YR_PLOT_NAME = "yr.png"

@app.route('/')
def index():
    return render_template(
        'form.html',
        data=[{'name':'Chałupy'}, {'name':'Jastarnia'}, {'name':'Jurata'},
        {'name':'Kadyny'}, {'name':'Kuźnica'}, {'name':'Rewa'}])

@app.route("/result", methods=['GET', 'POST'])
def result():

    city = request.form.get('comp_select')
    data = []
    error = None
    
    wf_data = wfinder(city)
    yr_data = yrno(city)

    plot(wf_data[0:20], os.path.join(IMG_DIR, WF_PLOT_NAME))
    plot(yr_data[0:20], os.path.join(IMG_DIR, YR_PLOT_NAME))

    return render_template(
        'table.html',
        wf_plot = "img/" + WF_PLOT_NAME,
        yr_plot = "img/" + YR_PLOT_NAME,
        city = city,
        wf_data = wf_data,
        
        yr_data = yr_data,
        error = error)