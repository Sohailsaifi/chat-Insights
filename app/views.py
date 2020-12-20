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


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join('uploads/' + uploaded_file.filename))

    return redirect(f'/process/{uploaded_file.filename}')

@app.route('/process/<file_name>')
def processing_phase(file_name):
    if file_name=='':
        abort(404)
    try:
        chats = ExtractDataFrame(os.path.join('uploads/' + file_name))
        chats.process()
        df = chats.dataframe()  # The Final Processed DataFrame 

        os.remove(os.path.join('uploads/' + file_name))
        stats = GenerateStats()

        media_ratio = round(stats.mediaRatio(df),2)  # Media Ratio

        total_emojis = stats.totalEmojis(df)  # Total Emojis

        unique_emojis = stats.uniqueEmojis(df)  # Total Unique Emojis

        frequent_emojis = stats.frequentEmojis(df)
        emoji_donut = Emojis_donut(frequent_emojis ,'Emoji Distribution')  # Emojis Donut Plot

        active_members = stats.activeMembers(df)
        activeMemberPlot = membersBarPlot(active_members, 'Active Members of The Group')  # Active Members Bar Chart

        lazy_members = stats.lazyMembers(df)
        lazyMemberPlot = membersBarPlot(lazy_members, 'Lazy Members of The Group')  # Lazy Members Bar Chart

        result_dates = stats.activityOverDates(df)
        datesActivityGraph = activityDate_Graph(result_dates)  # Overall Dates Activity Line Plot
