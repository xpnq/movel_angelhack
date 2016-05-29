from flask import Flask, render_template, send_from_directory

from flask import request
import re


app = Flask(__name__, static_folder='./static')

THE_DB = 'example.db'


@app.route('/')
def index():
    if _get_first_id():
        body_html = _get_phrases(_get_first_id())
    else:
        body_html = "Id not found."
    return render_template('get_body.html', body=body_html, left_menu=get_left_menu_html())


@app.route('/story', methods=['GET', 'POST'])
def index_story():
    id = request.args['id']
    body_html = _get_phrases(id)
    return render_template('get_body.html', body=body_html, left_menu=get_left_menu_html())

@app.route('/read_me')
def read_me():
    about='''
    <p style="padding: 10px">Visuals have longer impact on our brain than the plain texts. We have tried to populate plain text from Novels/News/Books with relevant images. As one scrolls down the article, one also navigates through the images - it helps in getting the context even without having to read the text. What's more, you can hover over the text to get them read aloud for you.</p>
    '''
    return render_template('get_body.html', body=about, left_menu=get_left_menu_html())

def _get_first_id(table_name='movel_headlines'):
    query = 'select id from {0} limit 1'.format(table_name)
    row = result(query).fetchone()
    if row:
        return row


def get_left_menu_html(table_name='movel_headlines'):
    li_list = ""
    query = "select id, headline from {0}".format(table_name)
    rows = result(query).fetchall()
    for row in rows:
        li_list += "<li style=\"padding:5px\"><a href=\"story?id={0}\">{1}</a></li>".format(
            row[0], row[1])
    return "<ul id=\"left_menu_ul\" style=\"font-size: 20px; padding-left:5px;\">{0}</ul>".format(li_list)


def _get_phrases(story_id, table_name='movel_phrases'):
    query = "select phrase, url,entity from {0} where id=\"{1}\"".format(
        table_name, story_id)
    rows = result(query).fetchall()

    body = ""
    for phrase in rows:
        speech_phrase = phrase[0].replace("'","").replace(" ",",")
        bold_phrase = phrase[0].replace(phrase[2], "<b style='color: orange'>{0}</b>".format(phrase[2]))
        body += """<div class="box tile">
                    <div class="story_image">
                    <img width="250px" height="200px" src="{1}">
                    </div><br/>
                    <div onMouseOver=speakPhrase('{2}') class="phrase">
                    {0}
                    </div> 
                   </div>
                """.format(bold_phrase,phrase[1],speech_phrase)
    return body


def result(query, db_name=THE_DB):
    print query
    print db_name
    return _cursor(db_name).execute(query)


def _cursor(db_name=THE_DB):
    import sqlite3 as lite
    return lite.connect(db_name).cursor()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
