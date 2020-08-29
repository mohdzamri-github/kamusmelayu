from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf import FlaskForm
from flask import Flask, request, render_template

from flask_caching import Cache
from typing import Dict, List
from flask_bootstrap import Bootstrap

from typing import Dict, List

import re

config = {
    "DEBUG": True,           # some Flask specific configs
    "CACHE_TYPE": "simple",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123'
bootstrap = Bootstrap(app)
app.config.from_mapping(config)
cache = Cache(app)

# norvig
alphabet = 'abcdefghijklmnopqrstuvwxyz'


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


##
def edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1))


class MelayuForm(FlaskForm):
    melayu = StringField('kata melayu', validators=[DataRequired()])
    submit = SubmitField('Submit')

# read data


f = open('KamusDewan4.txt', 'r')

# data is separate by newline
# one long line for each entries.
mDict: Dict[str, List[str]] = {}
for line in f:
    line = line.strip()
    if line == '':
        continue
    s = line.split()
    x = s[0].strip(",;")
    y = ' '.join(s[1:])

    if x not in mDict:
        mDict[x] = [y]
    else:
        mDict[x].append(y)


@app.route('/', methods=['GET', 'POST'])
def index():
    melayu = ''
    d = []
    form = MelayuForm()

    if form.validate_on_submit():
        melayu = form.melayu.data
        form.melayu.data = ''

    if melayu == '':
        return render_template('index.html', form=form, melayu=melayu, d=d)

    if melayu in mDict:
        d = mDict[melayu]

        # search for kata terbitan
        l = []
        for i in d: # d is a List of definations. ['saya suka','makan nasi']
            for j in i.split():
                # split ['saya suka','makan nasi']
                #  j = ['saya','suka']
                # strip(), x = str(j) = 'saya' !! not x=['saya']
                x = str(j).strip(",;:.)(")
                if re.search(melayu,x):
                    if x not in l:
                        l.append(str(x))
                # search for sakit -> penyakit
                if re.search(melayu[1:],x):
                    if x not in l:
                        l.append(str(x))
        return render_template('index.html', form=form,
                               l=l, melayu=melayu, d=d)
    else:
        guest1 = edits1(melayu)
        guest2 = []
        for c in guest1:
            if c in mDict:
                guest2.append(c)
        return render_template('index.html', form=form, melayu=melayu,
                               guest2=guest2, d=d)


@app.route('/info')
def info():
    return render_template('info.html')
# read kamus
# Setup Index Page
# Use web form for user input
# process input, display result from Kamus
