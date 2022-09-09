import config
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

filter_words = ["fuck"]

# console log when bot is ready
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")

# ping the bot
@client.event
async def on_message(msg):
    if msg.author != client.user: # to check that message wasn't from bot
        # ping the bot
        if msg.content.lower().startswith("!ping"):
            await msg.channel.send(f"Hi, I am awake {msg.author.display_name}")

        # word filter
        for text in filter_words:
            if "Moderator" not in str(msg.author.roles) and text in str(msg.content.lower()):
                await msg.delete()
                return

        print("Not Deleting...")
        
        # create note
        if msg.content.lower().startswith("!createnote"):
            if os.path.exists("note.txt") == False:
                f = open("note.txt","w")
                f.close()
                await msg.channel.send(f"note.txt has been created {msg.author.display_name}")
            else:
                await msg.channel.send(f"there is already an existing note {msg.author.display_name}")

        # delete note
        if msg.content.lower().startswith("!deletenote"):
            if os.path.exists("note.txt") == True:
                os.remove("note.txt")
                await msg.channel.send(f"deleted note.txt {msg.author.display_name}")
            else:
                await msg.channel.send("file does not exist, unable to delete note!")

        # bot idle
        if msg.content.lower().startswith("!botidle"):
            await client.change_presence(status=discord.Status.idle)

        # bot online
        if msg.content.lower().startswith("!botonline"):
            await client.change_presence(status=discord.Status.online)



client.run(config.token)