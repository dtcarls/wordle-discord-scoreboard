import os
import json
from json.decoder import JSONDecodeError
from apscheduler.schedulers.blocking import BlockingScheduler

def new_day():
    #new day logic

    scoreboard = {}
    scoreboard_file = open('scoreboard.json', 'r')

    try:
        scoreboard = json.load(scoreboard_file)
    except JSONDecodeError:
        # empty file
        pass
    scoreboard_file.close()

    max_games=0
    for key in scoreboard:
        games = scoreboard[key]['games']
        if games > max_games:
            max_games = games

    if max_games >= 30:
        open('scoreboard.json', 'w').close()
        open('history_scoreboard.json', 'w').close()
        return

    for key in scoreboard:
        games = scoreboard[key]['games']
        if games < max_games:
            missed_games = max_games - games
            print(key+': '+str(missed_games)+"!")
            scoreboard[key]['scores']['X'] = scoreboard[key]['scores']['X']+missed_games

            total = 0
            golf_score = 0
            for score in scoreboard[key]['scores']:
                if score == 'X':
                    total += scoreboard[key]['scores'][score]*8
                    golf_score += scoreboard[key]['scores'][score]*4
                else:
                    total += scoreboard[key]['scores'][score]*int(score)

                if score == '1':
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

            scoreboard[key]['games'] = scoreboard[key]['games']+missed_games
            scoreboard[key]['mean'] = total/scoreboard[key]['games']
            scoreboard[key]['golf'] = golf_score

            scoreboard_file = open('scoreboard.json', 'w')
            json.dump(scoreboard, scoreboard_file)
            scoreboard_file.close()

            #historical for graphs
            history_scoreboard = {}
            history_scoreboard_file = open('history_scoreboard.json', 'r')

            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            yesterday = yesterday.strftime('%m/%d')

            try:
                history_scoreboard = json.load(history_scoreboard_file)
            except JSONDecodeError:
                # empty file
                pass
            history_scoreboard_file.close()

            history_scoreboard[yesterday][key] = golf_score
            history_scoreboard_file = open('history_scoreboard.json', 'w')
            json.dump(history_scoreboard, history_scoreboard_file)
            history_scoreboard_file.close()

if __name__ == '__main__':
    try:
        my_timezone = os.environ["TIMEZONE"]
    except KeyError:
        my_timezone = 'America/New_York'

    sched = BlockingScheduler(job_defaults={'misfire_grace_time': 15*60})

    sched.add_job(new_day, 'cron', id='new_day',
                  hour=0, minute=1,
                  timezone=my_timezone, replace_existing=True)

    print("Start Schedule")
    sched.start()
