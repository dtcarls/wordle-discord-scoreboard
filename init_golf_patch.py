import discord
import os
import json
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

scoreboard = {}
scoreboard_file = open('scoreboard.json', 'r')
try:
    scoreboard = json.load(scoreboard_file)
except JSONDecodeError:
    # empty file
    pass
scoreboard_file.close()

for key in scoreboard:
    golf_score=0
    for score in scoreboard[key]['scores']:
        if score == 'X':
            golf_score += scoreboard[key]['scores'][score]*8
        elif score == '1':
            golf_score += scoreboard[key]['scores'][score]*-3
        elif score == '2':
            golf_score += scoreboard[key]['scores'][score]*-2
        elif score == '3':
            golf_score += scoreboard[key]['scores'][score]*-1
        # 4 is par
        elif score == '5':
            golf_score += scoreboard[key]['scores'][score]
        elif score == '6':
            golf_score += scoreboard[key]['scores'][score]*2
    scoreboard[key]['golf'] = golf_score

scoreboard_file = open('scoreboard.json', 'w')
json.dump(scoreboard, scoreboard_file)
scoreboard_file.close()
