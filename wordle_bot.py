import discord
import os
import io
import json
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from json.decoder import JSONDecodeError
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEBUG = os.getenv('DEBUG')

if(not TOKEN):
    print("DISCORD_TOKEN not defined in your .env file")
    quit()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}! READY!'.format(self.user))

    async def on_message(self, message):
        if message.author == client.user or message.attachments:
            return
        if DEBUG:
            print('Message {0.author}: {0.content}'.format(message))

        author = message.author.name

        if DEBUG:
            print("Author: " + str(author))
            print("Message:" + str(message.content))
            print("Channel:" + str(message.channel))

        if 'Wordle' in message.content and '/6' in message.content:
            line = message.content.split('\n')[0]

            score = line.split('/')[0][-1]
            if DEBUG:
                print("inside")
                print(line)
                print(score)

            scoreboard = {}
            scoreboard_file = open('scoreboard.json', 'r')

            try:
                scoreboard = json.load(scoreboard_file)
            except JSONDecodeError:
                # empty file
                pass
            scoreboard_file.close()

            if author not in scoreboard:
                scoreboard[author] = {'streak': 0, 'games': 0, 'mean': 0, 'scores': {
                    '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'X': 0}, 'golf': 0}

            scoreboard[author]['scores'][score] = scoreboard[author]['scores'][score]+1

            # if score == '2':
            #     await message.add_reaction('\U+0023')
            # elif score == '3':
            #     await message.add_reaction('\U00000033')

            # recalc mean
            # recalc golf score
            total = 0
            golf_score = 0
            for score in scoreboard[author]['scores']:
                if score == 'X':
                    total += scoreboard[author]['scores'][score]*8
                    golf_score += scoreboard[author]['scores'][score]*4
                else:
                    total += scoreboard[author]['scores'][score]*int(score)

                if score == '1':
                    golf_score += scoreboard[author]['scores'][score]*-3
                elif score == '2':
                    golf_score += scoreboard[author]['scores'][score]*-2
                elif score == '3':
                    golf_score += scoreboard[author]['scores'][score]*-1
                # 4 is par
                elif score == '5':
                    golf_score += scoreboard[author]['scores'][score]
                elif score == '6':
                    golf_score += scoreboard[author]['scores'][score]*2

            scoreboard[author]['games'] = scoreboard[author]['games']+1
            scoreboard[author]['mean'] = total/scoreboard[author]['games']
            scoreboard[author]['golf'] = golf_score

            scoreboard_file = open('scoreboard.json', 'w')
            json.dump(scoreboard, scoreboard_file)
            scoreboard_file.close()

            #############################
            ### Historical for graphs ###
            #############################
            history_scoreboard = {}
            history_scoreboard_file = open('history_scoreboard.json', 'a+')
            history_scoreboard_file.close()
            history_scoreboard_file = open('history_scoreboard.json', 'r')

            current_date = datetime.datetime.now()
            current_date = current_date.strftime("%m/%d")

            try:
                history_scoreboard = json.load(history_scoreboard_file)
            except JSONDecodeError:
                # empty file
                pass
            history_scoreboard_file.close()

            if current_date not in history_scoreboard:
                history_scoreboard[current_date] = {}

            history_scoreboard[current_date][author] = golf_score
            history_scoreboard_file = open('history_scoreboard.json', 'w')
            json.dump(history_scoreboard, history_scoreboard_file)
            history_scoreboard_file.close()

            msg="Game recorded:\n"+author+"\n"+str(scoreboard[author]['games'])+" games\n"+str(round(scoreboard[author]['mean'],2))+" avg round\n"+str(scoreboard[author]['golf'])+" golf score"
            await message.channel.send(msg)

            #
            # Lifetime scoreboard
            #

            lifetime_scoreboard = {}
            lifetime_scoreboard_file = open('lifetime_scoreboard.json', 'r')

            try:
                lifetime_scoreboard = json.load(lifetime_scoreboard_file)
            except JSONDecodeError:
                # empty file
                pass
            lifetime_scoreboard_file.close()

            if author not in lifetime_scoreboard:
                lifetime_scoreboard[author] = {'streak': 0, 'games': 0, 'mean': 0, 'scores': {
                    '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'X': 0}, 'golf': 0}

            score = line.split('/')[0][-1]
            lifetime_scoreboard[author]['scores'][score] = lifetime_scoreboard[author]['scores'][score]+1

            # if score == '2':
            #     await message.add_reaction('\U+0023')
            # elif score == '3':
            #     await message.add_reaction('\U00000033')

            # recalc mean
            # recalc golf score
            total = 0
            golf_score = 0
            for score in lifetime_scoreboard[author]['scores']:
                if score == 'X':
                    total += lifetime_scoreboard[author]['scores'][score]*8
                    golf_score += lifetime_scoreboard[author]['scores'][score]*4
                else:
                    total += lifetime_scoreboard[author]['scores'][score]*int(score)

                if score == '1':
                    golf_score += lifetime_scoreboard[author]['scores'][score]*-3
                elif score == '2':
                    golf_score += lifetime_scoreboard[author]['scores'][score]*-2
                elif score == '3':
                    golf_score += lifetime_scoreboard[author]['scores'][score]*-1
                # 4 is par
                elif score == '5':
                    golf_score += lifetime_scoreboard[author]['scores'][score]
                elif score == '6':
                    golf_score += lifetime_scoreboard[author]['scores'][score]*2

            lifetime_scoreboard[author]['games'] = lifetime_scoreboard[author]['games']+1
            lifetime_scoreboard[author]['mean'] = total/lifetime_scoreboard[author]['games']
            lifetime_scoreboard[author]['golf'] = golf_score

            lifetime_scoreboard_file = open('lifetime_scoreboard.json', 'w')
            json.dump(lifetime_scoreboard, lifetime_scoreboard_file)
            lifetime_scoreboard_file.close()
            #msg="Game recorded:\n"+author+"\n"+str(lifetime_scoreboard[author]['games'])+" games\n"+str(round(lifetime_scoreboard[author]['mean'],2))+" avg round\n"+str(lifetime_scoreboard[author]['golf'])+" golf score"
            #await message.channel.send(msg)

        if '!scoreboard' in message.content:
            history_scoreboard_file = open('history_scoreboard.json', 'r')
            history_scoreboard = json.load(history_scoreboard_file)
            history_scoreboard_file.close()
            #graph creation
            x_axis = []
            score_dict = {}
            for key in history_scoreboard:
                x_axis.append(key)
                for user in history_scoreboard[key]:
                    if user not in score_dict:
                        score_dict[user]=[]
                    score_dict[user]+=[history_scoreboard[key][user]]

            for key in score_dict:
                while len(score_dict[key]) < len(x_axis):
                    score_dict[key]+=score_dict[key][-1:]

            df = pd.DataFrame(score_dict,index=x_axis)
            for col in df.columns:
                plt.plot(x_axis, df[col], label=col, linestyle='-', marker='o')
            plt.gca().invert_yaxis()
            plt.legend(bbox_to_anchor=(-0.1,1))
            plt.savefig('history.png', bbox_inches='tight')
            f = discord.File("history.png", filename="history.png")
            e = discord.Embed(title="Historical")
            e.set_image(url="attachment://history.png")
            plt.close()

            #sorted scoreboard
            scoreboard_file = open('scoreboard.json', 'r')
            scoreboard = json.load(scoreboard_file)
            scoreboard_file.close()
            max_games = 0
            for key in scoreboard:
                games = scoreboard[key]['games']
                if games > max_games:
                    max_games = games

            sorted_scoreboard=sorted(scoreboard, key=lambda x: scoreboard[x]['golf'])
            n=1
            msg="```Day " + str(max_games) + " of 30\n"
            msg+="Current Scoreboard\n"
            for key in sorted_scoreboard:
                msg+=str(n).zfill(2)+": "+key.ljust(20)+"["+str(scoreboard[key]['games']).zfill(2)+" games]\n\t"+str(scoreboard[key]['golf']).rjust(2)+" golf score - "+str(round(scoreboard[key]['mean'],2)).ljust(4,'0')+" avg round\n"
                # msg+=str(n).zfill(2)+": "+key.ljust(20)+" - "+str(scoreboard[key]['games']).zfill(2)+" games "+str(round(scoreboard[key]['mean'],2))+" avg round "+str(scoreboard[key]['golf'])+" golf score\n"
                # msg+=str(n)+": "+key)+" - "+str(scoreboard[key]['games']).zfill(2)+" games "+str(round(scoreboard[key]['mean'],2))+" avg round "+str(scoreboard[key]['golf'])+" golf score\n"
                n+=1
            await message.channel.send(file=f, embed=e, content=msg+"```")

        if '!lifetime_scoreboard' in message.content or '!lifetime' in message.content:
            lifetime_scoreboard_file = open('lifetime_scoreboard.json', 'r')
            lifetime_scoreboard = json.load(lifetime_scoreboard_file)
            lifetime_scoreboard_file.close()

            sorted_lifetime_scoreboard=sorted(lifetime_scoreboard, key=lambda x: lifetime_scoreboard[x]['golf'])
            n=1
            msg="```Current Lifetime Scoreboard\n"
            for key in sorted_lifetime_scoreboard:
                msg+=str(n).zfill(2)+": "+key.ljust(20)+"["+str(lifetime_scoreboard[key]['games']).zfill(2)+" games]\n\t"+str(lifetime_scoreboard[key]['golf']).rjust(2)+" golf score - "+str(round(lifetime_scoreboard[key]['mean'],2)).ljust(4,'0')+" avg round\n"
                # msg+=str(n).zfill(2)+": "+key.ljust(20)+" - "+str(lifetime_scoreboard[key]['games']).zfill(2)+" games "+str(round(lifetime_scoreboard[key]['mean'],2))+" avg round "+str(lifetime_scoreboard[key]['golf'])+" golf score\n"
                # msg+=str(n)+": "+key)+" - "+str(lifetime_scoreboard[key]['games']).zfill(2)+" games "+str(round(lifetime_scoreboard[key]['mean'],2))+" avg round "+str(lifetime_scoreboard[key]['golf'])+" golf score\n"
                n+=1
            await message.channel.send(msg+"```")

        # if '!stats' in message.content:
        #     scoreboard_file = open('scoreboard.json', 'r')
        #     scoreboard = json.load(scoreboard_file)
        #     scoreboard_file.close()

        #     msg="Stats for "+author+":\n"+str(scoreboard[author]['games'])+" games\n"+str(round(scoreboard[author]['mean'],2))+" avg round\n"+str(scoreboard[author]['golf'])+" golf score\n"+str(scoreboard[author]['scores'])
        #     await message.channel.send(msg)

print("Start Client")
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
