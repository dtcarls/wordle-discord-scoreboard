import discord
import os
import json
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

        if 'Wordle' and '/6' in message.content:
            line = message.content.split('\n')[0]

            score = line.split('/')[0][-1]
            if DEBUG:
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
                    '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, 'X': 0}}

            scoreboard[author]['scores'][score] = scoreboard[author]['scores'][score]+1

            # if score == '2':
            #     await message.add_reaction('\U+0023')
            # elif score == '3':
            #     await message.add_reaction('\U00000033')

            # recalc mean
            # div = 0
            total = 0
            for score in scoreboard[author]['scores']:
                if score == 'X':
                    total += scoreboard[author]['scores'][score]*10
                else:
                    total += scoreboard[author]['scores'][score]*int(score)
                # div += scoreboard[author]['scores'][score]

            scoreboard[author]['games'] = scoreboard[author]['games']+1
            scoreboard[author]['mean'] = total/scoreboard[author]['games']

            scoreboard_file = open('scoreboard.json', 'w')
            json.dump(scoreboard, scoreboard_file)
            scoreboard_file.close()
            msg="Game recorded:\n"+author+"\n"+str(scoreboard[author]['games'])+" games\n"+str(round(scoreboard[author]['mean'],2))+" avg round"
            await message.channel.send(msg)

        if '!scoreboard' in message.content:
            scoreboard_file = open('scoreboard.json', 'r')
            scoreboard = json.load(scoreboard_file)
            scoreboard_file.close()

            sorted_scoreboard=sorted(scoreboard, key=lambda x: scoreboard[x]['mean'])
            n=1
            msg="Current Scoreboard\n"
            for key in sorted_scoreboard:
                msg+=str(n)+": "+key+" - "+str(scoreboard[key]['games'])+" games "+str(round(scoreboard[key]['mean'],2))+" avg round\n"
                n+=1
            await message.channel.send(msg)

        if '!stats' in message.content:
            scoreboard_file = open('scoreboard.json', 'r')
            scoreboard = json.load(scoreboard_file)
            scoreboard_file.close()

            msg="Stats for "+author+":\n"+str(scoreboard[author]['games'])+" games\n"+str(round(scoreboard[author]['mean'],2))+" avg round\n"+str(scoreboard[author]['scores'])
            await message.channel.send(msg)


client = MyClient()
client.run(TOKEN)