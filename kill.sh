kill -9 $(ps aux | grep -e "wordle_boy.py" | awk '{ print $2 }')
kill -9 $(ps aux | grep -e "missed_games.py" | awk '{ print $2 }')