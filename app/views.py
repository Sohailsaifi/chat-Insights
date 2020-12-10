from flask import current_app as app
from flask import render_template, request, redirect, abort
from WhatsApp.functions import ExtractDataFrame, GenerateStats
from app.graphs import *
import os




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')