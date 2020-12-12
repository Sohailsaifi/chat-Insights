from flask import current_app as app
from flask import render_template, request, redirect, abort
from WhatsApp.functions import ExtractDataFrame, GenerateStats
from app.graphs import *
import os


@app.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 404


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')