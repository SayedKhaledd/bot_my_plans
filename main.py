import os
import discord
import requests
import json
import random
from replit import db

sad_words=['زعلان', 'مضايق', 'مكتئب', 'sad','depressed','angry', 'depressing'];
encouraging=['cheer up', 'معلش','حصل خير', 'خلاص يسطا' ]

client =discord.Client();
def update_encouragments(encouraing_msg):
  if "encouragements" in db.keys():
    encouragments =db["encouragements"]
    encouragments.append(encouraing_msg)
    db["encouragements"]=encouragments
  else:
    db["encouragements"]=[encouraing_msg]
def delete_msg(index):
   encouragments =db["encouragements"]
   if len(encouragments) > index :
    del encouragments[index]
    db["encouragements"]=encouragments

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote=json_data[0]['q']+ ' - ' + json_data[0]['a']
  return quote
@client.event
async def on_ready():
  print ('we have logged in as {0.user}'.format(client))


  
@client.event
async def on_message(message):
  msg= message.content
  if message.author==client.user:
    return 
  if msg.startswith('$hello'):
    await message.channel.send('hello')
  if msg.startswith('$inspire'):
    await message.channel.send(get_quote())
  options=encouraging
  if "encouragements" in db.keys():
    options= options+ db["encouragements"]
  if any(word in  msg for word in sad_words):
    await message.channel.send(random.choice(options))
  if msg.startswith('$new'):
     encouraging_msg= msg.split("$new ",1)[1]
     update_encouragments(encouraging_msg)
     await message.channel.send("تمام يسطا")
    

my_secret = os.environ['TOKEN']

client.run(my_secret)
