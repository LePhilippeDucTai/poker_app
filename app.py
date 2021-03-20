from flask import Flask, render_template, url_for

from poker_game import game_simulation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/poker')
def poker_computing():
    return game_simulation(n_other_players=7)